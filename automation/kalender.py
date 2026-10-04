"""Termine aus automatik/plan.json – liest der Google-Kalender-Sync (automatik/kalender_sync.py).

Enthält:
- jeden Feed-Beitrag (Reel, Karussell, Bild) zur Postzeit: „live – Kommentare beantworten“, „von Hand posten“,
  „erst freigeben“ oder „wartet …“
- Storys nur, wenn sie von Hand gepostet werden
- To-dos: fehlende Clips/Musik 5 Tage vorher, fehlende Dateien – 5 Tage vorher 19:00, nie nach der Postzeit
Feste UIDs je Eintrag → der Sync aktualisiert Termine statt sie zu verdoppeln.
Jeder Termin hat eine Art (ART): bestimmt Farbe, Erinnerung und ob er für Reclaim „beschäftigt“ ist –
nur Postzeiten blocken Demo-Slots, To-dos und LinkedIn-Erinnerungen stehen als „frei“ drin.
(Bis 03.10.2026 entstand hieraus auch kalender.ics zum Abonnieren – ersetzt durch den Direkt-Sync.)
"""
from datetime import timedelta
import os

from lage import WURZEL, TYP, zeit, dateien_fehlen, erinnerungen

REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/Instagram-maehrsteuern")
FEED = ("reel", "karussell", "bild")
CHROME = f"https://github.com/{REPO}/blob/claude/instagram/strategie/14_chrome_module.md"
FREIGABEN = f"https://github.com/{REPO}/issues?q=is%3Aopen+label%3Afreigabe"
RUECKBLICK = timedelta(days=14)

# Art → (Google-Farbe colorId, Pop-up-Erinnerungen in Minuten vorher, beschäftigt für Reclaim)
# Farben: 3 Traube, 5 Banane, 6 Mandarine, 7 Pfau, 9 Heidelbeere, 10 Basilikum, 11 Tomate
ART = {
    "live":     ("10", [10, 0], True),   # geht automatisch online – erste Stunde Kommentare
    "manuell":  ("9", [30, 0], True),    # von Hand posten
    "freigabe": ("5", [0], True),        # Postzeit, aber erst nach „go“
    "wartet":   ("6", [0], True),        # Postzeit, es fehlt noch etwas
    "fehler":   ("11", [0], True),       # Posten ist gescheitert
    "liefern":  ("6", [0], False),       # To-do: Sprachnachricht/Clips liefern
    "musik":    ("3", [0], False),       # To-do: Musik wählen
    "dateien":  ("11", [0], False),      # To-do: Dateien fehlen
    "linkedin": ("7", [0], False),       # Chrome Modul 5
    "erinnerung": ("3", [1440, 0], False),  # Frist/Entscheidung aus automatik/erinnerungen.json
}


def termin(uid, start, minuten, titel, text, art):
    """Ein Termin als Daten für den Google-Sync (kalender_sync.py)."""
    return {"uid": uid, "start": start, "ende": start + timedelta(minutes=minuten), "titel": titel, "text": text,
            "art": art}


def name(e):
    thema = e["id"].split("-", 1)[-1]
    thema = thema.removeprefix(e["typ"] + "-").replace("-", " ")
    return f"{TYP.get(e['typ'], e['typ'])} „{thema}“"


def erste_zeile(e):
    datei = WURZEL / e["ordner"] / e.get("text", "")
    if e.get("text") and datei.exists():
        return datei.read_text(encoding="utf-8").strip().splitlines()[0]
    return ""


def drehbuch(e):
    pfad = f"{e['ordner']}/drehbuch.md"
    return f"Drehbuch: https://github.com/{REPO}/blob/claude/instagram/{pfad}\n" if (WURZEL / pfad).exists() else ""


