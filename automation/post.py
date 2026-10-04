"""Autopilot: publishes due, approved entries from plan.json through the Instagram API.

Usage (runs every 15 minutes via GitHub Actions, workflow "Instagram post"):
  python automation/post.py            – wait for due entries (next 75 min) and post them
  python automation/post.py --dry-run  – only show what would happen (no API call, no commit)
  python automation/post.py --now ID   – post one approved entry right away
  python automation/post.py --test ID  – test run: Instagram uploads everything, but NOTHING is published

Environment: IG_TOKEN, IG_USER_ID (GitHub secrets), GITHUB_REPOSITORY (set by GitHub).
Instagram fetches the files from public links; images must be JPEG – the script converts PNGs,
commits the JPEGs and links them via the commit (raw.githubusercontent.com/<repo>/<sha>/...).
All plan times are US Eastern (America/New_York).
"""
import json, os, subprocess, sys, time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "automation" / "plan.json"
ZONE = ZoneInfo("America/New_York")
API = "https://graph.instagram.com/v23.0"
WINDOW = timedelta(minutes=75)      # how far ahead we wait
CATCH_UP = timedelta(hours=6)       # late runs catch up to 6 h after the planned time
FEED = ("carousel", "reel", "image")


def now():
    return datetime.now(ZONE)


def planned(e):
    return datetime.strptime(e["time"], "%Y-%m-%d %H:%M").replace(tzinfo=ZONE)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def save(plan, message):
    """Commit and push – with retries: if the status "published" got lost, the next run would post the same
    entry again."""
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    git("add", "-A")
    if git("status", "--porcelain"):
        git("commit", "-m", message)
        for attempt in range(6):
            try:
                git("pull", "--rebase", "-q")
                git("push")
                break
            except subprocess.CalledProcessError as err:
                subprocess.run(["git", "rebase", "--abort"], cwd=ROOT, capture_output=True)
                print(f"Push attempt {attempt + 1} failed: {err.stderr.strip()[:200]}")
                time.sleep(5 * (attempt + 1))
        else:
            raise RuntimeError(f"plan.json not pushed ({message}) – the post may already be live, check the plan!")
    return git("rev-parse", "HEAD")


def as_jpeg(folder, names):
    """PNG → JPEG (Instagram only accepts JPEG images). Returns the repo paths of the JPEGs."""
    from PIL import Image
    paths = []
    for n in names:
        source = ROOT / folder / n
        target = ROOT / folder / "_jpg" / (Path(n).stem + ".jpg")
        target.parent.mkdir(exist_ok=True)
        if not target.exists():
            Image.open(source).convert("RGB").save(target, "JPEG", quality=92, optimize=True)
        paths.append(target.relative_to(ROOT).as_posix())
    return paths


def link(sha, path):
    return f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/{sha}/{path}"


class Instagram:
    def __init__(self):
        missing = [k for k in ("IG_TOKEN", "IG_USER_ID") if not os.environ.get(k)]
        if missing:
            sys.exit(f"✗ {', '.join(missing)} missing – add the secrets first (see SETUP.md). Nothing was posted.")
        self.token = os.environ["IG_TOKEN"]
        self.user = os.environ["IG_USER_ID"]

    def _request(self, method, path, retry=True, **kwargs):
        """Retry short hiccups (connection, timeout, 5xx) up to 3× – except for media_publish:
        there a timeout can mean the post is already live."""
        import requests
        for attempt in range(3 if retry else 1):
            try:
                r = requests.request(method, f"{API}/{path}", **kwargs)
            except (requests.ConnectionError, requests.Timeout):
                if not retry or attempt == 2:
                    raise
            else:
                if r.ok:
                    return r.json()
                if r.status_code < 500 or not retry or attempt == 2:
                    raise RuntimeError(f"{path}: {r.status_code} {r.text}")
            time.sleep(10 * (attempt + 1))

    def _post(self, path, retry=True, **data):
        return self._request("POST", path, retry, data={**data, "access_token": self.token}, timeout=120)

    def _get(self, path, **params):
        return self._request("GET", path, params={**params, "access_token": self.token}, timeout=60)

    def container(self, **data):
        cid = self._post(f"{self.user}/media", **data)["id"]
        for _ in range(60):  # Instagram processes videos asynchronously
            status = self._get(cid, fields="status_code").get("status_code")
            if status == "FINISHED":
                return cid
            if status in ("ERROR", "EXPIRED"):
                raise RuntimeError(f"Container {cid}: {status}")
            time.sleep(10)
        raise RuntimeError(f"Container {cid}: timed out")

    def publish(self, cid):
        mid = self._post(f"{self.user}/media_publish", retry=False, creation_id=cid)["id"]
        try:  # from here on the post is live – a missing link must not mark it as "error"
            return mid, self._get(mid, fields="permalink").get("permalink")
        except Exception as err:
            print(f"Note: link for {mid} not available ({err})")
            return mid, None


