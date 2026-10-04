"""Status page: writes STATUS.md – what is running, what comes next, what you need to do, and every change in the repo.

Usage:  python automation/status.py          – rewrite STATUS.md (and STATUS.html)
Runs automatically via GitHub Actions (.github/workflows/status.yml) after every push and after every run
of post, approval, stats, key refresh and music. Sources: plan.json, git history, stats/*.csv,
optionally the workflow status via the GitHub API (GH_TOKEN + GITHUB_REPOSITORY).
Hand-written notes ("in progress", decisions) live in automation/status_notes.md and are shown near the top.
Also writes STATUS.html (automation/status_html.py) – the same status as a visual page (GitHub Pages).
All times are US Eastern (America/New_York), shown like "Mon 10/12 12:30 PM ET".
"""
import csv, json, os, re, subprocess
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "automation" / "plan.json"
NOTES = ROOT / "automation" / "status_notes.md"
INTERACTION = ROOT / "automation" / "interaction.json"
ACCOUNT = ROOT / "automation" / "stats" / "account.csv"
REMINDERS = ROOT / "automation" / "reminders.json"
TARGET = ROOT / "STATUS.md"
ZONE = ZoneInfo("America/New_York")
CATCH_UP = timedelta(hours=6)  # like post.py: after that a missed entry is not caught up any more
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/maehrtax---instagram")
BRANCH = "main"
PAGES_URL = "https://maehrsteuern.github.io/maehrtax---instagram/"
STATUS_COMMIT = "Status updated"

TYPE = {"carousel": "🖼️ Carousel", "reel": "🎬 Reel", "story": "📱 Story", "image": "🖼️ Image"}
STATUS = {
    "approved": "🟢 approved (posts automatically)",
    "draft": "🟡 draft (waiting for approval)",
    "manual": "✋ manual (you post in the app)",
    "published": "✅ published",
    "error": "🔴 error",
    "cancelled": "⚪ cancelled",
}
DONE = ("published", "cancelled")
WORKFLOWS = [  # file, name, when
    ("status.yml", "Status + Google Calendar", "after every post run, every push, daily (STATUS.md, calendar sync, watchdog)"),
    ("post.yml", "Instagram post", "every 15 min (posts approved entries)"),
    ("approval.yml", "Approval", "on new drafts / reply in the issue"),
    ("stats.yml", "Instagram stats", "daily around 9:00 AM ET"),
    ("token.yml", "Refresh Instagram key", "1st of the month"),
    ("radar.yml", "Radar (+ LinkedIn if enabled)", "daily around 7:00 AM ET (issue with work list)"),
    ("comments.yml", "Comments", "after every post run (suggestions in the issue)"),
    ("weekly_report.yml", "Weekly report", "Sundays around 6:00 PM ET (one issue)"),
    ("music.yml", "Fetch music", "manual only"),
]
WEEKDAY = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""


def planned(e):
    return datetime.strptime(e["time"], "%Y-%m-%d %H:%M").replace(tzinfo=ZONE)


def clock(d):
    """12:30 PM"""
    return f"{d.hour % 12 or 12}:{d:%M} {'AM' if d.hour < 12 else 'PM'}"


def day(d):
    """Mon 10/12"""
    return f"{WEEKDAY[d.weekday()]} {d.month}/{d.day}"


def when(d):
    """Mon 10/12 12:30 PM ET"""
    return f"{day(d)} {clock(d)} ET"


def status(e):
    s = e["status"]
    if s.startswith("waiting_"):
        return "⏳ waiting: " + s.removeprefix("waiting_").replace("_", " ")
    return STATUS.get(s, s)


def issue_link(e):
    return f" · [Approval #{e['issue']}](https://github.com/{REPO}/issues/{e['issue']})" if e.get("issue") else ""


def missing_files(e):
    names = list(e.get("images", [])) + [e[k] for k in ("video", "cover", "caption") if e.get(k)]
    return [n for n in names if not (ROOT / e["folder"] / n).exists()]


# Calls to action like 'DM "TOOL"' / 'Comment TOOL' in captions
CALL = re.compile(r"(?i:dm|comment|reply|type|send|message|text)\s+(?:(?i:me|us|the\s+word|just|now|below|with)\s+)*"
                  r"[\"“'‘]?([A-Z]{3,})\b")


