"""Daily report as an image:  python3 automation/daily_report.py [YYYY-MM-DD]

Reads the newest (or given) and the previous automation/stats/insights_*.json and writes
automation/reports/daily_report_<date>.html, .png (1080 wide) and .json (metrics + method check
for the assessment). Image via Playwright (installed globally, Chromium from /opt/pw-browsers) – without
Playwright/Node only HTML + JSON are written. Times in US Eastern (ET), numbers in US format.
"""
import html, json, shutil, subprocess, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
STATS = ROOT / "automation/stats"
OUT = ROOT / "automation/reports"
ZONE = ZoneInfo("America/New_York")
PACIFIC = ZoneInfo("America/Los_Angeles")  # Instagram reports online_followers hours in Pacific time
START = "2026-10-11"  # launch of @maehrtax; older posts do not count as a benchmark
WEEKDAY = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

files = sorted(STATS.glob("insights_*.json"))
if len(sys.argv) > 1:
    files = [d for d in files if d.stem.split("_")[1] <= sys.argv[1]]
if not files:
    print("Daily report: no automation/stats/insights_*.json yet – nothing to report (stats start after setup).")
    sys.exit(0)
today_f, prev_f = files[-1], (files[-2] if len(files) > 1 else None)
d = json.loads(today_f.read_text())
v = json.loads(prev_f.read_text()) if prev_f else {}
# previous day = state of the last report (morning snapshot), not the insights file overwritten during the day
OUT.mkdir(parents=True, exist_ok=True)
baseline = sorted(p for p in OUT.glob("baseline_*.json") if p.stem.split("_")[1] < d["fetched"])
if baseline:
    v = json.loads(baseline[-1].read_text())
(OUT / f"baseline_{d['fetched']}.json").write_text(json.dumps(d, ensure_ascii=False))
day = d["fetched"]
plan = json.loads((ROOT / "automation/plan.json").read_text())["entries"]


def fmt(x):
    return "–" if x is None else f"{x:,.0f}"


def delta(a, b):
    if a is None or b is None or a == b:
        return ""
    return f'<span class="d {"up" if a > b else "down"}">{"+" if a > b else "−"}{fmt(abs(a - b))}</span>'


def pct(q, n=0):
    return "–" if q is None else f"{q * 100:.{n}f}%"


def ratio(a, b):
    return None if not b or a is None else a / b


def et(ts):
    t = datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=ZoneInfo("UTC")).astimezone(ZONE)
    return f"{WEEKDAY[t.weekday()]} {t.month}/{t.day} {t.hour % 12 or 12}:{t:%M} {'AM' if t.hour < 12 else 'PM'}"


k, kv = d["account"], v.get("account", {})
fol, fol_v = k["followers_count"], kv.get("followers_count")
dr = d.get("daily_reach") or {}
days = sorted(dr)[-14:]
yesterday = days[-1] if days else None
r_yesterday = dr.get(yesterday)
r_before = dr.get(days[-2]) if len(days) > 1 else None
m30 = (d.get("account_history") or [{}])[0]
split = (m30.get("reach") or {}).get("breakdown", {}) if isinstance(m30.get("reach"), dict) else {}
nf, ff = split.get("NON_FOLLOWER", 0), split.get("FOLLOWER", 0)
nf_ratio = ratio(nf, nf + ff)
links = (m30.get("profile_links_taps") or {}).get("total") or 0 if isinstance(m30.get("profile_links_taps"), dict) else 0

# posts since launch
prev_media = {b["id"]: b for b in v.get("media", [])}
media = [b for b in d.get("media", []) if (b.get("timestamp") or "")[:10] >= START]
media.sort(key=lambda b: b["timestamp"], reverse=True)
plan_by_link = {e.get("link"): e for e in plan if e.get("link")}


def name(b):
    e = plan_by_link.get(b.get("permalink"))
    if e:
        return e["id"]
    return (b.get("caption") or "").split("\n")[0][:34]


