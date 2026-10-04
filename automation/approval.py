"""Approval via GitHub issue: one issue per post, Loris replies "go" or "stop".

  python automation/approval.py request             – open an issue for every post with entries in status "draft"
  python automation/approval.py reply ISSUE TEXT    – evaluate a comment ("go" → approved, "stop" → waiting_changes)

One post = all entries with the same number at the start of the ID (e.g. 03-excel-mistakes, 03-story-teaser).
A post whose group contains a "waiting_<reason>" entry gets no issue until nothing is waiting any more.
Environment: GH_TOKEN (GitHub token with issues:write), GITHUB_REPOSITORY.
"""
import json, os, re, subprocess, sys, time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "automation" / "plan.json"
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/maehrtax---instagram")
LABEL = "approval"
STOPPED = "waiting_changes"   # status after "stop"
TYPE_NAME = {"carousel": "Carousel", "reel": "Reel", "story": "Story", "image": "Image"}


def gh(*args, stdin=None):
    return subprocess.run(["gh", *args, "--repo", REPO], input=stdin, check=True, capture_output=True, text=True).stdout.strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def et(time_str):
    """'2026-10-12 12:30' → 'Mon 10/12 12:30 PM ET'."""
    d = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    return f"{d:%a} {d.month}/{d.day} {d.hour % 12 or 12}:{d:%M} {'AM' if d.hour < 12 else 'PM'} ET"


def save(plan, message):
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    git("add", str(PLAN))
    if git("status", "--porcelain"):
        git("commit", "-m", message)
        # other workflows (post, status) commit in parallel – on conflict fetch again and retry
        for attempt in range(5):
            try:
                git("pull", "--rebase", "-q")
                git("push")
                return
            except subprocess.CalledProcessError:
                subprocess.run(["git", "rebase", "--abort"], cwd=ROOT, capture_output=True)  # otherwise every retry fails the same way
                time.sleep(5 * (attempt + 1))
        raise RuntimeError("plan.json could not be saved (push failed 5×)")


def groups(plan):
    g = {}
    for e in plan["entries"]:
        g.setdefault(e["id"].split("-")[0], []).append(e)
    return g


def open_for_approval(entries):
    """Entries of one group that need a new approval issue – empty while something in the group is waiting."""
    pending = [e for e in entries if e["status"] == "draft" and not e.get("issue")]
    if not pending or any(e["status"].startswith("waiting_") for e in entries):
        return []
    return pending


def raw(path):
    return f"https://raw.githubusercontent.com/{REPO}/{git('rev-parse', 'HEAD')}/{path}"


def preview(entries):
    lines = []
    for e in entries:
        lines.append(f"### {TYPE_NAME.get(e['type'], e['type'])} · {et(e['time'])} · `{e['id']}`")
        if e["type"] == "reel":
            hint = " ⚠️ no music yet – will not be posted automatically like this" if e.get("music_missing") else ""
            if e.get("video"):
                lines.append(f"▶️ [Watch Reel]({raw(e['folder'] + '/' + e['video'])}){hint}")
            if e.get("cover"):
                lines.append(f'<img src="{raw(e["folder"] + "/" + e["cover"])}" width="180">')
        else:
            lines.append(" ".join(f'<img src="{raw(e["folder"] + "/" + b)}" width="180">' for b in e.get("images", [])))
        if e.get("note"):
            lines.append(f"_{e['note']}_")
        caption = ROOT / e["folder"] / e["caption"] if e.get("caption") else None
        if caption and caption.exists():
            lines.append("<details><summary>Caption</summary>\n\n```\n" + caption.read_text().strip() + "\n```\n</details>")
        fact_check = ROOT / e["folder"] / "fact_check.md"
        if fact_check.exists():
            lines.append(f"🔎 Fact check before \"go\": [fact_check.md](https://github.com/{REPO}/blob/main/{e['folder']}/fact_check.md)")
        lines.append("")
    return "\n".join(lines)


def request():
    plan = json.loads(PLAN.read_text())
    try:
        gh("label", "create", LABEL, "--color", "53C3A2", "--description", "Post waiting for go/stop")
    except subprocess.CalledProcessError:
        pass  # already exists
    created = 0
    for nr, entries in sorted(groups(plan).items()):
        pending = open_for_approval(entries)
        if not pending:
            continue
        # name the issue after the group's feed post (Reel/carousel), not after a story that happens to come first
        main = next((e for e in pending if e["type"] != "story"), pending[0])
        title = f"Approval {nr}: {main['id'].split('-', 1)[1].replace('-', ' ')} – {et(main['time'])}"
        body = (f"@{REPO.split('/')[0]} please take a quick look.\n\n"
                f"**Reply `go`** → goes live automatically at the times below.\n"
                f"**Reply `stop`** → paused. Tell Claude what to change.\n\n"
                + preview(pending))
        url = gh("issue", "create", "--title", title, "--label", LABEL, "--body-file", "-", stdin=body)
        for e in pending:
            e["issue"] = int(url.rstrip("/").split("/")[-1])
        created += 1
        print("✓", title, url)
    if created:
        save(plan, f"Approval requested ({created} post{'s' if created != 1 else ''})")
    else:
        print("No new drafts.")


def parse_word(comment):
    match = re.match(r"\s*(go|stop)\b", comment.lower())
    return match.group(1) if match else ""


def apply(plan, issue, word, issue_title=None):
    """Sets the status of the draft entries that belong to `issue`. Returns the changed entries."""
    affected = [e for e in plan["entries"] if e.get("issue") == issue and e["status"] == "draft"]
    if not affected and issue_title:  # issue number never saved (e.g. push failed after creating) → match via title
        nr = re.match(r"Approval (\w+):", issue_title)
        affected = [e for e in plan["entries"] if nr and e["id"].split("-")[0] == nr.group(1)
                    and e["status"] == "draft" and not e.get("issue")]
        for e in affected:
            e["issue"] = issue
    target = "approved" if word == "go" else STOPPED
    for e in affected:
        e["status"] = target
    return affected


def reply(issue, comment):
    word = parse_word(comment)
    if not word:
        print("No go/stop – nothing to do.")
        return
    plan = json.loads(PLAN.read_text())
    affected = [e for e in plan["entries"] if e.get("issue") == issue and e["status"] == "draft"]
    title = None if affected else gh("issue", "view", str(issue), "--json", "title", "--jq", ".title")
    affected = apply(plan, issue, word, title)
    if not affected:
        gh("issue", "comment", str(issue), "--body", "Nothing left to approve in this issue.")
        return
    save(plan, f"Approval #{issue}: {word}")
    lines = "\n".join(f"- `{e['id']}` → {et(e['time'])}" + (" (⚠️ Reel has no music yet)" if e.get("music_missing") else "")
                      for e in affected)
    text = (f"✅ Scheduled – the autopilot posts automatically:\n{lines}" if word == "go"
            else f"⏸️ Paused (`{STOPPED}`):\n{lines}\nTell Claude what to change to continue.")
    gh("issue", "comment", str(issue), "--body", text)
    gh("issue", "close", str(issue))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("request", "reply"):
        sys.exit("Usage: approval.py request | reply ISSUE TEXT")
    if sys.argv[1] == "request":
        request()
    else:
        reply(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "")
