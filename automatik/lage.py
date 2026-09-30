"""Lagebericht: schreibt LAGE.md – was gerade läuft, was als Nächstes kommt, was du tun musst, und jede Änderung im Repo.

Aufruf:  python automatik/lage.py          – LAGE.md neu schreiben
Läuft automatisch per GitHub Actions (.github/workflows/lage.yml) nach jedem Push und nach jedem Lauf
von Posten, Freigabe, Statistik, Schlüssel und Musik. Quellen: plan.json, Git-Verlauf, statistik/*.csv,
optional der Workflow-Status über die GitHub-API (GH_TOKEN + GITHUB_REPOSITORY).
Handnotizen („gerade in Arbeit“, Entscheidungen) stehen in automatik/lage_notizen.md und werden oben eingebunden.
"""
import csv, json, os, subprocess
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

WURZEL = Path(__file__).resolve().parent.parent
PLAN = WURZEL / "automatik" / "plan.json"
NOTIZEN = WURZEL / "automatik" / "lage_notizen.md"
KONTO = WURZEL / "automatik" / "statistik" / "konto.csv"
ZIEL = WURZEL / "LAGE.md"
ZONE = ZoneInfo("Europe/Berlin")
NACHHOLEN = timedelta(hours=6)  # wie posten.py: danach wird ein verpasster Eintrag nicht mehr nachgeholt
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/Instagram-maehrsteuern")
LAGE_COMMIT = "Lage aktualisiert"

TYP = {"karussell": "🖼️ Karussell", "reel": "🎬 Reel", "story": "📱 Story", "bild": "🖼️ Bild"}
STATUS = {
    "freigegeben": "🟢 freigegeben (geht automatisch online)",
    "entwurf": "🟡 Entwurf (wartet auf Freigabe)",
    "manuell": "✋ manuell (postest du in der App)",
    "veroeffentlicht": "✅ veröffentlicht",
    "fehler": "🔴 Fehler",
    "entfaellt": "⚪ entfällt",
}
WORKFLOWS = [  # Datei, Name, wann
    ("posten.yml", "Posten", "alle 15 Min. (postet freigegebene Einträge)"),
    ("freigabe.yml", "Freigabe", "bei neuen Entwürfen / Antwort im Issue"),
    ("statistik.yml", "Statistik", "täglich ca. 08:45"),
    ("token.yml", "Schlüssel verlängern", "am 1. des Monats ca. 06:27"),
    ("musik.yml", "Musik holen", "nur von Hand"),
]
WOCHENTAG = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


def git(*args):
    return subprocess.run(["git", *args], cwd=WURZEL, capture_output=True, text=True).stdout.strip()


def zeit(e):
    return datetime.strptime(e["zeit"], "%Y-%m-%d %H:%M").replace(tzinfo=ZONE)


def tag(d):
    return f"{WOCHENTAG[d.weekday()]} {d:%d.%m.} {d:%H:%M}"


def status(e):
    s = e["status"]
    return STATUS.get(s, "⏳ " + s.replace("_", " ") if s.startswith("wartet") else s)


def issue_link(e):
    return f" · [Freigabe #{e['issue']}](https://github.com/{REPO}/issues/{e['issue']})" if e.get("issue") else ""


def dateien_fehlen(e):
    namen = list(e.get("bilder", [])) + [e[k] for k in ("video", "titelbild", "text") if e.get(k)]
    return [n for n in namen if not (WURZEL / e["ordner"] / n).exists()]


# ---------- Abschnitte ----------