def manychat_keywords():
    return {w.lower() for w in json.loads(INTERACTION.read_text())["comments"]["manychat_keywords"]}


def keyword_check(entries):
    """ManyChat keywords live only in automation/interaction.json. If a planned post asks for a different word,
    neither ManyChat nor the comment helper match – this is reported here."""
    try:
        known = manychat_keywords()
    except (OSError, KeyError, ValueError):
        return ["🔴 **Keywords:** `automation/interaction.json` is missing or broken – ManyChat check not possible"]
    points = []
    for e in entries:
        if e["status"] in DONE or not e.get("caption"):
            continue
        file = ROOT / e["folder"] / e["caption"]
        foreign = sorted({w for w in CALL.findall(file.read_text()) if w.lower() not in known}) if file.exists() else []
        if foreign:
            points.append(f"⚠️ **Keyword does not match ManyChat** `{e['id']}` ({when(planned(e))}): "
                          f"{', '.join(f'“{w}”' for w in foreign)} – set it up in ManyChat and add it to `automation/interaction.json` "
                          "(`manychat_keywords`), or change the caption to TOOL")
    return points


# ---------- sections ----------

def reminders():
    """Open one-time reminders from automation/reminders.json, with "start" as a datetime (ET)."""
    try:
        raw = json.loads(REMINDERS.read_text()).get("reminders", [])
    except (OSError, ValueError):
        return []
    out = []
    for r in raw:
        if r.get("done"):
            continue
        try:
            out.append({**r, "start": datetime.fromisoformat(r["when"]).replace(tzinfo=ZONE)})
        except (KeyError, ValueError):
            continue
    return out


def open_points(entries, n):
    points = []
    drafts = {}
    for e in sorted(entries, key=planned):
        t, s, name = planned(e), e["status"], f"`{e['id']}` ({when(planned(e))})"
        if s == "error":
            points.append(f"🔴 **Posting failed** {name}: {e.get('error_message', '')[:200]}")
        elif s == "approved" and t < n - CATCH_UP:
            points.append(f"🔴 **Missed** {name}: was approved but did not go live – set a new time or post by hand")
        elif s == "draft" and t > n - CATCH_UP:
            drafts.setdefault((e["id"].split("-")[0], e.get("issue")), []).append(e)
        elif s.startswith("waiting_") and t > n - CATCH_UP:
            points.append(f"⏳ **Waiting: {s.removeprefix('waiting_').replace('_', ' ')}** {name}"
                          + (f" – {e['note']}" if e.get("note") else ""))
        elif s == "manual" and t > n - timedelta(days=1):
            points.append(f"✋ **Post by hand** {name}" + (f" – {e['note']}" if e.get("note") else ""))
        if s in ("approved", "manual") and t > n and (missing := missing_files(e)):
            points.append(f"🔴 **Files missing** {name}: {', '.join(missing)}")
        if e.get("music_missing") and t > n and s not in DONE:
            points.append(f"🎵 **Music missing** {name}")
        if e.get("after") and not e.get("after_done") and (s == "published" and n - t < timedelta(days=2)
                                                           or s == "manual" and t > n - timedelta(days=1)):
            points.append(f"👉 **Afterwards:** {e['after']} ({name})")
        if s == "published" and e.get("note", "").startswith("Afterwards") and n - t < timedelta(days=2):
            points.append(f"👉 **{e['note']}** ({name})")
    for r in sorted(reminders(), key=lambda r: r["start"]):  # deadlines before the (long) list of approvals
        if r["start"] - timedelta(days=r.get("show_days_before", 3)) <= n <= r["start"] + timedelta(days=1):
            first = (r.get("text") or "").splitlines()[0] if r.get("text") else ""
            points.append(f"⏰ **{r['title']}** ({when(r['start'])})" + (f" – {first}" if first else ""))
    for (nr, issue), group in drafts.items():
        everyone = [x for x in entries if x["id"].split("-")[0] == nr]
        waiting = next((x["id"] for x in everyone if x["status"].startswith("waiting_")), None)
        how = (issue_link(group[0]).lstrip(" ·") or (f"issue comes once `{waiting}` is ready" if waiting
                                                     else "issue is created automatically"))
        ids = ", ".join(f"`{x['id']}`" for x in group)
        missing = sorted({f for x in group for f in missing_files(x)})
        files = f" · ⚠️ files not there yet: {', '.join(missing[:4])}{' …' if len(missing) > 4 else ''}" if missing else ""
        points.append(f"🟡 **Approve** post {nr} – {ids} (first {when(planned(group[0]))}) – \"go\" or \"stop\" in the issue "
                      f"({how}){files}")
    points += keyword_check(entries)
    return points or ["Nothing open. 🎉"]


