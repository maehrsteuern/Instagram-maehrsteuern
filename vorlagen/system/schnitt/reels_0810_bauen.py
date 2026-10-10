"""Baut alle Reels aus Loris' Aufnahmen vom 08.10. (aufnahmen/08.10.2026 10.38–10.44(2).mp3):
Stimme aufbereiten (stimme.py), wörtliche Untertitel, Hook-Text ab 0,3 s, Szenen → schnitt/<id>.json → montage.py.

    cd vorlagen/system/schnitt && python3 reels_0810_bauen.py [id …]

Zeiten in SZENEN/AKZENTE/RAUS = Sekunden in der Originalaufnahme (aus aufnahmen/woerter_small.json).
KORR = gegengelesener Wortlaut: {"Wort": "neu"} oder {"Wort#2": "neu"} (2. Vorkommen); "" = Wort hängt am vorigen.
"""
import json, subprocess, sys
from pathlib import Path

hier = Path(__file__).resolve().parent
sys.path.insert(0, str(hier.parent))
from stimme import aufbereiten, lufs

REPO = hier.parent.parent.parent
AUF = REPO / "aufnahmen"
WOERTER = json.loads((AUF / "woerter_small.json").read_text())
ZOOM = {"von": [540, 960, 1080], "nach": [540, 930, 1010]}  # Bildbereich bleibt über y≈1250 (Untertitel frei)
UT = {"groesse": 62, "y": 1330, "x": 470, "breite": 780}  # Untertitel: unter dem Bildbereich, rechts 150 px frei
MAX_ZEICHEN = 22
SCHLUSS = 0.7  # Standbild nach dem letzten Wort