def offene_punkte(eintraege, n):
    punkte = []
    for e in sorted(eintraege, key=zeit):
        t, s, name = zeit(e), e["status"], f"`{e['id']}` ({tag(zeit(e))})"
        if s == "fehler":
            punkte.append(f"🔴 **Fehler beim Posten** {name}: {e.get('fehler', '')[:200]}")
        elif s == "freigegeben" and t < n - NACHHOLEN:
            punkte.append(f"🔴 **Verpasst** {name}: war freigegeben, ist aber nicht online gegangen – Zeit neu setzen oder von Hand posten")
        elif s == "entwurf" and t > n - NACHHOLEN:
            gruppe = [x for x in eintraege if x["id"].split("-")[0] == e["id"].split("-")[0]]
            wartet = next((x["id"] for x in gruppe if x["status"].startswith("wartet")), None)
            wie = (issue_link(e).lstrip(" ·") or (f"Issue kommt, sobald `{wartet}` fertig ist" if wartet
                                                   else "Issue wird automatisch angelegt"))
            punkte.append(f"🟡 **Freigeben** {name} – „go“ oder „stop“ im Issue ({wie})")
        elif s.startswith("wartet") and t > n - NACHHOLEN:
            punkte.append(f"⏳ **{s.replace('_', ' ').capitalize()}** {name}" + (f" – {e['hinweis']}" if e.get("hinweis") else ""))
        elif s == "manuell" and t > n - timedelta(days=1):
            punkte.append(f"✋ **Von Hand posten** {name}" + (f" – {e['hinweis']}" if e.get("hinweis") else ""))
        if s in ("freigegeben", "entwurf", "manuell") and t > n and (fehlt := dateien_fehlen(e)):
            punkte.append(f"🔴 **Dateien fehlen** {name}: {', '.join(fehlt)}")
        if e.get("musik_fehlt") and t > n:
            punkte.append(f"🎵 **Musik fehlt** {name}")
        if e.get("danach") and (s == "veroeffentlicht" and n - t < timedelta(days=2) or s == "manuell" and t > n - timedelta(days=1)):
            punkte.append(f"👉 **Danach:** {e['danach']} ({name})")
        if s == "veroeffentlicht" and e.get("hinweis", "").startswith("Danach") and n - t < timedelta(days=2):
            punkte.append(f"👉 **{e['hinweis']}** ({name})")
    return punkte or ["Nichts offen. 🎉"]


def tabelle(eintraege, mit_status=True):
    zeilen = ["| Wann | Was | Status | Hinweis |", "|---|---|---|---|"]
    for e in sorted(eintraege, key=zeit):
        hinweis = (e.get("hinweis", "") + issue_link(e)).replace("|", "/")
        zeilen.append(f"| {tag(zeit(e))} | {TYP.get(e['typ'], e['typ'])} `{e['id']}` | {status(e)} | {hinweis} |")
    return zeilen


def veroeffentlicht(eintraege):
    fertig = sorted((e for e in eintraege if e["status"] == "veroeffentlicht"), key=zeit, reverse=True)[:10]
    if not fertig:
        return ["Über den Autopiloten noch nichts veröffentlicht."]
    return [f"- {tag(zeit(e))} · {TYP.get(e['typ'], e['typ'])} `{e['id']}`"
            + (f" · [ansehen]({e['link']})" if e.get("link") else "")
            + (f" (online {e['veroeffentlicht_am']})" if e.get("veroeffentlicht_am") else "") for e in fertig]


def insights_dateien():
    return sorted((WURZEL / "automatik" / "statistik").glob("insights_*.json"))


def lokal(zeitstempel):
    return datetime.strptime(zeitstempel, "%Y-%m-%dT%H:%M:%S%z").astimezone(ZONE)


def zahlen(n):
    """Tagesbericht aus konto.csv und der neuesten insights_*.json (Abruf täglich ca. 08:45)."""
    zeilen = list(csv.DictReader(KONTO.open())) if KONTO.exists() else []
    dateien = insights_dateien()
    if not zeilen and not dateien:
        return ["Noch keine Statistik."]
    aus = []
    if zeilen:
        letzte = zeilen[-1]
        text = f"**{letzte['followers_count']} Follower** · {letzte['media_count']} Beiträge im Profil (Abruf {letzte['datum']})"
        frueher = [z for z in zeilen if z["datum"] < letzte["datum"]]
        if frueher:
            diff = int(letzte["followers_count"]) - int(frueher[-1]["followers_count"])
            text += f" · **{diff:+d}** seit {frueher[-1]['datum']}" + (" ⚠️" if diff < 0 else "")
        aus.append(text)
    if dateien:
        d = json.loads(dateien[-1].read_text())
        alt = {b["id"]: b for b in json.loads(dateien[-2].read_text()).get("beitraege", [])} if len(dateien) > 1 else {}
        tage = sorted((d.get("tageswerte_reichweite") or {}).items())[-4:]
        if tage:
            aus.append("Reichweite pro Tag: " + " · ".join(f"{t[8:10]}.{t[5:7]}. **{v}**" for t, v in tage))
        storys = sorted(d.get("storys_aktiv") or [], key=lambda x: x.get("zeit") or "")
        if storys:
            aus += ["", "| Story (letzte 24 h) | Aufrufe | Erreicht | Antworten | Profilbesuche | Follows |", "|---|---|---|---|---|---|"]
            aus += [f"| {tag(lokal(s['zeit']))} | {s.get('views', '–')} | {s.get('reach', '–')} | {s.get('replies', '–')} | "
                    f"{s.get('profile_visits', '–')} | {s.get('follows', '–')} |" for s in storys if s.get("zeit")]
        neu = [b for b in d.get("beitraege", []) if b.get("timestamp") and n - lokal(b["timestamp"]) < timedelta(days=14)]
        if neu:
            aus += ["", "| Beitrag (letzte 14 Tage) | Aufrufe | Erreicht | Likes | Komm. | Gespeichert | Geteilt |", "|---|---|---|---|---|---|---|"]
            for b in sorted(neu, key=lambda x: x["timestamp"], reverse=True):
                plus = f" (+{b['views'] - alt[b['id']]['views']})" if isinstance(alt.get(b["id"], {}).get("views"), int) and isinstance(b.get("views"), int) else ""
                name = (b.get("caption") or "").split("\n")[0][:40].replace("|", "/")
                aus.append(f"| {tag(lokal(b['timestamp']))} [{name}]({b.get('permalink', '')}) | {b.get('views', '–')}{plus} | "
                           f"{b.get('reach', '–')} | {b.get('likes', '–')} | {b.get('comments', '–')} | {b.get('saved', '–')} | {b.get('shares', '–')} |")
    return aus + ["", "Rohdaten: `automatik/statistik/`, Auswertung: `strategie/06_auswertung.md`"]


