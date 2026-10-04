"""Weekly report (Sundays around 6:00 PM ET): ONE issue "📊 Week 42" – one notification per week.

  python automation/weekly_report.py report           – build the report, quietly close last week's issue
  python automation/weekly_report.py reply NR "TEXT"  – take over Loris' additions from the issue:
        demos 2                      → demos booked this week
        manychat 14/6                → ManyChat: sent / clicks on the demo link
        source manychat 1, bio 1     → where the demos came from (free text, comma separated)
     Several items in one comment work too. Taken over quietly into the issue body (no reply notification).

Sources: automation/stats/account.csv + media.csv (Instagram), closed radar issues (ticks),
automation/interaction/comments.json (comment helper), strategy/dm_tracking.csv (demo_booked = yes),
demo bookings as copies in the calendar "maehrtax Autopilot" (Apps Script automation/apps_script/demo_copy.gs).
All values also go into automation/stats/weeks.csv. Weeks are Mon–Sun in US Eastern time.
Environment: GH_TOKEN, GITHUB_REPOSITORY, GOOGLE_SA_KEY + GOOGLE_CALENDAR_ID (optional, for demo bookings).
"""
import csv, json, os, re, subprocess, sys, time
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
STATS = ROOT / "automation" / "stats"
WEEKS = STATS / "weeks.csv"
COMMENTS = ROOT / "automation" / "interaction" / "comments.json"
DM_TRACKING = ROOT / "strategy" / "dm_tracking.csv"
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/maehrtax---instagram")
LABEL = "weekly"
DEMO_MARKER = "maehrtax-demo"
FIELDS = ["week", "from", "to", "followers_start", "followers_end", "growth", "views_week", "reach_new",
          "saves_new", "shares_new", "new_posts", "radar_commented", "radar_dms", "comments_answered",
          "demos_tracking", "demos_calendar", "source_calendar", "demos_manual", "manychat_sent", "manychat_clicks", "source"]
MANUAL = ("demos_manual", "manychat_sent", "manychat_clicks", "source")