REELS = {
    "p06_reel_split": dict(
        datei="08.10.2026 10.38.mp3", ordner="posts/06_2026-10-08_reel_split",
        korr={"Excel,": "Excel:", "Tool,": "Tool:", "Schreibt": "Schreib", "Tool#2": "„TOOL“", "DM,": "DM –", "Quelle,": "Quelle.", "das#1": "Das"},
        hook=[("Gleiche Aufgabe.", "weiss"), ("Zwei Wege.", "gelb")],
        video="posts/02_2026-10-06_excel_fehler/edits_paket/1_split_rohvideo.mp4",
        akzente=[(7.34, "#BEZUG!", "rot", 700), (9.04, "fertig ✓", "gruen", 1180)],
        musik=("07_runway_minimal_tech.mp3", 8.10, 0.11),
        atmo=[("tippen_fehlerton.mp3", 3.56, 0.8, 0.7, 0.9), ("fehlerton.mp3", 7.20, 0, 0.6, 0.5), ("uhr_ticken.mp3", 9.84, 0.3, 3.2, 0.25)]),
    "p08_reel_kst_staffel": dict(
        datei="08.10.2026 10.39.mp3", ordner="posts/08_2026-10-09_reel_kst_staffel",
        raus=[(24.81, 25.12)],  # „gestern“ raus – Reel läuft 2 Tage nach dem Karussell (Kanten am Pegel gemessen, 10.10.)
        korr={"Zeile.": "Zelle.", "30": "30", "eingedippt,": "eingetippt,", "Körperschutzsteuer": "Körperschaftsteuer", "am": "um",
              "rechten": "Rechenweg", "Weg": "", "willst,": "willst:", "Tool.": "„TOOL“."},
        hook=[("30 % fest", "weiss"), ("eingetippt?", "gelb")],
        szenen=[(0, "tabelle_30prozent", {"von": [540, 960, 1080], "nach": [700, 940, 940]}), (7.58, "karte_staffel", {"rein": "whip"}),
                (12.70, "karte_umkehr", {}), (20.20, "k_staffel", {}), (23.90, "karte_ende", {})],
        akzente=[(18.94, "FALSCH", "rot", 1180)],
        musik=("09_runway_lofi_piano.mp3", 20.20, 0.1),
        atmo=[("tippen_fehlerton.mp3", 4.10, 0.8, 0.8, 0.8), ("fehlerton.mp3", 19.20, 0, 0.6, 0.35)]),
    "p12_reel_zeile": dict(
        datei="08.10.2026 10.42.mp3", ordner="posts/12_2026-10-09_reel_zeile",
        raus=[(17.94, 19.475)],  # Versprecher „Zellen dazukommen oder“ – Kanten am Pegel gemessen (Ende „300“ / Anfang „Zeilen“) („Jutta“ bleibt – erfundene Person, Wunsch Loris 08.10.)
        korr={"Bezugfehler.": "#BEZUG!-Fehler.", "so#1": "summier", "mir": "", "300": "300", "oder#1": "oder|", "Zeilen.": "Zeilen.",
              "2": "2", "5": "5-Dinge-Reel.", "-Dinger": "", "-Real.": "", "wird": "willst", "es#2": "du", "so#2": "", "nächstes": "Nächstes"},
        hook=[("Zeile eingefügt.", "weiss"), ("Summe weg.", "rot")],
        szenen=[(0, "2a", {"von": [540, 960, 1080], "nach": [560, 1000, 900]}), (4.88, "2a", {"von": [540, 930, 1010], "nach": [540, 960, 1080]}),
                (12.06, "2b", {"rein": "whip"}), (21.40, "s_ende2", {})],
        akzente=[(3.72, "#BEZUG!", "rot", 1180), (20.18, "✓ stimmt", "gruen", 1180)],
        musik=("12_runway_pop_electronic.mp3", 12.06, 0.1),
        atmo=[("tippen_fehlerton.mp3", 1.42, 0.8, 0.6, 0.8), ("fehlerton.mp3", 3.60, 0, 0.6, 0.45)]),
    "p13_reel_verknuepfung": dict(
        datei="08.10.2026 10.42(2).mp3", ordner="posts/13_2026-10-11_reel_verknuepfung",
        korr={"Bezugfehler?": "#BEZUG!", "hingen": "hing", "hat": "hatte", "er": "", "Schreibst": "Schreib's", "sofort": "sofort,"},
        hook=[("#BEZUG!", "rot"), ("2 Tage vor Abgabe.", "weiss")],
        szenen=[(0, "v_hook", {"von": [540, 960, 1080], "nach": [580, 930, 1000]}), (6.84, "v_dialog", {}), (11.96, "v_dialog", {"von": [540, 930, 1010], "nach": [540, 960, 1080]}),
                (18.44, "v_pfad", {"rein": "whip"}), (21.22, "v_ende", {})],
        akzente=[(9.84, "umbenannt.", "rot", 1180)],
        musik=("08_runway_chill_house.mp3", 18.44, 0.1),
        atmo=[("uhr_ticken.mp3", 0.6, 0.3, 11.0, 0.22), ("fehlerton.mp3", 5.30, 0, 0.6, 0.4), ("10_runway_spannung.mp3", 6.84, 0, 11.4, 0.06)]),
    "p14_reel_versionen": dict(
        datei="08.10.2026 10.43.mp3", ordner="posts/14_2026-10-12_reel_versionen",
        korr={"Final,#1": "Final.", "Final,#2": "Final", "Final,#3": "final.", "Final,#4": "Final", "3,": "3.", "Final,#5": "Final",
              "Final,#6": "final", "Final,#7": "final", "Final#1": "final –", "weiß": "weiß,", "Richtige": "richtige", "was?": "was.",
              "gestiegen": "gestiegen –", "schief": "schiefgeht,", "geht,": "", "5": "5-Dinge-Reel.", "-Dinge": "", "-Real.": ""},
        hook=[("final_final_v3.xlsx", "rot"), ("Welche gilt?", "gelb")],
        szenen=[(0, "3a", {"von": [540, 960, 1080], "nach": [560, 940, 980]}), (10.72, "3b", {"rein": "whip"}),
                (15.24, "3b", {"von": [540, 930, 1010], "nach": [540, 960, 1080]}), (22.98, "s_ende3", {})],
        akzente=[(20.26, "1 Schritt zurück", "gruen", 1180)],
        musik=("11_runway_future_garage.mp3", 10.72, 0.1),
        atmo=[("tippen_fehlerton.mp3", 1.02, 0.8, 5.2, 0.5)]),
    "p15_reel_rechnungsnummern": dict(
        datei="08.10.2026 10.43(2).mp3", ordner="posts/15_2026-10-13_reel_rechnungsnummern",
        korr={"Minuten": "Minuten.", "und#1": "Und", "Sortieren,": "sortieren,", "Scrollen": "scrollen,", "und#2": "", "Hoffen.": "hoffen.",
              "ihr#1": "jede", "den": "", "Doppelt,": "Doppelt?", "Rot.#1": "Rot.", "Folge,": "Folge?", "Rot.#2": "Auch rot.", "auch": "",
              "Sekunde": "Sekunde.", "und#3": "Und", "Prüfung": "Prüfung –", "und#4": "", "5": "5-Dinge-Reel.", "-Dinger": "", "-Reel.": "",
              "Speichert": "Speicher", "ihr#2": "dir"},
        hook=[("Doppelte Rechnungsnummer?", "rot"), ("Der Prüfer findet sie.", "weiss")],
        szenen=[(0, "4a", {"von": [540, 960, 1080], "nach": [540, 1000, 880]}), (7.94, "4b", {"rein": "whip"}), (17.64, "s_ende4", {})],
        akzente=[(10.46, "DOPPELT", "rot", 1180), (11.80, "LÜCKE", "rot", 1180), (14.06, "1 Sekunde ✓", "gruen", 1180)],
        musik=("07_runway_minimal_tech.mp3", 7.94, 0.1),
        atmo=[("uhr_ticken.mp3", 2.48, 0.3, 4.8, 0.2), ("fehlerton.mp3", 10.40, 0, 0.6, 0.3)]),
    "p16_reel_listen": dict(
        datei="08.10.2026 10.44(2).mp3", ordner="posts/16_2026-10-15_reel_listen",
        korr={"S": "SVERWEIS,", "-Verweis,": "", "runterziehen,": "runterziehen,", "NV": "#NV-Fehler,", "-Fehler,": "", "-Abgleichen": "abgleichen",
              "Heute": "Heute:", "mir": "mir,", "Zehntausend": "10.000", "Zeilen#2": "Zeilen?", "5,": "5 –"},
        hook=[("SVERWEIS. #NV.", "rot"), ("Nochmal.", "weiss")],
        szenen=[(0, "5a", {"von": [540, 960, 1080], "nach": [640, 960, 880]}), (11.62, "5a", {"von": [540, 930, 1010], "nach": [540, 960, 1080]}),
                (15.58, "5b", {"rein": "whip"}), (24.48, "s_ende5", {})],
        akzente=[(21.70, "< 1 Sekunde", "gruen", 1180)],
        musik=("08_runway_chill_house.mp3", 15.58, 0.1),
        atmo=[("tippen_fehlerton.mp3", 6.98, 0.8, 4.0, 0.6), ("fehlerton.mp3", 9.20, 0, 0.6, 0.35)]),
    "p04_reel_mein_weg": dict(
        datei="08.10.2026 10.44.mp3", ordner="posts/04_2026-10-20_reel_mein_weg",
        korr={"heute.": "heute.", "Davor": "Davor:", "KI#1": "KI-Porträt,", "Porträt,": "", "KI#2": "KI-Avatar", "-Avatar": "",
              "X": "×", "-Code.": "Code.", "Mit": "mit", "Schreibt": "Schreib", "Tool": "„TOOL“"},
        hook=[("Mein Weg.", "weiss"), ("Rückwärts.", "gruen")],
        karten={"k1": "assets/marke/karte_1_aktuell_9x16.png", "k2": "assets/marke/karte_2_ki_portrait_9x16.png",
                "k3": "assets/marke/karte_3_ki_avatar_2025_9x16.png", "abspann": "posts/04_2026-10-20_reel_mein_weg/bausteine/abspann.png"},
        szenen=[(0, "k1", {"von": [540, 960, 1080], "nach": [540, 900, 960]}), (3.18, "k2", {"rein": "whip", "nach": [540, 940, 1010]}),
                (6.72, "k3", {"nach": [540, 940, 1010]}), (10.20, "k1", {"rein": "whip", "von": [540, 900, 960], "nach": [540, 960, 1080]}),
                (13.08, "abspann", {})],
        akzente=[],
        musik=("09_runway_lofi_piano.mp3", 10.20, 0.11),
        atmo=[("uhr_ticken.mp3", 0.4, 0.3, 9.6, 0.2)]),
}


