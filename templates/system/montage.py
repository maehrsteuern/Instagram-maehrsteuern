"""Cut a Reel from recordings, clips and stills:  python3 montage.py cuts/r01_ref_error.json

Hard cuts, camera moves, big outline hook text (Outfit Bold), PNG overlays (CTA bar, end card) and several audio tracks.
Output: 1080x1920, H.264 + AAC, 30 fps. Times are seconds or beats ("2b" = 2 beats, "1/2b" = an eighth),
beat length from "beat": {"bpm": 122, "drop": 1.3} (the drop sits exactly on a beat).

Cut-list schema (all keys English):
{
  "output": "../../posts/<reel>/reel.mp4",
  "fps": 30, "crf": 19,
  "font": "fonts/Outfit-Bold.ttf",          – hook font (default)
  "text_width": 780,                        – max. text width in px; centred at x 540 → keeps the right ~150 px (IG buttons) free
  "sources": {"rec": {"video": "clip.mp4"}, "still": {"image": "frame.png"}},   – videos are cropped/scaled to 9:16 (cover)
  "audio": [{"file": "../../music/x.mp3", "at": 3.2, "start": 0, "duration": 2, "volume": 0.8, "fade_in": 0.3, "fade_out": 0.2}],
           at = position in the Reel, start = start second in the file, no duration = until the end. The whole mix fades out at the end.
  "music": "../../music/x.mp3", "music_start": 4.2, "volume": 0.9   – short form: one track from second 0
  "scenes": [{
     "source": "rec" | "card": "image.png",   – a source key or a still image (e.g. the end card)
     "duration": 2.5,
     "start": 1.2, "speed": 1.0,              – video only: start second in the clip, playback speed
     "from": [cx, cy, w], "to": [cx, cy, w],  – camera move in 1080x1920 space (omit = full frame)
     "in": "fade" | "flash" | "whip" | "glitch" | "flash+whip",  "fade": 0.3   – transition at the start of the scene
     "punch": 0.08, "shake": 14, "glitch": 0.3,   – effects (use sparingly, see strategy/09_reel_rules.md)
     "darken": 0.35,                          – darken busy screens behind text
     "text": [{"text": "#REF!", "at": 0.3, "until": 2.0, "color": "red", "size": 150, "y": 700, "x": 540}],
              no "at" = visible from the first frame of the scene, no pop (use this for the hook in frame 1)
              colors: white | red | green | yellow | any CSS hex
     "overlay": [{"image": "cta.png", "at": 0.2, "until": 3.0, "fade": 0.25}]   – transparent 1080x1920 PNG on top
  }]
}
"""
import json, math, random, subprocess, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
import imageio_ffmpeg

W, H = 1080, 1920
here = Path(__file__).parent
cfg = json.loads(Path(sys.argv[1]).read_text())
fps = cfg.get("fps", 30)
path = lambda p: (here / p).resolve()
ff = imageio_ffmpeg.get_ffmpeg_exe()
beat_cfg = cfg.get("beat", {})
beat = 60 / beat_cfg.get("bpm", 120)
drop = beat_cfg.get("drop", 0)
COLORS = {"white": "#FFFFFF", "red": "#FF4B3E", "green": "#53C3A2", "yellow": "#F2B84B"}
font_file = str(path(cfg.get("font", "fonts/Outfit-Bold.ttf")))
text_width = cfg.get("text_width", 780)
rng = random.Random(7)


def secs(v):
    """Seconds or beats ("2b", "1/2b")."""
    if isinstance(v, str) and v.endswith("b"):
        z = v[:-1]
        if "/" in z:
            a, b = z.split("/"); return float(a) / float(b) * beat
        return float(z) * beat
    return float(v)


def cover(im):  # scale + crop to 9:16
    s = max(W / im.width, H / im.height)
    if abs(s - 1) > 1e-6:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H)) if (x or y or im.size != (W, H)) else im


class VideoReader:
    """Streams one scene's frames from a clip (memory stays small even for long recordings)."""
    def __init__(self, file, start, speed):
        self.speed = speed
        self.gen = imageio_ffmpeg.read_frames(str(path(file)), input_params=["-ss", f"{start:.3f}"], output_params=["-r", str(fps)])
        meta = next(self.gen); self.size = meta["size"]
        self.idx, self.cur = -1, None

    def frame(self, t):
        want = int(t * self.speed * fps + 1e-6)
        while self.idx < want:
            try:
                raw = next(self.gen)
            except StopIteration:
                break   # clip ended: hold the last frame
            self.idx += 1; self.cur = raw
        if self.cur is None:
            raise SystemExit("no frames read – check start/clip length")
        return cover(Image.frombytes("RGB", self.size, self.cur))


