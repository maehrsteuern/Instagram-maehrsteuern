"""Schnelle Hook-Montage im Takt der Musik:  python3 montage.py schnitt/p01_reel_ampel_hook.json

Wie reel.py, aber für harte Schnitte, Effekte und große Outline-Texte (Wort für Wort).
Zeiten dürfen in Takten stehen: "dauer": "2b" = 2 Schläge, "1/2b" = Achtel. Schlaglänge aus "takt": {"bpm": 122}.
"takt": {"drop": 1.3} legt das Schlagraster fest (ein Schlag liegt genau auf dem Drop).

Quellen: {"datei": "bild.png"} (Standbild) oder {"video": "clip.mp4"} (wird auf 1080x1920 zugeschnitten).
Szene:
  {"quelle": "app" | "karte": "bild.png", "dauer": "2b",
   "von": [cx,cy,w], "nach": [cx,cy,w],   – Kamerafahrt (weglassen = ganzes Bild)
   "ab": 1.2, "tempo": 1.0,                – nur Video: Startsekunde im Clip, Abspieltempo
   "rein": "flash" | "whip" | "glitch" | "flash+whip",   – Übergang am Szenenanfang
   "punch": 0.08,     – Zoom-Stoß auf jedem Schlag (Stärke)
   "shake": 14,       – Wackeln in Pixeln
   "glitch": 0.3,     – Anteil Bilder mit Glitch (RGB-Versatz, verschobene Streifen)
   "abdunkeln": 0.35, – Hintergrund abdunkeln, damit Text auf unruhigen Screens lesbar bleibt
   "text": [{"wort": "#BEZUG!", "ab": "0b", "farbe": "rot", "groesse": 190, "y": 700}]}
Texte ohne "ab" stehen sofort (ohne Aufpoppen) – so bleibt ein Text über mehrere Schnitte stehen.
"""
import json, math, random, subprocess, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
import imageio_ffmpeg

W, H = 1080, 1920
hier = Path(__file__).parent
cfg = json.loads(Path(sys.argv[1]).read_text())
fps = cfg.get("fps", 30)
pfad = lambda p: (hier / p).resolve()
ff = imageio_ffmpeg.get_ffmpeg_exe()
takt = cfg.get("takt", {})
schlag = 60 / takt.get("bpm", 120)
drop = takt.get("drop", 0)
FARBEN = {"weiss": "#FFFFFF", "rot": "#FF4B3E", "gruen": "#53C3A2", "gelb": "#F2B84B"}
schrift = str(pfad(cfg.get("schrift", "schriften/Outfit-Bold.ttf")))
zufall = random.Random(7)


def zeit(v):
    """Sekunden oder Takte ("2b", "1/2b")."""
    if isinstance(v, str) and v.endswith("b"):
        z = v[:-1]
        if "/" in z:
            a, b = z.split("/"); return float(a) / float(b) * schlag
        return float(z) * schlag
    return float(v)


def fuellen(im):  # auf 9:16 zuschneiden (cover)
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def lade_video(datei):
    r = imageio_ffmpeg.read_frames(str(pfad(datei)), output_params=["-r", str(fps)])
    meta = next(r); w, h = meta["size"]
    return [fuellen(Image.frombytes("RGB", (w, h), f)) for f in r]


quellen = {}
for k, q in cfg["quellen"].items():
    quellen[k] = lade_video(q["video"]) if "video" in q else Image.open(pfad(q["datei"])).convert("RGB")


def ausschnitt(im, cx, cy, w):
    h = w * H / W
    x0 = min(max(cx - w / 2, 0), im.width - w)
    y0 = min(max(cy - h / 2, 0), im.height - h)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC)


def rgb_versatz(im, d):
    r, g, b = im.split()
    return Image.merge("RGB", (ImageChops.offset(r, d, 0), g, ImageChops.offset(b, -d, 0)))


def glitch(im, staerke):
    im = rgb_versatz(im, int(18 * staerke) + 4)
    for _ in range(int(3 + 5 * staerke)):  # verschobene Streifen
        y = zufall.randrange(0, H - 40); h = zufall.randrange(12, 90)
        streifen = im.crop((0, y, W, min(y + h, H)))
        im.paste(ImageChops.offset(streifen, zufall.randint(-80, 80), 0), (0, y))
    return im


def wisch(im, versatz, unschaerfe):  # Whip-Pan: seitlich hereinziehen mit Bewegungsunschärfe
    bild = ImageChops.offset(im, int(versatz), 0)
    n = 6
    for k in range(1, n):
        bild = Image.blend(bild, ImageChops.offset(im, int(versatz + unschaerfe * k / n), 0), 1 / (k + 1))
    return bild


_fonts = {}
def font(g):
    if g not in _fonts: _fonts[g] = ImageFont.truetype(schrift, g)
    return _fonts[g]


