"""Tagesbericht als Bild:  python3 automatik/tagesbericht.py [JJJJ-MM-TT]

Liest die neueste (bzw. angegebene) und die vorherige automatik/statistik/insights_*.json und schreibt
automatik/berichte/tagesbericht_<datum>.html, .png (1080 breit) und .json (Kennzahlen + Methoden-Check
für die Einschätzung). Bild per Playwright (global installiert, Chromium aus /opt/pw-browsers).
"""
import json, subprocess, sys, html
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ST = ROOT / "automatik/statistik"
OUT = ROOT / "automatik/berichte"
START = "2026-09-29"  # Neustart der Seite; ältere Beiträge zählen nicht als Maßstab

dateien = sorted(ST.glob("insights_*.json"))
if len(sys.argv) > 1:
    dateien = [d for d in dateien if d.stem.split("_")[1] <= sys.argv[1]]
heute_f, vor_f = dateien[-1], (dateien[-2] if len(dateien) > 1 else None)
d = json.loads(heute_f.read_text())
v = json.loads(vor_f.read_text()) if vor_f else {}
tag = d["abgerufen"]
plan = json.loads((ROOT / "automatik/plan.json").read_text())["eintraege"]

def zahl(x):
    return "–" if x is None else f"{x:,.0f}".replace(",", ".")

def delta(a, b):
    if a is None or b is None or a == b: return ""
    return f'<span class="d {"up" if a > b else "down"}">{"+" if a > b else "−"}{zahl(abs(a - b))}</span>'

def pct(q, n=0):
    return "–" if q is None else f"{q*100:.{n}f} %".replace(".", ",")

def quote(a, b):
    return None if not b or a is None else a / b

k, kv = d["konto"], v.get("konto", {})
fol, fol_v = k["followers_count"], kv.get("followers_count")
tw = d["tageswerte_reichweite"]
tage = sorted(tw)[-14:]
gestern = tage[-1] if tage else None
r_gestern = tw.get(gestern)
r_vortag = tw.get(tage[-2]) if len(tage) > 1 else None
m30 = d["konto_verlauf"][0]
nf = m30["reach"]["aufgeteilt"].get("NON_FOLLOWER", 0); ff = m30["reach"]["aufgeteilt"].get("FOLLOWER", 0)
nf_quote = quote(nf, nf + ff)
links = (m30.get("profile_links_taps") or {}).get("gesamt") or 0

# Beiträge seit Neustart
vor_bt = {b["id"]: b for b in v.get("beitraege", [])}
bt = [b for b in d["beitraege"] if b["timestamp"][:10] >= START]
bt.sort(key=lambda b: b["timestamp"], reverse=True)
plan_link = {e.get("link"): e for e in plan if e.get("link")}

def name(b):
    e = plan_link.get(b.get("permalink"))
    if e: return e["id"]
    return (b.get("caption") or "").split("\n")[0][:34]

def ortszeit(ts):
    t = datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc) + timedelta(hours=2)
    return t.strftime("%a %d.%m. %H:%M").replace("Mon","Mo").replace("Tue","Di").replace("Wed","Mi").replace("Thu","Do").replace("Fri","Fr").replace("Sat","Sa").replace("Sun","So")

zeilen = []
for b in bt:
    p = vor_bt.get(b["id"], {})
    typ = "Reel" if b["media_product_type"] == "REELS" else ("Karussell" if b["media_type"] == "CAROUSEL_ALBUM" else "Bild")
    zeilen.append(dict(name=name(b), typ=typ, zeit=ortszeit(b["timestamp"]), link=b["permalink"],
        views=b.get("views"), reach=b.get("reach"), likes=b.get("likes"), comments=b.get("comments"),
        saved=b.get("saved"), shares=b.get("shares"), profil=b.get("profile_visits"), follows=b.get("follows"),
        sehdauer=(b.get("ig_reels_avg_watch_time") or 0) / 1000 or None, skip=b.get("reels_skip_rate"),
        v_views=p.get("views"), v_reach=p.get("reach"), v_saved=p.get("saved"), v_shares=p.get("shares"), v_comments=p.get("comments")))