rows = []
for b in media:
    p = prev_media.get(b["id"], {})
    kind = "Reel" if b.get("media_product_type") == "REELS" else ("Carousel" if b.get("media_type") == "CAROUSEL_ALBUM" else "Image")
    rows.append(dict(name=name(b), type=kind, time=et(b["timestamp"]), link=b.get("permalink"),
        views=b.get("views"), reach=b.get("reach"), likes=b.get("likes"), comments=b.get("comments"),
        saved=b.get("saved"), shares=b.get("shares"), profile=b.get("profile_visits"), follows=b.get("follows"),
        watch=(b.get("ig_reels_avg_watch_time") or 0) / 1000 or None, skip=b.get("reels_skip_rate"),
        v_views=p.get("views"), v_reach=p.get("reach"), v_saved=p.get("saved"), v_shares=p.get("shares"), v_comments=p.get("comments")))

stories = [s for s in d.get("active_stories", []) if s.get("views") is not None]


# method check: (method, metric, value text, goal, status)
def st(value, goal, close=None):
    if value is None:
        return "⏳"
    if value >= goal:
        return "✅"
    if close is not None and value >= close:
        return "⚠️"
    return "❌"


reels = [z for z in rows if z["type"] == "Reel"]
carousels = [z for z in rows if z["type"] == "Carousel"]
r0 = reels[0] if reels else None
c0 = carousels[0] if carousels else None
s_reach = max((s.get("reach") or 0 for s in stories), default=None)
s_replies = sum(s.get("replies") or 0 for s in stories) if stories else None
profile = sum(z["profile"] or 0 for z in rows)
follows = sum(z["follows"] or 0 for z in rows)
online = d.get("online_followers", {})
on = next((online[t] for t in sorted(online, reverse=True) if online[t]), {})
# hours from Instagram (Pacific) → ET hours
on_et = {}
for h, n in (on or {}).items():
    pt = datetime(2026, 1, 15, int(h), tzinfo=PACIFIC)
    on_et[pt.astimezone(ZONE).hour] = n
peak = max(on_et.values()) if on_et else None
on_1230 = ratio(on_et.get(12), peak) if on_et else None
on_1930 = ratio(on_et.get(19), peak) if on_et else None
ref = c0 or r0 or {}

methods = [
    ("Reels reach non-followers", "Share of non-followers in reach (30 days)",
     pct(nf_ratio) if nf_ratio is not None else "–", "≥ 50%", st(nf_ratio, .5, .35)),
    ("Hook in the first 1.5 s", f"Skip rate of the last Reel ({r0['name'] if r0 else '–'})",
     f"{r0['skip']:.0f}%" if r0 and r0["skip"] is not None else "–", "< 60%",
     "⏳" if not r0 or r0["skip"] is None else ("✅" if r0["skip"] < 60 else ("⚠️" if r0["skip"] < 70 else "❌"))),
    ("\"Who sends this to whom?\"", f"Shares ÷ reach ({ref.get('name', '–')})",
     (lambda q: pct(q, 1) if q is not None else "–")(ratio(ref.get("shares"), ref.get("reach"))),
     "≥ 3%", st(ratio(ref.get("shares"), ref.get("reach")), .03, .015)),
    ("Saveable content", f"Saves ÷ reach ({c0['name'] if c0 else '–'})",
     (lambda q: pct(q, 1) if q is not None else "–")(ratio(c0 and c0["saved"], c0 and c0["reach"])),
     "≥ 2%", st(ratio(c0 and c0["saved"], c0 and c0["reach"]), .02, .01)),
    ("Morning story with a question", "Story reach ÷ followers · replies",
     f"{pct(s_reach / fol)} · {s_replies} replies" if s_reach and fol else "–", "≥ 15% · ≥ 1",
     "⏳" if not s_reach or not fol else ("✅" if s_reach / fol >= .15 and s_replies else "⚠️")),
    ("Profile converts visitors", "Follows ÷ profile visits (posts since launch)",
     f"{follows} / {profile}" if profile else "–", "≥ 10%", st(ratio(follows, profile), .10, .05) if profile else "⏳"),
    ("DM TOOL / bio link", "Bio link taps (30 days)", str(links), "≥ 1 per week", "✅" if links else "❌"),
    ("Reels at 12:30 PM ET", "Followers online 12–1 PM ET ÷ peak hour", pct(on_1230) if on_1230 else "–", "≥ 85%", st(on_1230, .85, .7)),
    ("Carousels at 7:30 PM ET", "Followers online 7–8 PM ET ÷ peak hour", pct(on_1930) if on_1930 else "–", "≥ 85%", st(on_1930, .85, .7)),
]

live_today = [e for e in plan if e["time"][:10] == day and e["status"] in ("approved", "manual")]
errors = [e["id"] for e in plan if e["status"] == "error"]


