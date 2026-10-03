"""Termine aus automatik/plan.json – liest der Google-Kalender-Sync (automatik/kalender_sync.py).

Enthält:
- jeden Feed-Beitrag (Reel, Karussell, Bild) zur Postzeit: „live – Kommentare beantworten“, „von Hand posten“,
  „erst freigeben“ oder „wartet …“
- Storys nur, wenn sie von Hand gepostet werden
- To-dos: fehlende Clips/Musik 5 Tage vorher, Freigabe offen 2 Tage vorher (19:00)
Feste UIDs je Eintrag → der Sync aktualisiert Termine statt sie zu verdoppeln.
(Bis 03.10.2026 entstand hieraus auch kalender.ics zum Abonnieren – ersetzt durch den Direkt-Sync.)
"""
from datetime import timedelta
import os

from lage import WURZEL, TYP, zeit, dateien_fehlen

REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/Instagram-maehrsteuern")
FEED = ("reel", "karussell", "bild")
FREIGABEN = f"https://github.com/{REPO}/issues?q=is%3Aopen+label%3Afreigabe"
RUECKBLICK = timedelta(days=14)


def termin(uid, start, minuten, titel, text):
    """Ein Termin als Daten für den Google-Sync (kalender_sync.py)."""
    return {"uid": uid, "start": start, "ende": start + timedelta(minutes=minuten), "titel": titel, "text": text}


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
                titel, text = f"✋ {name(e)} – von Hand posten", "In der Instagram-App posten."
            elif s == "entwurf":
                titel, text = f"🟡 {name(e)} – erst freigeben", f"Geht nur online nach „go“ im Issue: {FREIGABEN}"
            elif s.startswith("wartet"):
                titel, text = f"⏳ {name(e)} – {s.replace('_', ' ')}", "Geht erst online, wenn das Fehlende da ist."
            elif s == "fehler":
                titel, text = f"🔴 {name(e)} – Fehler beim Posten", e.get("fehler", "")[:300]
            else:
                titel = f"{name(e)} live – Kommentare beantworten"
                text = "Geht automatisch online. Erste Stunde: jeden Kommentar mit Gegenfrage beantworten, TOOL-DMs prüfen."
                if e.get("online"):
                    text += f"\n{e['online']}"
            if e.get("danach"):
                text += f"\nDanach: {e['danach']}"
            t.append(termin(e["id"], beginn, 45 if e["typ"] in FEED else 15, titel, f"{text}\n{info}".strip()))
        if beginn <= jetzt:
            continue
        bald = jetzt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        frist = max((beginn - timedelta(days=5)).replace(hour=19, minute=0), bald)
        if s.startswith("wartet"):
            t.append(termin(f"{e['id']}-todo", frist,
                            20, f"📦 Liefern für {name(e)}: {s.replace('wartet_auf_', '').replace('_', ' ')}",
                            f"Postzeit {beginn:%d.%m. %H:%M}. Dateien hochladen oder Claude Bescheid geben.\n{drehbuch(e)}{info}"))
        if e.get("musik_fehlt"):
            t.append(termin(f"{e['id']}-musik", frist, 15,
                            f"🎵 Musik fehlt: {name(e)}", f"Postzeit {beginn:%d.%m. %H:%M}. Titel/Stimmung an Claude oder in der App wählen."))
        if s in ("freigegeben", "entwurf", "manuell") and (fehlt := dateien_fehlen(e)):
            t.append(termin(f"{e['id']}-dateien", frist, 15,
                            f"🔴 Dateien fehlen: {name(e)}", ", ".join(fehlt)))
    return t
