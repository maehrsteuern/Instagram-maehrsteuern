"""Instagram-Zugangsschlüssel verlängern (läuft monatlich). Ein Schlüssel gilt 60 Tage und wird hier erneuert.
Kommt ein neuer Schlüssel zurück und ist GH_PAT gesetzt, wird das Secret IG_TOKEN automatisch ersetzt.
"""
import os, subprocess, sys
import requests

alt = os.environ["IG_TOKEN"]
r = requests.get("https://graph.instagram.com/refresh_access_token",
                 params={"grant_type": "ig_refresh_token", "access_token": alt}, timeout=60)
if not r.ok:
    sys.exit(f"✗ Verlängern fehlgeschlagen: {r.status_code} {r.text}")
neu, tage = r.json()["access_token"], r.json().get("expires_in", 0) // 86400
print(f"✓ Schlüssel verlängert, gültig noch {tage} Tage")
if neu != alt:
    if os.environ.get("GH_TOKEN"):
        subprocess.run(["gh", "secret", "set", "IG_TOKEN", "--body", neu, "--repo", os.environ["GITHUB_REPOSITORY"]], check=True)
        print("✓ Secret IG_TOKEN ersetzt")
    else:
        sys.exit("✗ Neuer Schlüssel erhalten, aber GH_PAT fehlt – IG_TOKEN bitte von Hand ersetzen (siehe EINRICHTUNG.md)")