def gh(*args, stdin=None):
    return subprocess.run(["gh", *args, "--repo", REPO], input=stdin, check=True, capture_output=True, text=True).stdout.strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def num(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return 0


def read(file, sep=","):
    if not file.exists():
        return []
    with file.open(newline="") as f:
        return list(csv.DictReader(f, delimiter=sep))


def us(d):
    return f"{d.month}/{d.day}/{d.year}"


# ---------- numbers ----------

def followers(start_day, end_day):
    rows = sorted(read(STATS / "account.csv"), key=lambda z: z["date"])
    before = [z for z in rows if z["date"] < start_day.isoformat()] or [z for z in rows if z["date"] <= end_day.isoformat()][:1]
    after = [z for z in rows if z["date"] <= end_day.isoformat()]
    start = num(before[-1]["followers_count"]) if before else 0
    end = num(after[-1]["followers_count"]) if after else start
    return start, end


def media(start_day, end_day):
    """Last state per post until the end of the week. Views of the week = growth per post compared with the state
    before the week – if that is missing (stats did not run yet), the first state in the week is the baseline, so old
    views do not show up as new. Top 3 only from posts of the last 4 weeks."""
    rows = sorted(read(STATS / "media.csv"), key=lambda z: z["date"])
    at_end, base = {}, {}
    for z in rows:
        if z["date"] < start_day.isoformat():
            base[z["id"]] = z
        elif z["date"] <= end_day.isoformat():
            if z["id"] not in base and z["posted"] < start_day.isoformat():
                base[z["id"]] = z  # first state in the week
            at_end[z["id"]] = z
    views = sum(max(0, num(z["views"]) - num(base.get(i, {}).get("views"))) for i, z in at_end.items())
    new = [z for z in at_end.values() if start_day.isoformat() <= z["posted"] <= end_day.isoformat()]
    recent = [z for z in at_end.values() if z["posted"] >= (start_day - timedelta(days=21)).isoformat() and num(z["reach"]) >= 20]
    top = sorted(recent, key=lambda z: -(num(z["saved"]) + num(z["shares"])) / max(1, num(z["reach"])))[:3]
    return views, new, top


def radar(start_day, end_day):
    """Ticked boxes in the radar issues of the week."""
    try:
        issues = json.loads(gh("issue", "list", "--label", "radar", "--state", "all", "--limit", "20",
                               "--json", "title,body,createdAt"))
    except (subprocess.CalledProcessError, OSError):
        return 0, 0
    commented = dms = 0
    for i in issues:
        if start_day.isoformat() <= i["createdAt"][:10] <= end_day.isoformat():
            commented += len(re.findall(r"^- \[[xX]\] 💬", i["body"], re.M))
            dms += len(re.findall(r"^- \[[xX]\] ✉️", i["body"], re.M))
    return commented, dms


def comments(start_day, end_day):
    if not COMMENTS.exists():
        return 0
    items = json.loads(COMMENTS.read_text()).get("comments", {}).values()
    return sum(1 for k in items if k.get("status") == "answered" and start_day.isoformat() <= k.get("date", "") <= end_day.isoformat())


def demos_tracking(start_day, end_day):
    rows = read(DM_TRACKING, ";")
    return sum(1 for z in rows if start_day.isoformat() <= z.get("date", "") <= end_day.isoformat()
               and z.get("demo_booked", "").strip().lower() in ("yes", "y", "x", "1"))


def demos_calendar(start_day, end_day):
    """Demo bookings of the week from the calendar GOOGLE_CALENDAR_ID ("maehrtax Autopilot"). There the Apps Script
    automation/apps_script/demo_copy.gs (runs in Loris' Google account) creates one copy per real Reclaim booking:
    description "maehrtax-demo / Booked: YYYY-MM-DD / Source: …" – without names and emails.
    Returns (count, "Instagram 2, LinkedIn 1") – or ("", "") without access."""
    if not os.environ.get("GOOGLE_SA_KEY") or not os.environ.get("GOOGLE_CALENDAR_ID"):
        return "", ""
    from calendar_sync import session
    s, page, events = session(), None, []
    # no q search: Google's full-text search splits "maehrtax-demo" unreliably – better fetch all events
    # (paging, the calendar has hundreds) and filter below
    while True:
        params = {"timeMin": f"{(start_day - timedelta(days=14)).isoformat()}T00:00:00Z",
                  "timeMax": f"{(end_day + timedelta(days=100)).isoformat()}T00:00:00Z",
                  "singleEvents": "true", "maxResults": 250}
        if page:
            params["pageToken"] = page
        r = s.get(f"https://www.googleapis.com/calendar/v3/calendars/{os.environ['GOOGLE_CALENDAR_ID']}/events",
                  params=params, timeout=60)
        r.raise_for_status()
        events += r.json().get("items", [])
        if not (page := r.json().get("nextPageToken")):
            break
    count, sources = 0, {}
    for e in events:
        text = e.get("description", "")
        booked = re.search(r"Booked:[ \t]*(\d{4}-\d{2}-\d{2})", text)
        if e.get("status") == "cancelled" or DEMO_MARKER not in text or not booked \
                or not start_day.isoformat() <= booked.group(1) <= end_day.isoformat():
            continue
        count += 1
        # [ \t]* instead of \s*: with an empty source, do not slip into the next line ("(Copy from …")
        source = (re.search(r"Source:[ \t]*([^\n]*)", text) or [None, ""])[1].strip() or "unknown"
        sources[source] = sources.get(source, 0) + 1
    return str(count), ", ".join(f"{q} {n}" for q, n in sorted(sources.items(), key=lambda x: -x[1]))


# ---------- file + issue ----------

def load_table():
    return {z["week"]: z for z in read(WEEKS)}


def save_table(rows, message):
    STATS.mkdir(parents=True, exist_ok=True)
    with WEEKS.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(sorted(rows.values(), key=lambda z: z["week"]))
    git("add", str(WEEKS))
    if not git("status", "--porcelain", "--", str(WEEKS)):
        return
    git("commit", "-m", message)
    for attempt in range(5):
        try:
            git("pull", "--rebase", "-q")
            git("push")
            return
        except subprocess.CalledProcessError:
            subprocess.run(["git", "rebase", "--abort"], cwd=ROOT, capture_output=True)  # otherwise every retry fails the same way
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("weeks.csv could not be saved")


def body(z, new, top):
    arrow = "📈" if num(z["growth"]) > 0 else ("📉" if num(z["growth"]) < 0 else "➖")
    manual = lambda k, empty="_open_": z.get(k) or empty
    lines = [
        f"@{REPO.split('/')[0]} Here is your week in one screen.",
        "",
        "## Reach",
        f"- Followers: {num(z['followers_start']):,} → **{num(z['followers_end']):,}** ({arrow} {num(z['growth']):+d})",
        f"- New views (all posts): **{num(z['views_week']):,}**",
        f"- New posts: {z['new_posts']} · reach {num(z['reach_new']):,} · saves {z['saves_new']} · shares {z['shares_new']}",
        "",
        "**Top 3 of the last 4 weeks – (saves + shares) / reach**",
    ]
    lines += [f"{n}. [{(t['first_line'] or t['type'])[:50]}]({t['link']}) – {num(t['saved'])} saves, "
              f"{num(t['shares'])} shares, reach {num(t['reach']):,}" for n, t in enumerate(top, 1)] or ["_not enough data yet_"]
    lines += [
        "",
        "## Engagement",
        f"- Radar: {z['radar_commented']} comments, {z['radar_dms']} DMs ticked",
        f"- Comment helper: {z['comments_answered']} answered",
        "",
        "## Funnel",
        "| Stage | Week |",
        "|---|---|",
        f"| ManyChat sent | {manual('manychat_sent')} |",
        f"| Clicks on the demo link | {manual('manychat_clicks')} |",
        f"| Demos booked (by hand) | {manual('demos_manual')} |",
        f"| Demos in the calendar (Reclaim) | {z.get('demos_calendar') or '_not connected yet_'} |",
        f"| Demos in `dm_tracking.csv` | {z['demos_tracking']} |",
        f"| Source (booking field) | {z.get('source_calendar') or '–'} |",
        f"| Source (by hand) | {manual('source', '_open_')} |",
        "",
        "**Add numbers** – just comment here, they are taken over quietly:",
        "`demos 2` · `manychat 14/6` (sent/clicks) · `source manychat 1, bio 1`",
        "",
        f"<sub>Week {z['week']} · {us(date.fromisoformat(z['from']))} to {us(date.fromisoformat(z['to']))} · raw data: `automation/stats/weeks.csv`</sub>",
    ]
    return "\n".join(lines)


def report():
    today = datetime.now(ZoneInfo("America/New_York")).date()
    end_day = today - timedelta(days=(today.weekday() + 1) % 7)  # last Sunday (today, if Sunday)
    start_day = end_day - timedelta(days=6)
    week = f"{end_day.isocalendar()[0]}-{end_day.isocalendar()[1]:02d}"
    table = load_table()
    old = table.get(week, {})
    start, end = followers(start_day, end_day)
    views, new, top = media(start_day, end_day)
    r_com, r_dm = radar(start_day, end_day)
    z = {"week": week, "from": start_day.isoformat(), "to": end_day.isoformat(), "followers_start": start, "followers_end": end,
         "growth": end - start, "views_week": views,
         "reach_new": sum(num(b["reach"]) for b in new), "saves_new": sum(num(b["saved"]) for b in new),
         "shares_new": sum(num(b["shares"]) for b in new), "new_posts": len(new),
         "radar_commented": r_com, "radar_dms": r_dm, "comments_answered": comments(start_day, end_day),
         "demos_tracking": demos_tracking(start_day, end_day), **{k: old.get(k, "") for k in MANUAL}}
    try:
        z["demos_calendar"], z["source_calendar"] = demos_calendar(start_day, end_day)
    except Exception as err:  # the calendar must never block the report
        print(f"Note: demo bookings not readable ({err})")
        z["demos_calendar"], z["source_calendar"] = "", ""
    table[week] = {k: str(v) for k, v in z.items()}
    nr = end_day.isocalendar()[1]
    title = f"📊 Week {nr} – {end:,} followers ({end - start:+d})"
    found = json.loads(gh("issue", "list", "--label", LABEL, "--state", "open", "--json", "number,title"))
    same = [i for i in found if f"Week {nr} " in i["title"]]
    try:
        gh("label", "create", LABEL, "--color", "53C3A2", "--description", "Weekly report, Sundays")
    except subprocess.CalledProcessError:
        pass
    if same:  # second run in the same week: only update, no new notification
        gh("issue", "edit", str(same[0]["number"]), "--title", title, "--body-file", "-", stdin=body(table[week], new, top))
    else:
        print(gh("issue", "create", "--title", title, "--label", LABEL, "--body-file", "-", stdin=body(table[week], new, top)))
        for i in found:
            gh("issue", "close", str(i["number"]))  # close last week quietly
    save_table(table, f"Weekly report week {week}")
    print(f"✓ {title}")


def reply(number, comment):
    title = gh("issue", "view", str(number), "--json", "title", "--jq", ".title")
    match = re.search(r"Week (\d+)", title)
    table = load_table()
    week = next((k for k in sorted(table, reverse=True) if match and k.endswith(f"-{int(match.group(1)):02d}")), None)
    if not week:
        print("No matching week found – nothing to do.")
        return
    z, before = table[week], dict(table[week])
    # only items at the start of a line or after a comma/semicolon – quoted issue lines ("> | Demos in …") and the
    # line "Total ManyChat: sent X / clicks Y" from Chrome module 1 do not count this way
    lead = r"(?:^|[,;]\s*)"
    lines = "\n".join(l for l in comment.splitlines() if not l.lstrip().startswith(">"))
    if m := re.search(lead + r"demos?\s*[:=]?\s*(\d+)\b", lines, re.I | re.M):
        z["demos_manual"] = m.group(1)
    if m := re.search(lead + r"manychat\s*[:=]?\s*(\d+)\s*/\s*(\d+)", lines, re.I | re.M):
        z["manychat_sent"], z["manychat_clicks"] = m.group(1), m.group(2)
    if m := re.search(lead + r"source\s*[:=]?\s*([^\n]+)", lines, re.I | re.M):
        z["source"] = m.group(1).strip()[:200]
    if z == before:
        print("Nothing recognized – nothing to do.")
        return
    start_day, end_day = date.fromisoformat(z["from"]), date.fromisoformat(z["to"])
    _, new, top = media(start_day, end_day)
    gh("issue", "edit", str(number), "--body-file", "-", stdin=body(z, new, top))
    save_table(table, f"Weekly report week {week}: addition")
    print("✓ taken over")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("report", "reply"):
        sys.exit("Usage: weekly_report.py report | reply ISSUE TEXT")
    if not os.environ.get("GH_TOKEN"):
        print("Weekly report: GH_TOKEN missing – nothing to do.")
        sys.exit(0)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    if sys.argv[1] == "report":
        report()
    else:
        reply(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "")