def korrigieren(woerter, korr):
    zaehler, aus = {}, []
    for w in woerter:
        zaehler[w[0]] = zaehler.get(w[0], 0) + 1
        neu = korr.get(f"{w[0]}#{zaehler[w[0]]}", korr.get(w[0], w[0]))
        aus.append([neu, *w[1:]])
    return aus


def zeilen(woerter):
    """Untertitel-Zeilen: ≤ MAX_ZEICHEN, Umbruch bevorzugt nach Satzzeichen; ""-Wörter hängen am vorigen."""
    tok = []
    for w, a, b in woerter:
        if w == "" and tok: tok[-1][2] = b
        elif w: tok.append([w, a, b])
    out, akt = [], []
    for w in tok:
        text = " ".join(x[0] for x in akt + [w])
        if akt and (len(text) > MAX_ZEICHEN or akt[-1][0][-1] in ".?!:–|"):
            out.append(akt); akt = []
        akt.append(w)
    if akt: out.append(akt)
    return [(" ".join(x[0] for x in z).replace("|", ""), z[0][1], z[-1][2]) for z in out]  # "|" am Wort = Zeilenumbruch erzwingen


def neue_zeit(t_orig, orig, neu):
    """Originalzeit → Zeit in der aufbereiteten Stimme (über das erste Wort ab t_orig)."""
    for o, n in zip(orig, neu):
        if (o[1] + o[2]) / 2 >= t_orig: return max(n[1] - 0.08, 0)
    return neu[-1][2]