def text_ebene(eintraege, t):
    """Zeilen untereinander, jede mit schwarzer Outline; neue Zeilen poppen kurz groß auf."""
    ebene = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for e in eintraege:
        ab = zeit(e["ab"]) if "ab" in e else -1
        if t < ab: continue
        zeile = e["wort"]
        g = e.get("groesse", 150)
        breit = ImageDraw.Draw(ebene).textbbox((0, 0), zeile, font=font(g), stroke_width=round(g * 0.075))
        g = min(g, int(g * (W - 90) / (breit[2] - breit[0])))  # nie breiter als das Bild
        k = min((t - ab) / 0.15, 1) if ab >= 0 else 1
        skala = 0.6 + 0.4 * k + 0.3 * math.sin(math.pi * k)  # klein rein, kurz überschwingen
        f = font(max(round(g * skala), 8))
        rand = max(round(g * skala * 0.075), 4)
        box = ImageDraw.Draw(ebene).textbbox((0, 0), zeile, font=f, stroke_width=rand)
        bw, bh = box[2] - box[0], box[3] - box[1]
        x, y = (W - bw) / 2 - box[0], e.get("y", 760) - bh / 2 - box[1]
        schatten = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(schatten).text((x + 8, y + 12), zeile, font=f, fill=(0, 0, 0, 150), stroke_width=rand, stroke_fill=(0, 0, 0, 150))
        ebene.alpha_composite(schatten.filter(ImageFilter.GaussianBlur(10)))
        ImageDraw.Draw(ebene).text((x, y), zeile, font=f, fill=FARBEN.get(e.get("farbe", "weiss"), e.get("farbe")),
                                   stroke_width=rand, stroke_fill="#000000")
    return ebene


szenen = cfg["szenen"]
grenzen = [0]  # Schnittpunkte aus der absoluten Zeit runden, damit die Schnitte nicht vom Takt wegdriften
for sz in szenen: grenzen.append(grenzen[-1] + zeit(sz["dauer"]))
bilder = [round(b * fps) for b in grenzen]
dauer = bilder[-1] / fps
ziel = pfad(cfg["ausgabe"]); ziel.parent.mkdir(parents=True, exist_ok=True)
if cfg.get("musik"):
    start = max(cfg.get("musik_start", 0), 0)
    ton = ["-ss", f"{start:.2f}", "-i", str(pfad(cfg["musik"])), "-af",
           f"volume={cfg.get('lautstaerke', 0.9)},afade=t=in:d=0.03,afade=t=out:st={max(dauer - 1.0, 0):.2f}:d=1.0", "-shortest"]
else:
    ton = ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest"]
proc = subprocess.Popen([ff, "-loglevel", "error", "-y",
    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", *ton,
    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(ziel)], stdin=subprocess.PIPE)

bild_nr = 0
for nr, sz in enumerate(szenen):
    n = bilder[nr + 1] - bilder[nr]
    q = Image.open(pfad(sz["karte"])).convert("RGB") if "karte" in sz else quellen[sz["quelle"]]
    breite = (q[0] if isinstance(q, list) else q).width
    hoehe = (q[0] if isinstance(q, list) else q).height
    von = sz.get("von") or [breite / 2, hoehe / 2, breite]
    nach = sz.get("nach") or von
    rein = sz.get("rein", "")
    for i in range(n):
        t = i / fps; t_abs = bild_nr / fps; k = i / max(n - 1, 1)
        k = 1 - (1 - k) ** 3  # schnell los, weich aus
        cx, cy, w = [a + (b - a) * k for a, b in zip(von, nach)]
        if sz.get("punch"):  # Zoom-Stoß auf dem letzten Schlag
            seit = (t_abs - drop) % schlag
            w /= 1 + sz["punch"] * math.exp(-seit / 0.09)
        if sz.get("shake"):
            a = sz["shake"] * w / W
            cx += zufall.uniform(-a, a); cy += zufall.uniform(-a, a)
        if isinstance(q, list):
            f = min(int((sz.get("ab", 0) + t * sz.get("tempo", 1)) * fps), len(q) - 1)
            bild = ausschnitt(q[f], cx, cy, w)
        else:
            bild = ausschnitt(q, cx, cy, w)
        if "whip" in rein and i < 5:
            r = (1 - i / 5) ** 2
            bild = wisch(bild, -W * 0.35 * r, W * 0.25 * r)
        if ("glitch" in rein and i < 4) or (sz.get("glitch") and zufall.random() < sz["glitch"]):
            bild = glitch(bild, 1 - i / 6 if i < 4 else 0.5)
        if sz.get("punch") and (t_abs - drop) % schlag < 1.5 / fps:
            bild = rgb_versatz(bild, 10)
        if sz.get("abdunkeln"):
            bild = Image.blend(bild, Image.new("RGB", (W, H), "black"), sz["abdunkeln"])
        if sz.get("text"):
            bild = bild.convert("RGBA"); bild.alpha_composite(text_ebene(sz["text"], t)); bild = bild.convert("RGB")
        if "flash" in rein and i < 4:
            bild = Image.blend(bild, Image.new("RGB", (W, H), "white"), [0.95, 0.6, 0.3, 0.1][i])
        proc.stdin.write(bild.tobytes())
        bild_nr += 1
proc.stdin.close(); proc.wait()
print("✓", ziel, f"{dauer:.2f} s")
