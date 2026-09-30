"""Holt gemeinfreie Musik (CC0) aus dem Internet Archive und legt die 5 Titel mit dem kräftigsten Einstieg in musik/ ab.
Läuft auf GitHub (Workflow „Musik holen“), weil dort das Internet frei erreichbar ist. Quelle je Titel steht in musik/QUELLEN.md.
"""
import re, subprocess
from pathlib import Path

import requests
import imageio_ffmpeg

ZIEL = Path(__file__).resolve().parent.parent / "musik"
FF = imageio_ffmpeg.get_ffmpeg_exe()
ANZAHL, KANDIDATEN = 5, 20
KOPF = {"User-Agent": "maehrsteuern-musik/1.0"}
CC0 = ['"http://creativecommons.org/publicdomain/zero/1.0/"', '"https://creativecommons.org/publicdomain/zero/1.0/"']
STILE = ["electronic", "lofi", "chillhop", "beats", "instrumental", "hip hop instrumental"]


def sekunden(wert):
    """Länge aus dem Archiv: '123.4', '01:00' oder '1:02:03' → Sekunden."""
    try:
        teile = [float(t) for t in str(wert or 0).split(":")]
    except ValueError:
        return 0.0
    ges = 0.0
    for t in teile:
        ges = ges * 60 + t
    return ges


def lautstaerke_anfang(datei):
    """Mittlere Lautstärke der ersten 1,5 s in dB (höher = kräftiger Einstieg) und Gesamtlänge in s."""
    aus = subprocess.run([FF, "-hide_banner", "-t", "1.5", "-i", str(datei), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    mittel = re.search(r"mean_volume: (-?[\d.]+) dB", aus)
    laenge = re.search(r"Duration: (\d+):(\d+):([\d.]+)", aus)
    sek = int(laenge[1]) * 3600 + int(laenge[2]) * 60 + float(laenge[3]) if laenge else 0
    return (float(mittel[1]) if mittel else -99.0), sek


docs, gesehen = [], set()
for lizenz in CC0:
    for stil in STILE:
        q = f'licenseurl:{lizenz} AND mediatype:audio AND subject:"{stil}"'
        antwort = requests.get("https://archive.org/advancedsearch.php", headers=KOPF, timeout=60, params={
            "q": q, "fl[]": ["identifier", "title"], "rows": 25, "sort[]": "downloads desc", "output": "json"})
        daten = antwort.json() if antwort.ok else {}
        if "response" not in daten:
            print("  Suche fehlgeschlagen:", q, antwort.status_code, antwort.text[:200])
            continue
        for d in daten["response"]["docs"]:
            if d["identifier"] not in gesehen:
                gesehen.add(d["identifier"]); docs.append(d)
print(f"{len(docs)} Sammlungen gefunden")

kandidaten = []
for d in docs:
    try:
        meta = requests.get(f"https://archive.org/metadata/{d['identifier']}", headers=KOPF, timeout=60).json()
    except (requests.RequestException, ValueError):
        continue
    if "publicdomain/zero" not in str(meta.get("metadata", {}).get("licenseurl", "")):
        continue
    for f in meta.get("files", []):
        if f.get("name", "").lower().endswith(".mp3") and 20 <= sekunden(f.get("length")) <= 300:
            kandidaten.append((d["identifier"], f["name"], meta["metadata"].get("licenseurl")))
            break  # ein Titel je Sammlung, damit es abwechslungsreich bleibt
    if len(kandidaten) >= KANDIDATEN:
        break
print(f"{len(kandidaten)} Kandidaten")

tmp = Path("/tmp/musik"); tmp.mkdir(exist_ok=True)
bewertet = []
for ident, name, lizenz in kandidaten:
    url = f"https://archive.org/download/{ident}/{requests.utils.quote(name)}"
    datei = tmp / re.sub(r"[^A-Za-z0-9.]+", "_", f"{ident}_{name}")
    try:
        r = requests.get(url, timeout=120, headers=KOPF); r.raise_for_status()
    except requests.RequestException:
        continue
    datei.write_bytes(r.content)
    db, sek = lautstaerke_anfang(datei)
    print(f"  {name[:50]}: Einstieg {db} dB, {sek:.0f} s")
    if sek >= 20:
        bewertet.append((db, datei, url, f"https://archive.org/details/{ident}", lizenz))

if not bewertet:
    raise SystemExit("✗ Keine passenden Titel gefunden")
ZIEL.mkdir(exist_ok=True)
quellen = ["# Quellen", "", "Alle Titel aus dem Internet Archive, Lizenz CC0 (gemeinfrei) – frei nutzbar ohne Namensnennung.", ""]
for nr, (db, datei, url, seite, lizenz) in enumerate(sorted(bewertet, reverse=True)[:ANZAHL], 1):
    ziel = f"{nr:02d}_{re.sub(r'[^a-z0-9]+', '_', datei.stem.lower())[:40].strip('_')}.mp3"
    (ZIEL / ziel).write_bytes(datei.read_bytes())
    quellen.append(f"- `{ziel}` ← {seite} ({lizenz}), Einstieg {db} dB")
    print("✓", ziel)
(ZIEL / "QUELLEN.md").write_text("\n".join(quellen) + "\n")
