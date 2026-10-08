"""Alle verfügbaren Instagram-Insights abholen → automatik/statistik/insights_<datum>.json

Holt: Konto-Kennzahlen (30-Tage-Blöcke, so weit Instagram zurückliefert), Zielgruppe (Alter, Geschlecht,
Städte, Länder – Follower, erreichte und interagierende Konten), aktive Zeiten der Follower,
alle Beiträge mit allen erlaubten Kennzahlen und die Kommentartexte (ohne Nutzernamen, das Repo ist öffentlich).
Nicht erlaubte Metriken werden übersprungen und unter "_fehlt" vermerkt.
"""
import json, os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

WURZEL = Path(__file__).resolve().parent.parent
API = "https://graph.instagram.com/v23.0"
TOKEN, USER = os.environ["IG_TOKEN"], os.environ["IG_USER_ID"]
heute = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%d")
fehlt = []

MEDIA_METRIKEN = ["views", "reach", "likes", "comments", "saved", "shares", "total_interactions",
                  "ig_reels_avg_watch_time", "ig_reels_video_view_total_time", "reels_skip_rate",
                  "profile_visits", "profile_activity", "follows", "navigation", "replies"]
KONTO_METRIKEN = ["reach", "views", "accounts_engaged", "total_interactions", "likes", "comments", "shares",
                  "saves", "replies", "profile_links_taps", "follows_and_unfollows"]
AUFSCHLUESSELUNG = {"reach": "follow_type", "views": "follow_type", "follows_and_unfollows": "follow_type",
                    "profile_links_taps": "contact_button_type"}


def get(pfad, **params):
    r = requests.get(f"{API}/{pfad}", params={**params, "access_token": TOKEN}, timeout=60)
    if not r.ok:
        raise RuntimeError(f"{r.status_code} {r.json().get('error', {}).get('message', r.text)[:200]}")
    return r.json()


def wert(d):
    if d.get("values"):
        return d["values"][0]["value"]
    tv = d.get("total_value") or {}
    if tv.get("breakdowns"):
        return {"gesamt": tv.get("value"),
                "aufgeteilt": {"/".join(e.get("dimension_values", [])): e.get("value")
                               for b in tv["breakdowns"] for e in b.get("results", [])}}
    return tv.get("value")


def media_insights(m):
    werte = {}
    for metrik in MEDIA_METRIKEN:
        try:
            for d in get(f"{m['id']}/insights", metric=metrik)["data"]:
                werte[d["name"]] = wert(d)
        except (RuntimeError, KeyError, TypeError):
            werte.setdefault("_fehlt", []).append(metrik)
    # Reichweite nach Follower/Nicht-Follower (für den Testmonat); liefert Instagram das nicht, nur vermerken
    try:
        for d in get(f"{m['id']}/insights", metric="reach", breakdown="follow_type", metric_type="total_value")["data"]:
            werte["reach_aufgeteilt"] = wert(d)
    except (RuntimeError, KeyError, TypeError):
        werte.setdefault("_fehlt", []).append("reach_aufgeteilt")
    try:
        werte["kommentare_text"] = [
            {"text": c.get("text"), "zeit": c.get("timestamp"), "von_mir": c.get("username") == konto.get("username"),
             "likes": c.get("like_count"), "antworten": len((c.get("replies") or {}).get("data", []))}
            for c in get(f"{m['id']}/comments", fields="text,timestamp,username,like_count,replies{id}", limit=100).get("data", [])]
    except RuntimeError:
        pass
    return werte


konto = get(USER, fields="username,name,biography,website,followers_count,follows_count,media_count")
ergebnis = {"abgerufen": heute, "konto": {k: konto.get(k) for k in
            ("username", "name", "biography", "website", "followers_count", "follows_count", "media_count")}}