storys = [s for s in d.get("storys_aktiv", []) if s.get("views") is not None]

# Methoden-Check: (Methode, Kennzahl, Wert-Text, Ziel, Status)
def st(wert, ziel, knapp=None):
    if wert is None: return "⏳"
    if wert >= ziel: return "✅"
    if knapp is not None and wert >= knapp: return "⚠️"
    return "❌"

reels = [z for z in zeilen if z["typ"] == "Reel"]
kar = [z for z in zeilen if z["typ"] == "Karussell"]
r0 = reels[0] if reels else None
k0 = kar[0] if kar else None
s_reach = max((s.get("reach") or 0 for s in storys), default=None)
s_repl = sum(s.get("replies") or 0 for s in storys) if storys else None
profil = sum(z["profil"] or 0 for z in zeilen); follows = sum(z["follows"] or 0 for z in zeilen)
online = d.get("online_follower", {})
on = next((online[t] for t in sorted(online, reverse=True) if online[t]), {})
on_cest = {(int(h) + 9) % 24: n for h, n in on.items()}
on_1930 = quote(on_cest.get(19), max(on_cest.values())) if on_cest else None

methoden = [
    ("Reels bringen Nicht-Follower", "Anteil Nicht-Follower an der Reichweite (30 Tage)",
     pct(nf_quote) if nf_quote is not None else "–", "≥ 50 %", st(nf_quote, .5, .35)),
    ("Hook in den ersten 1,5 s", f"Überspringrate letztes Reel ({r0['name'] if r0 else '–'})",
     f"{r0['skip']:.0f} %" if r0 and r0["skip"] is not None else "–", "< 60 %",
     "⏳" if not r0 or r0["skip"] is None else ("✅" if r0["skip"] < 60 else ("⚠️" if r0["skip"] < 70 else "❌"))),
    ("„Wer schickt das an wen?“", f"Geteilt ÷ Erreicht ({(k0 or r0 or {}).get('name','–')})",
     (lambda q: pct(q, 1) if q is not None else "–")(quote((k0 or r0 or {}).get("shares"), (k0 or r0 or {}).get("reach"))),
     "≥ 3 %", st(quote((k0 or r0 or {}).get("shares"), (k0 or r0 or {}).get("reach")), .03, .015)),
    ("Speicherbare Inhalte", f"Gespeichert ÷ Erreicht ({k0['name'] if k0 else '–'})",
     (lambda q: pct(q, 1) if q is not None else "–")(quote(k0 and k0["saved"], k0 and k0["reach"])),
     "≥ 2 %", st(quote(k0 and k0["saved"], k0 and k0["reach"]), .02, .01)),
    ("Mittags-Story mit Frage", "Story-Reichweite ÷ Follower · Antworten",
     f"{pct(s_reach/fol)} · {s_repl} Antw." if s_reach else "–", "≥ 15 % · ≥ 1",
     "⏳" if not s_reach else ("✅" if s_reach / fol >= .15 and s_repl else "⚠️")),
    ("Profil verwandelt Besucher", "Follows ÷ Profilbesuche (Beiträge seit 29.09.)",
     f"{follows} / {profil}" if profil else "–", "≥ 10 %", st(quote(follows, profil), .10, .05) if profil else "⏳"),
    ("TOOL-Aufruf / Bio-Link", "Link-Klicks in der Bio (30 Tage)", str(links), "≥ 1 pro Woche", "✅" if links else "❌"),
    ("Posten um 19:30", "Follower online 19–20 Uhr ÷ Spitzenstunde", pct(on_1930) if on_1930 else "–", "≥ 85 %", st(on_1930, .85, .7)),
]

heute_online = [e for e in plan if e["zeit"][:10] == tag and e["status"] in ("freigegeben", "manuell")]
fehler = [e["id"] for e in plan if e["status"] == "fehler"]

