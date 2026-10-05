"""Fetch stats (runs daily around 9:00 AM ET via GitHub Actions) and append them to automation/stats/*.csv.

media.csv   – per published post: views, reach, likes, comments, saves, shares
account.csv – followers and number of posts
Without IG_TOKEN / IG_USER_ID: prints a note and exits cleanly.
"""
import csv, os, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / "automation" / "stats"
API = "https://graph.instagram.com/v23.0"
METRICS = ["views", "reach", "likes", "comments", "saved", "shares", "total_interactions"]
today = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")

if not os.environ.get("IG_TOKEN") or not os.environ.get("IG_USER_ID"):
    print("Stats: IG_TOKEN / IG_USER_ID missing – nothing to fetch (see SETUP.md).")
    sys.exit(0)

import requests

TOKEN, USER = os.environ["IG_TOKEN"], os.environ["IG_USER_ID"]


def get(path, **params):
    r = requests.get(f"{API}/{path}", params={**params, "access_token": TOKEN}, timeout=60)
    if not r.ok:  # show Meta's reason (e.g. invalid token, wrong account ID) instead of a bare "400 Bad Request"
        try:
            message = r.json().get("error", {}).get("message", r.text)
        except ValueError:
            message = r.text
        raise requests.HTTPError(f"{r.status_code} {message[:200]}", response=r)
    return r.json()


def insights(mid):
    values = {}
    try:  # all at once; if a metric is not allowed for this type, one by one
        data = get(f"{mid}/insights", metric=",".join(METRICS))["data"]
    except requests.HTTPError:
        data = []
        for m in METRICS:
            try:
                data += get(f"{mid}/insights", metric=m)["data"]
            except requests.HTTPError:
                pass
    for d in data:
        values[d["name"]] = d["values"][0]["value"] if d.get("values") else d.get("total_value", {}).get("value")
    return values


def append(file, rows, fields):
    file.parent.mkdir(parents=True, exist_ok=True)
    new = not file.exists()
    with file.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if new:
            w.writeheader()
        w.writerows(rows)


if (FOLDER / "account.csv").exists() and f"\n{today}," in (FOLDER / "account.csv").read_text():
    print(f"Stats for {today} already exist.")
    raise SystemExit(0)

account = get(USER, fields="followers_count,follows_count,media_count")
append(FOLDER / "account.csv", [{"date": today, **{k: account.get(k) for k in ("followers_count", "follows_count", "media_count")}}],
       ["date", "followers_count", "follows_count", "media_count"])

rows = []
for m in get(f"{USER}/media", fields="id,caption,media_type,media_product_type,timestamp,permalink", limit=50).get("data", []):
    rows.append({"date": today, "id": m["id"], "type": m.get("media_product_type") or m.get("media_type"),
                 "posted": m["timestamp"][:10], "link": m.get("permalink"),
                 "first_line": (m.get("caption") or "").split("\n")[0][:60], **insights(m["id"])})
append(FOLDER / "media.csv", rows, ["date", "id", "type", "posted", "link", "first_line", *METRICS])
print(f"✓ {len(rows)} posts, {account.get('followers_count')} followers")
