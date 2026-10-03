"""Wochenbericht (sonntags ca. 18:00): EIN Issue „📊 Woche KW xx“ – eine Benachrichtigung pro Woche.

  python automatik/wochenbericht.py bericht          – Bericht bauen, Vorwochen-Issue still schließen
  python automatik/wochenbericht.py antwort "TEXT"   – Loris' Nachtrag im Issue übernehmen:
        demos 2                      → gebuchte Demos der Woche
        manychat 14/6                → ManyChat: gesendet / Klicks auf den Demo-Link
        herkunft manychat 1, bio 1   → woher die Demos kamen (frei, kommagetrennt)
     Mehrere Angaben in einem Kommentar gehen auch. Übernommen wird still in den Issue-Text (keine Antwort-Mail).

Quellen: automatik/statistik/konto.csv + beitraege.csv (Instagram), geschlossene Radar-Issues (Haken),
automatik/interaktion/kommentare.json (Kommentar-Hilfe), strategie/dm_tracking.csv (termin_gebucht = ja),
Reclaim-Buchungen „Demo + Erstgespräch“ im Kalender „maehrsteuern Autopilot“ inkl. Feld „Woher kennst du mich?“.
Alle Werte landen zusätzlich in automatik/statistik/woche.csv.
Umgebung: GH_TOKEN, GITHUB_REPOSITORY, GOOGLE_SA_KEY + GOOGLE_CALENDAR_ID (optional, für Demo-Buchungen).
"""
import csv, json, os, re, subprocess, sys, time
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

WURZEL = Path(__file__).resolve().parent.parent
STATISTIK = WURZEL / "automatik" / "statistik"
WOCHE = STATISTIK / "woche.csv"
KOMMENTARE = WURZEL / "automatik" / "interaktion" / "kommentare.json"
DM_TRACKING = WURZEL / "strategie" / "dm_tracking.csv"
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/Instagram-maehrsteuern")
LABEL = "wochenbericht"
FELDER = ["kw", "von", "bis", "follower_start", "follower_ende", "zuwachs", "views_woche", "reichweite_neue",
          "speichern_neue", "teilen_neue", "neue_beitraege", "radar_kommentiert", "radar_dms", "kommentare_beantwortet",
          "demos_tracking", "demos_kalender", "herkunft_kalender", "demos_hand", "manychat_gesendet", "manychat_klicks", "herkunft"]
HAND = ("demos_hand", "manychat_gesendet", "manychat_klicks", "herkunft")


def gh(*args, eingabe=None):
    return subprocess.run(["gh", *args, "--repo", REPO], input=eingabe, check=True, capture_output=True, text=True).stdout.strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=WURZEL, check=True, capture_output=True, text=True).stdout.strip()


