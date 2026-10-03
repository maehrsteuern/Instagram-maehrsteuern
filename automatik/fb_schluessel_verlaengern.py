"""Facebook-Zugangsschlüssel für den Radar verlängern (läuft monatlich mit dem Instagram-Schlüssel).
Ein langlebiger Schlüssel gilt 60 Tage; solange er noch gilt, gibt Facebook einen neuen zurück.
Braucht FB_TOKEN, FB_APP_ID, FB_APP_SECRET und GH_PAT (zum Ersetzen des Secrets). Ohne FB_TOKEN: nichts zu tun.
"""
import os, subprocess, sys
import requests

from ablauf import ablauf_merken


alt = os.environ.get("FB_TOKEN")
if not alt:
    sys.exit(print("Kein FB_TOKEN – Radar noch nicht eingerichtet, nichts zu tun."))
if not os.environ.get("FB_APP_ID") or not os.environ.get("FB_APP_SECRET"):
    sys.exit("✗ FB_APP_ID / FB_APP_SECRET fehlen – FB_TOKEN läuft nach 60 Tagen ab (EINRICHTUNG.md Schritt 7)")
r = requests.get("https://graph.facebook.com/v23.0/oauth/access_token", timeout=60, params={
    "grant_type": "fb_exchange_token", "client_id": os.environ["FB_APP_ID"],
    "client_secret": os.environ["FB_APP_SECRET"], "fb_exchange_token": alt})
if not r.ok:
    sys.exit(f"✗ Verlängern fehlgeschlagen: {r.status_code} {r.text[:300]}")
neu, tage = r.json()["access_token"], r.json().get("expires_in", 0) // 86400
print(f"::add-mask::{neu}")  # neuer Schlüssel ist (noch) kein Secret – im öffentlichen Log maskieren
print(f"✓ Facebook-Schlüssel verlängert, gültig noch {tage} Tage" if tage else "✓ Facebook-Schlüssel verlängert")
if neu != alt:
    if not os.environ.get("GH_TOKEN"):
        sys.exit("✗ Neuer Schlüssel erhalten, aber GH_PAT fehlt – FB_TOKEN bitte von Hand ersetzen")
    # Schlüssel über stdin, nicht als Argument – sonst stünde er bei einem Fehler in der Meldung
    erg = subprocess.run(["gh", "secret", "set", "FB_TOKEN", "--repo", os.environ["GITHUB_REPOSITORY"]],
                         input=neu, text=True, capture_output=True)
    if erg.returncode:
        sys.exit(f"✗ Secret FB_TOKEN nicht ersetzt (GH_PAT abgelaufen?): {erg.stderr.strip()[:300]}")
    print("✓ Secret FB_TOKEN ersetzt")
# Ablauf erst merken, wenn der neue Schlüssel wirklich im Secret steht – sonst schweigt der Wächter zu Unrecht
if r.json().get("expires_in"):
    ablauf_merken("FB_TOKEN", r.json()["expires_in"])
