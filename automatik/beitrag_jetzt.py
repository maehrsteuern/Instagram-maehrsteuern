"""Schnellabruf: aktuelle Kennzahlen einzelner Beiträge – nur Ausgabe im Protokoll, schreibt KEINE Statistikdateien
(die Tageswerte für Tagesbericht/Wochenbericht bleiben unberührt).

  python automatik/beitrag_jetzt.py 18154273729518650 [weitere media_ids …]
  python automatik/beitrag_jetzt.py neueste 3        – die 3 neuesten Beiträge
Workflow: „Instagram-Statistik“ manuell starten mit Eingabe „beitrag“ (media_id oder „neueste 3“).
"""
import os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

API = "https://graph.instagram.com/v23.0"
TOKEN, USER = os.environ["IG_TOKEN"], os.environ["IG_USER_ID"]
METRIKEN = ["views", "reach", "likes", "comments", "saved", "shares", "total_interactions",
            "ig_reels_avg_watch_time", "reels_skip_rate", "profile_visits", "follows"]


def get(pfad, **params):
    r = requests.get(f"{API}/{pfad}", params={**params, "access_token": TOKEN}, timeout=60)
    if not r.ok:
        raise RuntimeError(f"{r.status_code} {r.json().get('error', {}).get('message', r.text)[:200]}")
    return r.json()


args = sys.argv[1:]
if args[:1] == ["neueste"]:
    n = int(args[1]) if len(args) > 1 else 3
    ids = [m["id"] for m in get(f"{USER}/media", fields="id", limit=n)["data"]]
else:
    ids = args
jetzt = datetime.now(ZoneInfo("Europe/Berlin"))
konto = get(USER, fields="followers_count")
print(f"Abruf {jetzt:%d.%m. %H:%M} · Follower {konto.get('followers_count')}")
for mid in ids:
    m = get(mid, fields="timestamp,permalink,media_product_type,caption")
    seit = jetzt - datetime.fromisoformat(m["timestamp"].replace("+0000", "+00:00")).astimezone(ZoneInfo("Europe/Berlin"))
    werte = {}
    for metrik in METRIKEN:
        try:
            for d in get(f"{mid}/insights", metric=metrik)["data"]:
                werte[d["name"]] = d["values"][0]["value"] if d.get("values") else (d.get("total_value") or {}).get("value")
        except (RuntimeError, KeyError, TypeError, IndexError):
            werte[metrik] = "–"
    std = seit.total_seconds() / 3600
    print(f"\n{m.get('media_product_type')} {m['permalink']} · online seit {std:.1f} h")
    print("  „" + (m.get("caption") or "").split("\n")[0][:70] + "“")
    for k, v in werte.items():
        if k == "ig_reels_avg_watch_time" and isinstance(v, (int, float)):
            v = f"{v / 1000:.1f} s"
        print(f"  {k:<24} {v}")
