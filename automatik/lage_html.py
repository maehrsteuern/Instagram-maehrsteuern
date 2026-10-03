"""LAGE.html – dieselbe Lage wie LAGE.md, als grafische Seite (Kacheln, Kalender, Diagramme, filterbares Protokoll).

Wird von automatik/lage.py am Ende von main() aufgerufen (schreiben(...)) – nie allein bearbeiten, LAGE.html wird
bei jedem Lauf überschrieben. Veröffentlicht über GitHub Pages (Workflow lage.yml). Eine Datei, ohne externe
Skripte; nur die IBM-Plex-Schriften kommen von Google Fonts (fällt sonst auf Systemschriften zurück).
"""
import csv, html, json, re
from datetime import datetime, timedelta

from lage import (KONTO, NOTIZEN, REPO, STATUS, TYP, WOCHENTAG, WURZEL, insights_dateien, issue_link, lokal, tag,
                  zeit)

ZIEL = WURZEL / "LAGE.html"
ART_NAME = {"🤖": "Autopilot", "✅": "Freigabe", "📈": "Statistik", "🎵": "Musik", "🔑": "Schlüssel", "🔀": "Merge",
            "📡": "Radar", "💬": "Kommentare", "💼": "LinkedIn", "✍️": "von Hand / Claude"}


# ---------- Hilfen ----------

def e(text):
    return html.escape(str(text), quote=True)


def md(text):
    """Inline-Markdown aus LAGE.md-Bausteinen → HTML (`code`, **fett**, [Link](url))."""
    codes = []
    def halten(m):
        codes.append(f"<code>{m.group(1)}</code>")
        return f"\x00{len(codes) - 1}\x00"
    t = re.sub(r"`([^`]+)`", halten, e(text))
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], t)


def stufe(status):
    """Status → Darstellungsstufe (Farbe kommt immer zusammen mit Symbol + Text)."""
    if status == "freigegeben":
        return "ok"
    if status == "veroeffentlicht":
        return "done"
    if status == "fehler":
        return "crit"
    if status == "entfaellt":
        return "muted"
    if status == "manuell":
        return "info"
    return "warn"  # entwurf, wartet_*


def status_text(s):
    return STATUS.get(s, "⏳ " + s.replace("_", " ") if s.startswith("wartet") else s)


def status_pille(s):
    return f'<span class="pill {stufe(s)}">{e(status_text(s))}</span>'


def punkt_stufe(p):
    if p.startswith("🔴"):
        return "crit"
    if p.startswith(("👉", "Nichts")):
        return "info"
    return "warn"


# ---------- Bausteine ----------

def kopf(stand, naechster):
    teile = [f'''<header class="top">
  <div>
    <div class="kicker">maehrsteuern · Instagram</div>
    <h1>Lage</h1>
    <p class="sub">Stand: letzte Änderung {e(tag(stand))} Uhr · automatisch aus <code>automatik/lage.py</code> ·
      <a href="https://github.com/{REPO}/blob/claude/instagram/LAGE.md" target="_blank" rel="noopener">LAGE.md</a></p>
  </div>
  <nav class="sprung">
    <a href="#braucht">Braucht dich</a><a href="#arbeit">In Arbeit</a><a href="#kalender">Kalender</a>
    <a href="#plan">Plan</a><a href="#zahlen">Zahlen</a><a href="#automatik">Automatik</a><a href="#protokoll">Protokoll</a>
  </nav>
</header>''']
    if naechster:
        t = zeit(naechster)
        hinweis = f'<p class="hero-hinweis">{md(naechster["hinweis"] + issue_link(naechster))}</p>' if naechster.get("hinweis") else ""
        teile.append(f'''<section class="hero">
  <div class="hero-links">
    <div class="kicker">Als Nächstes online</div>
    <div class="hero-titel">{e(TYP.get(naechster["typ"], naechster["typ"]))} <code>{e(naechster["id"])}</code></div>
    <div class="hero-zeit">{e(tag(t))} Uhr · {status_pille(naechster["status"])}</div>
    {hinweis}
  </div>
  <div class="countdown" data-ziel="{t.isoformat()}"><span class="cd-wert">–</span><span class="cd-label">bis online</span></div>
</section>''')
    return "\n".join(teile)


