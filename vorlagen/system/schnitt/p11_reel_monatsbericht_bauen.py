"""Erzeugt p11_reel_monatsbericht.json (Schnitt für montage.py) – Version 3 vom 06.10.:
neuer Sprechtext (kürzer, Hook „Zwei verdammte Stunden“), Aufnahme 06.10. 09:02 (letzter Durchgang, Satz „Weil so viele …“ rausgeschnitten, Atmer raus, Pausen mit Raumton gefüllt, feste Verstärkung statt loudnorm), Zeiten = Sekunden in ton/stimme_final.flac."""
import json
from pathlib import Path

P = "../../posts/11_2026-10-07_reel_monatsbericht"
ENDE = 30.15
ZOOM = {"von": [540, 960, 1080], "nach": [540, 930, 1010]}
# (Bild, von, bis, Untertitel [(Text, von, bis)], Extra)
SZENEN = [
    ("hook2", 0.0, 5.90, [("Zwei verdammte Stunden", 0.0, 1.85), ("jeden Monat.", 1.85, 2.93), ("Nur Copy-Paste", 2.93, 3.95),
                          ("für einen einzigen Bericht.", 3.95, 5.90)], {"von": [540, 960, 1080], "nach": [540, 900, 980]}),
    ("knopf", 5.90, 9.60, [("Heute drücke ich einen Knopf.", 5.90, 8.15), ("Und zwar drei Schritte.", 8.15, 9.60)], {"rein": "whip"}),
    ("schritt1", 9.60, 13.45, [("Der Code zieht sich die", 9.60, 11.05), ("Summen- und Saldenliste", 11.05, 12.19),
                              ("direkt aus dem Export.", 12.19, 13.45)], {}),
    ("schritt2", 13.45, 18.50, [("Danach stimmt er ihn ab.", 13.45, 15.00), ("Passt was nicht, stoppt er –", 15.00, 16.43),
                               ("bevor ein falscher Bericht rausgeht.", 16.43, 18.50)], {}),
    ("schritt3", 18.50, 24.40, [("Und der letzte Punkt:", 18.50, 19.65), ("Er baut den Bericht.", 19.65, 21.10),
                                ("Tabellen, Diagramm, PDF.", 21.10, 23.45), ("Fertig.", 23.45, 24.40)], {}),
    ("ende2", 24.40, ENDE, [("Das war Nummer eins", 24.40, 25.29), ("aus meinem letzten Video.", 25.29, 26.55),
                            ("Welche Nummer willst du", 26.55, 27.61), ("als Nächstes sehen?", 27.61, 28.65),
                            ("Schreib es mir gerne.", 28.65, ENDE)], {}),
]
AKZENTE = {"schritt2": [("STOPP", 15.93, "rot")], "schritt3": [("PDF ✓", 22.72, "gruen")]}

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
        {"datei": "../../musik/atmo/fehlerton.mp3", "ab": 15.15, "dauer": 0.6, "lautstaerke": 0.18},
        {"datei": "../../musik/06_runway_lofi_ruhig.mp3", "ab": 5.9, "start": 0, "lautstaerke": 0.1, "ein": 1.0},
    ],
}
Path(__file__).with_name("p11_reel_monatsbericht.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
print("✓ p11_reel_monatsbericht.json", round(sum(s["dauer"] for s in szenen), 2), "s")
