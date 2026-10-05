"""Erzeugt p01_reel_5dinge.json (Schnitt für montage.py) aus den Zeitmarken der Sprachnachricht vom 04.10.
Zeiten unten = Sekunden in der Rohaufnahme; das Reel beginnt bei START."""
import json
from pathlib import Path

START, ENDE = 1.8, 43.0
P = "../../posts/01_2026-10-04_reel_5dinge"
ZOOM = {"von": [540, 960, 1080], "nach": [540, 930, 1010]}
# (Bild, von, bis, Untertitel [(Text, von, bis)], Extra)
SZENEN = [
    ("hook", 1.8, 6.4, [("Ich hab fünf Sachen", 1.8, 3.16), ("aus Excel rausgeschmissen.", 3.16, 4.12),
                         ("Und Nummer eins spart mir am meisten Zeit.", 4.12, 6.4)], {}),
    ("5a", 6.4, 12.0, [("Nummer fünf:", 6.4, 7.6), ("Listen abgleichen.", 7.6, 9.0),
                       ("Früher ein SVERWEIS", 9.0, 10.12), ("und überall #NV-Fehler.", 10.12, 12.0)], {}),
    ("5b", 12.0, 15.5, [("Heute drei Zeilen Code,", 12.0, 13.6), ("egal wie lang die Liste ist.", 13.6, 15.5)], {"rein": "whip"}),
    ("4a", 15.5, 18.0, [("Vier:", 15.5, 16.5), ("Doppelte Rechnungsnummern.", 16.5, 18.0)], {}),
    ("4b", 18.0, 20.8, [("Findet der Code in einer Sekunde,", 18.0, 19.5), ("nicht erst der Prüfer.", 19.5, 20.8)], {}),
    ("3a", 20.8, 22.9, [("Drei:", 20.8, 21.8), ("Wer hat was geändert?", 21.8, 22.9)], {}),
    ("3b", 22.9, 24.6, [("Jede Version bleibt gespeichert.", 22.9, 24.6)], {}),
    ("3a", 24.6, 28.0, [("Schluss mit „final_final_v3“.", 24.6, 28.0)], {"von": [540, 880, 1080], "nach": [560, 900, 920]}),
    ("2a", 28.0, 30.84, [("Zwei:", 28.0, 29.4), ("Jemand fügt eine Zeile ein", 29.4, 30.84)], {}),
    ("2b", 30.84, 31.98, [("und nichts geht kaputt.", 30.84, 31.98)], {}),
    ("1a", 31.98, 34.1, [("Und eins:", 31.98, 32.9), ("Der Monatsbericht.", 32.9, 34.1)], {}),
    ("1b", 34.1, 38.4, [("Daten rein.", 34.1, 35.1), ("Ein Klick.", 35.1, 36.0), ("Fertig.", 36.0, 36.85),
                        ("Nie wieder Copy-Paste.", 36.85, 38.4)], {}),
    ("ende", 38.4, 43.0, [("Speicher dir das und schreib mir:", 38.4, 40.3), ("Welche Nummer soll ich dir", 40.3, 41.38),
                          ("Schritt für Schritt zeigen?", 41.38, 43.0)], {}),
]
AKZENTE = {  # große Schlagworte als Verstärkung des Gesagten (Rohzeit, Farbe)
    "5a": [("#NV", 10.7, "rot")], "4b": [("in 1 Sekunde", 18.9, "gruen")],
    "2a": [("#BEZUG!", 29.9, "rot")], "1b": [("1 Klick", 35.26, "gruen")],
}

szenen, quellen = [], {}
for bild, a, b, texte, extra in SZENEN:
    quellen[bild] = {"datei": f"{P}/bausteine/{bild}.png"}
    t = [{"wort": w, "groesse": 66, "y": 1440 if bild == "hook" else 1330, "ab": round(max(x - a, 0), 2), "bis": round(y - a, 2)} for w, x, y in texte]
    for w, x, f in AKZENTE.get(bild, []):
        t.append({"wort": w, "farbe": f, "groesse": 115, "y": 1222, "ab": round(x - a, 2), "bis": round(b - a, 2)})
    sz = {"quelle": bild, "dauer": round(b - a, 3), "text": t, **ZOOM}
    sz.update(extra)
    szenen.append(sz)

cfg = {
    "ausgabe": f"{P}/reel.mp4", "fps": 30, "quellen": quellen, "szenen": szenen,
    "ton": [
        {"datei": f"{P}/ton/stimme_roh.m4a", "ab": 0, "start": START, "dauer": ENDE - START, "lautstaerke": 0.8, "ein": 0.05, "aus": 0.4},
        {"datei": "../../musik/06_runway_lofi_ruhig.mp3", "ab": 4.6, "start": 0, "lautstaerke": 0.1, "ein": 1.5},
    ],
}
Path(__file__).with_name("p01_reel_5dinge.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
print("✓ p01_reel_5dinge.json", round(sum(s["dauer"] for s in szenen), 2), "s")