def kacheln(n, punkte, kommend, ablaeufe):
    zeilen = list(csv.DictReader(KONTO.open())) if KONTO.exists() else []
    follower, diff_text = "–", ""
    if zeilen:
        follower = zeilen[-1]["followers_count"]
        if len(zeilen) > 1:
            diff = int(zeilen[-1]["followers_count"]) - int(zeilen[-2]["followers_count"])
            diff_text = f'<span class="delta {"neg" if diff < 0 else "pos" if diff > 0 else ""}">{diff:+d} seit {e(zeilen[-2]["datum"][8:10])}.{e(zeilen[-2]["datum"][5:7])}.</span>'
    reich, reich_text = "–", ""
    if (dateien := insights_dateien()):
        tage = sorted((json.loads(dateien[-1].read_text()).get("tageswerte_reichweite") or {}).items())
        if tage:
            reich = tage[-1][1]
            reich_text = f'<span class="delta">am {tage[-1][0][8:10]}.{tage[-1][0][5:7]}. · Ø 7 Tage {round(sum(v for _, v in tage[-7:]) / len(tage[-7:]))}</span>'
    woche = [x for x in kommend if zeit(x) <= n + timedelta(days=7)]
    offen = [p for p in punkte if not p.startswith("Nichts")]
    rot = sum(p.startswith("🔴") for p in offen)
    ok = sum(l.startswith("✅") for _, _, l in ablaeufe)
    fehl = sum(l.startswith("🔴") for _, _, l in ablaeufe)
    auto_text = f"{fehl} mit Fehler" if fehl else ("alle ok" if ok else "Status nur in Actions sichtbar")
    return f'''<section class="kacheln">
  <div class="kachel"><div class="k-label">Follower</div><div class="k-wert">{e(follower)}</div>{diff_text}</div>
  <div class="kachel"><div class="k-label">Reichweite (letzter Tag)</div><div class="k-wert">{e(reich)}</div>{reich_text}</div>
  <div class="kachel"><div class="k-label">Geplant · nächste 7 Tage</div><div class="k-wert">{len(woche)}</div>
    <span class="delta">{sum(x["status"] == "freigegeben" for x in woche)} freigegeben</span></div>
  <div class="kachel {"k-warn" if offen else ""}"><div class="k-label">Braucht dich</div><div class="k-wert">{len(offen)}</div>
    <span class="delta {"neg" if rot else ""}">{f"{rot} rot" if rot else "nichts Dringendes"}</span></div>
  <div class="kachel {"k-crit" if fehl else ""}"><div class="k-label">Automatik</div><div class="k-wert">{ok}/{len(ablaeufe)}</div>
    <span class="delta {"neg" if fehl else ""}">{e(auto_text)}</span></div>
</section>'''


def braucht(punkte):
    li = "".join(f'<li class="karte {punkt_stufe(p)}">{md(p)}</li>' for p in punkte)
    return f'<section id="braucht"><h2>👉 Braucht dich</h2><ul class="karten">{li}</ul></section>'


def notizen():
    if not NOTIZEN.exists() or not (text := NOTIZEN.read_text().strip()):
        return ""
    aus, offen = [], False
    for zeile in text.splitlines():
        if m := re.match(r"\s*[-*] (.*)", zeile):
            if not offen:
                aus.append("<ul class='notizen'>")
                offen = True
            aus.append(f"<li>{md(m.group(1))}</li>")
        elif zeile.strip():
            if offen:
                aus.append("</ul>")
                offen = False
            aus.append(f"<p>{md(zeile.lstrip('# '))}</p>")
    if offen:
        aus.append("</ul>")
    return f'<section id="arbeit"><h2>📝 Gerade in Arbeit</h2><div class="block">{"".join(aus)}</div></section>'


def kalender(n, eintraege):
    """Vier Wochen ab Montag dieser Woche, jeder Beitrag als Chip mit Uhrzeit, Art und Status."""
    start = (n - timedelta(days=n.weekday())).date()
    tage = [start + timedelta(days=i) for i in range(28)]
    nach_tag = {}
    for x in eintraege:
        if x["status"] != "entfaellt":
            nach_tag.setdefault(zeit(x).date(), []).append(x)
    zellen = "".join(f'<div class="kal-kopf">{w}</div>' for w in WOCHENTAG)
    for d in tage:
        chips = "".join(
            f'<div class="chip {stufe(x["status"])}" title="{e(x["id"])} · {e(status_text(x["status"]))}">'
            f'<span class="chip-zeit">{zeit(x):%H:%M}</span> {e(TYP.get(x["typ"], x["typ"]).split(" ")[0])} '
            f'<span class="chip-id">{e(x["id"])}</span></div>'
            for x in sorted(nach_tag.get(d, []), key=zeit))
        klasse = "kal-tag" + (" heute" if d == n.date() else "") + (" vorbei" if d < n.date() else "")
        zellen += f'<div class="{klasse}"><div class="kal-datum">{WOCHENTAG[d.weekday()]} {d:%d.%m.}</div>{chips}</div>'
    legende = "".join(f'<span class="pill {s}">{t}</span>' for s, t in (
        ("done", "✅ veröffentlicht"), ("ok", "🟢 freigegeben"), ("warn", "🟡 Entwurf / ⏳ wartet"),
        ("info", "✋ von Hand"), ("crit", "🔴 Fehler")))
    return f'''<section id="kalender"><h2>🗓️ Kalender – 4 Wochen</h2>
<div class="legende">{legende}</div>
<div class="kal-scroll"><div class="kal">{zellen}</div></div></section>'''