# --- HTML ---
def balken():
    w, h, pad = 960, 220, 30
    mx = max([tw[t] for t in tage] + [1])
    bw = (w - 2 * pad) / len(tage)
    gepostet = {z["zeit"][3:9].strip() for z in zeilen}
    out = [f'<svg viewBox="0 0 {w} {h+46}" width="{w}" height="{h+46}">',
           f'<line x1="{pad}" y1="{h}" x2="{w-pad}" y2="{h}" stroke="#2a3a33" stroke-width="1"/>']
    for i, t in enumerate(tage):
        val = tw[t]; bh = max(3, (h - 20) * val / mx); x = pad + i * bw + 4
        tt = f"{t[8:10]}.{t[5:7]}."
        farbe = "#53C3A2" if tt in gepostet else "#2E6B5B"
        out.append(f'<rect x="{x:.1f}" y="{h-bh:.1f}" width="{bw-8:.1f}" height="{bh:.1f}" rx="4" fill="{farbe}"/>')
        out.append(f'<text x="{x+(bw-8)/2:.1f}" y="{h-bh-6:.1f}" text-anchor="middle" class="bv">{val}</text>')
        out.append(f'<text x="{x+(bw-8)/2:.1f}" y="{h+20}" text-anchor="middle" class="bl">{tt}</text>')
    out.append(f'<text x="{pad}" y="{h+42}" class="bl">hell = Tag mit neuem Beitrag</text></svg>')
    return "".join(out)

def kachel(titel, wert, d_html="", unter=""):
    return f'<div class="kachel"><div class="kt">{titel}</div><div class="kw">{wert}{d_html}</div><div class="ku">{unter}</div></div>'

reihen = "".join(
    f'<tr><td><b>{html.escape(z["name"])}</b><br><span class="m">{z["typ"]} · {z["zeit"]}</span></td>'
    f'<td>{zahl(z["views"])}{delta(z["views"], z["v_views"])}</td><td>{zahl(z["reach"])}{delta(z["reach"], z["v_reach"])}</td>'
    f'<td>{zahl(z["likes"])}</td><td>{zahl(z["comments"])}{delta(z["comments"], z["v_comments"])}</td>'
    f'<td>{zahl(z["saved"])}{delta(z["saved"], z["v_saved"])}</td><td>{zahl(z["shares"])}{delta(z["shares"], z["v_shares"])}</td>'
    f'<td>{zahl(z["profil"])}</td>'
    f'<td>{(f"{z[chr(115)+chr(107)+chr(105)+chr(112)]:.0f} % · {str(round(z[chr(115)+chr(101)+chr(104)+chr(100)+chr(97)+chr(117)+chr(101)+chr(114)],1)).replace(chr(46),chr(44))} s") if z["skip"] is not None else "–"}</td></tr>'
    for z in zeilen)
s_reihen = "".join(
    f'<tr><td>Story {ortszeit(s["zeit"])}</td><td>{zahl(s.get("views"))}</td><td>{zahl(s.get("reach"))}</td>'
    f'<td>{zahl(s.get("replies"))}</td><td>{zahl(s.get("navigation"))}</td><td>{zahl(s.get("profile_visits"))}</td></tr>'
    for s in storys) or '<tr><td colspan="6" class="m">keine Story in den letzten 24 h</td></tr>'
m_reihen = "".join(
    f'<tr><td class="st">{s}</td><td><b>{html.escape(a)}</b><br><span class="m">{html.escape(b)}</span></td><td class="w">{html.escape(c)}</td><td class="m">{html.escape(z)}</td></tr>'
    for a, b, c, z, s in methoden)
wt = datetime.strptime(tag, "%Y-%m-%d")
titel_tag = ["Mo","Di","Mi","Do","Fr","Sa","So"][wt.weekday()] + wt.strftime(" %d.%m.%Y")

