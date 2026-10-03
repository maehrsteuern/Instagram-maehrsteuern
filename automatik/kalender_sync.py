"""Termine aus dem Plan direkt in den Google-Kalender „maehrsteuern Autopilot“ schreiben (läuft mit jedem Lage-Lauf).

Gleiche Termine wie kalender.ics (automatik/kalender.py), aber sofort statt mit Abo-Verzögerung – und als
„beschäftigt“, damit Reclaim keine Demo auf Postzeiten oder To-dos legt.

Sicherheit / Rechte:
- Zugang nur über das Dienstkonto aus GOOGLE_SA_KEY, Scope ausschließlich calendar.events.
- Kalender immer aus GOOGLE_CALENDAR_ID – nie „primary“, keine Domain-Delegation, keine Teilnehmer, keine Einladungen.
- Angefasst werden nur Termine mit extendedProperties.private.maehrsteuern = "1" (also selbst angelegte).

Idempotent: feste Event-ID je Termin (sha1 der UID) + Inhalts-Prüfsumme → ein Re-Run ändert nur, was sich geändert hat.
Termine, die es im Plan nicht mehr gibt, werden gelöscht (nur eigene, nur ab 14 Tagen Rückblick).
Ohne GOOGLE_SA_KEY / GOOGLE_CALENDAR_ID: Hinweis, nichts zu tun.
"""
import hashlib, json, os, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kalender import RUECKBLICK, eintraege_zu_terminen
from lage import PLAN, ZONE

SCOPE = "https://www.googleapis.com/auth/calendar.events"
MARKE = "maehrsteuern"


def event_id(uid):
    # Google erlaubt a–v und 0–9; Hex (0–9, a–f) passt immer
    return "ms" + hashlib.sha1(uid.encode()).hexdigest()


def als_event(t):
    inhalt = {
        "summary": t["titel"],
        "description": t["text"],
        "start": {"dateTime": t["start"].isoformat(), "timeZone": "Europe/Berlin"},
        "end": {"dateTime": t["ende"].isoformat(), "timeZone": "Europe/Berlin"},
        "transparency": "opaque",  # „beschäftigt“ – Reclaim plant drumherum
        "reminders": {"useDefault": True},
    }
    pruefsumme = hashlib.sha1(json.dumps(inhalt, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    return {**inhalt, "id": event_id(t["uid"]), "status": "confirmed",
            "extendedProperties": {"private": {MARKE: "1", "uid": t["uid"], "pruefsumme": pruefsumme}}}


def sitzung():
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account
    info = json.loads(os.environ["GOOGLE_SA_KEY"])
    return AuthorizedSession(service_account.Credentials.from_service_account_info(info, scopes=[SCOPE]))


def eigene_events(s, basis, ab):
    events, seite = {}, None
    while True:
        params = {"privateExtendedProperty": f"{MARKE}=1", "timeMin": ab.isoformat(), "showDeleted": "false",
                  "singleEvents": "true", "maxResults": 250}
        if seite:
            params["pageToken"] = seite
        r = s.get(f"{basis}/events", params=params, timeout=60)
        r.raise_for_status()
        daten = r.json()
        events.update({e["id"]: e for e in daten.get("items", [])})
        seite = daten.get("nextPageToken")
        if not seite:
            return events


def main():
    if not os.environ.get("GOOGLE_SA_KEY") or not os.environ.get("GOOGLE_CALENDAR_ID"):
        print("Kalender-Sync: GOOGLE_SA_KEY / GOOGLE_CALENDAR_ID fehlen – nichts zu tun.")
        return
    jetzt = datetime.now(ZONE)
    soll = {e["id"]: e for e in map(als_event, eintraege_zu_terminen(json.loads(PLAN.read_text())["eintraege"], jetzt))}
    s = sitzung()
    basis = f"https://www.googleapis.com/calendar/v3/calendars/{os.environ['GOOGLE_CALENDAR_ID']}"
    ist = eigene_events(s, basis, jetzt - RUECKBLICK)
    neu = geaendert = geloescht = 0
    for eid, event in soll.items():
        vorhanden = ist.get(eid)
        if vorhanden and vorhanden.get("extendedProperties", {}).get("private", {}).get("pruefsumme") == \
                event["extendedProperties"]["private"]["pruefsumme"]:
            continue
        # PUT legt nichts an – existiert das Event (auch gelöscht/storniert) → aktualisieren, sonst neu anlegen
        r = s.put(f"{basis}/events/{eid}", params={"sendUpdates": "none"}, json=event, timeout=60)
        if r.status_code == 404:
            r = s.post(f"{basis}/events", params={"sendUpdates": "none"}, json=event, timeout=60)
            neu += 1
        else:
            geaendert += 1
        r.raise_for_status()
    for eid in set(ist) - set(soll):
        r = s.delete(f"{basis}/events/{eid}", params={"sendUpdates": "none"}, timeout=60)
        if r.status_code not in (200, 204, 404, 410):
            r.raise_for_status()
        geloescht += 1
    print(f"✓ Kalender-Sync: {len(soll)} Termine – {neu} neu, {geaendert} geändert, {geloescht} gelöscht")


if __name__ == "__main__":
    main()