# --- HTML ---
def chart():
    if not days:
        return '<p class="m">No daily reach yet.</p>'
    w, h, pad = 960, 220, 30
    mx = max([dr[t] for t in days] + [1])
    bw = (w - 2 * pad) / len(days)
    posted = {z["time"].split(" ")[1] for z in rows}
    out = [f'<svg viewBox="0 0 {w} {h + 46}" width="{w}" height="{h + 46}">',
           f'<line x1="{pad}" y1="{h}" x2="{w - pad}" y2="{h}" stroke="#2a3a33" stroke-width="1"/>']
    for i, t in enumerate(days):
        val = dr[t]
        bh = max(3, (h - 20) * val / mx)
        x = pad + i * bw + 4
        label = f"{int(t[5:7])}/{int(t[8:10])}"
        color = "#53C3A2" if label in posted else "#2E6B5B"
        out.append(f'<rect x="{x:.1f}" y="{h - bh:.1f}" width="{bw - 8:.1f}" height="{bh:.1f}" rx="4" fill="{color}"/>')
        out.append(f'<text x="{x + (bw - 8) / 2:.1f}" y="{h - bh - 6:.1f}" text-anchor="middle" class="bv">{val:,}</text>')
        out.append(f'<text x="{x + (bw - 8) / 2:.1f}" y="{h + 20}" text-anchor="middle" class="bl">{label}</text>')
    out.append(f'<text x="{pad}" y="{h + 42}" class="bl">bright = day with a new post</text></svg>')
    return "".join(out)


def tile(title, value, d_html="", sub=""):
    return f'<div class="tile"><div class="kt">{title}</div><div class="kw">{value}{d_html}</div><div class="ku">{sub}</div></div>'


def skip_watch(z):
    if z["skip"] is None:
        return "–"
    return f"{z['skip']:.0f}% · {z['watch']:.1f} s" if z["watch"] else f"{z['skip']:.0f}%"


post_rows = "".join(
    f'<tr><td><b>{html.escape(z["name"])}</b><br><span class="m">{z["type"]} · {z["time"]}</span></td>'
    f'<td>{fmt(z["views"])}{delta(z["views"], z["v_views"])}</td><td>{fmt(z["reach"])}{delta(z["reach"], z["v_reach"])}</td>'
    f'<td>{fmt(z["likes"])}</td><td>{fmt(z["comments"])}{delta(z["comments"], z["v_comments"])}</td>'
    f'<td>{fmt(z["saved"])}{delta(z["saved"], z["v_saved"])}</td><td>{fmt(z["shares"])}{delta(z["shares"], z["v_shares"])}</td>'
    f'<td>{fmt(z["profile"])}</td><td>{skip_watch(z)}</td></tr>'
    for z in rows) or '<tr><td colspan="9" class="m">no posts since launch yet</td></tr>'
story_rows = "".join(
    f'<tr><td>Story {et(s["time"])}</td><td>{fmt(s.get("views"))}</td><td>{fmt(s.get("reach"))}</td>'
    f'<td>{fmt(s.get("replies"))}</td><td>{fmt(s.get("navigation"))}</td><td>{fmt(s.get("profile_visits"))}</td></tr>'
    for s in stories) or '<tr><td colspan="6" class="m">no story in the last 24 h</td></tr>'
method_rows = "".join(
    f'<tr><td class="st">{s}</td><td><b>{html.escape(a)}</b><br><span class="m">{html.escape(b)}</span></td><td class="w">{html.escape(c)}</td><td class="m">{html.escape(z)}</td></tr>'
    for a, b, c, z, s in methods)
