"""Fetch every available Instagram insight → automation/stats/insights_<date>.json

Fetches: account metrics (30-day blocks, as far back as Instagram returns them), audience (age, gender,
cities, countries – followers, reached and engaged accounts), active hours of followers,
all posts with every allowed metric and the comment texts (without usernames, the repo is public).
Metrics that are not allowed are skipped and listed under "_missing".
Without IG_TOKEN / IG_USER_ID: prints a note and exits cleanly.
"""
import json, os, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
API = "https://graph.instagram.com/v23.0"
today = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
missing = []

if not os.environ.get("IG_TOKEN") or not os.environ.get("IG_USER_ID"):
    print("Insights: IG_TOKEN / IG_USER_ID missing – nothing to fetch (see SETUP.md).")
    sys.exit(0)

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ig_account

TOKEN = os.environ["IG_TOKEN"]
USER, _ = ig_account.resolve(TOKEN)

MEDIA_METRICS = ["views", "reach", "likes", "comments", "saved", "shares", "total_interactions",
                 "ig_reels_avg_watch_time", "ig_reels_video_view_total_time", "reels_skip_rate",
                 "profile_visits", "profile_activity", "follows", "navigation", "replies"]
ACCOUNT_METRICS = ["reach", "views", "accounts_engaged", "total_interactions", "likes", "comments", "shares",
                   "saves", "replies", "profile_links_taps", "follows_and_unfollows"]
BREAKDOWN = {"reach": "follow_type", "views": "follow_type", "follows_and_unfollows": "follow_type",
             "profile_links_taps": "contact_button_type"}
# @maehrtax was created in October 2026 – nothing to fetch before that
ACCOUNT_START = datetime(2026, 10, 1, tzinfo=timezone.utc)


def get(path, **params):
    r = requests.get(f"{API}/{path}", params={**params, "access_token": TOKEN}, timeout=60)
    if not r.ok:
        try:
            message = r.json().get("error", {}).get("message", r.text)
        except ValueError:
            message = r.text
        raise RuntimeError(f"{r.status_code} {message[:200]}")
    return r.json()


def value(d):
    if d.get("values"):
        return d["values"][0]["value"]
    tv = d.get("total_value") or {}
    if tv.get("breakdowns"):
        return {"total": tv.get("value"),
                "breakdown": {"/".join(e.get("dimension_values", [])): e.get("value")
                              for b in tv["breakdowns"] for e in b.get("results", [])}}
    return tv.get("value")


def media_insights(m):
    values = {}
    for metric in MEDIA_METRICS:
        try:
            for d in get(f"{m['id']}/insights", metric=metric)["data"]:
                values[d["name"]] = value(d)
        except (RuntimeError, KeyError, TypeError):
            values.setdefault("_missing", []).append(metric)
    try:
        values["comment_texts"] = [
            {"text": c.get("text"), "time": c.get("timestamp"), "by_me": c.get("username") == account.get("username"),
             "likes": c.get("like_count"), "replies": len((c.get("replies") or {}).get("data", []))}
            for c in get(f"{m['id']}/comments", fields="text,timestamp,username,like_count,replies{id}", limit=100).get("data", [])]
    except RuntimeError:
        pass
    return values


account = get(USER, fields="username,name,biography,website,followers_count,follows_count,media_count")
result = {"fetched": today, "account": {k: account.get(k) for k in
          ("username", "name", "biography", "website", "followers_count", "follows_count", "media_count")}}

# Account metrics in 30-day blocks backwards to the account start
blocks = []
end = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
while end > ACCOUNT_START:
    start = max(end - timedelta(days=30), ACCOUNT_START)
    block = {"from": start.strftime("%Y-%m-%d"), "to": end.strftime("%Y-%m-%d")}
    for metric in ACCOUNT_METRICS:
        params = dict(metric=metric, period="day", metric_type="total_value",
                      since=int(start.timestamp()), until=int(end.timestamp()))
        if metric in BREAKDOWN:
            params["breakdown"] = BREAKDOWN[metric]
        try:
            for d in get(f"{USER}/insights", **params)["data"]:
                block[d["name"]] = value(d)
        except (RuntimeError, KeyError, TypeError) as e:
            block.setdefault("_missing", {})[metric] = str(e)[:120]
    blocks.append(block)
    if len(block.get("_missing", {})) == len(ACCOUNT_METRICS):
        break
    end = start
result["account_history"] = blocks

# Daily reach of the last 30 days (for weekday patterns)
try:
    result["daily_reach"] = {
        v["end_time"][:10]: v["value"] for d in get(f"{USER}/insights", metric="reach", period="day",
            since=int((datetime.now(timezone.utc) - timedelta(days=29)).timestamp()),
            until=int(datetime.now(timezone.utc).timestamp()))["data"] for v in d.get("values", [])}
except RuntimeError as e:
    missing.append(f"daily_reach: {e}")

# Audience
audience = {}
for metric in ("follower_demographics", "engaged_audience_demographics", "reached_audience_demographics"):
    for timeframe in ("this_month", "this_week"):
        for dim in ("age", "gender", "city", "country"):
            try:
                d = get(f"{USER}/insights", metric=metric, period="lifetime", timeframe=timeframe,
                        breakdown=dim, metric_type="total_value")["data"][0]
                audience.setdefault(metric, {}).setdefault(timeframe, {})[dim] = value(d).get("breakdown") if isinstance(value(d), dict) else value(d)
            except (RuntimeError, IndexError, AttributeError) as e:
                missing.append(f"{metric}/{timeframe}/{dim}: {e}")
        if metric == "follower_demographics":
            break  # follower audience exists only once
result["audience"] = audience

# Active hours of followers (hour → number online, per day; Instagram reports Pacific time hours)
try:
    result["online_followers"] = {v["end_time"][:10]: v["value"] for d in get(
        f"{USER}/insights", metric="online_followers", period="lifetime")["data"] for v in d.get("values", [])}
except RuntimeError as e:
    missing.append(f"online_followers: {e}")

# All posts
media, page = [], get(f"{USER}/media", fields="id,caption,media_type,media_product_type,timestamp,permalink,"
                                               "like_count,comments_count", limit=50)
while True:
    media += page.get("data", [])
    nxt = page.get("paging", {}).get("next")
    if not nxt:
        break
    page = requests.get(nxt, timeout=60).json()
result["media"] = [{**{k: m.get(k) for k in ("id", "media_product_type", "media_type", "timestamp", "permalink",
                                             "like_count", "comments_count", "caption")},
                    **media_insights(m)} for m in media]

# Current stories (only available for 24 h)
try:
    result["active_stories"] = [{"id": s["id"], "time": s.get("timestamp"), **media_insights(s)}
                                for s in get(f"{USER}/stories", fields="id,timestamp").get("data", [])]
except RuntimeError as e:
    missing.append(f"stories: {e}")

result["_missing"] = missing
target = ROOT / "automation" / "stats" / f"insights_{today}.json"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n")
print(f"✓ {len(result['media'])} posts, {len(blocks)} monthly blocks, audience: {list(audience)}")
print(f"  not available: {len(missing)} ({'; '.join(missing[:5])})")
