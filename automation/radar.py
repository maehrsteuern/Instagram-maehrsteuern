"""Radar (runs daily around 7:00 AM ET via GitHub Actions): find fresh posts in the niche and write them as a
~15-minute work list for doing by hand into a GitHub issue.

  1. Comment – 5–8 fresh posts from watched accounts (and hashtags, once unlocked) with a comment suggestion
     from Claude. Loris comments by hand in the app and ticks the box.
  2. DM drafts – for accounts where Loris has commented at least 2× (ticked), a personal first message.
     Loris sends it by hand (or not at all).
  3. Collab – once a week (Mon) a suggestion for a joint post with a fitting account.

Nothing is ever commented, followed or sent automatically. Ticked boxes in the previous issue are counted on the
next run (automation/interaction/contacts.json) – that is how the radar knows who is already "warm".

Only radar.accounts in automation/interaction.json is read (verified US accounts). radar.candidates_to_verify is a
to-do list for Cowork/Loris and is never queried. With an empty account list the radar still works (hashtags,
upkeep suggestions) and skips everything else with a clear message.

Environment: FB_TOKEN + FB_IG_USER_ID (access via Facebook login, needed for other profiles, see SETUP.md),
ANTHROPIC_API_KEY (optional, for suggestions), GH_TOKEN, GITHUB_REPOSITORY.
  python automation/radar.py            – normal run
  python automation/radar.py --dry-run  – only query and print the issue text, save nothing
"""
import json, os, re, subprocess, sys, time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai

ROOT = Path(__file__).resolve().parent.parent
SETTINGS_FILE = ROOT / "automation" / "interaction.json"
SETTINGS = json.loads(SETTINGS_FILE.read_text())["radar"]
FOLDER = ROOT / "automation" / "interaction"
CONTACTS, SEEN = FOLDER / "contacts.json", FOLDER / "seen.json"
UPKEEP, COMMENTS = FOLDER / "upkeep.json", FOLDER / "comments.json"
KINDS = {}  # account → kind from the suggestion line ("· CPA firm, …")

# keyword → kind (allowed: cpa_firm | creator | tax_team | software | education); order = priority
KIND_WORDS = (("cpa_firm", "cpa_firm"), ("cpa", "cpa_firm"), ("accounting firm", "cpa_firm"), ("firm", "cpa_firm"),
              ("enrolled agent", "cpa_firm"), ("preparer", "cpa_firm"), ("tax_team", "tax_team"),
              ("tax team", "tax_team"), ("in-house", "tax_team"), ("corporate", "tax_team"),
              ("software", "software"), ("tool", "software"), ("app", "software"), ("saas", "software"),
              ("creator", "creator"), ("influencer", "creator"), ("education", "education"),
              ("student", "education"), ("exam", "education"), ("course", "education"), ("academy", "education"),
              ("university", "education"), ("school", "education"), ("association", "education"))
KINDS_ALLOWED = {"cpa_firm", "creator", "tax_team", "software", "education"}
BROKEN = {}  # account → error text, only for permanent errors (renamed, private, deleted …)
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/maehrtax---instagram")
API = "https://graph.facebook.com/v23.0"
LABEL = "radar"
ZONE = ZoneInfo("America/New_York")
NOW = datetime.now(ZONE)
WEEKDAY = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DRY_RUN = "--dry-run" in sys.argv
FIELDS = "id,caption,permalink,timestamp,like_count,comments_count,media_product_type"
SKIP = "skip"


def kind_from_text(text):
    """Kind from "· about 2,300 followers · CPA firm, topic …": first the first word of the last section, otherwise
    keywords in the whole section ("Tax preparer, tips …" → cpa_firm). Nothing recognized → "" (note in the issue)."""
    section = text.split("·")[-1].strip().lower()
    first = (section.split(",")[0].split() or [""])[0]
    for t in (first, section):
        for word, kind in KIND_WORDS:
            if word in t:
                return kind
    return ""


def accounts():
    return SETTINGS.get("accounts") or []


def account_name(a):
    return a["name"] if isinstance(a, dict) else a


# ---------- helpers ----------