def plan_tabelle(n, kommend):
    woche = sorted((x for x in kommend if zeit(x) <= n + timedelta(days=7)), key=zeit)
    spaeter = sorted((x for x in kommend if zeit(x) > n + timedelta(days=7)), key=zeit)

    def zeilen(liste):
        return "".join(
            f'<tr><td class="nowrap">{e(tag(zeit(x)))}</td><td class="nowrap">{e(TYP.get(x["typ"], x["typ"]))}<br><code>{e(x["id"])}</code></td>'
            f'<td>{status_pille(x["status"])}</td><td class="hinweis">{md(x.get("hinweis", "") + issue_link(x))}</td></tr>'
            for x in liste) or '<tr><td colspan="4">Nichts geplant.</td></tr>'
    kopf = "<thead><tr><th>Wann</th><th>Was</th><th>Status</th><th>Hinweis</th></tr></thead>"
    teile = [f'<section id="plan"><h2>⏭️ Nächste 7 Tage</h2><div class="tab-scroll"><table>{kopf}<tbody>{zeilen(woche)}</tbody></table></div>']
    if spaeter:
        teile.append(f'<h3>Danach</h3><div class="tab-scroll"><table>{kopf}<tbody>{zeilen(spaeter)}</tbody></table></div>')
    return "".join(teile) + "</section>"


def zuletzt(eintraege):
    fertig = sorted((x for x in eintraege if x["status"] == "veroeffentlicht"), key=zeit, reverse=True)[:10]
    if not fertig:
        return ""
    li = "".join(
        f'<li><span class="nowrap">{e(tag(zeit(x)))}</span> · {e(TYP.get(x["typ"], x["typ"]))} <code>{e(x["id"])}</code>'
        + (f' · <a href="{e(x["link"])}" target="_blank" rel="noopener">ansehen ↗</a>' if x.get("link") else "") + "</li>"
        for x in fertig)
    return f'<section><h2>✅ Zuletzt veröffentlicht</h2><ul class="liste">{li}</ul></section>'


