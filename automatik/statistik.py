"""Statistik abholen (läuft montags per GitHub Actions) und an automatik/statistik/*.csv anhängen.

beitraege.csv – je veröffentlichtem Beitrag: Aufrufe, Reichweite, Likes, Kommentare, Speicherungen, Geteilt
konto.csv     – Follower und Anzahl Beiträge
"""
import csv, json, os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

WURZEL = Path(__file__).resolve().parent.parent
ORDNER = WURZEL / "automatik" / "statistik"
API = "https://graph.instagram.com/v23.0"
TOKEN, USER = os.environ["IG_TOKEN"], os.environ["IG_USER_ID"]
METRIKEN = ["views", "reach", "likes", "comments", "saved", "shares", "total_interactions"]
heute = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%d")


def get(pfad, **params):
    r = requests.get(f"{API}/{pfad}", params={**params, "access_token": TOKEN}, timeout=60)
    r.raise_for_status()
    return r.json()


def insights(mid):
    werte = {}
    try:  # alle auf einmal; falls eine Metrik für den Typ nicht erlaubt ist, einzeln
        daten = get(f"{mid}/insights", metric=",".join(METRIKEN))["data"]
    except requests.HTTPError:
        daten = []
        for m in METRIKEN:
            try:
                daten += get(f"{mid}/insights", metric=m)["data"]
            except requests.HTTPError:
                pass
    for d in daten:
        werte[d["name"]] = d["values"][0]["value"] if d.get("values") else d.get("total_value", {}).get("value")
    return werte


def anhaengen(datei, zeilen, felder):
    datei.parent.mkdir(parents=True, exist_ok=True)
    neu = not datei.exists()
    with datei.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=felder)
        if neu:
            w.writeheader()
        w.writerows(zeilen)


if (ORDNER / "konto.csv").exists() and f"\n{heute}," in (ORDNER / "konto.csv").read_text():
    raise SystemExit(f"Statistik für {heute} ist schon da.")

konto = get(USER, fields="followers_count,follows_count,media_count")
anhaengen(ORDNER / "konto.csv", [{"datum": heute, **{k: konto.get(k) for k in ("followers_count", "follows_count", "media_count")}}],
          ["datum", "followers_count", "follows_count", "media_count"])

zeilen = []
for m in get(f"{USER}/media", fields="id,caption,media_type,media_product_type,timestamp,permalink", limit=50).get("data", []):
    zeilen.append({"datum": heute, "id": m["id"], "typ": m.get("media_product_type") or m.get("media_type"),
                   "gepostet": m["timestamp"][:10], "link": m.get("permalink"),
                   "anfang": (m.get("caption") or "").split("\n")[0][:60], **insights(m["id"])})
anhaengen(ORDNER / "beitraege.csv", zeilen, ["datum", "id", "typ", "gepostet", "link", "anfang", *METRIKEN])
print(f"✓ {len(zeilen)} Beiträge, {konto.get('followers_count')} Follower")
