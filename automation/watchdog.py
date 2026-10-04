"""Watchdog (runs with every status run): ONE open issue "🚨 Watchdog" that only comments on real problems.

- Workflow failed → one comment; while it stays red, no further one. Green again → only the status in the
  issue body changes (no notification).
- A key is valid for less than 14 days (automation/key_expiry.json, written by token.yml) → one comment per expiry
  date. Placeholder values ("set after setup") are ignored.
Several new problems in one run are bundled into one comment. The state is stored invisibly in the issue body,
so nothing needs to be committed.
Environment: GH_TOKEN (issues:write, actions:read), GITHUB_REPOSITORY. Without GH_TOKEN: prints a note, does nothing.
"""
import json, os, re, subprocess, sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from status import WORKFLOWS, when
from expiry import load as load_expiry

REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/maehrtax---instagram")
LABEL = "watchdog"
WARN_DAYS = 14
STATE = re.compile(r"<!-- state (\{.*?\}) -->", re.S)


def gh(*args, stdin=None):
    return subprocess.run(["gh", *args], input=stdin, check=True, capture_output=True, text=True).stdout.strip()


def last_run(file):
    raw = gh("api", f"repos/{REPO}/actions/workflows/{file}/runs?status=completed&per_page=100", "--jq",
             '[.workflow_runs[] | select(.conclusion=="success" or .conclusion=="failure")][0]'
             ' | [.conclusion, .html_url, .updated_at] | @tsv')
    return raw.split("\t") if raw else None


def get_issue():
    raw = gh("issue", "list", "--repo", REPO, "--label", LABEL, "--state", "open", "--json", "number,body", "--limit", "1")
    found = json.loads(raw)
    if found:
        match = STATE.search(found[0]["body"])
        return found[0]["number"], json.loads(match.group(1)) if match else {}
    try:
        gh("label", "create", LABEL, "--repo", REPO, "--color", "D73A4A", "--description", "Failures and expiring keys")
    except subprocess.CalledProcessError:
        pass
    url = gh("issue", "create", "--repo", REPO, "--title", "🚨 Watchdog", "--label", LABEL, "--body", "filling in …")
    return int(url.rstrip("/").split("/")[-1]), {}


def check_keys(state, today):
    """→ (table rows, new warnings). Placeholder values in key_expiry.json are skipped."""
    rows, new = [], []
    for name, expires in sorted(load_expiry().items()):
        days = (expires - today).days
        warn = days < WARN_DAYS
        rows.append(f"| {name} | {expires.month}/{expires.day}/{expires.year} | {'⚠️ ' if warn else ''}{days} days left |")
        if warn and state["warned"].get(name) != expires.isoformat():
            new.append(f"🔑 **{name}** is only valid for {days} more days (until {expires.month}/{expires.day}/{expires.year}) – "
                       "Actions → *Refresh Instagram key* → *Run workflow*, or renew it by hand (SETUP.md)")
            state["warned"][name] = expires.isoformat()
    return rows, new


def main():
    if not os.environ.get("GH_TOKEN"):
        print("Watchdog: GH_TOKEN missing – nothing to check.")
        return
    number, state = get_issue()
    old = json.dumps(state, sort_keys=True)
    state.setdefault("red", {})
    state.setdefault("warned", {})
    new, rows = [], []
    for file, name, _ in WORKFLOWS:
        try:
            run = last_run(file)
        except subprocess.CalledProcessError:
            run = None
        if not run:
            rows.append(f"| {name} | – |")
            continue
        result, url, _ran = run
        if result == "failure":
            if state["red"].get(file) is None:
                new.append(f"🔴 **{name}** failed – [view run]({url})")
            state["red"][file] = url
            rows.append(f"| {name} | 🔴 [failed]({url}) |")
        else:
            state["red"].pop(file, None)
            rows.append(f"| {name} | ✅ |")
    key_rows, key_warnings = check_keys(state, date.today())
    new += key_warnings
    if new:
        gh("issue", "comment", str(number), "--repo", REPO, "--body", "Heads-up, something needs attention:\n\n" + "\n".join(f"- {z}" for z in new))
        print(f"✓ {len(new)} new problems reported")
    if new or json.dumps(state, sort_keys=True) != old or not old.strip("{}"):
        as_of = when(datetime.now(ZoneInfo("America/New_York")))
        body = (f"@{REPO.split('/')[0]} This issue stays open. It only speaks up on **real problems** "
                f"(workflow red, key < {WARN_DAYS} days) – when everything is green, it stays quiet. "
                "Please don't close it.\n\n"
                f"**As of {as_of}**\n\n| Workflow | Last run |\n|---|---|\n" + "\n".join(rows) +
                "\n\n| Key | valid until | |\n|---|---|---|\n" + ("\n".join(key_rows) or "| – (dates are set after setup) | – | – |") +
                f"\n\n<!-- state {json.dumps(state, sort_keys=True)} -->")
        gh("issue", "edit", str(number), "--repo", REPO, "--body", body)
    print("Watchdog: all quiet." if not new else "Watchdog: reported.")


if __name__ == "__main__":
    main()
