"""Erzeugt p11_reel_monatsbericht.json (Schnitt für montage.py) – Version 3 vom 06.10.:
neuer Sprechtext (kürzer, Hook „Zwei verdammte Stunden“), Aufnahme 06.10. 09:02 (letzter Durchgang, Satz „Weil so viele …“ rausgeschnitten, Atmer stumm), Zeiten = Sekunden in ton/stimme_final.flac."""
import json
from pathlib import Path

P = "../../posts/11_2026-10-07_reel_monatsbericht"
ENDE = 30.0
ZOOM = {"von": [540, 960, 1080], "nach": [540, 930, 1010]}
# (Bild, von, bis, Untertitel [(Text, von, bis)], Extra)
SZENEN = [
    ("hook2", 0.0, 5.75, [("Zwei verdammte Stunden", 0.0, 1.7), ("jeden Monat.", 1.7, 2.78), ("Nur Copy-Paste", 2.78, 3.8),
                          ("für einen einzigen Bericht.", 3.8, 5.75)], {"von": [540, 960, 1080], "nach": [540, 900, 980]}),
    ("knopf", 5.75, 9.45, [("Heute drücke ich einen Knopf.", 5.75, 8.0), ("Und zwar drei Schritte.", 8.0, 9.45)], {"rein": "whip"}),
    ("schritt1", 9.45, 13.3, [("Der Code zieht sich die", 9.45, 10.9), ("Summen- und Saldenliste", 10.9, 12.04),
                              ("direkt aus dem Export.", 12.04, 13.3)], {}),
    ("schritt2", 13.3, 18.35, [("Danach stimmt er ihn ab.", 13.3, 14.85), ("Passt was nicht, stoppt er –", 14.85, 16.28),
                               ("bevor ein falscher Bericht rausgeht.", 16.28, 18.35)], {}),
    ("schritt3", 18.35, 24.25, [("Der letzte Punkt:", 18.35, 19.5), ("Er baut den Bericht.", 19.5, 20.95),
                                ("Tabellen, Diagramm, PDF.", 20.95, 23.3), ("Fertig.", 23.3, 24.25)], {}),
    ("ende2", 24.25, ENDE, [("Das war Nummer eins", 24.25, 25.14), ("aus meinem letzten Video.", 25.14, 26.4),
                            ("Welche Nummer willst du", 26.4, 27.46), ("als Nächstes sehen?", 27.46, 28.5),
                            ("Schreib es mir gerne.", 28.5, ENDE)], {}),
]
AKZENTE = {"schritt2": [("STOPP", 15.78, "rot")], "schritt3": [("PDF ✓", 22.54, "gruen")]}

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
        {"datei": "../../musik/atmo/uhr_ticken.mp3", "ab": 0.0, "start": 0.3, "dauer": 5.6, "lautstaerke": 0.14, "ein": 0.05, "aus": 0.4},
        {"datei": "../../musik/atmo/fehlerton.mp3", "ab": 15.0, "dauer": 0.6, "lautstaerke": 0.18},
        {"datei": "../../musik/06_runway_lofi_ruhig.mp3", "ab": 5.75, "start": 0, "lautstaerke": 0.1, "ein": 1.0},
    ],
}
Path(__file__).with_name("p11_reel_monatsbericht.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
print("✓ p11_reel_monatsbericht.json", round(sum(s["dauer"] for s in szenen), 2), "s")