def bauen(rid, r):
    ordner = REPO / r["ordner"]
    roh = WOERTER[r["datei"]]
    behalten = [w for w in roh if not any(a <= (w[1] + w[2]) / 2 < b for a, b in r.get("raus", []))]
    text = [x[0] or "·" for x in korrigieren(behalten, r["korr"])]
    neu = aufbereiten(AUF / r["datei"], roh, ordner / "ton" / "stimme.flac", raus=r.get("raus", []), text=text)
    for w in neu:
        if w[0] == "·": w[0] = ""
    ende = round(neu[-1][2] + SCHLUSS, 2)
    ut = zeilen(neu)
    for i, (z, a, b) in enumerate(ut):  # Zeile steht bis zur nächsten (ohne Flackern in kurzen Pausen)
        ut[i] = (z, a, ut[i + 1][1] if i + 1 < len(ut) and ut[i + 1][1] - b < 0.8 else b + 0.35)
    if "video" in r:
        quellen = {"split": {"video": f"../../{r['video']}"}}
        dauer_video = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(REPO / r["video"])],
                                           capture_output=True, text=True).stdout)
        abschnitte = [(0, ende - 2.2, "split", {"tempo": round((dauer_video - 0.4) / (ende - 2.2), 3)}),
                      (ende - 2.2, ende, "split", {"ab": dauer_video - 0.4, "tempo": 0, "abdunkeln": 0.55})]
    else:
        karten = r.get("karten", {})
        quellen = {k: {"datei": f"../../{karten.get(k, r['ordner'] + '/bausteine/' + k + '.png')}"} for _, k, _ in r["szenen"]}
        starts = [neue_zeit(t, behalten, neu) if t else 0 for t, _, _ in r["szenen"]]
        abschnitte = [(a, (starts[i + 1] if i + 1 < len(starts) else ende), k, ex) for i, (a, (_, k, ex)) in enumerate(zip(starts, r["szenen"]))]
    akzente = [(neue_zeit(t, behalten, neu), w, f, y) for t, w, f, y in r.get("akzente", [])]
    szenen = []
    for nr, (a, b, k, ex) in enumerate(abschnitte):
        t = [{"wort": z, **UT, "ab": round(max(x - a, 0), 2), "bis": round(y - a, 2)} for z, x, y in ut if x < b and y > a]
        for z, x, y in ut:  # Zeile, die vor dem Szenenwechsel begann, läuft ohne Aufpoppen weiter
            if x < a < y: t[[e["wort"] for e in t].index(z)].pop("ab", None)
        if nr == 0:
            for j, (z, f) in enumerate(r["hook"]):
                t.append({"wort": z, "farbe": f, "groesse": 118, "y": 700 + j * 150, "x": 470, "breite": 820, "ab": 0.3 + j * 0.6,
                          "bis": round(min(b - a, 3.6), 2)})
        for x, w, f, y in akzente:
            if a <= x < b: t.append({"wort": w, "farbe": f, "groesse": 104, "y": y, "x": 470, "breite": 780, "ab": round(x - a, 2), "bis": round(min(x - a + 1.6, b - a), 2)})
        sz = {"quelle": k, "dauer": round(b - a, 3), "text": t}
        sz.update({**ZOOM} if "video" not in r else {})
        if nr == 0 and "video" not in r: sz["abdunkeln"] = 0.25
        sz.update(ex)
        szenen.append(sz)
    m_datei, m_ab, m_vol = r["musik"]
    ton = [{"datei": f"../../{r['ordner']}/ton/stimme.flac", "ab": 0, "lautstaerke": 1.0, "ein": 0.02, "aus": 0.3},
           {"datei": f"../../musik/{m_datei}", "ab": round(neue_zeit(m_ab, behalten, neu), 2), "start": 0.4, "lautstaerke": m_vol, "ein": 0.8}]
    for datei, ab, start, dauer, vol in r.get("atmo", []):
        pfad = f"../../musik/{datei}" if datei.startswith("1") else f"../../musik/atmo/{datei}"
        ton.append({"datei": pfad, "ab": round(neue_zeit(ab, behalten, neu), 2), "start": start, "dauer": dauer, "lautstaerke": vol, "ein": 0.05, "aus": 0.3})
    cfg = {"ausgabe": f"../../{r['ordner']}/reel.mp4", "fps": 30, "quellen": quellen, "szenen": szenen, "ton": ton}
    (hier / f"{rid}_0810.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
    subprocess.run([sys.executable, str(hier.parent / "montage.py"), str(hier / f"{rid}_0810.json")], check=True, cwd=hier.parent)
    print(f"  {rid}: {ende:.1f} s · Mix {lufs(ordner / 'reel.mp4'):.1f} LUFS")


if __name__ == "__main__":
    for rid in sys.argv[1:] or REELS:
        bauen(rid, REELS[rid])
