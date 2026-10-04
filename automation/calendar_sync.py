"""Write the events from the plan straight into the Google calendar "maehrtax Autopilot" (runs with every status run).

Events come from automation/calendar_events.py. Posting times are "busy" so Reclaim does not put a demo on them;
to-dos and LinkedIn reminders are "free" (kind → calendar_events.KIND).

Safety / permissions:
- Access only via the service account in GOOGLE_SA_KEY, scope calendar.events only.
- Calendar always from GOOGLE_CALENDAR_ID – never "primary", no domain delegation, no attendees, no invitations.
- Only events with extendedProperties.private.source = "maehrtax" are touched (i.e. created by this script).
  The German sister repo marks its events differently (maehrsteuern = "1") and uses other event IDs, so the two
  syncs can never update or delete each other's events – even if both point at the same calendar.

Idempotent: fixed event ID per event (prefix "mt" + sha1 of "maehrtax:" + UID) + content checksum → a re-run only
changes what changed. Events no longer in the plan are deleted (only our own, only from 14 days back).
Without GOOGLE_SA_KEY / GOOGLE_CALENDAR_ID: prints a note, does nothing.
"""
import hashlib, json, os, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calendar_events import KIND, LOOKBACK, all_events
from status import ZONE

SCOPE = "https://www.googleapis.com/auth/calendar.events"
SOURCE = "maehrtax"          # value of extendedProperties.private.source on every event we own
TIME_ZONE = "America/New_York"


def event_id(uid):
    # Google allows a–v and 0–9; hex (0–9, a–f) always fits. "mt" + namespaced hash ≠ the German repo's "ms" + sha1(uid)
    return "mt" + hashlib.sha1(f"{SOURCE}:{uid}".encode()).hexdigest()


def to_google(t):
    color, popups, busy = KIND[t["kind"]]
    content = {
        "summary": t["title"],
        "description": t["text"],
        "start": {"dateTime": t["start"].isoformat(), "timeZone": TIME_ZONE},
        "end": {"dateTime": t["end"].isoformat(), "timeZone": TIME_ZONE},
        "transparency": "opaque" if busy else "transparent",  # opaque = Reclaim plans around it
        "colorId": color,
        "reminders": {"useDefault": False, "overrides": [{"method": "popup", "minutes": m} for m in popups]},
    }
    checksum = hashlib.sha1(json.dumps(content, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    return {**content, "id": event_id(t["uid"]), "status": "confirmed",
            "extendedProperties": {"private": {"source": SOURCE, "uid": t["uid"], "checksum": checksum}}}


def is_ours(ev):
    return (ev.get("extendedProperties") or {}).get("private", {}).get("source") == SOURCE


def session():
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account
    info = json.loads(os.environ["GOOGLE_SA_KEY"])
    return AuthorizedSession(service_account.Credentials.from_service_account_info(info, scopes=[SCOPE]))


def own_events(s, base, since):
    events, page = {}, None
    while True:
        params = {"privateExtendedProperty": f"source={SOURCE}", "timeMin": since.isoformat(), "showDeleted": "false",
                  "singleEvents": "true", "maxResults": 250}
        if page:
            params["pageToken"] = page
        r = s.get(f"{base}/events", params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        events.update({e["id"]: e for e in data.get("items", []) if is_ours(e)})
        page = data.get("nextPageToken")
        if not page:
            return events


def main():
    if not os.environ.get("GOOGLE_SA_KEY") or not os.environ.get("GOOGLE_CALENDAR_ID"):
        print("Calendar sync: GOOGLE_SA_KEY / GOOGLE_CALENDAR_ID missing – nothing to do.")
        return
    now = datetime.now(ZONE)
    wanted = {e["id"]: e for e in map(to_google, all_events(now))}
    s = session()
    base = f"https://www.googleapis.com/calendar/v3/calendars/{os.environ['GOOGLE_CALENDAR_ID']}"
    existing = own_events(s, base, now - LOOKBACK)
    created = changed = deleted = skipped = 0
    for eid, ev in wanted.items():
        current = existing.get(eid)
        if current and current.get("extendedProperties", {}).get("private", {}).get("checksum") == \
                ev["extendedProperties"]["private"]["checksum"]:
            continue
        if current:
            r = s.put(f"{base}/events/{eid}", params={"sendUpdates": "none"}, json=ev, timeout=60)
            r.raise_for_status()
            changed += 1
            continue
        r = s.post(f"{base}/events", params={"sendUpdates": "none"}, json=ev, timeout=60)
        if r.status_code == 409:
            # ID exists already (e.g. our own event, deleted/cancelled or outside the lookback) – only take it over if it is ours
            old = s.get(f"{base}/events/{eid}", timeout=60)
            if old.ok and is_ours(old.json()):
                r = s.put(f"{base}/events/{eid}", params={"sendUpdates": "none"}, json=ev, timeout=60)
                r.raise_for_status()
                changed += 1
            else:
                print(f"Note: event ID {eid} belongs to someone else – left untouched")
                skipped += 1
            continue
        r.raise_for_status()
        created += 1
    for eid in set(existing) - set(wanted):
        if not is_ours(existing[eid]):  # double check – never delete a foreign event
            continue
        r = s.delete(f"{base}/events/{eid}", params={"sendUpdates": "none"}, timeout=60)
        if r.status_code in (404, 410):
            continue  # already gone
        r.raise_for_status()
        deleted += 1
    print(f"✓ Calendar sync: {len(wanted)} events – {created} new, {changed} changed, {deleted} deleted"
          + (f", {skipped} skipped" if skipped else ""))


if __name__ == "__main__":
    main()