def check(e):
    """Returns a reason why the entry may not be posted (yet) – or None."""
    if e["type"] == "reel":
        if not e.get("video") or not (ROOT / e["folder"] / e["video"]).exists():
            return "video missing"
        if e.get("music_missing"):
            return "Reel is still silent (music_missing) – add music first or remove the field"
    for n in e.get("images", []):
        if not (ROOT / e["folder"] / n).exists():
            return f"image missing: {n}"
    if e["type"] in ("story", "image", "carousel") and not e.get("images"):
        return "no images listed"
    return None


def media_payload(e, sha, caption):
    """Graph API container parameters per entry type (without access token). Carousel children are separate."""
    if e["type"] == "image":
        return dict(image_url=link(sha, e["_jpg"][0]), caption=caption)
    if e["type"] == "story":
        return dict(media_type="STORIES", image_url=link(sha, e["_jpg"][0]))
    if e["type"] == "reel":
        data = dict(media_type="REELS", video_url=link(sha, f"{e['folder']}/{e['video']}"), caption=caption,
                    share_to_feed="true")
        if e.get("_jpg"):
            data["cover_url"] = link(sha, e["_jpg"][0])
        return data
    if e["type"] == "carousel":
        return dict(media_type="CAROUSEL", caption=caption)
    raise ValueError(f"Unknown type {e['type']}")


def post(ig, e, sha, publish=True):
    caption = (ROOT / e["folder"] / e["caption"]).read_text().strip() if e.get("caption") else ""
    data = media_payload(e, sha, caption)
    if e["type"] == "carousel":
        children = [ig.container(image_url=link(sha, p), is_carousel_item="true") for p in e["_jpg"]]
        data["children"] = ",".join(children)
    cid = ig.container(**data)
    if not publish:
        return cid, None
    return ig.publish(cid)


def images_for(e):
    """Images to convert: the slides/story image, or the Reel cover."""
    return e.get("images") or ([e["cover"]] if e.get("cover") else [])


def test_run(eid):
    """Create containers and let Instagram process them, but do not publish.
    Unpublished containers expire on their own after 24 hours."""
    plan = json.loads(PLAN.read_text())
    e = next((x for x in plan["entries"] if x["id"] == eid), None)
    if not e:
        sys.exit(f"✗ {eid}: not in plan.json")
    reason = check(e)
    if reason and not reason.startswith("Reel is still silent"):
        sys.exit(f"✗ {eid}: {reason}")
    ig = Instagram()
    e["_jpg"] = as_jpeg(e["folder"], images_for(e))
    sha = save(without_internal(plan), f"Autopilot: files prepared for test run {eid}")
    cid, _ = post(ig, e, sha, publish=False)
    print(f"✓ Test run {eid}: Instagram accepted everything (container {cid}). Nothing was published.")


def due(entries, n, only=None):
    """Approved entries in the posting window (or exactly the entry `only`)."""
    return [e for e in entries if e["status"] == "approved" and
            (e["id"] == only if only else n - CATCH_UP <= planned(e) <= n + WINDOW)]


