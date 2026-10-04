"""Comment helper: answer new comments under your own posts fast (first hour = more reach).

  python automation/comments.py check           – runs after every post run (every 15 min): fetch new comments,
                                                   reply suggestion from Claude, as a comment in the issue "💬 Comments"
  python automation/comments.py reply "TEXT"    – evaluate Loris' reply in the issue:
                                                   "C12 ok" → post the suggestion, "C12 Thanks, …" → post your own text

Comments with a ManyChat keyword (e.g. TOOL) are skipped – ManyChat answers them including the DM.
No DM is ever sent from here. Comments Loris already answered in the app are detected.
Environment: IG_TOKEN, IG_USER_ID, ANTHROPIC_API_KEY (optional), GH_TOKEN, GITHUB_REPOSITORY.
Without IG_TOKEN / IG_USER_ID: prints a note and exits cleanly.
"""
import json, os, re, subprocess, sys, time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai

ROOT = Path(__file__).resolve().parent.parent
SETTINGS = json.loads((ROOT / "automation" / "interaction.json").read_text())["comments"]
STATE = ROOT / "automation" / "interaction" / "comments.json"
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/maehrtax---instagram")
API = "https://graph.instagram.com/v23.0"
LABEL = "comments"
ZONE = ZoneInfo("America/New_York")
NOW = datetime.now(ZONE)
SKIP = "ignore"   # suggestion text for spam/insults


def gh(*args, stdin=None):
    return subprocess.run(["gh", *args, "--repo", REPO], input=stdin, check=True, capture_output=True, text=True).stdout.strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def ig(method, path, **params):
    import requests
    r = requests.request(method, f"{API}/{path}", params={**params, "access_token": os.environ["IG_TOKEN"]}, timeout=60)
    r.raise_for_status()
    return r.json()


def parse_time(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z").astimezone(ZONE)


def load():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"next_nr": 1, "comments": {}, "first_run": True}


def save(state, message):
    cutoff = (NOW - timedelta(days=30)).strftime("%Y-%m-%d")
    state["comments"] = {k: v for k, v in state["comments"].items() if v["date"] >= cutoff}
    state.pop("first_run", None)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n")
    git("add", str(STATE))
    if not git("status", "--porcelain", "--", str(STATE)):
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
    raise RuntimeError("comments.json could not be saved (push failed 5×)")


def collection_issue():
    """One open issue for all comments – GitHub sends a notification for every new entry."""
    numbers = gh("issue", "list", "--label", LABEL, "--state", "open", "--json", "number", "--jq", ".[].number").split()
    if numbers:
        return numbers[0]
    try:
        gh("label", "create", LABEL, "--color", "53C3A2", "--description", "New comments with a reply suggestion")
    except subprocess.CalledProcessError:
        pass
    body = (f"@{REPO.split('/')[0]} New comments under your posts land here – with a reply suggestion.\n\n"
            "**Reply:** comment here with\n"
            "- `C12 ok` → the suggestion is posted as a reply\n"
            "- `C12 Thanks, exactly …` → your own text is posted\n"
            "- several lines work too (one per comment)\n\n"
            "Or reply directly in the app – the next run detects it.\n"
            "Comments with a ManyChat keyword (TOOL) are answered by ManyChat and do not show up here.")
    url = gh("issue", "create", "--title", "💬 Reply to comments", "--label", LABEL, "--body-file", "-", stdin=body)
    return url.rstrip("/").split("/")[-1]


def is_manychat(text):
    return any(re.search(rf"\b{re.escape(w)}\b", text or "", re.I) for w in SETTINGS["manychat_keywords"])


SCHEMA = {"type": "object", "properties": {"replies": {"type": "array", "items": {"type": "object", "properties": {
    "nr": {"type": "integer"}, "text": {"type": "string"}}, "required": ["nr", "text"], "additionalProperties": False}}},
    "required": ["replies"], "additionalProperties": False}

TASK = f"""For each comment (nr) under Loris' own posts, write a reply he will post publicly.
1–2 sentences, max. 200 characters, personal (address the person by name/@ if it fits), US English.
Goal: keep the conversation going – answer questions briefly and correctly, otherwise ask a follow-up question.
Emoji-only or "👍" comments: a short, warm reply.
Questions about someone's own tax situation: stay general and educational, never give individual advice –
e.g. "It depends on your facts – talk to your CPA about your case. Happy to show you the tool."
Never claim to be a CPA or EA. Spam or insults: text = "{SKIP}"."""