stills = {k: cover(Image.open(path(q["image"])).convert("RGB")) for k, q in cfg["sources"].items() if "image" in q}


def crop(im, cx, cy, w):
    if (cx, cy, w) == (W / 2, H / 2, W):
        return im
    h = w * H / W
    x0 = min(max(cx - w / 2, 0), W - w)
    y0 = min(max(cy - h / 2, 0), H - h)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC)


def rgb_shift(im, d):
    r, g, b = im.split()
    return Image.merge("RGB", (ImageChops.offset(r, d, 0), g, ImageChops.offset(b, -d, 0)))


def glitch(im, strength):
    im = rgb_shift(im, int(18 * strength) + 4)
    for _ in range(int(3 + 5 * strength)):  # shifted stripes
        y = rng.randrange(0, H - 40); h = rng.randrange(12, 90)
        stripe = im.crop((0, y, W, min(y + h, H)))
        im.paste(ImageChops.offset(stripe, rng.randint(-80, 80), 0), (0, y))
    return im


def whip(im, offset, blur):  # whip pan: slide in sideways with motion blur
    out = ImageChops.offset(im, int(offset), 0)
    n = 6
    for k in range(1, n):
        out = Image.blend(out, ImageChops.offset(im, int(offset + blur * k / n), 0), 1 / (k + 1))
    return out


_fonts = {}
def font(size):
    if size not in _fonts: _fonts[size] = ImageFont.truetype(font_file, size)
    return _fonts[size]


