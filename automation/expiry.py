"""Remember when access keys expire – only the date, never the key. Read by the watchdog (watchdog.py).

automation/key_expiry.json maps a key name to an ISO date ("2026-12-01"). Values that are not a date
(e.g. "set after setup") are placeholders and are ignored everywhere.
"""
import json
from datetime import date, timedelta
from pathlib import Path

FILE = Path(__file__).resolve().parent / "key_expiry.json"


def load():
    """{name: date} – only real dates; placeholders, notes ("_note") and broken files are skipped."""
    try:
        raw = json.loads(FILE.read_text())
    except (OSError, ValueError):
        return {}
    out = {}
    for name, value in raw.items():
        if name.startswith("_") or not isinstance(value, str):
            continue
        try:
            out[name] = date.fromisoformat(value)
        except ValueError:
            continue
    return out


def remember_expiry(name, seconds):
    try:
        data = json.loads(FILE.read_text())
    except (OSError, ValueError):
        data = {}
    data[name] = (date.today() + timedelta(seconds=seconds)).isoformat()
    FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n")


def days_left(names=None):
    """Smallest number of days until one of `names` (default: all) expires – None if no date is known."""
    known = {k: v for k, v in load().items() if names is None or k in names}
    return min(((v - date.today()).days for v in known.values()), default=None)


if __name__ == "__main__":  # used by status.yml: prints the days left for IG_TOKEN/FB_TOKEN (99 if unknown)
    left = days_left(("IG_TOKEN", "FB_TOKEN"))
    print(99 if left is None else left)
