"""Instagram-Zugangsschlüssel verlängern (läuft monatlich). Ein Schlüssel gilt 60 Tage und wird hier erneuert.
Kommt ein neuer Schlüssel zurück und ist GH_PAT gesetzt, wird das Secret IG_TOKEN automatisch ersetzt.
"""
import os, subprocess, sys
import requests

from ablauf import ablauf_merken


alt = os.environ["IG_TOKEN"]
r = requests.get("https://graph.instagram.com/refresh_access_token",
                 params={"grant_type": "ig_refresh_token", "access_token": alt}, timeout=60)
if not r.ok:
    sys.exit(f"✗ Verlängern fehlgeschlagen: {r.status_code} {r.text}")
neu, tage = r.json()["access_token"], r.json().get("expires_in", 0) // 86400
print(f"::add-mask::{neu}")  # neuer Schlüssel ist (noch) kein Secret – im öffentlichen Log maskieren
print(f"✓ Schlüssel verlängert, gültig noch {tage} Tage")
if neu != alt:
    if not os.environ.get("GH_TOKEN"):
        sys.exit("✗ Neuer Schlüssel erhalten, aber GH_PAT fehlt – IG_TOKEN bitte von Hand ersetzen (siehe EINRICHTUNG.md)")
    # Schlüssel über stdin, nicht als Argument – sonst stünde er bei einem Fehler in der Meldung
    erg = subprocess.run(["gh", "secret", "set", "IG_TOKEN", "--repo", os.environ["GITHUB_REPOSITORY"]],
                         input=neu, text=True, capture_output=True)
    if erg.returncode:
        sys.exit(f"✗ Secret IG_TOKEN nicht ersetzt (GH_PAT abgelaufen?): {erg.stderr.strip()[:300]}")
    print("✓ Secret IG_TOKEN ersetzt")
# Ablauf erst merken, wenn der neue Schlüssel wirklich im Secret steht – sonst schweigt der Wächter zu Unrecht
if r.json().get("expires_in"):
    ablauf_merken("IG_TOKEN", r.json()["expires_in"])