def gh(*args, stdin=None):
    return subprocess.run(["gh", *args, "--repo", REPO], input=stdin, check=True, capture_output=True, text=True).stdout.strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def load(file, empty):
    return json.loads(file.read_text()) if file.exists() else empty


class Throttled(RuntimeError):
    """Meta throttles (HTTP 429 or error code 4/17/32/613/80002) – even after waiting."""


class TokenInvalid(RuntimeError):
    """FB_TOKEN expired or invalid (code 190/102/463/467) – a problem of the key, never of the queried account."""


# Meta error codes: throttling or a short hiccup – not a sign that an account is gone
THROTTLE_CODES = {4, 17, 32, 613, 80001, 80002}
HICCUP_CODES = {1, 2}
TOKEN_CODES = {102, 190, 463, 467}
WAIT = (30, 90, 270)  # seconds between attempts (backoff)


def api(path, **params):
    """GET on the Graph API. Throttling (429/code 4, 17, 32, 613, 8000x) and 5xx/code 1, 2 are retried with backoff;
    if Meta keeps throttling, Throttled is raised – the run then stops querying."""
    import requests
    for attempt in range(len(WAIT) + 1):
        try:
            r = requests.get(f"{API}/{path}", params={**params, "access_token": os.environ["FB_TOKEN"]}, timeout=60)
        except requests.RequestException as e:
            if attempt == len(WAIT):
                raise RuntimeError(f"Connection: {type(e).__name__}") from None  # without the URL – it contains the key
            time.sleep(WAIT[attempt])
            continue
        if r.ok:
            return r.json()
        try:
            err = r.json().get("error", {}) if r.headers.get("content-type", "").startswith(("application/json", "text/javascript")) else {}
        except ValueError:
            err = {}
        code = err.get("code") or r.status_code
        throttled = r.status_code == 429 or code in THROTTLE_CODES
        if not (throttled or r.status_code >= 500 or code in HICCUP_CODES) or attempt == len(WAIT):
            message = f"{code}: {err.get('message', r.text[:200])}"
            if code in TOKEN_CODES or err.get("type") == "OAuthException" and err.get("error_subcode") in (463, 467):
                raise TokenInvalid(message)
            raise Throttled(message) if throttled else RuntimeError(message)
        wait = WAIT[attempt]
        if (after := r.headers.get("Retry-After", "")).isdigit():
            wait = max(wait, min(int(after), 600))
        print(f"Radar: Meta {'throttles' if throttled else 'hiccups'} ({code}) – waiting {wait} s")
        time.sleep(wait)


def temporary(message):
    """Error text of a short hiccup (not: account gone)? Only permanent errors lead to 🧹 suggestions."""
    code = message.split(":", 1)[0].strip()
    return code.isdigit() and (int(code) in THROTTLE_CODES | HICCUP_CODES or int(code) == 429 or int(code) >= 500) \
        or message.startswith("Connection")