def zahl(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return 0


def lesen(datei, trenner=","):
    if not datei.exists():
        return []
    with datei.open(newline="") as f:
        return list(csv.DictReader(f, delimiter=trenner))


# ---------- Zahlen ----------

def follower(von, bis):
    zeilen = sorted(lesen(STATISTIK / "konto.csv"), key=lambda z: z["datum"])
    vorher = [z for z in zeilen if z["datum"] < von.isoformat()] or [z for z in zeilen if z["datum"] <= bis.isoformat()][:1]
    nachher = [z for z in zeilen if z["datum"] <= bis.isoformat()]
    start = zahl(vorher[-1]["followers_count"]) if vorher else 0
    ende = zahl(nachher[-1]["followers_count"]) if nachher else start
    return start, ende


def beitraege(von, bis):
    """Letzter Stand je Beitrag bis Wochenende. Aufrufe der Woche = Zuwachs je Beitrag gegenüber dem Stand vor der
    Woche – fehlt der (Statistik lief noch nicht), zählt der erste Stand in der Woche als Basis, damit alte Aufrufe
    nicht als neu erscheinen. Top 3 nur aus Beiträgen der letzten 4 Wochen."""
    zeilen = sorted(lesen(STATISTIK / "beitraege.csv"), key=lambda z: z["datum"])
    stand_ende, basis = {}, {}
    for z in zeilen:
        if z["datum"] < von.isoformat():
            basis[z["id"]] = z
        elif z["datum"] <= bis.isoformat():
            if z["id"] not in basis and z["gepostet"] < von.isoformat():
                basis[z["id"]] = z  # erster Stand in der Woche
            stand_ende[z["id"]] = z
    views = sum(max(0, zahl(z["views"]) - zahl(basis.get(i, {}).get("views"))) for i, z in stand_ende.items())
    neu = [z for z in stand_ende.values() if von.isoformat() <= z["gepostet"] <= bis.isoformat()]
    frisch = [z for z in stand_ende.values() if z["gepostet"] >= (von - timedelta(days=21)).isoformat() and zahl(z["reach"]) >= 20]
    top = sorted(frisch, key=lambda z: -(zahl(z["saved"]) + zahl(z["shares"])) / max(1, zahl(z["reach"])))[:3]
    return views, neu, top


def radar(von, bis):
    """Abgehakte Kästchen in den Radar-Issues der Woche."""
    try:
        issues = json.loads(gh("issue", "list", "--label", "radar", "--state", "all", "--limit", "20",
                               "--json", "title,body,createdAt"))
    except subprocess.CalledProcessError:
        return 0, 0
    kommentiert = dms = 0
    for i in issues:
        if von.isoformat() <= i["createdAt"][:10] <= bis.isoformat():
            kommentiert += len(re.findall(r"^- \[[xX]\] 💬", i["body"], re.M))
            dms += len(re.findall(r"^- \[[xX]\] ✉️", i["body"], re.M))
    return kommentiert, dms


def kommentare(von, bis):
    if not KOMMENTARE.exists():
        return 0
    eintraege = json.loads(KOMMENTARE.read_text()).get("kommentare", {}).values()
    return sum(1 for k in eintraege if k.get("status") == "beantwortet" and von.isoformat() <= k.get("datum", "") <= bis.isoformat())


def demos_tracking(von, bis):
    zeilen = lesen(DM_TRACKING, ";")
    return sum(1 for z in zeilen if von.isoformat() <= z.get("datum", "") <= bis.isoformat()
               and z.get("termin_gebucht", "").strip().lower() in ("ja", "j", "yes", "x"))


def demos_kalender(von, bis):
    """Reclaim-Buchungen „Demo + Erstgespräch“, die in der Woche gebucht wurden – gelesen aus dem Kalender
    GOOGLE_CALENDAR_ID („maehrsteuern Autopilot“, Dienstkonto). Klappt, sobald Reclaim Buchungen dort einträgt.
    Herkunft aus dem Buchungsfeld „Woher kennst du mich?“. Eigene Testbuchungen (nur Loris als Gast) zählen nicht.
    Gibt (Anzahl, „Instagram 2, LinkedIn 1“) zurück – oder ("", "") ohne Zugang."""
    if not os.environ.get("GOOGLE_SA_KEY") or not os.environ.get("GOOGLE_CALENDAR_ID"):
        return "", ""
    from html import unescape
    from kalender_sync import MARKE, sitzung
    s = sitzung()
    r = s.get(f"https://www.googleapis.com/calendar/v3/calendars/{os.environ['GOOGLE_CALENDAR_ID']}/events",
              params={"q": "Demo + Erstgespräch", "timeMin": f"{von.isoformat()}T00:00:00Z",
                      "timeMax": f"{(bis + timedelta(days=70)).isoformat()}T00:00:00Z", "singleEvents": "true",
                      "maxResults": 250}, timeout=60)
    r.raise_for_status()
    anzahl, herkunft = 0, {}
    for e in r.json().get("items", []):
        if e.get("extendedProperties", {}).get("private", {}).get(MARKE) or e.get("status") == "cancelled":
            continue
        if not von.isoformat() <= e.get("created", "")[:10] <= bis.isoformat():
            continue
        veranstalter = e.get("organizer", {}).get("email")
        gaeste = [a.get("email") for a in e.get("attendees", [])
                  if not a.get("organizer") and not a.get("self") and a.get("email") != veranstalter]
        if not gaeste:
            continue  # niemand außer Loris selbst = Testbuchung
        anzahl += 1
        text_ = re.sub(r"<[^>]+>", "\n", unescape(e.get("description", "")))
        m = re.search(r"Woher kennst du mich\??\s*[:\-–]?\s*\n*\s*([^\n]+)", text_, re.I)
        quelle = (m.group(1).strip() if m else "unbekannt")[:40] or "unbekannt"
        herkunft[quelle] = herkunft.get(quelle, 0) + 1
    return str(anzahl), ", ".join(f"{q} {n}" for q, n in sorted(herkunft.items(), key=lambda x: -x[1]))


# ---------- Datei + Issue ----------

def tabelle_laden():
    return {z["kw"]: z for z in lesen(WOCHE)}


def tabelle_speichern(zeilen, nachricht):
    STATISTIK.mkdir(parents=True, exist_ok=True)
    with WOCHE.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FELDER)
        w.writeheader()
        w.writerows(sorted(zeilen.values(), key=lambda z: z["kw"]))
    git("add", str(WOCHE))
    if not git("status", "--porcelain", "--", str(WOCHE)):
        return
    git("commit", "-m", nachricht)
    for versuch in range(5):
        try:
            git("pull", "--rebase", "-q")
            git("push")
            return
        except subprocess.CalledProcessError:
            time.sleep(5 * (versuch + 1))
    raise RuntimeError("woche.csv konnte nicht gespeichert werden")