wt = datetime.strptime(day, "%Y-%m-%d")
title_day = f"{WEEKDAY[wt.weekday()]} {wt.month}/{wt.day}/{wt.year}"

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><style>
@import url("../../templates/fonts.css");
body{{margin:0;width:1080px;background:#0B110E;color:#EAF1EC;font-family:"IBM Plex Sans",sans-serif;padding:44px 50px}}
h1{{font-family:"IBM Plex Serif",serif;font-weight:600;font-size:46px;margin:0 0 4px}}
.kick{{font-family:"IBM Plex Mono",monospace;letter-spacing:.25em;text-transform:uppercase;color:#53C3A2;font-size:16px;font-weight:600}}
h2{{font-family:"IBM Plex Mono",monospace;letter-spacing:.18em;text-transform:uppercase;color:#53C3A2;font-size:15px;margin:34px 0 12px}}
.tiles{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}}
.tile{{background:#12201B;border:1px solid #1f3a31;border-radius:16px;padding:16px 18px}}
.kt{{font-size:15px;color:#8FA398}} .kw{{font-size:40px;font-weight:600;margin-top:4px}} .ku{{font-size:14px;color:#8FA398;margin-top:2px}}
.d{{font-size:16px;font-weight:600;margin-left:8px;vertical-align:middle}} .up{{color:#53C3A2}} .down{{color:#E07A6B}}
table{{width:100%;border-collapse:collapse;font-size:17px}}
th{{text-align:left;color:#8FA398;font-weight:500;font-size:14px;padding:8px 8px;border-bottom:1px solid #2a3a33}}
td{{padding:10px 8px;border-bottom:1px solid #18261f;vertical-align:top}}
td .d{{font-size:13px;margin-left:5px}}
.m{{color:#8FA398;font-size:14px}} .st{{font-size:24px;width:40px}} .w{{font-weight:600;white-space:nowrap}}
.bv{{fill:#C9D6CE;font-size:14px;font-family:"IBM Plex Mono",monospace}} .bl{{fill:#8FA398;font-size:13px;font-family:"IBM Plex Sans",sans-serif}}
.leg{{color:#8FA398;font-size:14px;margin-top:10px}}
</style></head><body>
<div class="kick">@maehrtax · Daily report</div><h1>{title_day}</h1>
<div class="tiles">
{tile("Followers", fmt(fol), delta(fol, fol_v), f"you follow {k.get('follows_count', 0):,}")}
{tile("Reach yesterday", fmt(r_yesterday), delta(r_yesterday, r_before), "accounts reached")}
{tile("Non-followers (30 d)", pct(nf_ratio) if nf_ratio is not None else "–", "", f"{nf:,} of {nf + ff:,} accounts")}
{tile("Bio link taps", str(links), "", f"30 days · {m30.get('replies', 0) or 0} story replies")}
</div>
<h2>Reach per day</h2>{chart()}
<h2>Posts since launch (Δ vs. previous day)</h2>
<table><tr><th>Post</th><th>Views</th><th>Reach</th><th>Likes</th><th>Comm.</th><th>Saves</th><th>Shares</th><th>Profile</th><th>Skip · avg watch</th></tr>{post_rows}</table>
<h2>Stories (last 24 h)</h2>
<table><tr><th>Story</th><th>Views</th><th>Reach</th><th>Replies</th><th>Taps</th><th>Profile</th></tr>{story_rows}</table>
<h2>Are our methods working?</h2>
<table><tr><th></th><th>Method · metric</th><th>Actual</th><th>Goal</th></tr>{method_rows}</table>
<div class="leg">✅ working · ⚠️ close / too early · ❌ not working (yet) · ⏳ no data</div>
</body></html>"""

html_f = OUT / f"daily_report_{day}.html"
png_f = OUT / f"daily_report_{day}.png"
html_f.write_text(page)
(OUT / f"daily_report_{day}.json").write_text(json.dumps(dict(
    day=day, followers=fol, followers_prev=fol_v, reach_yesterday=r_yesterday, reach_day_before=r_before,
    non_follower_ratio=nf_ratio, link_taps=links, posts=rows, stories=stories,
    methods=[dict(method=a, metric=b, actual=c, goal=z, status=s) for a, b, c, z, s in methods],
    live_today=[f'{e["time"][11:]} ET {e["type"]} {e["id"]}' for e in live_today], errors=errors),
    ensure_ascii=False, indent=1, default=str))

if not shutil.which("node"):
    print(f"Note: node not found – only {html_f.name} + JSON written, no PNG.")
    sys.exit(0)
js = f"""const {{createRequire}}=require('module');const {{execSync}}=require('child_process');
const {{chromium}}=createRequire(execSync('npm root -g').toString().trim()+'/')('playwright');
(async()=>{{const b=await chromium.launch({{executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'}});
const p=await b.newPage({{viewport:{{width:1080,height:800}},deviceScaleFactor:1.5}});
await p.goto('file://{html_f}');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({{path:'{png_f}',fullPage:true}});await b.close();}})();"""
subprocess.run(["node", "-e", js], check=True)
print(png_f)