def automatik():
    zeilen = ["| Ablauf | Wann | Letzter Lauf |", "|---|---|---|"]
    token = os.environ.get("GH_TOKEN")
    for datei, name, wann in WORKFLOWS:
        letzter = "–"
        if token:
            try:
                roh = subprocess.run(
                    ["gh", "api", f"repos/{REPO}/actions/workflows/{datei}/runs?status=completed&per_page=20",
                     "--jq", '[.workflow_runs[] | select(.conclusion=="success" or .conclusion=="failure")][0]'
                             ' | [.conclusion, .updated_at, .html_url] | @tsv'],
                    capture_output=True, text=True, timeout=30).stdout.strip()
                if roh:
                    ergebnis, wann_lief, url = roh.split("\t")
                    t = datetime.fromisoformat(wann_lief.replace("Z", "+00:00")).astimezone(ZONE)
                    # erfolgreiche Läufe ohne Zeit, damit LAGE.md nicht bei jedem Posten-Lauf neu committet wird
                    letzter = "✅ ok" if ergebnis == "success" else f"🔴 [fehlgeschlagen]({url}) {tag(t)}"
            except Exception:
                pass
        zeilen.append(f"| {name} | {wann} | {letzter} |")
    return zeilen


# ---------- Protokoll ----------

def art(nachricht):
    for anfang, symbol in (("Autopilot", "🤖"), ("Freigabe", "✅"), ("Statistik", "📈"), ("Musik", "🎵"),
                           ("Schlüssel", "🔑"), ("Merge", "🔀")):
        if nachricht.startswith(anfang):
            return symbol
    return "✍️"


def plan_von(sha):
    try:
        return {e["id"]: e for e in json.loads(git("show", f"{sha}:automatik/plan.json") or "{}").get("eintraege", [])}
    except json.JSONDecodeError:
        return {}


def plan_aenderungen(sha):
    """Was sich an plan.json in diesem Commit geändert hat (neu, gelöscht, Status, Zeit)."""
    if not git("diff-tree", "--no-commit-id", "-r", "--name-only", "--root", sha, "--", "automatik/plan.json"):
        return []
    eltern = git("rev-parse", "-q", "--verify", f"{sha}^")
    alt, neu = plan_von(eltern) if eltern else {}, plan_von(sha)
    teile = [f"neu `{i}` ({neu[i]['zeit']}, {neu[i]['status']})" for i in neu if i not in alt]
    teile += [f"entfernt `{i}`" for i in alt if i not in neu]
    for i in neu:
        if i in alt:
            for feld in ("status", "zeit"):
                if alt[i].get(feld) != neu[i].get(feld):
                    teile.append(f"`{i}` {feld}: {alt[i].get(feld)} → {neu[i].get(feld)}")
            if neu[i].get("issue") and not alt[i].get("issue"):
                teile.append(f"`{i}` → Freigabe-Issue #{neu[i]['issue']}")
            if neu[i].get("fehler") and neu[i].get("fehler") != alt[i].get("fehler"):
                teile.append(f"`{i}` Fehler: {neu[i]['fehler'][:120]}")
            if neu[i].get("link") and not alt[i].get("link"):
                teile.append(f"`{i}` online: {neu[i]['link']}")
    return teile