def balken(werte, hoehe=180):
    """Säulendiagramm (eine Reihe) als SVG; Hover-Tooltip über data-tip."""
    if not werte:
        return ""
    breite, links, unten, oben = 1100, 34, 22, 8
    hoch = max(v for _, v in werte) or 1
    schritt = next(s for s in (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 5000, 10**9) if hoch / s <= 4)
    top = -(-hoch // schritt) * schritt
    y = lambda v: oben + (hoehe - oben - unten) * (1 - v / top)
    feld = (breite - links) / len(werte)
    teile = [f'<svg class="chart" viewBox="0 0 {breite} {hoehe}" role="img" aria-label="Reichweite pro Tag">']
    for t in range(0, top + 1, schritt):
        teile.append(f'<line class="grid" x1="{links}" x2="{breite}" y1="{y(t):.1f}" y2="{y(t):.1f}"/>'
                     f'<text class="achse" x="{links - 6}" y="{y(t) + 4:.1f}" text-anchor="end">{t}</text>')
    b = max(2, min(18, feld - 2))
    for i, (d, v) in enumerate(werte):
        x = links + i * feld + (feld - b) / 2
        h = max(0.0, (hoehe - unten) - y(v))
        rad = min(4, b / 2, h)
        tip = f"{d[8:10]}.{d[5:7]}.: {v} erreicht"
        teile.append(f'<rect class="hit" x="{links + i * feld:.1f}" y="{oben}" width="{feld:.1f}" height="{hoehe - oben - unten}" data-tip="{e(tip)}"/>')
        if h > 0:
            teile.append(f'<path class="bar" d="M{x:.1f},{hoehe - unten} v{-(h - rad):.1f} q0,{-rad:.1f} {rad:.1f},{-rad:.1f} '
                         f'h{b - 2 * rad:.1f} q{rad:.1f},0 {rad:.1f},{rad:.1f} v{h - rad:.1f} z" pointer-events="none"/>')
        jede = max(1, len(werte) // 8)
        if (i % jede == 0 and len(werte) - 1 - i >= jede / 2) or i == len(werte) - 1:
            teile.append(f'<text class="achse" x="{x + b / 2:.1f}" y="{hoehe - 6}" text-anchor="middle">{d[8:10]}.{d[5:7]}.</text>')
    letzter = werte[-1]
    teile.append(f'<text class="wert" x="{links + (len(werte) - 0.5) * feld:.1f}" y="{y(letzter[1]) - 6:.1f}" text-anchor="end">{letzter[1]}</text>')
    return "".join(teile) + "</svg>"


def linie(punkte, hoehe=150):
    """Follower-Verlauf als Linie (eine Reihe), Punkte ≥ 8 px, Hover-Tooltip."""
    if len(punkte) < 2:
        return ""
    breite, links, unten, oben = 1100, 40, 22, 16
    werte = [v for _, v in punkte]
    lo, hi = min(werte), max(werte)
    if hi - lo < 4:
        lo, hi = lo - 2, hi + 2
    y = lambda v: oben + (hoehe - oben - unten) * (1 - (v - lo) / (hi - lo))
    x = lambda i: links + 10 + (breite - links - 20) * i / (len(punkte) - 1)
    teile = [f'<svg class="chart" viewBox="0 0 {breite} {hoehe}" role="img" aria-label="Follower-Verlauf">']
    for t in (lo, (lo + hi) / 2, hi):
        teile.append(f'<line class="grid" x1="{links}" x2="{breite}" y1="{y(t):.1f}" y2="{y(t):.1f}"/>'
                     f'<text class="achse" x="{links - 6}" y="{y(t) + 4:.1f}" text-anchor="end">{round(t)}</text>')
    pfad = " ".join(f"{'M' if i == 0 else 'L'}{x(i):.1f},{y(v):.1f}" for i, (_, v) in enumerate(punkte))
    teile.append(f'<path class="line" d="{pfad}"/>')
    for i, (d, v) in enumerate(punkte):
        teile.append(f'<circle class="dot" cx="{x(i):.1f}" cy="{y(v):.1f}" r="4.5"/>'
                     f'<circle class="hit" cx="{x(i):.1f}" cy="{y(v):.1f}" r="14" data-tip="{e(f"{d[8:10]}.{d[5:7]}.: {v} Follower")}"/>')
        jede = max(1, len(punkte) // 8)
        if (i % jede == 0 and len(punkte) - 1 - i >= jede / 2) or i == len(punkte) - 1:
            teile.append(f'<text class="achse" x="{x(i):.1f}" y="{hoehe - 6}" text-anchor="middle">{d[8:10]}.{d[5:7]}.</text>')
    teile.append(f'<text class="wert" x="{x(len(punkte) - 1):.1f}" y="{y(punkte[-1][1]) - 10:.1f}" text-anchor="end">{punkte[-1][1]}</text>')
    return "".join(teile) + "</svg>"


def zahlen(n):
    zeilen = list(csv.DictReader(KONTO.open())) if KONTO.exists() else []
    dateien = insights_dateien()
    if not zeilen and not dateien:
        return '<section id="zahlen"><h2>📈 Zahlen</h2><p>Noch keine Statistik.</p></section>'
    teile = ['<section id="zahlen"><h2>📈 Zahlen <span class="leise">(täglich ca. 08:45)</span></h2><div class="stapel">']
    if dateien:
        d = json.loads(dateien[-1].read_text())
        tage = sorted((d.get("tageswerte_reichweite") or {}).items())[-30:]
        teile.append(f'<figure class="block"><figcaption>Reichweite pro Tag · letzte {len(tage)} Tage</figcaption>{balken(tage)}</figure>')
    if zeilen:
        teile.append(f'<figure class="block"><figcaption>Follower</figcaption>'
                     f'{linie([(z["datum"], int(z["followers_count"])) for z in zeilen][-60:])}</figure>')
    teile.append("</div>")
    if dateien:
        d = json.loads(dateien[-1].read_text())
        alt = {b["id"]: b for b in json.loads(dateien[-2].read_text()).get("beitraege", [])} if len(dateien) > 1 else {}
        neu = [b for b in d.get("beitraege", []) if b.get("timestamp") and n - lokal(b["timestamp"]) < timedelta(days=14)]
        if neu:
            zeilen_html = ""
            for b in sorted(neu, key=lambda x: x["timestamp"], reverse=True):
                plus = (f' <span class="leise">(+{b["views"] - alt[b["id"]]["views"]})</span>'
                        if isinstance(alt.get(b["id"], {}).get("views"), int) and isinstance(b.get("views"), int) else "")
                name = (b.get("caption") or "").split("\n")[0][:50]
                zeilen_html += (f'<tr><td><span class="nowrap">{e(tag(lokal(b["timestamp"])))}</span><br>'
                                f'<a href="{e(b.get("permalink", ""))}" target="_blank" rel="noopener">{e(name)}</a></td>'
                                + "".join(f'<td class="num">{e(b.get(k, "–"))}{plus if k == "views" else ""}</td>'
                                          for k in ("views", "reach", "likes", "comments", "saved", "shares")) + "</tr>")
            teile.append('<h3>Beiträge (letzte 14 Tage)</h3><div class="tab-scroll"><table><thead><tr><th>Beitrag</th>'
                         '<th class="num">Aufrufe</th><th class="num">Erreicht</th><th class="num">Likes</th><th class="num">Komm.</th>'
                         f'<th class="num">Gespeichert</th><th class="num">Geteilt</th></tr></thead><tbody>{zeilen_html}</tbody></table></div>')
        storys = sorted((s for s in d.get("storys_aktiv") or [] if s.get("zeit")), key=lambda x: x["zeit"])
        if storys:
            zeilen_html = "".join(
                f'<tr><td class="nowrap">{e(tag(lokal(s["zeit"])))}</td>'
                + "".join(f'<td class="num">{e(s.get(k, "–"))}</td>' for k in ("views", "reach", "replies", "profile_visits", "follows"))
                + "</tr>" for s in storys)
            teile.append('<h3>Storys (letzte 24 h)</h3><div class="tab-scroll"><table><thead><tr><th>Story</th><th class="num">Aufrufe</th>'
                         '<th class="num">Erreicht</th><th class="num">Antworten</th><th class="num">Profilbesuche</th>'
                         f'<th class="num">Follows</th></tr></thead><tbody>{zeilen_html}</tbody></table></div>')
    teile.append('<p class="leise">Rohdaten: <code>automatik/statistik/</code> · Auswertung: <code>strategie/06_auswertung.md</code></p></section>')
    return "".join(teile)


def automatik(ablaeufe):
    karten = ""
    for name, wann, letzter in ablaeufe:
        s = "crit" if letzter.startswith("🔴") else "ok" if letzter.startswith("✅") else "muted"
        karten += f'<div class="ablauf {s}"><div class="ab-name">{e(name)}</div><div class="ab-wann">{e(wann)}</div><div class="ab-status">{md(letzter)}</div></div>'
    return f'<section id="automatik"><h2>⚙️ Automatik</h2><div class="ablaeufe">{karten}</div></section>'


def protokoll(n, commits):
    zaehler = {}
    for c in commits:
        zaehler[c["art"]] = zaehler.get(c["art"], 0) + 1
    filter_html = '<button class="filt aktiv" data-art="">Alle <span>{}</span></button>'.format(len(commits)) + "".join(
        f'<button class="filt" data-art="{e(a)}">{e(a)} {e(ART_NAME.get(a, ""))} <span>{z}</span></button>'
        for a, z in sorted(zaehler.items(), key=lambda kv: -kv[1]))
    tage = {}
    for c in commits:
        tage.setdefault(c["zeit"].date(), []).append(c)
    bloecke = ""
    for d, liste in tage.items():
        eintraege = ""
        for c in liste:
            details = ("Plan: " + "; ".join(c["plan"])) if c["plan"] else ", ".join(f"`{x}`" for x in c["bereiche"])
            such = (c["nachricht"] + " " + details).lower()
            eintraege += (f'<li class="pk" data-art="{e(c["art"])}" data-such="{e(such)}">'
                          f'<span class="pk-zeit">{c["zeit"]:%H:%M}</span><span class="pk-art" title="{e(ART_NAME.get(c["art"], ""))}">{e(c["art"])}</span>'
                          f'<div class="pk-text"><div>{e(c["nachricht"])} <a class="sha" href="https://github.com/{REPO}/commit/{c["sha"]}" '
                          f'target="_blank" rel="noopener">{c["sha"][:7]}</a></div>'
                          + (f'<div class="pk-details">{md(details)}</div>' if details else "") + "</div></li>")
        offen = " open" if (n.date() - d).days < 7 else ""
        bloecke += (f'<details class="pk-tag"{offen}><summary>{WOCHENTAG[d.weekday()]} {d:%d.%m.%Y} '
                    f'<span class="leise">· {len(liste)}</span></summary><ul class="pk-liste">{eintraege}</ul></details>')
    return f'''<section id="protokoll"><h2>📜 Protokoll – jede Änderung</h2>
<div class="pk-werkzeug"><input type="search" id="pk-suche" placeholder="Suchen (z. B. Reel, Radar, 04-…)" aria-label="Protokoll durchsuchen">
<div class="filter">{filter_html}</div></div>
<div id="pk">{bloecke}</div><p id="pk-leer" class="leise" hidden>Nichts gefunden.</p></section>'''


# ---------- Seite ----------

CSS = """
:root{--bg:#F4F7F5;--flaeche:#FFFFFF;--flaeche2:#EAF1EC;--linie:#D5E0D9;--text:#0B110E;--text2:#3D4D44;--leise:#66766D;
--akzent:#2E8F72;--akzent-text:#1F6F57;--ok:#1F7A4D;--ok-bg:#E2F3E9;--warn:#8A5A00;--warn-bg:#FBF0D9;--crit:#B42318;--crit-bg:#FCE4E1;
--info:#1D5FA8;--info-bg:#E2ECF8;--done:#4C5A52;--done-bg:#E9EEEB;--grid:#E1E8E4;--bar:#2E8F72;--schatten:0 1px 2px rgba(11,17,14,.06)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0B110E;--flaeche:#111A15;--flaeche2:#153A31;--linie:#22332A;
--text:#EAF1EC;--text2:#C3D1C8;--leise:#8FA398;--akzent:#53C3A2;--akzent-text:#6FD3B4;--ok:#6FD3A0;--ok-bg:#15301F;--warn:#F2C36B;
--warn-bg:#33280F;--crit:#FF8A7A;--crit-bg:#3A1512;--info:#8DB9F0;--info-bg:#14243A;--done:#A9B8AF;--done-bg:#1A231E;--grid:#1E2C24;
--bar:#53C3A2;--schatten:none}}
:root[data-theme="dark"]{--bg:#0B110E;--flaeche:#111A15;--flaeche2:#153A31;--linie:#22332A;--text:#EAF1EC;--text2:#C3D1C8;--leise:#8FA398;
--akzent:#53C3A2;--akzent-text:#6FD3B4;--ok:#6FD3A0;--ok-bg:#15301F;--warn:#F2C36B;--warn-bg:#33280F;--crit:#FF8A7A;--crit-bg:#3A1512;
--info:#8DB9F0;--info-bg:#14243A;--done:#A9B8AF;--done-bg:#1A231E;--grid:#1E2C24;--bar:#53C3A2;--schatten:none}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.55 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1180px;margin:0 auto;padding:24px 16px 64px}
h1,h2,h3{font-family:"IBM Plex Serif",Georgia,serif;font-weight:600;margin:0}
h1{font-size:34px;letter-spacing:-.01em}
h2{font-size:21px;margin:40px 0 14px}
h3{font-size:16px;margin:24px 0 10px}
a{color:var(--akzent-text)}
code{font:12.5px "IBM Plex Mono",ui-monospace,monospace;background:var(--flaeche2);padding:1px 5px;border-radius:4px;word-break:break-word}
.kicker{font:12px "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--akzent-text)}
.sub,.leise{color:var(--leise);font-size:13px;font-weight:400}
.top{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
.sprung{display:flex;flex-wrap:wrap;gap:6px}
.sprung a{font-size:13px;text-decoration:none;color:var(--text2);border:1px solid var(--linie);border-radius:999px;padding:4px 10px;background:var(--flaeche)}
.sprung a:hover{border-color:var(--akzent)}
.hero{margin-top:20px;display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;padding:22px;border-radius:14px;
background:linear-gradient(135deg,var(--flaeche2),var(--flaeche));border:1px solid var(--linie)}
.hero-titel{font:600 24px "IBM Plex Serif",serif;margin:4px 0}
.hero-titel code{font-size:18px}
.hero-zeit{color:var(--text2);display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.hero-hinweis{color:var(--text2);font-size:13.5px;max-width:720px;margin:10px 0 0}
.hero-links{flex:1 1 420px;min-width:0}
.countdown{text-align:center;padding:12px 20px;border-radius:12px;background:var(--flaeche);border:1px solid var(--linie);min-width:150px}
.cd-wert{display:block;font:600 30px "IBM Plex Mono",monospace;color:var(--akzent-text);font-variant-numeric:tabular-nums}
.cd-label{font-size:12px;color:var(--leise)}
.kacheln{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-top:16px}
.kachel{background:var(--flaeche);border:1px solid var(--linie);border-radius:12px;padding:14px 16px;box-shadow:var(--schatten)}
.k-label{font-size:12.5px;color:var(--leise)}
.k-wert{font:600 30px "IBM Plex Serif",serif;margin:2px 0;font-variant-numeric:tabular-nums}
.k-warn{border-color:var(--warn)}.k-crit{border-color:var(--crit)}
.delta{font-size:12.5px;color:var(--leise)}.delta.pos{color:var(--ok)}.delta.neg{color:var(--crit)}
.karten{list-style:none;padding:0;margin:0;display:grid;gap:8px}
.karte{background:var(--flaeche);border:1px solid var(--linie);border-left:4px solid var(--leise);border-radius:10px;padding:10px 14px}
.karte.crit{border-left-color:var(--crit);background:var(--crit-bg)}.karte.warn{border-left-color:var(--warn)}.karte.info{border-left-color:var(--info)}
.block{background:var(--flaeche);border:1px solid var(--linie);border-radius:12px;padding:14px 18px;margin:0}
.notizen{margin:0;padding-left:18px}.notizen li{margin:6px 0;color:var(--text2)}.notizen strong{color:var(--text)}
.pill{display:inline-block;font-size:12px;line-height:1.3;padding:3px 9px;border-radius:999px;white-space:nowrap;border:1px solid transparent}
.pill.ok{background:var(--ok-bg);color:var(--ok)}.pill.warn{background:var(--warn-bg);color:var(--warn)}.pill.crit{background:var(--crit-bg);color:var(--crit)}
.pill.info{background:var(--info-bg);color:var(--info)}.pill.done{background:var(--done-bg);color:var(--done)}.pill.muted{background:var(--done-bg);color:var(--leise)}
.legende{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.kal-scroll,.tab-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.kal{display:grid;grid-template-columns:repeat(7,minmax(120px,1fr));gap:6px;min-width:860px}
.kal-kopf{font:12px "IBM Plex Mono",monospace;color:var(--leise);text-transform:uppercase;padding:0 4px}
.kal-tag{background:var(--flaeche);border:1px solid var(--linie);border-radius:10px;padding:6px;min-height:92px}
.kal-tag.heute{border-color:var(--akzent);box-shadow:0 0 0 1px var(--akzent)}
.kal-tag.vorbei{opacity:.62}
.kal-datum{font-size:12px;color:var(--leise);margin-bottom:4px}
.chip{font-size:11.5px;line-height:1.3;border-radius:6px;padding:3px 6px;margin-top:3px;border-left:3px solid var(--leise);background:var(--flaeche2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chip.ok{border-left-color:var(--ok);background:var(--ok-bg)}.chip.warn{border-left-color:var(--warn);background:var(--warn-bg)}
.chip.crit{border-left-color:var(--crit);background:var(--crit-bg)}.chip.info{border-left-color:var(--info);background:var(--info-bg)}
.chip.done{border-left-color:var(--done);background:var(--done-bg)}
.chip-zeit{font-family:"IBM Plex Mono",monospace;color:var(--text2)}
.chip-id{color:var(--text)}
table{width:100%;border-collapse:collapse;background:var(--flaeche);border:1px solid var(--linie);border-radius:12px;overflow:hidden;font-size:13.5px}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--linie);vertical-align:top}
th{font-weight:600;font-size:12.5px;color:var(--leise);background:var(--flaeche2)}
tr:last-child td{border-bottom:0}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
td.hinweis{color:var(--text2);min-width:260px}
.nowrap{white-space:nowrap}
.liste{margin:0;padding-left:18px}.liste li{margin:4px 0}
.stapel{display:grid;gap:12px}
figcaption{font-size:13px;color:var(--leise);margin-bottom:6px}
.chart{width:100%;height:auto;display:block;overflow:visible}
.chart .grid{stroke:var(--grid);stroke-width:1}
.chart .achse{fill:var(--leise);font:11px "IBM Plex Mono",monospace}
.chart .wert{fill:var(--text);font:600 12px "IBM Plex Sans",sans-serif}
.chart .bar{fill:var(--bar)}
.chart .line{fill:none;stroke:var(--bar);stroke-width:2;stroke-linejoin:round}
.chart .dot{fill:var(--bar);stroke:var(--flaeche);stroke-width:2}
.chart .hit{fill:transparent;cursor:default}
.chart .hit:hover{fill:var(--flaeche2);fill-opacity:.55}
#tip{position:fixed;pointer-events:none;background:var(--text);color:var(--bg);font-size:12.5px;padding:5px 9px;border-radius:6px;opacity:0;transition:opacity .1s;z-index:9}
.ablaeufe{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}
.ablauf{background:var(--flaeche);border:1px solid var(--linie);border-left:4px solid var(--leise);border-radius:10px;padding:10px 14px}
.ablauf.ok{border-left-color:var(--ok)}.ablauf.crit{border-left-color:var(--crit);background:var(--crit-bg)}
.ab-name{font-weight:600}.ab-wann{font-size:12.5px;color:var(--leise);margin:2px 0 6px}.ab-status{font-size:13px}
.pk-werkzeug{display:flex;flex-direction:column;gap:10px;margin-bottom:12px}
#pk-suche{font:inherit;padding:9px 12px;border-radius:10px;border:1px solid var(--linie);background:var(--flaeche);color:var(--text);max-width:420px}
.filter{display:flex;flex-wrap:wrap;gap:6px}
.filt{font:inherit;font-size:12.5px;border:1px solid var(--linie);background:var(--flaeche);color:var(--text2);border-radius:999px;padding:4px 10px;cursor:pointer}
.filt span{color:var(--leise)}
.filt.aktiv{border-color:var(--akzent);background:var(--flaeche2);color:var(--text)}
.pk-tag{background:var(--flaeche);border:1px solid var(--linie);border-radius:12px;margin-bottom:8px}
.pk-tag summary{cursor:pointer;padding:10px 14px;font-weight:600}
.pk-liste{list-style:none;margin:0;padding:0 14px 10px}
.pk{display:grid;grid-template-columns:44px 26px 1fr;gap:6px;padding:7px 0;border-top:1px solid var(--linie)}
.pk-zeit{font:12.5px "IBM Plex Mono",monospace;color:var(--leise);padding-top:1px}
.pk-text{min-width:0;overflow-wrap:anywhere}
.pk-details{font-size:12.5px;color:var(--leise);margin-top:2px}
.sha{font:11.5px "IBM Plex Mono",monospace;color:var(--leise)}
footer{margin-top:48px;color:var(--leise);font-size:12.5px}
@media (max-width:600px){h1{font-size:28px}.hero{padding:16px}.k-wert{font-size:26px}}
"""

JS = """
(function(){
  var cd=document.querySelector('.countdown');
  if(cd){var ziel=new Date(cd.dataset.ziel),w=cd.querySelector('.cd-wert'),l=cd.querySelector('.cd-label');
    var tick=function(){var s=Math.round((ziel-new Date())/1000);
      if(s<=0){w.textContent='jetzt';l.textContent='sollte online sein';return;}
      var d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60);
      w.textContent=d>0?d+' T '+h+' h':h>0?h+' h '+m+' min':m+' min';};
    tick();setInterval(tick,30000);}
  var tip=document.getElementById('tip');
  document.querySelectorAll('[data-tip]').forEach(function(el){
    el.addEventListener('mousemove',function(ev){tip.textContent=el.dataset.tip;tip.style.opacity=1;
      var x=Math.min(ev.clientX+12,window.innerWidth-tip.offsetWidth-8);tip.style.left=x+'px';tip.style.top=(ev.clientY-34)+'px';});
    el.addEventListener('mouseleave',function(){tip.style.opacity=0;});});
  var art='',suche=document.getElementById('pk-suche');
  function filtern(){var q=(suche.value||'').toLowerCase().trim(),treffer=0;
    document.querySelectorAll('.pk-tag').forEach(function(t){var n=0;
      t.querySelectorAll('.pk').forEach(function(li){var ok=(!art||li.dataset.art===art)&&(!q||li.dataset.such.indexOf(q)>=0);
        li.hidden=!ok;if(ok)n++;});
      t.hidden=n===0;if(q||art){if(n)t.open=true;}treffer+=n;});
    document.getElementById('pk-leer').hidden=treffer>0;}
  suche.addEventListener('input',filtern);
  document.querySelectorAll('.filt').forEach(function(b){b.addEventListener('click',function(){
    document.querySelectorAll('.filt').forEach(function(x){x.classList.remove('aktiv');});
    b.classList.add('aktiv');art=b.dataset.art;filtern();});});
})();
"""


def schreiben(n, stand, eintraege, kommend, naechster, punkte, ablaeufe, commits):
    koerper = "\n".join([
        kopf(stand, naechster),
        kacheln(n, punkte, kommend, ablaeufe),
        braucht(punkte),
        notizen(),
        kalender(n, eintraege),
        plan_tabelle(n, kommend),
        zuletzt(eintraege),
        zahlen(n),
        automatik(ablaeufe),
        protokoll(n, commits),
    ])
    seite = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>Lage maehrsteuern</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Serif:wght@600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<main>
{koerper}
<footer>Automatisch erzeugt von <code>automatik/lage_html.py</code> – nicht von Hand bearbeiten. Notizen: <code>automatik/lage_notizen.md</code>.</footer>
</main>
<div id="tip" role="tooltip"></div>
<script>{JS}</script>
</body>
</html>
"""
    ZIEL.write_text(seite)
    print(f"✓ {ZIEL.relative_to(WURZEL)} geschrieben")