def check():
    if not os.environ.get("IG_TOKEN") or not os.environ.get("IG_USER_ID"):
        print("Comments: IG_TOKEN / IG_USER_ID missing – nothing to check (see SETUP.md).")
        return
    state = load()
    me = ig("GET", os.environ["IG_USER_ID"], fields="username")["username"]
    media = ig("GET", f"{os.environ['IG_USER_ID']}/media", fields="id,caption,permalink",
               limit=SETTINGS["posts_to_check"]).get("data", [])
    new, done = [], 0
    cutoff = NOW - timedelta(hours=48 if state.get("first_run") else 24 * 7)
    for m in media:
        for c in ig("GET", f"{m['id']}/comments", fields="id,text,timestamp,username,replies{username}", limit=50).get("data", []):
            if c.get("username") == me or is_manychat(c.get("text")):
                continue
            answered = any(r.get("username") == me for r in c.get("replies", {}).get("data", []))
            known = state["comments"].get(c["id"])
            if known:
                if answered and known["status"] == "open":
                    known["status"] = "answered"
                    done += 1
                continue
            if answered or parse_time(c["timestamp"]) < cutoff:
                continue
            new.append({"c": c, "m": m})
    if not new:
        print(f"No new comments ({done} answered in the app).")
        if done:
            save(state, f"Comments: {done} answered in the app")
        return
    for n in new:
        n["nr"] = state["next_nr"]
        state["next_nr"] += 1
    suggestions = ai.json_answer(TASK, [{"nr": n["nr"], "from": n["c"].get("username"), "comment": n["c"].get("text"),
                                         "post": (n["m"].get("caption") or "")[:600]} for n in new], SCHEMA) or {}
    suggestion = {a["nr"]: a["text"] for a in suggestions.get("replies", [])}
    lines = []
    for n in new:
        s = suggestion.get(n["nr"], "")
        state["comments"][n["c"]["id"]] = {"nr": n["nr"], "suggestion": s, "status": "open",
                                           "date": NOW.strftime("%Y-%m-%d"), "from": n["c"].get("username")}
        start = " ".join((n["m"].get("caption") or "Post").split()[:6])
        lines += [f"**C{n['nr']}** · @{n['c'].get('username')} under [{start} …]({n['m']['permalink']}):",
                  f"> {' '.join((n['c'].get('text') or '').split())}", ""]
        lines += [f"✍️ {s}", ""] if s and s.strip().lower() != SKIP else (["_(better ignore)_", ""] if s else [])
    lines.append("Reply here with `C<nr> ok` or `C<nr> your own text`.")
    gh("issue", "comment", collection_issue(), "--body", "\n".join(lines))
    save(state, f"Comments: {len(new)} new")
    print(f"✓ {len(new)} new comments reported")


def reply(text):
    if not os.environ.get("IG_TOKEN"):
        print("Comments: IG_TOKEN missing – cannot post replies (see SETUP.md).")
        return
    import requests
    state = load()
    by_nr = {v["nr"]: (cid, v) for cid, v in state["comments"].items()}
    result = []
    for nr, content in re.findall(r"^\s*C(\d+)\s+(.+?)\s*$", text, re.M | re.I):
        cid, v = by_nr.get(int(nr), (None, None))
        if not cid:
            result.append(f"❓ C{nr}: not found (older than 30 days?)")
            continue
        answer = v["suggestion"] if content.strip().lower() == "ok" else content.strip()
        if not answer or answer.lower() == SKIP:
            result.append(f"❓ C{nr}: no suggestion – please write your own text")
            continue
        try:
            ig("POST", f"{cid}/replies", message=answer)
        except requests.HTTPError as e:
            result.append(f"🔴 C{nr}: Instagram refused ({e.response.status_code})")
            continue
        v["status"] = "answered"
        result.append(f"✅ C{nr} to @{v.get('from')}: {answer}")
    if not result:
        print("No C number in the comment – nothing to do.")
        return
    number = gh("issue", "list", "--label", LABEL, "--state", "open", "--json", "number", "--jq", ".[0].number")
    if number:
        gh("issue", "comment", number, "--body", "\n".join(result))
    save(state, f"Comments: {sum(z.startswith('✅') for z in result)} answered")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("check", "reply"):
        sys.exit("Usage: comments.py check | reply TEXT")
    if sys.argv[1] == "check":
        check()
    else:
        reply(sys.argv[2] if len(sys.argv) > 2 else "")