def eintraege_zu_terminen(eintraege, jetzt):
    t = []
    for e in eintraege:
        s, beginn = e["status"], zeit(e)
        if s == "entfaellt" or beginn < jetzt - RUECKBLICK:
            continue
        info = "\n".join(x for x in (erste_zeile(e), e.get("hinweis", ""),
                                      f"Freigabe: https://github.com/{REPO}/issues/{e['issue']}" if e.get("issue") else "") if x)
        if e["typ"] in FEED or s == "manuell":
            if s == "manuell":
                art, titel, text = "manuell", f"✋ {name(e)} – von Hand posten", "In der Instagram-App posten."
            elif s == "entwurf":
                art, titel = "freigabe", f"🟡 {name(e)} – erst freigeben"
                text = f"Geht nur online nach „go“ im Issue: {FREIGABEN}"
            elif s.startswith("wartet"):
                art, titel = "wartet", f"⏳ {name(e)} – {s.replace('_', ' ')}"
                text = "Geht erst online, wenn das Fehlende da ist."
            elif s == "fehler":
                art, titel, text = "fehler", f"🔴 {name(e)} – Fehler beim Posten", e.get("fehler", "")[:300]
            else:
                art, titel = "live", f"{name(e)} live – Kommentare beantworten"
                text = "Geht automatisch online. Erste Stunde: jeden Kommentar mit Gegenfrage beantworten, TOOL-DMs prüfen."
                if e.get("online"):
                    text += f"\n{e['online']}"
            if e.get("danach"):
                text += f"\nDanach: {e['danach']}"
            t.append(termin(e["id"], beginn, 45 if e["typ"] in FEED else 15, titel, f"{text}\n{info}".strip(), art))
        if e["typ"] == "karussell" and s in ("freigegeben", "veroeffentlicht") \
                and (WURZEL / e["ordner"] / "linkedin" / "karussell.pdf").exists():
            li = (beginn + timedelta(days=1)).replace(hour=8, minute=0)
            while li.weekday() >= 5:  # LinkedIn nie am Wochenende
                li += timedelta(days=1)
            t.append(termin(f"{e['id']}-linkedin", li, 15, f"💼 LinkedIn: {name(e)} posten (Chrome Modul 5)",
                            f"PDF + Text liegen im Issue: https://github.com/{REPO}/issues?q=is%3Aopen+label%3Alinkedin\n"
                            f"Chrome-Claude: Gesamtprompt aus {CHROME} einfügen, dann „Modul 5“. Absenden nur nach deinem go.",
                            "linkedin"))
        if beginn <= jetzt:
            continue
        bald = jetzt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        # 5 Tage vorher 19:00, frühestens zur nächsten vollen Stunde – aber nie nach der Postzeit
        frist = min(max((beginn - timedelta(days=5)).replace(hour=19, minute=0), bald),
                    beginn - timedelta(minutes=30))
        if s.startswith("wartet"):
            t.append(termin(f"{e['id']}-todo", frist,
                            20, f"📦 Liefern für {name(e)}: {s.replace('wartet_auf_', '').replace('_', ' ')}",
                            f"Postzeit {beginn:%d.%m. %H:%M}. Dateien hochladen oder Claude Bescheid geben.\n{drehbuch(e)}{info}", "liefern"))
        if e.get("musik_fehlt"):
            t.append(termin(f"{e['id']}-musik", frist, 15,
                            f"🎵 Musik fehlt: {name(e)}", f"Postzeit {beginn:%d.%m. %H:%M}. Titel/Stimmung an Claude oder in der App wählen.", "musik"))
        if s in ("freigegeben", "entwurf", "manuell") and (fehlt := dateien_fehlen(e)):
            t.append(termin(f"{e['id']}-dateien", frist, 15,
                            f"🔴 Dateien fehlen: {name(e)}", ", ".join(fehlt), "dateien"))
    return t


def erinnerungen_zu_terminen(jetzt):
    """Einmalige Erinnerungen aus automatik/erinnerungen.json (nur kalender = true, nicht erledigt)."""
    return [termin(f"erinnerung-{r['id']}", r["start"], 30, r["titel"], r.get("text", ""), "erinnerung")
            for r in erinnerungen() if r.get("kalender") and r["start"] >= jetzt - RUECKBLICK]
