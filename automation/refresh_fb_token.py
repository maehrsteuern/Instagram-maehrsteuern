"""Refresh the Facebook access key for the radar (runs monthly together with the Instagram key).
A long-lived key is valid for 60 days; while it is still valid, Facebook returns a new one.
Needs FB_TOKEN, FB_APP_ID, FB_APP_SECRET and GH_PAT (to replace the secret). Without FB_TOKEN: nothing to do.
"""
import os, subprocess, sys

from expiry import remember_expiry

old = os.environ.get("FB_TOKEN")
if not old:
    print("No FB_TOKEN – radar not set up yet, nothing to do.")
    sys.exit(0)
if not os.environ.get("FB_APP_ID") or not os.environ.get("FB_APP_SECRET"):
    sys.exit("✗ FB_APP_ID / FB_APP_SECRET missing – FB_TOKEN expires after 60 days (see SETUP.md, radar section)")

import requests

r = requests.get("https://graph.facebook.com/v23.0/oauth/access_token", timeout=60, params={
    "grant_type": "fb_exchange_token", "client_id": os.environ["FB_APP_ID"],
    "client_secret": os.environ["FB_APP_SECRET"], "fb_exchange_token": old})
if not r.ok:
    sys.exit(f"✗ Refresh failed: {r.status_code} {r.text[:300]}")
new, days = r.json()["access_token"], r.json().get("expires_in", 0) // 86400
print(f"::add-mask::{new}")  # the new key is not a secret (yet) – mask it in the public log
print(f"✓ Facebook key refreshed, valid for {days} more days" if days else "✓ Facebook key refreshed")
if new != old:
    if not os.environ.get("GH_TOKEN"):
        sys.exit("✗ Got a new key, but GH_PAT is missing – replace FB_TOKEN by hand")
    # key via stdin, not as an argument – otherwise it would show up in an error message
    res = subprocess.run(["gh", "secret", "set", "FB_TOKEN", "--repo", os.environ["GITHUB_REPOSITORY"]],
                         input=new, text=True, capture_output=True)
    if res.returncode:
        sys.exit(f"✗ Secret FB_TOKEN not replaced (GH_PAT expired?): {res.stderr.strip()[:300]}")
    print("✓ Secret FB_TOKEN replaced")
# remember the expiry only once the new key really is in the secret – otherwise the watchdog would stay quiet wrongly
if r.json().get("expires_in"):
    remember_expiry("FB_TOKEN", r.json()["expires_in"])
