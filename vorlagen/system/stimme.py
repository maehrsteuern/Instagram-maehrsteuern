"""Sprachaufnahme fürs Reel aufbereiten: Versprecher raus, Pausen kürzen, Lautheit auf −18 LUFS.

    from stimme import aufbereiten
    woerter = aufbereiten("aufnahmen/x.mp3", woerter_json, "posts/…/ton/stimme.flac", raus=[(0.0, 1.42)], text="Eine Zeile …")

woerter_json = Wortliste aus faster-whisper ([wort, start, ende, wahrscheinlichkeit], Sekunden in der Originaldatei).
raus = Zeitbereiche (Original) die wegfallen – Kanten exakt setzen (Pegel prüfen), sie werden ohne Rand geschnitten. Pausen zwischen Wörtern werden auf höchstens PAUSE s gekürzt (Raumton bleibt).
text = gegengelesener Wortlaut (String oder Liste), gleich viele Wörter wie die behaltenen Whisper-Wörter (ersetzt deren Schreibweise).
Gibt die Wörter mit neuen Zeiten zurück (Sekunden in der fertigen Datei). Feste Verstärkung statt loudnorm (kein Pumpen).
"""
import json, re, subprocess
from pathlib import Path
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
PAUSE, VOR, NACH = 0.30, 0.10, 0.16  # max. Pause, Luft vor dem ersten / nach dem letzten Wort eines Blocks
HART_LUECKE = 0.14  # Stille nach einem harten Schnitt (raus-Kante mitten im Redefluss)
ZIEL_LUFS = -18.0


def lufs(datei):
    out = subprocess.run([FF, "-hide_banner", "-i", str(datei), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])


def aufbereiten(quelle, woerter, ziel, raus=(), text=None):
    behalten = [w for w in woerter if not any(a <= (w[1] + w[2]) / 2 < b for a, b in raus)]
    if text is not None:
        neu = text if isinstance(text, list) else text.split()
        assert len(neu) == len(behalten), f"{len(neu)} Wörter im Text, {len(behalten)} behalten: {[w[0] for w in behalten]}"
        behalten = [[t, *w[1:]] for t, w in zip(neu, behalten)]
    # Blöcke: Wörter mit kurzer Lücke bleiben zusammen, sonst neuer Block (Lücke wird gekürzt / Ausgeschnittenes fällt weg)
    bloecke = []
    for i, w in enumerate(behalten):
        mitte = lambda x: (x[1] + x[2]) / 2
        geschnitten = i and any(mitte(behalten[i - 1]) < a and b <= mitte(w) for a, b in raus)  # Schnitt liegt zwischen den Wörtern
        if bloecke and not geschnitten and w[1] - bloecke[-1][-1][2] <= PAUSE:
            bloecke[-1].append(w)
        else:
            bloecke.append([w])
    stuecke, ergebnis, t = [], [], 0.0
    for blk in bloecke:
        a, b = max(blk[0][1] - VOR, 0), blk[-1][2] + NACH
        # Schnittkanten aus raus sind hart: nichts aus dem Ausgeschnittenen mitnehmen (sonst hört man Wortreste, z. B. „300 Ze… oder Zeilen“)
        a = max([a] + [y for x, y in raus if y <= mitte(blk[0])])
        hart = [x for x, y in raus if x >= mitte(blk[-1])]
        if hart and min(hart) - blk[-1][2] < PAUSE:  # Schnitt mitten im Redefluss: genau bis zur Kante, danach kurz Luft
            b, luecke = min(hart), HART_LUECKE  # sonst verschmelzen die Wörter („300|Zeilen“ → „teilen“)
        else:
            luecke = 0
        if stuecke: a = max(a, stuecke[-1][1])  # nie überlappen
        for w in blk: ergebnis.append([w[0], round(t + w[1] - a, 3), round(t + w[2] - a, 3)])
        stuecke.append((a, b, luecke)); t += b - a + luecke
    teile = [f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st={b - a - 0.02:.3f}:d=0.02,apad=pad_dur={l:.3f}[t{i}]"
             for i, (a, b, l) in enumerate(stuecke)]
    kette = ";".join(teile) + ";" + "".join(f"[t{i}]" for i in range(len(stuecke))) + f"concat=n={len(stuecke)}:v=0:a=1,"
    kette += "highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=1"
    ziel = Path(ziel); ziel.parent.mkdir(parents=True, exist_ok=True)
    roh = ziel.with_suffix(".roh.flac")
    subprocess.run([FF, "-loglevel", "error", "-y", "-i", str(quelle), "-filter_complex", kette + ",aformat=sample_rates=44100:channel_layouts=mono",
                    str(roh)], check=True)
    gain = ZIEL_LUFS - lufs(roh)
    subprocess.run([FF, "-loglevel", "error", "-y", "-i", str(roh), "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89:level=false",
                    str(ziel)], check=True)
    roh.unlink()
    ziel.with_suffix(".json").write_text(json.dumps(ergebnis, ensure_ascii=False))
    print(f"✓ {ziel.name}: {t:.2f} s, {lufs(ziel):.1f} LUFS")
    return ergebnis