def table(entries):
    lines = ["| When (ET) | What | Status | Note |", "|---|---|---|---|"]
    for e in sorted(entries, key=planned):
        note = (e.get("note", "") + issue_link(e)).replace("|", "/")
        lines.append(f"| {when(planned(e))} | {TYPE.get(e['type'], e['type'])} `{e['id']}` | {status(e)} | {note} |")
    return lines


def published(entries):
    done = sorted((e for e in entries if e["status"] == "published"), key=planned, reverse=True)[:10]
    if not done:
        return ["Nothing published through the autopilot yet."]
    return [f"- {when(planned(e))} · {TYPE.get(e['type'], e['type'])} `{e['id']}`"
            + (f" · [view]({e['link']})" if e.get("link") else "")
            + (f" (live {e['published_at']} ET)" if e.get("published_at") else "") for e in done]


def insights_files():
    return sorted((ROOT / "automation" / "stats").glob("insights_*.json"))


def local(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z").astimezone(ZONE)


def short_date(iso):
    """'2026-10-12' → '10/12'"""
    return f"{int(iso[5:7])}/{int(iso[8:10])}"


def numbers(n):
    """Daily numbers from account.csv and the newest insights_*.json (fetched daily around 9:00 AM ET)."""
    rows = list(csv.DictReader(ACCOUNT.open())) if ACCOUNT.exists() else []
    files = insights_files()
    if not rows and not files:
        return ["No stats yet – they start after the Instagram secrets are set and the first stats run (daily around 9:00 AM ET)."]
    out = []
    if rows:
        last = rows[-1]
        text = f"**{int(last['followers_count']):,} followers** · {last['media_count']} posts on the profile (fetched {short_date(last['date'])})"
        earlier = [z for z in rows if z["date"] < last["date"]]
        if earlier:
            diff = int(last["followers_count"]) - int(earlier[-1]["followers_count"])
            text += f" · **{diff:+d}** since {short_date(earlier[-1]['date'])}" + (" ⚠️" if diff < 0 else "")
        out.append(text)
    if files:
        d = json.loads(files[-1].read_text())
        old = {b["id"]: b for b in json.loads(files[-2].read_text()).get("media", [])} if len(files) > 1 else {}
        days = sorted((d.get("daily_reach") or {}).items())[-4:]
        if days:
            out.append("Reach per day: " + " · ".join(f"{short_date(t)} **{v:,}**" for t, v in days))
        stories = sorted(d.get("active_stories") or [], key=lambda x: x.get("time") or "")
        if stories:
            out += ["", "| Story (last 24 h) | Views | Reach | Replies | Profile visits | Follows |", "|---|---|---|---|---|---|"]
            out += [f"| {when(local(s['time']))} | {s.get('views', '–')} | {s.get('reach', '–')} | {s.get('replies', '–')} | "
                    f"{s.get('profile_visits', '–')} | {s.get('follows', '–')} |" for s in stories if s.get("time")]
        new = [b for b in d.get("media", []) if b.get("timestamp") and n - local(b["timestamp"]) < timedelta(days=14)]
        if new:
            out += ["", "| Post (last 14 days) | Views | Reach | Likes | Comments | Saves | Shares |", "|---|---|---|---|---|---|---|"]
            for b in sorted(new, key=lambda x: x["timestamp"], reverse=True):
                plus = f" (+{b['views'] - old[b['id']]['views']})" if isinstance(old.get(b["id"], {}).get("views"), int) and isinstance(b.get("views"), int) else ""
                name = (b.get("caption") or "").split("\n")[0][:40].replace("|", "/")
                out.append(f"| {when(local(b['timestamp']))} [{name}]({b.get('permalink', '')}) | {b.get('views', '–')}{plus} | "
                           f"{b.get('reach', '–')} | {b.get('likes', '–')} | {b.get('comments', '–')} | {b.get('saved', '–')} | {b.get('shares', '–')} |")
    return out + ["", "Raw data: `automation/stats/`, analysis: `strategy/06_analytics.md`"]


def automation_data():
    """[(name, when, last run as Markdown)] – workflow status via the GitHub API (only with GH_TOKEN)."""
    out = []
    token = os.environ.get("GH_TOKEN")
    for file, name, schedule in WORKFLOWS:
        last = "–"
        if token:
            try:
                raw = subprocess.run(
                    ["gh", "api", f"repos/{REPO}/actions/workflows/{file}/runs?status=completed&per_page=20",
                     "--jq", '[.workflow_runs[] | select(.conclusion=="success" or .conclusion=="failure")][0]'
                             ' | [.conclusion, .updated_at, .html_url] | @tsv'],
                    capture_output=True, text=True, timeout=30).stdout.strip()
                if raw:
                    result, ran, url = raw.split("\t")
                    t = datetime.fromisoformat(ran.replace("Z", "+00:00")).astimezone(ZONE)
                    # successful runs without a time, so STATUS.md is not re-committed after every post run
                    last = "✅ ok" if result == "success" else f"🔴 [failed]({url}) {when(t)}"
            except Exception:
                pass
        out.append((name, schedule, last))
    return out


def automation(data):
    lines = ["| Workflow | When | Last run |", "|---|---|---|"] + [f"| {n} | {w} | {l} |" for n, w, l in data]
    if all(l == "–" for _, _, l in data):
        lines += ["", "_No runs yet (or no GH_TOKEN locally) – the status is visible under Actions once the repo is live._"]
    return lines


# ---------- log ----------

def kind(message):
    for start, symbol in (("Autopilot", "🤖"), ("Approval", "✅"), ("Stats", "📈"), ("Music", "🎵"),
                          ("Keys", "🔑"), ("Merge", "🔀"), ("Radar", "📡"), ("Comments", "💬"),
                          ("LinkedIn", "💼"), ("Weekly report", "📊")):
        if message.startswith(start):
            return symbol
    return "✍️"


def plan_at(sha):
    try:
        data = json.loads(git("show", f"{sha}:automation/plan.json") or "{}")
    except ValueError:
        return {}
    entries = data.get("entries") if isinstance(data, dict) else None
    return {e["id"]: e for e in entries or [] if isinstance(e, dict) and "id" in e}


def plan_changes(sha):
    """What changed in plan.json in this commit (new, removed, status, time)."""
    if not git("diff-tree", "--no-commit-id", "-r", "--name-only", "--root", sha, "--", "automation/plan.json"):
        return []
    parent = git("rev-parse", "-q", "--verify", f"{sha}^")
    old, new = plan_at(parent) if parent else {}, plan_at(sha)
    if not old and len(new) > 5:
        return [f"{len(new)} entries created"]
    parts = [f"new `{i}` ({new[i].get('time')}, {new[i].get('status')})" for i in new if i not in old]
    parts += [f"removed `{i}`" for i in old if i not in new]
    for i in new:
        if i in old:
            for field in ("status", "time"):
                if old[i].get(field) != new[i].get(field):
                    parts.append(f"`{i}` {field}: {old[i].get(field)} → {new[i].get(field)}")
            if new[i].get("issue") and not old[i].get("issue"):
                parts.append(f"`{i}` → approval issue #{new[i]['issue']}")
            if new[i].get("error_message") and new[i].get("error_message") != old[i].get("error_message"):
                parts.append(f"`{i}` error: {new[i]['error_message'][:120]}")
            if new[i].get("link") and not old[i].get("link"):
                parts.append(f"`{i}` live: {new[i]['link']}")
    return parts


def areas(sha):
    paths = git("diff-tree", "--no-commit-id", "-r", "--name-only", "--root", sha).splitlines()
    out = []
    for p in paths:
        parts = p.split("/")
        x = "/".join(parts[:2]) if parts[0] in ("posts", "strategy", "automation", "templates", "assets", ".github") and len(parts) > 2 else p
        if x not in out and x not in ("STATUS.md", "STATUS.html"):
            out.append(x)
    return out[:6] + (["…"] if len(out) > 6 else [])


def log_data():
    """All commits (without status commits) as dicts, newest first."""
    out = []
    for line in git("log", "--format=%H%x09%aI%x09%s").splitlines():
        try:
            sha, date, message = line.split("\t", 2)
        except ValueError:
            continue
        if message.startswith(STATUS_COMMIT):
            continue
        changes = plan_changes(sha)
        out.append({"sha": sha, "time": datetime.fromisoformat(date).astimezone(ZONE), "message": message,
                    "kind": kind(message), "plan": changes, "areas": [] if changes else areas(sha)})
    return out


def log(n, data):
    days = {}
    for c in data:
        t, sha = c["time"], c["sha"]
        text = f"- {clock(t)} {c['kind']} {c['message']} ([`{sha[:7]}`](https://github.com/{REPO}/commit/{sha}))"
        if c["plan"]:
            text += "\n  - Plan: " + "; ".join(c["plan"])
        elif c["areas"]:
            text += "\n  - " + ", ".join(f"`{x}`" for x in c["areas"])
        days.setdefault(t.date(), []).append(text)
    lines, older = [], []
    for d, entries in days.items():
        block = [f"**{WEEKDAY[d.weekday()]} {d.month}/{d.day}/{d.year}**", *entries, ""]
        (lines if (n.date() - d).days < 7 else older).extend(block)
    if older:
        lines += ["<details><summary>Older than 7 days</summary>", "", *older, "</details>"]
    return lines or ["No commits yet."]


# ---------- assembly ----------

def next_up(upcoming):
    """Next entry that goes live by itself (approved) or by hand (manual) – else the next planned entry."""
    ordered = sorted(upcoming, key=planned)
    return (next((e for e in ordered if e["status"] in ("approved", "manual")), None),
            next(iter(ordered), None))


def main():
    n = datetime.now(ZONE)
    entries = json.loads(PLAN.read_text())["entries"]
    active = [e for e in entries if e["status"] not in DONE]
    upcoming = [e for e in active if planned(e) >= n - CATCH_UP]
    up_next, next_planned = next_up(upcoming)
    # without our own status commits, otherwise every run changes the timestamp and causes the next commit
    last = git("log", "-1", "--format=%aI", "--invert-grep", f"--grep=^{STATUS_COMMIT}")
    as_of = datetime.fromisoformat(last).astimezone(ZONE) if last else n

    parts = [
        "# 🧭 Status – @maehrtax on Instagram",
        "",
        f"_Generated by `automation/status.py` – do not edit by hand (notes: `automation/status_notes.md`). "
        f"As of: last change {when(as_of)} · visual page: {PAGES_URL}_",
        "",
    ]
    if up_next:
        parts += [f"**Up next:** {TYPE.get(up_next['type'])} `{up_next['id']}` on **{when(planned(up_next))}** "
                  f"– {status(up_next)}", ""]
    elif next_planned:
        parts += [f"**Up next:** nothing approved yet – first planned: {TYPE.get(next_planned['type'])} `{next_planned['id']}` "
                  f"on **{when(planned(next_planned))}** – {status(next_planned)}", ""]
    if NOTES.exists() and (note := NOTES.read_text().strip()):
        parts += ["## 📝 In progress", "", note, ""]
    points = open_points(entries, n)
    parts += ["## 👉 Needs you", "", *[f"- {p}" for p in points], ""]
    week = [e for e in upcoming if planned(e) <= n + timedelta(days=7)]
    later = [e for e in upcoming if planned(e) > n + timedelta(days=7)]
    parts += ["## ⏭️ Next 7 days", "", *(table(week) if week else ["Nothing planned."]), ""]
    if later:
        parts += ["## 🗓️ Later", "", *table(later), ""]
    parts += ["## ✅ Recently published (autopilot)", "", *published(entries), ""]
    parts += ["## 📈 Numbers (daily around 9:00 AM ET)", "", *numbers(n), ""]
    workflows, commits = automation_data(), log_data()
    parts += ["## ⚙️ Automation", "", *automation(workflows), ""]
    parts += ["## 📜 Log – every change", "",
              "🤖 Autopilot · ✅ Approval · 📈 Stats · 📊 Weekly report · 🎵 Music · 🔀 Merge · ✍️ by hand / Claude", "",
              *log(n, commits)]
    TARGET.write_text("\n".join(parts).rstrip() + "\n")
    print(f"✓ {TARGET.relative_to(ROOT)} written")

    import status_html  # same data as a visual page (STATUS.html)
    status_html.write(n=n, as_of=as_of, entries=entries, upcoming=upcoming, up_next=up_next or next_planned,
                      points=points, workflows=workflows, commits=commits)


if __name__ == "__main__":
    main()
