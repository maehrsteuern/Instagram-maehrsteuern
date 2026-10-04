"""Refresh the Instagram access key (runs monthly). A key is valid for 60 days and is renewed here.
If a new key comes back and GH_PAT is set, the secret IG_TOKEN is replaced automatically.
Without IG_TOKEN: nothing to do (setup not finished yet).
"""
import os, subprocess, sys

from expiry import remember_expiry

old = os.environ.get("IG_TOKEN")
if not old:
    print("No IG_TOKEN – Instagram not set up yet, nothing to refresh.")
    sys.exit(0)

import requests

r = requests.get("https://graph.instagram.com/refresh_access_token",
                 params={"grant_type": "ig_refresh_token", "access_token": old}, timeout=60)
if not r.ok:
    sys.exit(f"✗ Refresh failed: {r.status_code} {r.text}")
new, days = r.json()["access_token"], r.json().get("expires_in", 0) // 86400
print(f"::add-mask::{new}")  # the new key is not a secret (yet) – mask it in the public log
print(f"✓ Key refreshed, valid for {days} more days")
if new != old:
    if not os.environ.get("GH_TOKEN"):
        sys.exit("✗ Got a new key, but GH_PAT is missing – replace IG_TOKEN by hand (see SETUP.md)")
    # key via stdin, not as an argument – otherwise it would show up in an error message
    res = subprocess.run(["gh", "secret", "set", "IG_TOKEN", "--repo", os.environ["GITHUB_REPOSITORY"]],
                         input=new, text=True, capture_output=True)
    if res.returncode:
        sys.exit(f"✗ Secret IG_TOKEN not replaced (GH_PAT expired?): {res.stderr.strip()[:300]}")
    print("✓ Secret IG_TOKEN replaced")
# remember the expiry only once the new key really is in the secret – otherwise the watchdog would stay quiet wrongly
if r.json().get("expires_in"):
    remember_expiry("IG_TOKEN", r.json()["expires_in"])
