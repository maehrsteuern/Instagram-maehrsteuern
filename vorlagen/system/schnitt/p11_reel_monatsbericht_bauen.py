"""Erzeugt p11_reel_monatsbericht.json (Schnitt für montage.py) – Version 2 vom 06.10.:
neuer Sprechtext (kürzer, Hook „Zwei verdammte Stunden“), Aufnahme 06.10. 08:29 (Take B), Zeiten = Sekunden in ton/stimme_final.flac."""
import json
from pathlib import Path

P = "../../posts/11_2026-10-07_reel_monatsbericht"
ENDE = 27.0
ZOOM = {"von": [540, 960, 1080], "nach": [540, 930, 1010]}
# (Bild, von, bis, Untertitel [(Text, von, bis)], Extra)
SZENEN = [
    ("hook2", 0.0, 5.1, [("Zwei verdammte Stunden", 0.0, 1.42), ("jeden Monat,", 1.42, 2.6), ("nur Copy-Paste", 2.6, 3.5),
                         ("für einen einzigen Bericht.", 3.5, 5.1)], {"von": [540, 960, 1080], "nach": [540, 900, 980]}),
    ("knopf", 5.1, 8.15, [("Heute drück ich einen Knopf", 5.1, 6.6), ("und so geht's:", 6.6, 8.15)], {"rein": "whip"}),
    ("schritt1", 8.15, 12.2, [("Eins:", 8.15, 8.8), ("Der Code zieht sich die", 8.8, 9.75), ("Summen- und Saldenliste", 9.75, 10.74),
                              ("direkt aus dem Export.", 10.74, 12.2)], {}),
    ("schritt2", 12.2, 16.9, [("Zwei: Er stimmt ab.", 12.2, 13.7), ("Passt was nicht, stoppt er,", 13.7, 15.18),
                              ("bevor ein falscher Bericht rausgeht.", 15.18, 16.9)], {}),
    ("schritt3", 16.9, 21.5, [("Drei: Er baut den Bericht.", 16.9, 18.82), ("Tabellen, Diagramm, PDF –", 18.82, 20.7),
                              ("fertig.", 20.7, 21.5)], {}),
    ("ende2", 21.5, ENDE, [("Das war Nummer eins", 21.5, 22.7), ("aus meinem letzten Video.", 22.7, 23.9),
                           ("Welche Nummer willst du", 23.9, 24.9), ("als Nächstes sehen?", 24.9, 25.8), ("Schreib's mir.", 25.8, ENDE)], {}),
]
AKZENTE = {"schritt2": [("STOPP", 14.62, "rot")], "schritt3": [("PDF ✓", 20.22, "gruen")]}

szenen, quellen = [], {}
for bild, a, b, texte, extra in SZENEN:
    quellen[bild] = {"datei": f"{P}/bausteine/{bild}.png"}
    t = [{"wort": w, "groesse": 66, "y": 1330, "ab": round(max(x - a, 0), 2), "bis": round(y - a, 2)} for w, x, y in texte]
    for w, x, f in AKZENTE.get(bild, []):
        t.append({"wort": w, "farbe": f, "groesse": 115, "y": 1222, "ab": round(x - a, 2), "bis": round(b - a, 2)})
    sz = {"quelle": bild, "dauer": round(b - a, 3), "text": t, **ZOOM}
    sz.update(extra)
    szenen.append(sz)

cfg = {
    "ausgabe": f"{P}/reel.mp4", "fps": 30, "quellen": quellen, "szenen": szenen,
    "ton": [
        {"datei": f"{P}/ton/stimme_final.flac", "ab": 0, "lautstaerke": 1.0, "ein": 0.02, "aus": 0.3},
        {"datei": "../../musik/atmo/uhr_ticken.mp3", "ab": 0.0, "start": 0.3, "dauer": 5.0, "lautstaerke": 0.14, "ein": 0.05, "aus": 0.4},
        {"datei": "../../musik/atmo/fehlerton.mp3", "ab": 14.0, "dauer": 0.6, "lautstaerke": 0.18},
        {"datei": "../../musik/06_runway_lofi_ruhig.mp3", "ab": 5.1, "start": 0, "lautstaerke": 0.1, "ein": 1.0},
    ],
}
Path(__file__).with_name("p11_reel_monatsbericht.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
print("✓ p11_reel_monatsbericht.json", round(sum(s["dauer"] for s in szenen), 2), "s")