# Konto-Kennzahlen in 30-Tage-Blöcken rückwärts bis zum Kontostart (Mai 2025)
KONTOSTART = datetime(2025, 5, 1, tzinfo=timezone.utc)
bloecke = []
ende = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
while ende > KONTOSTART:
    start = max(ende - timedelta(days=30), KONTOSTART)
    block = {"von": start.strftime("%Y-%m-%d"), "bis": ende.strftime("%Y-%m-%d")}
    for metrik in KONTO_METRIKEN:
        params = dict(metric=metrik, period="day", metric_type="total_value",
                      since=int(start.timestamp()), until=int(ende.timestamp()))
        if metrik in AUFSCHLUESSELUNG:
            params["breakdown"] = AUFSCHLUESSELUNG[metrik]
        try:
            for d in get(f"{USER}/insights", **params)["data"]:
                block[d["name"]] = wert(d)
        except (RuntimeError, KeyError, TypeError) as e:
            block.setdefault("_fehlt", {})[metrik] = str(e)[:120]
    bloecke.append(block)
    if len(block.get("_fehlt", {})) == len(KONTO_METRIKEN):
        break
    ende = start
ergebnis["konto_verlauf"] = bloecke

# Tageswerte der letzten 30 Tage (für Wochentags-Muster)
try:
    ergebnis["tageswerte_reichweite"] = {
        v["end_time"][:10]: v["value"] for d in get(f"{USER}/insights", metric="reach", period="day",
            since=int((datetime.now(timezone.utc) - timedelta(days=29)).timestamp()),
            until=int(datetime.now(timezone.utc).timestamp()))["data"] for v in d.get("values", [])}
except RuntimeError as e:
    fehlt.append(f"tageswerte_reichweite: {e}")

# Zielgruppe
zielgruppe = {}
for metrik in ("follower_demographics", "engaged_audience_demographics", "reached_audience_demographics"):
    for zeitraum in ("this_month", "this_week"):
        for dim in ("age", "gender", "city", "country"):
            try:
                d = get(f"{USER}/insights", metric=metrik, period="lifetime", timeframe=zeitraum,
                        breakdown=dim, metric_type="total_value")["data"][0]
                zielgruppe.setdefault(metrik, {}).setdefault(zeitraum, {})[dim] = wert(d).get("aufgeteilt") if isinstance(wert(d), dict) else wert(d)
            except (RuntimeError, IndexError, AttributeError) as e:
                fehlt.append(f"{metrik}/{zeitraum}/{dim}: {e}")
        if metrik == "follower_demographics":
            break  # Follower-Zielgruppe gibt es nur einmal
ergebnis["zielgruppe"] = zielgruppe

# Aktive Zeiten der Follower (Stunde → Anzahl online, je Tag)
try:
    ergebnis["online_follower"] = {v["end_time"][:10]: v["value"] for d in get(
        f"{USER}/insights", metric="online_followers", period="lifetime")["data"] for v in d.get("values", [])}
except RuntimeError as e:
    fehlt.append(f"online_followers: {e}")

# Alle Beiträge
beitraege, weiter = [], None
felder = "id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count"
seite = get(f"{USER}/media", fields=felder, limit=50)
while True:
    beitraege += seite.get("data", [])
    weiter = seite.get("paging", {}).get("next")
    if not weiter:
        break
    seite = requests.get(weiter, timeout=60).json()
ergebnis["beitraege"] = [{**{k: m.get(k) for k in ("id", "media_product_type", "media_type", "timestamp", "permalink",
                                                   "like_count", "comments_count", "caption")},
                          **media_insights(m)} for m in beitraege]

# Aktuelle Storys (nur 24 h abrufbar)
try:
    ergebnis["storys_aktiv"] = [{"id": s["id"], "zeit": s.get("timestamp"), **media_insights(s)}
                                for s in get(f"{USER}/stories", fields="id,timestamp").get("data", [])]
except RuntimeError as e:
    fehlt.append(f"stories: {e}")

ergebnis["_fehlt"] = fehlt
ziel = WURZEL / "automatik" / "statistik" / f"insights_{heute}.json"
ziel.parent.mkdir(parents=True, exist_ok=True)
ziel.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=1) + "\n")
print(f"✓ {len(ergebnis['beitraege'])} Beiträge, {len(bloecke)} Monatsblöcke, Zielgruppe: {list(zielgruppe)}")
print(f"  nicht verfügbar: {len(fehlt)} ({'; '.join(fehlt[:5])})")
