"""Fetches public-domain music (CC0) from the Internet Archive and puts the 5 tracks with the strongest intro into music/.
Runs on GitHub (workflow "Fetch music") because the internet is freely reachable there. The source of every track
is listed in music/SOURCES_fetched.md (merge into music/SOURCES.md by hand).
"""
import re, subprocess, tempfile
from pathlib import Path

import requests
import imageio_ffmpeg

TARGET = Path(__file__).resolve().parent.parent / "music"
FF = imageio_ffmpeg.get_ffmpeg_exe()
COUNT, CANDIDATES = 5, 20
HEADERS = {"User-Agent": "maehrtax-music/1.0"}
CC0 = ['"http://creativecommons.org/publicdomain/zero/1.0/"', '"https://creativecommons.org/publicdomain/zero/1.0/"']
STYLES = ["electronic", "lofi", "chillhop", "beats", "instrumental", "hip hop instrumental"]


def seconds(value):
    """Length from the archive: '123.4', '01:00' or '1:02:03' → seconds."""
    try:
        parts = [float(t) for t in str(value or 0).split(":")]
    except ValueError:
        return 0.0
    total = 0.0
    for t in parts:
        total = total * 60 + t
    return total


def intro_loudness(file):
    """Mean loudness of the first 1.5 s in dB (higher = stronger intro) and total length in s."""
    out = subprocess.run([FF, "-hide_banner", "-t", "1.5", "-i", str(file), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    mean = re.search(r"mean_volume: (-?[\d.]+) dB", out)
    length = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    sec = int(length[1]) * 3600 + int(length[2]) * 60 + float(length[3]) if length else 0
    return (float(mean[1]) if mean else -99.0), sec


docs, seen = [], set()
for license_url in CC0:
    for style in STYLES:
        q = f'licenseurl:{license_url} AND mediatype:audio AND subject:"{style}"'
        resp = requests.get("https://archive.org/advancedsearch.php", headers=HEADERS, timeout=60, params={
            "q": q, "fl[]": ["identifier", "title"], "rows": 25, "sort[]": "downloads desc", "output": "json"})
        data = resp.json() if resp.ok else {}
        if "response" not in data:
            print("  search failed:", q, resp.status_code, resp.text[:200])
            continue
        for d in data["response"]["docs"]:
            if d["identifier"] not in seen:
                seen.add(d["identifier"])
                docs.append(d)
print(f"{len(docs)} collections found")

candidates = []
for d in docs:
    try:
        meta = requests.get(f"https://archive.org/metadata/{d['identifier']}", headers=HEADERS, timeout=60).json()
    except (requests.RequestException, ValueError):
        continue
    if "publicdomain/zero" not in str(meta.get("metadata", {}).get("licenseurl", "")):
        continue
    for f in meta.get("files", []):
        if f.get("name", "").lower().endswith(".mp3") and 20 <= seconds(f.get("length")) <= 300:
            candidates.append((d["identifier"], f["name"], meta["metadata"].get("licenseurl")))
            break  # one track per collection, to keep it varied
    if len(candidates) >= CANDIDATES:
        break
print(f"{len(candidates)} candidates")

tmp = Path(tempfile.mkdtemp(prefix="music_"))
rated = []
for ident, name, license_url in candidates:
    url = f"https://archive.org/download/{ident}/{requests.utils.quote(name)}"
    file = tmp / re.sub(r"[^A-Za-z0-9.]+", "_", f"{ident}_{name}")
    try:
        r = requests.get(url, timeout=120, headers=HEADERS)
        r.raise_for_status()
    except requests.RequestException:
        continue
    file.write_bytes(r.content)
    db, sec = intro_loudness(file)
    print(f"  {name[:50]}: intro {db} dB, {sec:.0f} s")
    if sec >= 20:
        rated.append((db, file, url, f"https://archive.org/details/{ident}", license_url))

if not rated:
    raise SystemExit("✗ No suitable tracks found")
TARGET.mkdir(exist_ok=True)
sources = ["# Sources", "", "All tracks from the Internet Archive, license CC0 (public domain) – free to use without attribution.", ""]
for nr, (db, file, url, page, license_url) in enumerate(sorted(rated, reverse=True)[:COUNT], 1):
    target = f"{nr:02d}_{re.sub(r'[^a-z0-9]+', '_', file.stem.lower())[:40].strip('_')}.mp3"
    (TARGET / target).write_bytes(file.read_bytes())
    sources.append(f"- `{target}` ← {page} ({license_url}), intro {db} dB")
    print("✓", target)
# Never overwrite music/SOURCES.md – it also documents the Runway tracks and sound effects
(TARGET / "SOURCES_fetched.md").write_text("\n".join(sources) + "\n")
print("→ Check music/SOURCES_fetched.md and carry the new entries over to music/SOURCES.md by hand")