seite = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@import url("../../vorlagen/schriften.css");
body{{margin:0;width:1080px;background:#0B110E;color:#EAF1EC;font-family:"IBM Plex Sans",sans-serif;padding:44px 50px}}
h1{{font-family:"IBM Plex Serif",serif;font-weight:600;font-size:46px;margin:0 0 4px}}
.kick{{font-family:"IBM Plex Mono",monospace;letter-spacing:.25em;text-transform:uppercase;color:#53C3A2;font-size:16px;font-weight:600}}
h2{{font-family:"IBM Plex Mono",monospace;letter-spacing:.18em;text-transform:uppercase;color:#53C3A2;font-size:15px;margin:34px 0 12px}}
.kacheln{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}}
.kachel{{background:#12201B;border:1px solid #1f3a31;border-radius:16px;padding:16px 18px}}
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
<div class="kick">@maehrsteuern · Tagesbericht</div><h1>{titel_tag}</h1>
<div class="kacheln">
{kachel("Follower", zahl(fol), delta(fol, fol_v), f"du folgst {k['follows_count']}")}
{kachel("Reichweite gestern", zahl(r_gestern), delta(r_gestern, r_vortag), "erreichte Konten")}
{kachel("Nicht-Follower (30 T.)", pct(nf_quote) if nf_quote is not None else "–", "", f"{nf} von {nf+ff} Konten")}
{kachel("Bio-Link-Klicks", str(links), "", f"30 Tage · {m30.get('replies',0)} Story-Antworten")}
</div>
<h2>Reichweite pro Tag</h2>{balken()}
<h2>Beiträge seit Neustart (Δ zum Vortag)</h2>
<table><tr><th>Beitrag</th><th>Aufrufe</th><th>Erreicht</th><th>Likes</th><th>Komm.</th><th>Gespeich.</th><th>Geteilt</th><th>Profil</th><th>Skip · Ø Sehdauer</th></tr>{reihen}</table>
<h2>Storys (letzte 24 h)</h2>
<table><tr><th>Story</th><th>Aufrufe</th><th>Erreicht</th><th>Antworten</th><th>Tipps</th><th>Profil</th></tr>{s_reihen}</table>
<h2>Greifen unsere Methoden?</h2>
<table><tr><th></th><th>Methode · Kennzahl</th><th>Ist</th><th>Ziel</th></tr>{m_reihen}</table>
<div class="leg">✅ greift · ⚠️ knapp / zu früh · ❌ greift (noch) nicht · ⏳ keine Daten</div>
</body></html>"""

OUT.mkdir(parents=True, exist_ok=True)
html_f = OUT / f"tagesbericht_{tag}.html"; png_f = OUT / f"tagesbericht_{tag}.png"
html_f.write_text(seite)
(OUT / f"tagesbericht_{tag}.json").write_text(json.dumps(dict(
    tag=tag, follower=fol, follower_vortag=fol_v, reichweite_gestern=r_gestern, reichweite_vortag=r_vortag,
    nicht_follower_quote=nf_quote, link_klicks=links, beitraege=zeilen, storys=storys,
    methoden=[dict(methode=a, kennzahl=b, ist=c, ziel=z, status=s) for a, b, c, z, s in methoden],
    heute_online=[f'{e["zeit"][11:]} {e["typ"]} {e["id"]}' for e in heute_online], fehler=fehler),
    ensure_ascii=False, indent=1, default=str))

js = f"""const {{createRequire}}=require('module');const {{execSync}}=require('child_process');
const {{chromium}}=createRequire(execSync('npm root -g').toString().trim()+'/')('playwright');
(async()=>{{const b=await chromium.launch({{executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'}});
const p=await b.newPage({{viewport:{{width:1080,height:800}},deviceScaleFactor:1.5}});
await p.goto('file://{html_f}');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({{path:'{png_f}',fullPage:true}});await b.close();}})();"""
subprocess.run(["node", "-e", js], check=True)
print(png_f)