def text(z, neu, top):
    pfeil = "📈" if zahl(z["zuwachs"]) > 0 else ("📉" if zahl(z["zuwachs"]) < 0 else "➖")
    hand = lambda k, leer="_offen_": z.get(k) or leer
    zeilen = [
        f"@{REPO.split('/')[0]} Moin! Dein Wochenabschluss – kürzer als jede Steuererklärung.",
        "",
        "## Reichweite",
        f"- Follower: {z['follower_start']} → **{z['follower_ende']}** ({pfeil} {zahl(z['zuwachs']):+d})",
        f"- Aufrufe neu (alle Beiträge): **{z['views_woche']}**",
        f"- Neue Beiträge: {z['neue_beitraege']} · Reichweite {z['reichweite_neue']} · Speichern {z['speichern_neue']} · Teilen {z['teilen_neue']}",
        "",
        "**Top 3 der letzten 4 Wochen – (Speichern + Teilen) / Reichweite**",
    ]
    zeilen += [f"{n}. [{(t['anfang'] or t['typ'])[:50]}]({t['link']}) – {zahl(t['saved'])} gespeichert, "
               f"{zahl(t['shares'])} geteilt, Reichweite {zahl(t['reach'])}" for n, t in enumerate(top, 1)] or ["_noch zu wenig Daten_"]
    zeilen += [
        "",
        "## Interaktion",
        f"- Radar: {z['radar_kommentiert']} Kommentare, {z['radar_dms']} DMs abgehakt",
        f"- Kommentar-Hilfe: {z['kommentare_beantwortet']} beantwortet",
        "",
        "## Trichter",
        "| Stufe | Woche |",
        "|---|---|",
        f"| ManyChat gesendet | {hand('manychat_gesendet')} |",
        f"| Klicks Demo-Link | {hand('manychat_klicks')} |",
        f"| Demos gebucht (von Hand) | {hand('demos_hand')} |",
        f"| Demos laut Kalender (Reclaim) | {z.get('demos_kalender') or '_noch nicht verbunden_'} |",
        f"| Demos laut `dm_tracking.csv` | {z['demos_tracking']} |",
        f"| Herkunft (Buchungsfeld) | {z.get('herkunft_kalender') or '–'} |",
        f"| Herkunft (von Hand) | {hand('herkunft', '_offen_')} |",
        "",
        "**Nachtragen** – einfach hier kommentieren, wird still übernommen:",
        "`demos 2` · `manychat 14/6` (gesendet/Klicks) · `herkunft manychat 1, bio 1`",
        "",
        f"<sub>KW {z['kw']} · {z['von']} bis {z['bis']} · Rohdaten: `automatik/statistik/woche.csv`</sub>",
    ]
    return "\n".join(zeilen)