def text_layer(entries, t):
    """Each line centred, black outline + soft shadow; new lines pop in (small → overshoot → normal)."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for e in entries:
        at = secs(e["at"]) if "at" in e else -1
        if t < at or ("until" in e and t >= secs(e["until"])): continue
        line = e["text"]
        g = e.get("size", 150)
        wide = ImageDraw.Draw(layer).textbbox((0, 0), line, font=font(g), stroke_width=round(g * 0.075))
        g = min(g, int(g * e.get("width", text_width) / (wide[2] - wide[0])))  # never wider than the safe width
        k = min((t - at) / 0.15, 1) if at >= 0 else 1
        scale = 0.6 + 0.4 * k + 0.3 * math.sin(math.pi * k)
        f = font(max(round(g * scale), 8))
        edge = max(round(g * scale * 0.075), 4)
        box = ImageDraw.Draw(layer).textbbox((0, 0), line, font=f, stroke_width=edge)
        bw, bh = box[2] - box[0], box[3] - box[1]
        x, y = e.get("x", W / 2) - bw / 2 - box[0], e.get("y", 760) - bh / 2 - box[1]
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).text((x + 8, y + 12), line, font=f, fill=(0, 0, 0, 150), stroke_width=edge, stroke_fill=(0, 0, 0, 150))
        layer.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
        ImageDraw.Draw(layer).text((x, y), line, font=f, fill=COLORS.get(e.get("color", "white"), e.get("color")),
                                   stroke_width=edge, stroke_fill="#000000")
    return layer


_overlays = {}
def overlay_img(p):
    if p not in _overlays: _overlays[p] = Image.open(path(p)).convert("RGBA")
    return _overlays[p]


scenes = cfg["scenes"]
bounds = [0]  # cut points from absolute time, so cuts don't drift off the beat
for sc in scenes: bounds.append(bounds[-1] + secs(sc["duration"]))
frames = [round(b * fps) for b in bounds]
total = frames[-1] / fps
target = path(cfg["output"]); target.parent.mkdir(parents=True, exist_ok=True)
tracks = list(cfg.get("audio", []))
if cfg.get("music"):
    tracks.append({"file": cfg["music"], "start": cfg.get("music_start", 0), "volume": cfg.get("volume", 0.9)})
inputs, filters = [], []
for k, tr in enumerate(tracks):
    inputs += ["-i", str(path(tr["file"]))]
    at = secs(tr.get("at", 0)); length = secs(tr["duration"]) if "duration" in tr else total - at
    # resample first, then trim and renumber the samples: clean timestamps from 0 even for files that start at 0.023 s
    chain = ["aresample=44100", "aformat=sample_rates=44100:channel_layouts=stereo",
             f"atrim=start={tr.get('start', 0):.3f}:duration={length:.3f}", "asetpts=N/SR/TB", f"volume={tr.get('volume', 0.9)}",
             f"afade=t=in:d={tr.get('fade_in', 0.03)}", f"afade=t=out:st={max(length - tr.get('fade_out', 0.05), 0):.3f}:d={tr.get('fade_out', 0.05)}",
             f"adelay=delays={round(at * 1000)}:all=1", "asetpts=N/SR/TB"]   # renumber again: ffmpeg 7 adelay can emit broken pts
    filters.append(f"[{k + 1}:a]{','.join(chain)}[s{k}]")
if tracks:
    filters.append("".join(f"[s{k}]" for k in range(len(tracks))) +
                   f"amix=inputs={len(tracks)}:normalize=0,apad=whole_dur={total:.3f},afade=t=out:st={max(total - 0.8, 0):.3f}:d=0.8[mix]")
    audio = [*inputs, "-filter_complex", ";".join(filters), "-map", "0:v", "-map", "[mix]"]
else:
    audio = ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest"]
proc = subprocess.Popen([ff, "-loglevel", "error", "-y",
    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", *audio,
    "-c:v", "libx264", "-preset", "medium", "-crf", str(cfg.get("crf", 19)), "-pix_fmt", "yuv420p", "-r", str(fps),
    "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.3f}", "-movflags", "+faststart", str(target)], stdin=subprocess.PIPE)

frame_no, prev_last = 0, None
for nr, sc in enumerate(scenes):
    n = frames[nr + 1] - frames[nr]
    reader = None
    if "card" in sc:
        still = cover(Image.open(path(sc["card"])).convert("RGB"))
    elif sc["source"] in stills:
        still = stills[sc["source"]]
    else:
        still = None
        reader = VideoReader(cfg["sources"][sc["source"]]["video"], sc.get("start", 0), sc.get("speed", 1))
    frm = sc.get("from") or [W / 2, H / 2, W]
    to = sc.get("to") or frm
    trans = sc.get("in", "")
    fade_n = max(1, round(sc.get("fade", 0.3) * fps))
    last = None
    for i in range(n):
        t = i / fps; t_abs = frame_no / fps; k = i / max(n - 1, 1)
        k = 1 - (1 - k) ** 3  # fast start, soft landing
        cx, cy, w = [a + (b - a) * k for a, b in zip(frm, to)]
        if sc.get("punch"):  # zoom punch on every beat
            since = (t_abs - drop) % beat
            w /= 1 + sc["punch"] * math.exp(-since / 0.09)
        if sc.get("shake"):
            a = sc["shake"] * w / W
            cx += rng.uniform(-a, a); cy += rng.uniform(-a, a)
        base = reader.frame(t) if reader else still
        img = crop(base, cx, cy, w)
        if "whip" in trans and i < 5:
            r = (1 - i / 5) ** 2
            img = whip(img, -W * 0.35 * r, W * 0.25 * r)
        if ("glitch" in trans and i < 4) or (sc.get("glitch") and rng.random() < sc["glitch"]):
            img = glitch(img, 1 - i / 6 if i < 4 else 0.5)
        if sc.get("punch") and (t_abs - drop) % beat < 1.5 / fps:
            img = rgb_shift(img, 10)
        if sc.get("darken"):
            img = Image.blend(img, Image.new("RGB", (W, H), "black"), sc["darken"])
        if sc.get("overlay"):
            img = img.convert("RGBA")
            for o in sc["overlay"]:
                at = secs(o.get("at", 0)); until = secs(o["until"]) if "until" in o else 1e9
                if t < at or t >= until: continue
                fd = o.get("fade", 0.25)
                alpha = min(1, (t - at) / fd if fd and at > 0 else 1, (until - t) / fd if fd and until < 1e9 else 1)
                ov = overlay_img(o["image"])
                if alpha < 1:
                    ov = ov.copy(); ov.putalpha(ov.getchannel("A").point(lambda v: int(v * alpha)))
                img.alpha_composite(ov)
            img = img.convert("RGB")
        if sc.get("text"):
            img = img.convert("RGBA"); img.alpha_composite(text_layer(sc["text"], t)); img = img.convert("RGB")
        if trans == "fade" and prev_last is not None and i < fade_n:
            img = Image.blend(prev_last, img, (i + 1) / (fade_n + 1))
        if "flash" in trans and i < 4:
            img = Image.blend(img, Image.new("RGB", (W, H), "white"), [0.95, 0.6, 0.3, 0.1][i])
        proc.stdin.write(img.tobytes())
        last = img
        frame_no += 1
    prev_last = last
proc.stdin.close(); proc.wait()
print("✓", target, f"{total:.2f} s")
