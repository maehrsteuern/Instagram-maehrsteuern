"""Reel aus Standbildern schneiden:  python3 reel.py schnitt/p01_reel_ampel.json

Szenen laufen nacheinander. Eine Szene ist entweder
  {"karte": "bild.png", "dauer": 2.5}                      – volle Karte (Haken, Abspann), leichter Zoom
  {"quelle": "app", "von": [cx,cy,w], "nach": [cx,cy,w], "dauer": 3, "leiste": "leiste.png"}
                                                           – Kamerafahrt über ein großes Bild (Ausschnitt 9:16, Breite w)
"von" weglassen = weiter ab dem Ende der vorigen Szene. Zwischen Karte und Bild wird kurz überblendet.
Ton: stumm – Musik in der Instagram-App auswählen.
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image
import imageio_ffmpeg

W, H = 1080, 1920
hier = Path(__file__).parent
cfg = json.loads(Path(sys.argv[1]).read_text())
fps = cfg.get("fps", 30)
pfad = lambda p: (hier / p).resolve()


def lade_quelle(q):
    im = Image.open(pfad(q["datei"])).convert("RGB")
    extra = q.get("unten_auffuellen", 0)
    if extra:  # dunkle Fläche unten anfügen, damit auch die unterste Zeile mittig stehen kann
        neu = Image.new("RGB", (im.width, im.height + extra), im.getpixel((im.width // 2, im.height - 1)))
        neu.paste(im, (0, 0)); im = neu
    return im


quellen = {k: lade_quelle(v) for k, v in cfg["quellen"].items()}
glatt = lambda t: t * t * (3 - 2 * t)


def ausschnitt(im, cx, cy, w):
    h = w * H / W
    x0 = min(max(cx - w / 2, 0), im.width - w)
    y0 = min(max(cy - h / 2, 0), im.height - h)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC)


ff = imageio_ffmpeg.get_ffmpeg_exe()
ziel = pfad(cfg["ausgabe"]); ziel.parent.mkdir(parents=True, exist_ok=True)
proc = subprocess.Popen([ff, "-loglevel", "error", "-y",
    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-movflags", "+faststart", str(ziel)], stdin=subprocess.PIPE)

letztes, kamera, art_vorher = None, None, None
for sz in cfg["szenen"]:
    n = round(sz["dauer"] * fps)
    art = "karte" if "karte" in sz else "quelle"
    karte = Image.open(pfad(sz["karte"])).convert("RGB") if art == "karte" else None
    leiste = Image.open(pfad(sz["leiste"])).convert("RGBA") if sz.get("leiste") else None
    von = sz.get("von") or kamera
    nach = sz.get("nach")
    fahrt = min(0.9 * fps, n)
    for i in range(n):
        t = i / fps
        if art == "karte":
            z = 1 + 0.04 * i / n
            bild = ausschnitt(karte, W / 2, H / 2, W / z)
        else:
            if i < fahrt:
                k = glatt(i / fahrt); c = [a + (b - a) * k for a, b in zip(von, nach)]
            else:  # langsames Weiterzoomen
                k = (i - fahrt) / max(n - fahrt, 1); c = [nach[0], nach[1], nach[2] * (1 - 0.03 * k)]
            kamera = c
            bild = ausschnitt(quellen[sz["quelle"]], *c)
            if leiste is not None:
                a = min(max((t - 0.25) / 0.3, 0), 1)
                if a > 0:
                    l = leiste.copy(); l.putalpha(l.getchannel("A").point(lambda v: int(v * a)))
                    bild = bild.convert("RGBA"); bild.alpha_composite(l); bild = bild.convert("RGB")
        if letztes is not None and art != art_vorher and t < 0.3:  # Überblendung Karte <-> Bild
            bild = Image.blend(letztes, bild, t / 0.3)
        proc.stdin.write(bild.tobytes())
        ende = bild
    letztes, art_vorher = ende, art
    if art == "quelle":
        kamera = [nach[0], nach[1], nach[2] * 0.97]
proc.stdin.close(); proc.wait()
print("✓", ziel)
