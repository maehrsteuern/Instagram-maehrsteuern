"""Holt gemeinfreie Musik (CC0) von FreePD und legt die 5 Titel mit dem kräftigsten Einstieg in musik/ ab.
Läuft auf GitHub (Workflow „Musik holen“), weil dort das Internet frei erreichbar ist.
"""
import re, subprocess
from pathlib import Path
from urllib.parse import urljoin

import requests
import imageio_ffmpeg

ZIEL = Path(__file__).resolve().parent.parent / "musik"
SEITEN = ["https://freepd.com/electronic.php", "https://freepd.com/upbeat.php", "https://freepd.com/"]
FF = imageio_ffmpeg.get_ffmpeg_exe()
ANZAHL, KANDIDATEN = 5, 16


def lautstaerke_anfang(datei):
    """Mittlere Lautstärke der ersten 1,5 s in dB (höher = kräftiger Einstieg) und Gesamtlänge in s."""
    aus = subprocess.run([FF, "-hide_banner", "-t", "1.5", "-i", str(datei), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    mittel = re.search(r"mean_volume: (-?[\d.]+) dB", aus)
    laenge = re.search(r"Duration: (\d+):(\d+):([\d.]+)", aus)
    sek = int(laenge[1]) * 3600 + int(laenge[2]) * 60 + float(laenge[3]) if laenge else 0
    return (float(mittel[1]) if mittel else -99.0), sek


links = []
for seite in SEITEN:
    try:
        html = requests.get(seite, timeout=30).text
    except requests.RequestException:
        continue
    for href in re.findall(r'''["']([^"']+?\.mp3)["']''', html):
        url = urljoin(seite, href)
        if url not in links:
            links.append(url)
print(f"{len(links)} Titel gefunden")

tmp = Path("/tmp/musik"); tmp.mkdir(exist_ok=True)
bewertet = []
for url in links[:KANDIDATEN]:
    datei = tmp / Path(url).name.replace("%20", "_")
    try:
        r = requests.get(url, timeout=60); r.raise_for_status()
    except requests.RequestException:
        continue
    datei.write_bytes(r.content)
    db, sek = lautstaerke_anfang(datei)
    print(f"  {datei.name}: Einstieg {db} dB, {sek:.0f} s")
    if sek >= 20:
        bewertet.append((db, datei, url))

if not bewertet:
    raise SystemExit("✗ Keine passenden Titel gefunden")
ZIEL.mkdir(exist_ok=True)
quellen = ["# Quellen", "", "Alle Titel: FreePD.com, gemeinfrei (CC0) – frei nutzbar ohne Namensnennung, auch auf Instagram.", ""]
for nr, (db, datei, url) in enumerate(sorted(bewertet, reverse=True)[:ANZAHL], 1):
    name = f"{nr:02d}_{re.sub(r'[^a-z0-9]+', '_', datei.stem.lower()).strip('_')}.mp3"
    (ZIEL / name).write_bytes(datei.read_bytes())
    quellen.append(f"- `{name}` ← {url} (Einstieg {db} dB)")
    print("✓", name)
(ZIEL / "QUELLEN.md").write_text("\n".join(quellen) + "\n")
