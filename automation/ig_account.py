"""Which Instagram account does IG_TOKEN belong to? Shared by post, stats, insights and comments.

The account ID is read from the token itself (GET /me → user_id). IG_USER_ID only serves as a cross-check:
if it differs, the token's own ID is used and a warning tells Loris to fix the secret. post.py additionally
refuses to publish if the token does not belong to @maehrtax (never post the US content to another account).
"""
import os

API = "https://graph.instagram.com/v23.0"
EXPECTED_USERNAME = "maehrtax"


def resolve(token=None, configured=None):
    """→ (user_id, username). Falls back to IG_USER_ID if /me itself fails (username then None)."""
    import requests
    token = token or os.environ["IG_TOKEN"]
    configured = configured if configured is not None else os.environ.get("IG_USER_ID", "")
    try:
        r = requests.get(f"{API}/me", params={"fields": "user_id,username", "access_token": token}, timeout=60)
        me = r.json() if r.ok else {}
    except (requests.RequestException, ValueError):
        me = {}
    user_id = str(me.get("user_id") or me.get("id") or "")
    if not user_id:
        return configured, None
    if configured and configured != user_id:
        print(f"⚠️ IG_USER_ID does not match IG_TOKEN (@{me.get('username')}) – using the token's account ID. "
              "Please set the secret IG_USER_ID to the Instagram account ID from the Meta app (API setup with Instagram login).")
    return user_id, me.get("username")
