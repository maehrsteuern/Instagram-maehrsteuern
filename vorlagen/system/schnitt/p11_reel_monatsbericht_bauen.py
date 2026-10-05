"""Erzeugt p11_reel_monatsbericht.json (Schnitt für montage.py) aus der geschnittenen Sprachnachricht vom 05.10.
Zeiten = Sekunden in ton/stimme_final.flac (aus 4 Teilen der Rohaufnahme zusammengesetzt, siehe ton/schnitte.json)."""
import json
from pathlib import Path

P = "../../posts/11_2026-10-07_reel_monatsbericht"
ENDE = 39.6
ZOOM = {"von": [540, 960, 1080], "nach": [540, 930, 1010]}
# (Bild, von, bis, Untertitel [(Text, von, bis)], Extra)
SZENEN = [
    ("hook", 0.0, 4.45, [("Nummer eins", 0.0, 0.94), ("aus meinem letzten Reel:", 0.94, 1.8), ("der Monatsbericht.", 1.8, 2.8),
                         ("Ich zeig dir, wie ich das mache.", 2.8, 4.45)], {}),
    ("vorher", 4.45, 14.35, [("Früher: jeden Monat dieselbe Runde.", 4.45, 7.3), ("Exportieren, kopieren, einfügen,", 7.3, 10.1),
                             ("Formeln runterziehen.", 10.1, 11.3), ("Fast zwei Stunden", 11.3, 12.3),
                             ("und am Ende stimmt trotzdem irgendwas nicht.", 12.3, 14.35)],
     {"von": [540, 960, 1080], "nach": [540, 990, 990]}),
    ("hook", 14.35, 16.35, [("Heute sind es drei Schritte.", 14.35, 16.35)], {"rein": "whip"}),
    ("schritt1", 16.35, 21.55, [("Eins:", 16.35, 17.0), ("Der Code liest die", 17.0, 17.9), ("Summen- und Saldenliste ein.", 17.9, 19.3),
                                ("Direkt den Export.", 19.3, 20.35), ("Ich fass nichts an.", 20.35, 21.55)], {}),
    ("schritt2", 21.55, 27.76, [("Zwei: Er stimmt ab.", 21.55, 23.15), ("Passt die Summe nicht,", 23.15, 24.0),
                                ("hört er auf und sagt mir, um wie viel –", 24.0, 26.1), ("bevor ein falscher Bericht rausgeht.", 26.1, 27.76)], {}),
    ("schritt3", 27.76, 32.9, [("Drei: Er baut den Bericht.", 27.76, 30.15), ("Tabellen, Diagramm,", 30.15, 31.48),
                               ("fertiges PDF.", 31.48, 32.9)], {}),
    ("ende", 32.9, ENDE, [("Daten rein.", 32.9, 33.8), ("Einen Klick.", 33.8, 34.55), ("Fertig.", 34.55, 35.4),
                          ("Speichert ihr das", 35.4, 36.4), ("und schreibt mir, welche Nummer", 36.4, 37.85),
                          ("als Nächstes dran ist.", 37.85, ENDE)], {}),
]
AKZENTE = {  # große Schlagworte als Verstärkung des Gesagten (Zeit im Audio, Farbe)
    "vorher": [("~2 Stunden", 11.44, "rot")], "schritt2": [("STOPP", 24.0, "rot")], "schritt3": [("PDF ✓", 31.9, "gruen")],
}

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
        {"datei": "../../musik/atmo/fehlerton.mp3", "ab": 23.7, "dauer": 0.6, "lautstaerke": 0.18},
        {"datei": "../../musik/06_runway_lofi_ruhig.mp3", "ab": 14.35, "start": 0, "lautstaerke": 0.1, "ein": 1.5},
    ],
}
Path(__file__).with_name("p11_reel_monatsbericht.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
print("✓ p11_reel_monatsbericht.json", round(sum(s["dauer"] for s in szenen), 2), "s")