def parse_time(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z").astimezone(ZONE)


def short(text, n=220):
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " …"


def ago(t):
    h = (NOW - t).total_seconds() / 3600
    return f"{int(h)} h ago" if h < 48 else f"{int(h // 24)} days ago"


def dump_settings(data):
    """JSON like the hand-maintained file: one account per line, short lists on one line."""
    def fmt(v, indent):
        pad, inner = " " * indent, " " * (indent + 2)
        if isinstance(v, dict):
            if v and all(not isinstance(x, (dict, list)) for x in v.values()) and indent >= 6:
                return "{" + ", ".join(f"{json.dumps(k)}: {json.dumps(x, ensure_ascii=False)}" for k, x in v.items()) + "}"
            return "{\n" + ",\n".join(f"{inner}{json.dumps(k)}: {fmt(x, indent + 2)}" for k, x in v.items()) + f"\n{pad}}}"
        if isinstance(v, list):
            if not v:
                return "[]"
            if all(not isinstance(x, (dict, list)) for x in v):
                return "[" + ", ".join(json.dumps(x, ensure_ascii=False) for x in v) + "]"
            return "[\n" + ",\n".join(f"{inner}{fmt(x, indent + 2)}" for x in v) + f"\n{pad}]"
        return json.dumps(v, ensure_ascii=False)
    return fmt(data, 0) + "\n"


# ---------- count ticked boxes from last time ----------

def count_ticks(contacts):
    """Read open radar issues, transfer ticked boxes into contacts.json.
    Returns (issue numbers, ticked 🧹 to remove, ticked ➕ to add)."""
    try:
        found = json.loads(gh("issue", "list", "--label", LABEL, "--state", "open", "--json", "number,body,comments"))
    except (subprocess.CalledProcessError, OSError):
        return [], [], []
    remove, add = [], []
    owner = REPO.split("/")[0]
    for issue in found:
        # upkeep suggestions are in the issue body (Mondays) or in Loris' own comments (e.g. account search
        # via Chrome) – ticks in other people's comments do not count
        texts = [issue["body"]] + [c["body"] for c in issue.get("comments", [])
                                   if c.get("author", {}).get("login") == owner]
        for text in texts:
            remove += re.findall(r"^- \[[xX]\] 🧹[^@\n]*@([\w.]+)", text, re.M)
            for user, rest in re.findall(r"^- \[[xX]\] ➕[^@\n]*@([\w.]+)([^\n]*)", text, re.M):
                add.append(user)
                KINDS[user] = kind_from_text(rest)
        for kind, user in re.findall(r"^- \[[xX]\] (💬|✉️|🤝)[^@\n]*@([\w.]+)", issue["body"], re.M):
            k = contacts.setdefault(user, {"comments": 0})
            if kind == "💬":
                k["comments"] = k.get("comments", 0) + 1
                k["last_comment"] = NOW.strftime("%Y-%m-%d")
            elif kind == "✉️":
                k["dm"] = NOW.strftime("%Y-%m-%d")
            else:
                k["collab"] = NOW.strftime("%Y-%m-%d")
    return [i["number"] for i in found], remove, add


# ---------- radar upkeep: only what Loris ticked is changed ----------

def apply_upkeep(remove, add):
    """Transfer ticked upkeep suggestions into interaction.json (the tick is the decision)."""
    data = json.loads(SETTINGS_FILE.read_text())
    kept = [k for k in data["radar"].get("accounts", []) if account_name(k) not in remove]
    present = {account_name(k) for k in kept}
    kept += [{"name": n, "kind": KINDS.get(n, "")} for n in dict.fromkeys(add) if n not in present]
    data["radar"]["accounts"] = kept
    SETTINGS_FILE.write_text(dump_settings(data))
    SETTINGS["accounts"] = kept
    print(f"✓ Radar upkeep applied: −{len(remove)} / +{len(add)}")


def upkeep_suggestions(profiles):
    """Once a week (collab_day): quiet or broken accounts to remove, commenters with a business/creator
    account to add. A suggestion comes back at most every 60 days."""
    if WEEKDAY[NOW.weekday()] != SETTINGS["collab_day"]:
        return [], []
    upkeep = load(UPKEEP, {"suggested": {}})
    fresh = (NOW - timedelta(days=60)).strftime("%Y-%m-%d")
    due = lambda n: upkeep["suggested"].get(n, "") < fresh
    cutoff = NOW - timedelta(days=30)
    drop = [(n, f"not retrievable ({short(f, 80)})") for n, f in BROKEN.items()]
    for p in profiles:
        media = p.get("media", {}).get("data", [])
        if not media:
            drop.append((p["username"], "never posted"))
        elif parse_time(media[0]["timestamp"]) < cutoff:
            drop.append((p["username"], f"last post {ago(parse_time(media[0]['timestamp']))}"))
    drop = [(n, g) for n, g in drop if due(n)]
    present = {account_name(k) for k in accounts()}
    commenters = sorted({v.get("from") for v in load(COMMENTS, {}).get("comments", {}).values()
                         if v.get("from") and v.get("date", "") >= cutoff.strftime("%Y-%m-%d")} - present)
    add = []
    for name in [n for n in commenters if due(n)][:10]:
        try:  # only works for business/creator accounts – exactly the ones the radar can read
            d = api(os.environ["FB_IG_USER_ID"], fields=f"business_discovery.username({name}){{followers_count,media_count}}")
        except Throttled:
            break
        except RuntimeError:
            continue
        b = d["business_discovery"]
        if b.get("media_count"):
            add.append((name, f"commented on your posts · {b.get('followers_count') or 0:,} followers · {b['media_count']} posts"))
    for n, _ in drop + add:
        upkeep["suggested"][n] = NOW.strftime("%Y-%m-%d")
    if not DRY_RUN:
        UPKEEP.write_text(json.dumps(upkeep, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    return drop, add


# ---------- fetch data ----------

def query_accounts(notes):
    profiles = []
    items = accounts()
    for nr, item in enumerate(items):
        name = account_name(item)
        try:
            d = api(os.environ["FB_IG_USER_ID"],
                    fields=f"business_discovery.username({name}){{username,name,followers_count,media_count,"
                           f"media.limit(6){{{FIELDS}}}}}")["business_discovery"]
        except TokenInvalid:
            raise  # main() stops the whole run – no account may be marked as broken because of the key
        except Throttled as e:
            # querying on only makes it worse; the remaining accounts do NOT count as broken
            notes.append(f"Meta throttles ({e}) – {len(items) - nr} accounts not queried today, again tomorrow")
            break
        except RuntimeError as e:
            notes.append(f"@{name}: {e}")
            if not temporary(str(e)):
                BROKEN[name] = str(e)
            continue
        d["kind"] = item.get("kind", "") if isinstance(item, dict) else ""
        profiles.append(d)
        time.sleep(1)  # gently: ~50 queries in a row not within one second
    return profiles


def query_hashtags(notes):
    """Needs the Meta feature "Instagram Public Content Access". Without it: one note, nothing else."""
    posts, ids = [], load(FOLDER / "hashtag_ids.json", {})
    for tag in SETTINGS.get("hashtags", []):
        try:
            if tag not in ids:
                ids[tag] = api("ig_hashtag_search", user_id=os.environ["FB_IG_USER_ID"], q=tag)["data"][0]["id"]
            for m in api(f"{ids[tag]}/recent_media", user_id=os.environ["FB_IG_USER_ID"], fields=FIELDS, limit=30)["data"]:
                m["hashtag"] = tag
                posts.append(m)
        except TokenInvalid:
            raise
        except Throttled as e:
            notes.append(f"Hashtags: Meta throttles ({e}) – again tomorrow")
            break
        except (RuntimeError, IndexError, KeyError) as e:
            notes.append(f"Hashtags not available yet ({e}) – how to unlock: strategy/12_interaction.md")
            break
    if ids and not DRY_RUN:
        (FOLDER / "hashtag_ids.json").write_text(json.dumps(ids, indent=1) + "\n")
    return posts


# ---------- select ----------

def score(m, contact):
    age = (NOW - parse_time(m["timestamp"])).total_seconds() / 3600
    text = f" {(m.get('caption') or '').lower()} "
    hits = [w for w in SETTINGS.get("keywords", []) if w in text]
    p = 10 * max(0.0, 1 - age / SETTINGS["max_age_hours"])  # fresh = early = visible
    p += 4 * len(hits)
    p += min(10, (m.get("comments_count") or 0) * 0.5 + (m.get("like_count") or 0) * 0.05)
    p += 6 if contact and contact.get("comments") and not contact.get("dm") else 0  # keep building the relationship
    return p, [w.strip() for w in hits]


def select(profiles, hashtag_posts, contacts, seen):
    candidates = []
    for p in profiles:
        for m in p.get("media", {}).get("data", []):
            m["account"], m["kind"], m["followers"] = p["username"], p.get("kind", ""), p.get("followers_count")
            candidates.append(m)
    candidates += hashtag_posts
    cutoff = NOW - timedelta(hours=SETTINGS["max_age_hours"])
    rated = []
    for m in candidates:
        if m["id"] in seen or parse_time(m["timestamp"]) < cutoff:
            continue
        p, hits = score(m, contacts.get(m.get("account", "")))
        rated.append((p, hits, m))
    rated.sort(key=lambda x: -x[0])
    chosen, per_account = [], {}
    for p, hits, m in rated:  # at most 2 posts per account, so the list stays broad
        key = m.get("account") or m["id"]
        if per_account.get(key, 0) >= 2:
            continue
        per_account[key] = per_account.get(key, 0) + 1
        m["hits"] = hits
        chosen.append(m)
        if len(chosen) >= SETTINGS["max_posts"]:
            break
    return chosen


def dm_candidates(profiles, contacts):
    out = []
    for p in profiles:
        k = contacts.get(p["username"], {})
        if k.get("comments", 0) >= SETTINGS["comments_before_dm"] and not k.get("dm"):
            last = (p.get("media", {}).get("data") or [{}])[0]
            out.append({"account": p["username"], "name": p.get("name"), "kind": p.get("kind"),
                        "followers": p.get("followers_count"), "comments_by_loris": k["comments"],
                        "last_post": short(last.get("caption"), 500), "link": last.get("permalink")})
    return out[:SETTINGS["max_dm_drafts"]]


def collab_candidate(profiles, contacts):
    if WEEKDAY[NOW.weekday()] != SETTINGS["collab_day"]:
        return None
    low, high = SETTINGS["collab_followers"]
    fitting = []
    for p in profiles:
        k, followers = contacts.get(p["username"], {}), p.get("followers_count") or 0
        if k.get("collab") or not low <= followers <= high:
            continue
        media = p.get("media", {}).get("data", [])
        newest = max((parse_time(m["timestamp"]) for m in media if m.get("timestamp")), default=None)
        if not newest or newest < NOW - timedelta(days=30):
            continue  # nobody to collab with if the account hasn't posted for a month
        rate = sum((m.get("like_count") or 0) + 3 * (m.get("comments_count") or 0) for m in media) / len(media) / followers
        fitting.append((rate + 0.02 * k.get("comments", 0), p))
    if not fitting:
        return None
    p = max(fitting, key=lambda x: x[0])[1]
    return {"account": p["username"], "name": p.get("name"), "kind": p.get("kind"), "followers": p.get("followers_count"),
            "last_posts": [short(m.get("caption"), 300) for m in p.get("media", {}).get("data", [])[:4]]}


# ---------- suggestions ----------

SCHEMA = {
    "type": "object",
    "properties": {
        "comments": {"type": "array", "items": {"type": "object", "properties": {
            "nr": {"type": "integer"}, "text": {"type": "string"}}, "required": ["nr", "text"], "additionalProperties": False}},
        "dms": {"type": "array", "items": {"type": "object", "properties": {
            "account": {"type": "string"}, "text": {"type": "string"}}, "required": ["account", "text"], "additionalProperties": False}},
        "collab": {"type": "object", "properties": {
            "idea": {"type": "string"}, "text": {"type": "string"}}, "required": ["idea", "text"], "additionalProperties": False},
    },
    "required": ["comments", "dms", "collab"],
    "additionalProperties": False,
}

TASK = f"""Write suggestions that Loris uses by hand in the Instagram app. US English.

comments: for EVERY post (nr) one comment, 1–2 sentences, max. 220 characters. It should add real value for the
person and their followers: a professional addition, a practical example from an in-house tax team or a CPA firm,
or an honest follow-up question. A link to spreadsheets/automation is welcome when it fits naturally.
Never give individual tax advice. If the post is too thin or not in English, write exactly "{SKIP}" as text.

dms: for every account in dm_candidates a first direct message (3–5 sentences). Loris has already commented on
their posts several times. Pick up on the last post, one specific compliment, one real question or a small piece
of value (e.g. "I built a little calculator for this – happy to show you if you're curious"). No selling, no
meeting request, no link. It must read like it comes from a colleague.

collab: if collab_candidate is set: idea = one concrete joint post (1–2 sentences, e.g. a collab carousel
"Spreadsheet vs. code", a guest slide, a joint story Q&A), text = the request DM (4–6 sentences, casual, with a
clear suggestion and why it is interesting for both audiences). Otherwise both empty."""


def suggestions(chosen, dms, collab):
    data = {"posts": [{"nr": i + 1, "account": m.get("account") or f"#{m.get('hashtag')}", "kind": m.get("kind", ""),
                       "text": short(m.get("caption"), 900)} for i, m in enumerate(chosen)],
            "dm_candidates": dms, "collab_candidate": collab}
    if not chosen and not dms and not collab:
        return None
    return ai.json_answer(TASK, data, SCHEMA)


# ---------- issue ----------

def issue_text(chosen, dms, collab, ai_text, notes, contacts, upkeep=([], [])):
    com = {k["nr"]: k["text"] for k in (ai_text or {}).get("comments", [])}
    dm_text = {d["account"]: d["text"] for d in (ai_text or {}).get("dms", [])}
    parts = [f"@{REPO.split('/')[0]} – your radar for today, about 15 min. Everything **by hand in the app**, "
             "then tick it off here. The radar remembers ticked boxes (whoever is warm gets a DM draft later).", ""]
    parts += ["## 💬 Comment (about 10 min)",
              "Look at the post first, adapt the suggestion (your own words work better), then comment.", ""]
    if not chosen:
        parts.append("_Nothing fresh today – add verified accounts in `automation/interaction.json` (`radar.accounts`)._")
    for i, m in enumerate(chosen, 1):
        suggestion = com.get(i, "")
        if suggestion.strip().lower().startswith(SKIP):
            continue
        who = f"@{m['account']}" if m.get("account") else f"#{m['hashtag']}"
        warm = contacts.get(m.get("account", ""), {}).get("comments", 0)
        info = " · ".join(x for x in [
            ago(parse_time(m["timestamp"])),
            f"❤️ {m['like_count']:,}" if m.get("like_count") is not None else "",
            f"💬 {m.get('comments_count', 0)}",
            f"🔥 commented {warm}× already" if warm else "",
            ("keyword: " + ", ".join(m["hits"])) if m.get("hits") else ""] if x)
        parts += [f"- [ ] 💬 commented · {who} · [open post]({m['permalink']}) · {info}",
                  f"  > {short(m.get('caption'), 160)}"]
        if suggestion:
            parts += ["", f"  ✍️ {suggestion}"]
        parts.append("")
    if dms:
        parts += ["## ✉️ DM drafts (about 5 min)",
                  "Only send if it feels natural. Max. one DM per account, no follow-up if there is no answer.", ""]
        for d in dms:
            parts += [f"- [ ] ✉️ DM sent · @{d['account']} · commented {d['comments_by_loris']}× already"
                      + (f" · [last post]({d['link']})" if d.get("link") else ""),
                      "", f"  ✍️ {dm_text.get(d['account'], '_(no suggestion – your own words)_')}", ""]
    c = (ai_text or {}).get("collab", {})
    if collab:
        parts += ["## 🤝 Collab of the week", "",
                  f"- [ ] 🤝 asked · @{collab['account']} · {collab.get('followers') or 0:,} followers", "",
                  f"  💡 {c.get('idea') or 'Idea: joint carousel or story Q&A'}", ""]
        if c.get("text"):
            parts += [f"  ✍️ {c['text']}", ""]
    drop, add = upkeep
    if drop or add:
        parts += ["## 🧹 Radar upkeep (weekly)",
                  "Only what you tick is applied to `automation/interaction.json` on the next run. "
                  "Not ticked = stays as it is (the suggestion comes back in 60 days at the earliest).", ""]
        parts += [f"- [ ] 🧹 remove · @{n} · {g}" for n, g in drop]
        parts += [f"- [ ] ➕ add · @{n} · {g}" for n, g in add]
        parts.append("")
    if notes:
        parts += ["<details><summary>⚠️ Notes</summary>", "", *[f"- {f}" for f in notes], "", "</details>"]
    parts += ["", "_Rules: max. ~10 comments and ~5 DMs a day, never copy-paste mass messages – otherwise Instagram throttles the account._"]
    return "\n".join(parts)


def save(message):
    git("add", str(FOLDER), str(SETTINGS_FILE))
    if not git("status", "--porcelain", "--", str(FOLDER), str(SETTINGS_FILE)):
        return
    git("commit", "-m", message)
    for attempt in range(5):
        try:
            git("pull", "--rebase", "-q")
            git("push")
            return
        except subprocess.CalledProcessError:
            subprocess.run(["git", "rebase", "--abort"], cwd=ROOT, capture_output=True)  # otherwise every retry fails the same way
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("Radar data could not be saved (push failed 5×)")


def main():
    if not os.environ.get("FB_TOKEN") or not os.environ.get("FB_IG_USER_ID"):
        print("Radar: FB_TOKEN / FB_IG_USER_ID missing – setup see SETUP.md (radar section). Nothing to do.")
        return
    FOLDER.mkdir(parents=True, exist_ok=True)
    try:  # check the key once before anything else – an expired key must never look like 93 broken accounts
        api(os.environ["FB_IG_USER_ID"], fields="username")
    except TokenInvalid as e:
        sys.exit(f"✗ Radar: FB_TOKEN is expired or invalid ({short(str(e), 160)}).\n"
                 "→ Generate a long-lived token (60 days) for the Facebook page linked to @maehrtax and replace the "
                 "secret FB_TOKEN (SETUP.md, radar section). With FB_APP_ID + FB_APP_SECRET set, the monthly key "
                 "refresh keeps it alive. Nothing was queried, no account was marked as broken.")
    contacts, seen = load(CONTACTS, {}), load(SEEN, {})
    old_issues, remove, add = ([], [], []) if DRY_RUN else count_ticks(contacts)
    if remove or add:
        apply_upkeep(remove, add)
    notes = [f"@{k['name']}: kind “{k.get('kind', '')}” missing/unknown – in `automation/interaction.json` "
             f"set one of {', '.join(sorted(KINDS_ALLOWED))}"
             for k in accounts() if isinstance(k, dict) and k.get("kind") not in KINDS_ALLOWED]
    if not accounts():
        print("Radar: no verified accounts in interaction.json (radar.accounts is empty) – "
              "only hashtags and upkeep suggestions. Cowork fills radar.accounts from radar.candidates_to_verify.")
        notes.append("No verified accounts yet – `radar.accounts` in `automation/interaction.json` is empty "
                     "(candidates to check: `radar.candidates_to_verify`).")
    profiles = query_accounts(notes)
    upkeep = upkeep_suggestions(profiles)
    chosen = select(profiles, query_hashtags(notes), contacts, seen)
    dms, collab = dm_candidates(profiles, contacts), collab_candidate(profiles, contacts)
    title = (f"📡 Radar {WEEKDAY[NOW.weekday()]} {NOW.month}/{NOW.day} – {len(chosen)} posts"
             + (f", {len(dms)} DM drafts" if dms else "") + (", collab" if collab else "") + (", upkeep" if any(upkeep) else ""))
    nothing = not chosen and not dms and not collab and not any(upkeep)
    if nothing and not accounts():
        # no issue (it would only say "nothing"), but still store what was ticked and close the old issues
        print("Radar: nothing to show today – no issue created.", *[f"\n  · {n}" for n in notes])
        if not DRY_RUN:
            for nr in old_issues:
                gh("issue", "close", str(nr))
            CONTACTS.write_text(json.dumps(contacts, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
            save(f"Radar {NOW:%Y-%m-%d}: no accounts yet")
        return
    text = issue_text(chosen, dms, collab, suggestions(chosen, dms, collab), notes, contacts, upkeep)
    if DRY_RUN:
        print(title, "\n", text)
        return
    try:
        gh("label", "create", LABEL, "--color", "8FA398", "--description", "Daily engagement work list")
    except subprocess.CalledProcessError:
        pass
    print("✓", title, gh("issue", "create", "--title", title, "--label", LABEL, "--body-file", "-", stdin=text))
    for nr in old_issues:
        gh("issue", "close", str(nr))  # without a comment – saves one notification a day
    # remember seen posts for 30 days so nothing comes twice
    seen.update({m["id"]: NOW.strftime("%Y-%m-%d") for m in chosen})
    cutoff = (NOW - timedelta(days=30)).strftime("%Y-%m-%d")
    seen = {k: v for k, v in seen.items() if v >= cutoff}
    SEEN.write_text(json.dumps(seen, indent=1, sort_keys=True) + "\n")
    CONTACTS.write_text(json.dumps(contacts, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    save(f"Radar {NOW:%Y-%m-%d}: {len(chosen)} posts, {len(dms)} DM drafts"
         + (f", accounts −{len(remove)}/+{len(add)} (ticked)" if remove or add else ""))


if __name__ == "__main__":
    main()