def bericht():
    heute = datetime.now(ZoneInfo("Europe/Berlin")).date()
    bis = heute - timedelta(days=(heute.weekday() + 1) % 7)  # letzter Sonntag (heute, wenn Sonntag)
    von = bis - timedelta(days=6)
    kw = f"{bis.isocalendar()[0]}-{bis.isocalendar()[1]:02d}"
    tabelle = tabelle_laden()
    alt = tabelle.get(kw, {})
    start, ende = follower(von, bis)
    views, neu, top = beitraege(von, bis)
    r_kom, r_dm = radar(von, bis)
    z = {"kw": kw, "von": von.isoformat(), "bis": bis.isoformat(), "follower_start": start, "follower_ende": ende,
         "zuwachs": ende - start, "views_woche": views,
         "reichweite_neue": sum(zahl(b["reach"]) for b in neu), "speichern_neue": sum(zahl(b["saved"]) for b in neu),
         "teilen_neue": sum(zahl(b["shares"]) for b in neu), "neue_beitraege": len(neu),
         "radar_kommentiert": r_kom, "radar_dms": r_dm, "kommentare_beantwortet": kommentare(von, bis),
         "demos_tracking": demos_tracking(von, bis), **{k: alt.get(k, "") for k in HAND}}
    try:
        z["demos_kalender"], z["herkunft_kalender"] = demos_kalender(von, bis)
    except Exception as fehler:  # Kalender darf den Bericht nie verhindern
        print(f"Hinweis: Demo-Buchungen nicht lesbar ({fehler})")
        z["demos_kalender"], z["herkunft_kalender"] = "", ""
    tabelle[kw] = {k: str(v) for k, v in z.items()}
    titel = f"📊 Woche KW {bis.isocalendar()[1]} – {ende} Follower ({ende - start:+d})"
    offen = json.loads(gh("issue", "list", "--label", LABEL, "--state", "open", "--json", "number,title"))
    gleich = [i for i in offen if f"KW {bis.isocalendar()[1]} " in i["title"]]
    try:
        gh("label", "create", LABEL, "--color", "53C3A2", "--description", "Wochenbericht, sonntags")
    except subprocess.CalledProcessError:
        pass
    if gleich:  # zweiter Lauf in derselben Woche: nur aktualisieren, keine neue Benachrichtigung
        gh("issue", "edit", str(gleich[0]["number"]), "--title", titel, "--body-file", "-", eingabe=text(tabelle[kw], neu, top))
    else:
        print(gh("issue", "create", "--title", titel, "--label", LABEL, "--body-file", "-", eingabe=text(tabelle[kw], neu, top)))
        for i in offen:
            gh("issue", "close", str(i["number"]))  # Vorwoche still schließen
    tabelle_speichern(tabelle, f"Wochenbericht KW {kw}")
    print(f"✓ {titel}")


def antwort(nummer, kommentar):
    titel = gh("issue", "view", str(nummer), "--json", "title", "--jq", ".title")
    treffer = re.search(r"KW (\d+)", titel)
    tabelle = tabelle_laden()
    kw = next((k for k in sorted(tabelle, reverse=True) if treffer and k.endswith(f"-{int(treffer.group(1)):02d}")), None)
    if not kw:
        print("Keine passende Woche gefunden – nichts zu tun.")
        return
    z, vorher = tabelle[kw], dict(tabelle[kw])
    if m := re.search(r"demos?\s*[:=]?\s*(\d+)", kommentar, re.I):
        z["demos_hand"] = m.group(1)
    if m := re.search(r"manychat\s*[:=]?\s*(\d+)\s*/\s*(\d+)", kommentar, re.I):
        z["manychat_gesendet"], z["manychat_klicks"] = m.group(1), m.group(2)
    if m := re.search(r"herkunft\s*[:=]?\s*(.+)", kommentar, re.I):
        z["herkunft"] = m.group(1).strip()[:200]
    if z == vorher:
        print("Nichts erkannt – nichts zu tun.")
        return
    von, bis = date.fromisoformat(z["von"]), date.fromisoformat(z["bis"])
    _, neu, top = beitraege(von, bis)
    gh("issue", "edit", str(nummer), "--body-file", "-", eingabe=text(z, neu, top))
    tabelle_speichern(tabelle, f"Wochenbericht KW {kw}: Nachtrag")
    print("✓ übernommen")


if __name__ == "__main__":
    if sys.argv[1] == "bericht":
        bericht()
    else:
        antwort(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "")
