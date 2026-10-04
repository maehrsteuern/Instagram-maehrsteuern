"""Calendar events from automation/plan.json – read by the Google Calendar sync (automation/calendar_sync.py).

Contains:
- every feed post (Reel, carousel, image) at its posting time: "live – reply to comments", "post by hand",
  "approve first" or "waiting …"
- stories only when they are posted by hand
- to-dos: missing clips/music 5 days ahead, missing files – 5 days ahead at 7:00 PM ET, never after the posting time
- one-time reminders from automation/reminders.json (calendar = true)
Fixed UIDs per entry → the sync updates events instead of duplicating them.
Every event has a kind (KIND): sets color, reminders and whether it is "busy" for Reclaim –
only posting times block demo slots, to-dos and LinkedIn reminders are "free".
All times are US Eastern (America/New_York).

Try it without Google credentials:  python automation/calendar_events.py   (prints the events)
"""
from datetime import datetime, timedelta
import json, os

from status import BRANCH, ROOT, TYPE, ZONE, missing_files, planned, reminders, when

REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/maehrtax---instagram")
FEED = ("reel", "carousel", "image")
CHROME = f"https://github.com/{REPO}/blob/{BRANCH}/strategy/14_chrome_modules.md"
APPROVALS = f"https://github.com/{REPO}/issues?q=is%3Aopen+label%3Aapproval"
LOOKBACK = timedelta(days=14)

# kind → (Google colorId, pop-up reminders in minutes before, busy for Reclaim)
# colors: 3 grape, 5 banana, 6 tangerine, 7 peacock, 9 blueberry, 10 basil, 11 tomato
KIND = {
    "live":     ("10", [10, 0], True),    # goes live automatically – first hour: comments
    "manual":   ("9", [30, 0], True),     # post by hand
    "approval": ("5", [0], True),         # posting time, but only after "go"
    "waiting":  ("6", [0], True),         # posting time, something is still missing
    "error":    ("11", [0], True),        # posting failed
    "deliver":  ("6", [0], False),        # to-do: deliver voice note/clips/concept
    "music":    ("3", [0], False),        # to-do: pick music
    "files":    ("11", [0], False),       # to-do: files missing
    "linkedin": ("7", [0], False),        # Chrome module 5
    "reminder": ("3", [1440, 0], False),  # deadline/decision from automation/reminders.json
}


def event(uid, start, minutes, title, text, kind):
    """One event as data for the Google sync (calendar_sync.py)."""
    return {"uid": uid, "start": start, "end": start + timedelta(minutes=minutes), "title": title, "text": text,
            "kind": kind}


def name(e):
    topic = e["id"].split("-", 1)[-1]
    topic = topic.removeprefix(e["type"] + "-").replace("-", " ")
    return f"{TYPE.get(e['type'], e['type'])} “{topic}”"


def first_line(e):
    if not e.get("caption"):
        return ""
    file = ROOT / e["folder"] / e["caption"]
    if file.exists():
        lines = file.read_text(encoding="utf-8").strip().splitlines()
        return lines[0] if lines else ""
    return ""


def script_link(e):
    path = f"{e['folder']}/script.md"
    return f"Script: https://github.com/{REPO}/blob/{BRANCH}/{path}\n" if (ROOT / path).exists() else ""


def linkedin_enabled():
    try:
        return bool(json.loads((ROOT / "automation" / "interaction.json").read_text()).get("linkedin", {}).get("enabled"))
    except (OSError, ValueError):
        return False


def entries_to_events(entries, now):
    t = []
    li_on = linkedin_enabled()
    for e in entries:
        s, start = e["status"], planned(e)
        if s == "cancelled" or start < now - LOOKBACK:
            continue
        info = "\n".join(x for x in (first_line(e), e.get("note", ""),
                                      f"Approval: https://github.com/{REPO}/issues/{e['issue']}" if e.get("issue") else "") if x)
        if e["type"] in FEED or s == "manual":
            if s == "manual":
                kind, title, text = "manual", f"✋ {name(e)} – post by hand", "Post it in the Instagram app."
            elif s == "draft":
                kind, title = "approval", f"🟡 {name(e)} – approve first"
                text = f"Only goes live after \"go\" in the issue: {APPROVALS}"
            elif s.startswith("waiting_"):
                kind, title = "waiting", f"⏳ {name(e)} – waiting: {s.removeprefix('waiting_').replace('_', ' ')}"
                text = "Only goes live once the missing piece is there."
            elif s == "error":
                kind, title, text = "error", f"🔴 {name(e)} – posting failed", e.get("error_message", "")[:300]
            else:
                kind, title = "live", f"{name(e)} live – reply to comments"
                text = "Goes live automatically. First hour: answer every comment with a follow-up question, check TOOL DMs."
                if e.get("link"):
                    text += f"\n{e['link']}"
            if e.get("after"):
                text += f"\nAfterwards: {e['after']}"
            t.append(event(e["id"], start, 45 if e["type"] in FEED else 15, title, f"{text}\n{info}".strip(), kind))
        if li_on and e["type"] == "carousel" and s in ("approved", "published") \
                and (ROOT / e["folder"] / "linkedin" / "carousel.pdf").exists():
            li = (start + timedelta(days=1)).replace(hour=8, minute=0)
            while li.weekday() >= 5:  # LinkedIn never on weekends
                li += timedelta(days=1)
            t.append(event(f"{e['id']}-linkedin", li, 15, f"💼 LinkedIn: post {name(e)} (Chrome module 5)",
                           f"PDF + text are in the issue: https://github.com/{REPO}/issues?q=is%3Aopen+label%3Alinkedin\n"
                           f"Chrome Claude: paste the main prompt from {CHROME}, then \"module 5\". Only submit after your go.",
                           "linkedin"))
        if start <= now:
            continue
        soon = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        # 5 days ahead at 7:00 PM, at the earliest the next full hour – but never after the posting time
        due = min(max((start - timedelta(days=5)).replace(hour=19, minute=0), soon),
                  start - timedelta(minutes=30))
        if s.startswith("waiting_"):
            t.append(event(f"{e['id']}-todo", due,
                           20, f"📦 Deliver for {name(e)}: {s.removeprefix('waiting_').replace('_', ' ')}",
                           f"Posting time {when(start)}. Upload the files or tell Claude.\n{script_link(e)}{info}", "deliver"))
        if e.get("music_missing"):
            t.append(event(f"{e['id']}-music", due, 15,
                           f"🎵 Music missing: {name(e)}", f"Posting time {when(start)}. Send a track/mood to Claude or pick one in the app.", "music"))
        if s in ("approved", "draft", "manual") and (missing := missing_files(e)):
            t.append(event(f"{e['id']}-files", due, 15,
                           f"🔴 Files missing: {name(e)}", ", ".join(missing), "files"))
    return t


def reminders_to_events(now):
    """One-time reminders from automation/reminders.json (only calendar = true, not done)."""
    return [event(f"reminder-{r['id']}", r["start"], 30, r["title"], r.get("text", ""), "reminder")
            for r in reminders() if r.get("calendar") and r["start"] >= now - LOOKBACK]


def all_events(now=None):
    from status import PLAN
    now = now or datetime.now(ZONE)
    return entries_to_events(json.loads(PLAN.read_text())["entries"], now) + reminders_to_events(now)


if __name__ == "__main__":
    for ev in sorted(all_events(), key=lambda x: x["start"]):
        print(f"{when(ev['start'])} · {ev['kind']:<8} · {ev['title']}")