def bereiche(sha):
    pfade = git("diff-tree", "--no-commit-id", "-r", "--name-only", "--root", sha).splitlines()
    b = []
    for p in pfade:
        teile = p.split("/")
        x = "/".join(teile[:2]) if teile[0] in ("posts", "strategie", "automatik", ".github") and len(teile) > 2 else p
        if x not in b and x != "LAGE.md":
            b.append(x)
    return b[:6] + (["…"] if len(b) > 6 else [])


def protokoll(n):
    log = git("log", "--format=%H%x09%aI%x09%s")
    tage = {}
    for zeile in log.splitlines():
        sha, datum, nachricht = zeile.split("\t", 2)
        if nachricht.startswith(LAGE_COMMIT):
            continue
        t = datetime.fromisoformat(datum).astimezone(ZONE)
        text = f"- {t:%H:%M} {art(nachricht)} {nachricht} ([`{sha[:7]}`](https://github.com/{REPO}/commit/{sha}))"
        if aend := plan_aenderungen(sha):
            text += "\n  - Plan: " + "; ".join(aend)
        elif b := bereiche(sha):
            text += "\n  - " + ", ".join(f"`{x}`" for x in b)
        tage.setdefault(t.date(), []).append(text)
    zeilen, alt = [], []
    for d, eintraege in tage.items():
        block = [f"**{WOCHENTAG[d.weekday()]} {d:%d.%m.%Y}**", *eintraege, ""]
        (zeilen if (n.date() - d).days < 7 else alt).extend(block)
    if alt:
        zeilen += ["<details><summary>Älter als 7 Tage</summary>", "", *alt, "</details>"]
    return zeilen


# ---------- Zusammenbau ----------

def main():
    n = datetime.now(ZONE)
    eintraege = json.loads(PLAN.read_text())["eintraege"]
    aktiv = [e for e in eintraege if e["status"] not in ("veroeffentlicht", "entfaellt")]
    kommend = [e for e in aktiv if zeit(e) >= n - NACHHOLEN]
    naechster = next((e for e in sorted(kommend, key=zeit) if e["status"] in ("freigegeben", "manuell")), None)
    # ohne eigene Lage-Commits, sonst ändert jeder Lauf den Stand und erzeugt den nächsten Commit
    stand = datetime.fromisoformat(git("log", "-1", "--format=%aI", "--invert-grep", f"--grep=^{LAGE_COMMIT}")).astimezone(ZONE)

    teile = [
        "# 🧭 Lage – maehrsteuern auf Instagram",
        "",
        f"_Automatisch erzeugt von `automatik/lage.py` – nicht von Hand bearbeiten (Notizen: `automatik/lage_notizen.md`). "
        f"Stand: letzte Änderung {tag(stand)} Uhr._",
        "",
    ]
    if naechster:
        teile += [f"**Als Nächstes online:** {TYP.get(naechster['typ'])} `{naechster['id']}` am **{tag(zeit(naechster))} Uhr** "
                  f"– {status(naechster)}", ""]
    if NOTIZEN.exists() and (notiz := NOTIZEN.read_text().strip()):
        teile += ["## 📝 Gerade in Arbeit", "", notiz, ""]
    teile += ["## 👉 Braucht dich", "", *[f"- {p}" for p in offene_punkte(eintraege, n)], ""]
    woche = [e for e in kommend if zeit(e) <= n + timedelta(days=7)]
    spaeter = [e for e in kommend if zeit(e) > n + timedelta(days=7)]
    teile += ["## ⏭️ Nächste 7 Tage", "", *(tabelle(woche) if woche else ["Nichts geplant."]), ""]
    if spaeter:
        teile += ["## 🗓️ Danach", "", *tabelle(spaeter), ""]
    teile += ["## ✅ Zuletzt veröffentlicht (Autopilot)", "", *veroeffentlicht(eintraege), ""]
    teile += ["## 📈 Zahlen (täglich ca. 08:45)", "", *zahlen(n), ""]
    teile += ["## ⚙️ Automatik", "", *automatik(), ""]
    teile += ["## 📜 Protokoll – jede Änderung", "",
              "🤖 Autopilot · ✅ Freigabe · 📈 Statistik · 🎵 Musik · 🔀 Merge · ✍️ von Hand / Claude", "",
              *protokoll(n)]
    ZIEL.write_text("\n".join(teile).rstrip() + "\n")
    print(f"✓ {ZIEL.relative_to(WURZEL)} geschrieben")


if __name__ == "__main__":
    main()
