"""Cut a calm Reel from still images:  python3 reel.py cuts/<cut>.json

(For recordings, hook text and audio mixes use montage.py – this script is the simple "Ken Burns" variant.)
Scenes run one after another. A scene is either
  {"card": "image.png", "duration": 2.5}                       – full card (hook, end card), slight zoom
  {"source": "app", "from": [cx,cy,w], "to": [cx,cy,w], "duration": 3, "bar": "bar.png"}
                                                              – camera move over a large image (9:16 crop, width w)
     optional: "instant": true – overlay (bar) visible from the first frame (for the hook), otherwise it fades in
               "move": 1.6     – duration of the camera move in seconds (default 0.9)
               "ease": "fast"  – the move starts at full speed (against scrolling away in frame 1)
Omit "from" = continue where the previous scene ended. Card ↔ image cross-fade briefly.
Cut-list keys: "output", "fps", "sources": {"app": {"file": "app.png", "pad_bottom": 300}}, "scenes": [...],
audio: "music": "../../music/file.mp3" (built in, soft fade in/out), "music_start": 4.2 (skip the first seconds), "volume": 0.9.
Without "music" the Reel is silent – pick a sound in the Instagram app instead.
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image
import imageio_ffmpeg

W, H = 1080, 1920
here = Path(__file__).parent
cfg = json.loads(Path(sys.argv[1]).read_text())
fps = cfg.get("fps", 30)
path = lambda p: (here / p).resolve()


def load_source(q):
    im = Image.open(path(q["file"])).convert("RGB")
    extra = q.get("pad_bottom", 0)
    if extra:  # add a plain area at the bottom so the last row can also sit in the middle
        new = Image.new("RGB", (im.width, im.height + extra), im.getpixel((im.width // 2, im.height - 1)))
        new.paste(im, (0, 0)); im = new
    return im


sources = {k: load_source(v) for k, v in cfg.get("sources", {}).items()}
smooth = lambda t: t * t * (3 - 2 * t)


def crop(im, cx, cy, w):
    h = w * H / W
    x0 = min(max(cx - w / 2, 0), im.width - w)
    y0 = min(max(cy - h / 2, 0), im.height - h)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC)


ff = imageio_ffmpeg.get_ffmpeg_exe()
target = path(cfg["output"]); target.parent.mkdir(parents=True, exist_ok=True)
total = sum(sc["duration"] for sc in cfg["scenes"])
if cfg.get("music"):
    start = max(cfg.get("music_start", 0), 0)
    audio = ["-ss", f"{start:.2f}", "-i", str(path(cfg["music"])), "-af",
             f"volume={cfg.get('volume', 0.9)},afade=t=in:d={0.3 if start == 0 else 0.05},afade=t=out:st={max(total - 1.2, 0):.2f}:d=1.2", "-shortest"]
else:
    audio = ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest"]
proc = subprocess.Popen([ff, "-loglevel", "error", "-y",
    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", *audio,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-movflags", "+faststart", str(target)], stdin=subprocess.PIPE)

last, camera, kind_before = None, None, None
for sc in cfg["scenes"]:
    n = round(sc["duration"] * fps)
    kind = "card" if "card" in sc else "source"
    card = Image.open(path(sc["card"])).convert("RGB") if kind == "card" else None
    bar = Image.open(path(sc["bar"])).convert("RGBA") if sc.get("bar") else None
    frm = sc.get("from") or camera
    to = sc.get("to")
    move = min(sc.get("move", 0.9) * fps, n)
    curve = (lambda t: 1 - (1 - t) ** 2) if sc.get("ease") == "fast" else smooth
    for i in range(n):
        t = i / fps
        if kind == "card":
            z = 1 + 0.04 * i / n
            img = crop(card, card.width / 2, card.height / 2, card.width / z)
        else:
            if i < move:
                k = curve(i / move); c = [a + (b - a) * k for a, b in zip(frm, to)]
            else:  # slow drift
                k = (i - move) / max(n - move, 1); c = [to[0], to[1], to[2] * (1 - 0.03 * k)]
            camera = c
            img = crop(sources[sc["source"]], *c)
            if bar is not None:
                a = 1 if sc.get("instant") else min(max((t - 0.25) / 0.3, 0), 1)
                if a > 0:
                    b = bar.copy(); b.putalpha(b.getchannel("A").point(lambda v: int(v * a)))
                    img = img.convert("RGBA"); img.alpha_composite(b); img = img.convert("RGB")
        if last is not None and kind != kind_before and t < 0.3:  # cross-fade card <-> image
            img = Image.blend(last, img, t / 0.3)
        proc.stdin.write(img.tobytes())
        end = img
    last, kind_before = end, kind
    if kind == "source":
        camera = [to[0], to[1], to[2] * 0.97]
proc.stdin.close(); proc.wait()
print("✓", target)