def main():
    if "--test" in sys.argv:
        return test_run(sys.argv[sys.argv.index("--test") + 1])
    dry_run = "--dry-run" in sys.argv
    only = sys.argv[sys.argv.index("--now") + 1] if "--now" in sys.argv else None
    plan = json.loads(PLAN.read_text())
    n = now()
    todo = due(plan["entries"], n, only)
    if not todo:
        print("Nothing due.", f"{n:%m/%d %I:%M %p} ET")
        return
    ig = None if dry_run else Instagram()
    failed = []
    for e in sorted(todo, key=planned):
        # always take the entry from the current plan (the plan is re-read after waiting)
        e = next((x for x in plan["entries"] if x["id"] == e["id"]), None)
        if not e or e["status"] != "approved":
            continue
        reason = check(e)
        if reason:
            print(f"✗ {e['id']}: {reason}")
            continue
        images = images_for(e)
        if dry_run:
            print(f"• {e['id']} ({e['type']}) at {e['time']} ET: {len(images)} image(s)", e.get("video", ""))
            continue
        e["_jpg"] = as_jpeg(e["folder"], images)
        sha = save(without_internal(plan), f"Autopilot: files prepared for {e['id']}")
        wait = (planned(e) - now()).total_seconds()
        if wait > 0 and not only:
            print(f"… waiting {int(wait // 60)} min until {e['time']} ET for {e['id']}")
            time.sleep(wait)
            # while waiting, a "stop", a new time or "cancelled" may have come in
            try:
                git("pull", "--rebase", "-q")
                plan = json.loads(PLAN.read_text())
            except subprocess.CalledProcessError as err:
                subprocess.run(["git", "rebase", "--abort"], cwd=ROOT, capture_output=True)
                print(f"Note: plan not reloaded ({err.stderr.strip()[:200]}) – posting with the known state")
            current = next((x for x in plan["entries"] if x["id"] == e["id"]), None)
            if not current or current["status"] != "approved" or current["time"] != e["time"]:
                print(f"↷ {e['id']}: plan changed while waiting – skipped")
                continue
            current["_jpg"], e = e["_jpg"], current
        try:
            mid, permalink = post(ig, e, sha)
            e.update(status="published", media_id=mid, link=permalink, published_at=now().strftime("%Y-%m-%d %H:%M"))
            e.pop("error_message", None)
            print(f"✓ {e['id']} live: {permalink}")
            first_hour(e)
        except Exception as err:  # note the error in the plan so it is visible in the repo
            # connection errors contain the URL incl. access_token – never write it into the public repo
            message = str(err).replace(ig.token, "***")
            e.update(status="error", error_message=message[:500])
            failed.append(e["id"])
            print(f"✗ {e['id']}: {message}")
        e.pop("_jpg", None)
        save(plan, f"Autopilot: {e['id']} {e['status']}")
    if failed:
        sys.exit(1)


def first_hour(e):
    """After a feed post: checklist as a comment in the existing approval issue (no new issue).
    Errors here never stop posting."""
    if e["type"] not in FEED or not e.get("issue") or not os.environ.get("GH_TOKEN"):
        return
    repo = os.environ["GITHUB_REPOSITORY"]
    search = f"https://github.com/{repo}/issues?q=is%3Aopen+label%3A"
    lines = [f"`{e['id']}` is live 🚀 [View post]({e.get('link')})", "",
             "The first hour counts double:", "",
             "- [ ] Share it to your story (paper plane → \"Add to story\") with a sticker or a short question",
             f"- [ ] Reply to comments fast → [💬 Comments]({search}comments) (`C12 ok` is enough)",
             f"- [ ] Comment on 2–3 posts from the [📡 Radar]({search}radar) – people visit back"]
    if e["type"] == "carousel" and linkedin_enabled():
        lines.append(f"- [ ] LinkedIn package is ready → [💼 LinkedIn]({search}linkedin)")
    try:
        subprocess.run(["gh", "issue", "comment", str(e["issue"]), "--repo", repo, "--body", "\n".join(lines)],
                       check=True, capture_output=True, text=True, timeout=60)
    except Exception as err:
        print(f"Note: first-hour checklist not posted ({err})")


def linkedin_enabled():
    try:
        return bool(json.loads((ROOT / "automation" / "interaction.json").read_text()).get("linkedin", {}).get("enabled"))
    except (OSError, ValueError):
        return False


def without_internal(plan):
    return {**plan, "entries": [{k: v for k, v in e.items() if not k.startswith("_")} for e in plan["entries"]]}


if __name__ == "__main__":
    main()
