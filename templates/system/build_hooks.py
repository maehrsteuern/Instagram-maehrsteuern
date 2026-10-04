"""Hook-Bibliothek bauen:  python3 hooks_bauen.py [h01 h05 …]

Jeder Hook ist ein fertiger Einstieg (2–3 s, 1080x1920) mit Outline-Text ab 0,3 s und Atmo – ohne Musik,
damit er vor jedes Reel passt (Regeln: strategie/09_reel_regeln.md). Schreibt je Hook eine Schnittdatei nach
schnitt/hooks/ und rendert sie mit montage.py nach ../hooks/. Übersicht: ../hooks/README.md.
"""
import json, subprocess, sys
from pathlib import Path

hier = Path(__file__).parent
Q = {  # Quellen relativ zu vorlagen/system
    "ki_blick":   "../../posts/01_2026-10-04_reel_ampel/bausteine/hook_ki.mp4",
    "tabelle":    "../hooks/bausteine/karte_oben_tabelle.mp4",
    "tool":       "../hooks/bausteine/karte_unten_tool.mp4",
    "gewst":      "../../posts/03_2026-10-13_gewst_hinzurechnung/aufnahme_hinzurechnung.mp4",
    "ampel":      "../../posts/01_2026-10-04_reel_ampel/bausteine/aufnahme_gelb_gruen.mp4",
    "ki_hand":    "../hooks/bausteine/ki_taschenrechner.mp4",
    "ki_buero":   "../hooks/bausteine/ki_buero_abend.mp4",
    "ki_tabelle": "../hooks/bausteine/ki_ueber_schulter.mp4",
}
A = "../../musik/atmo/"
tippen = lambda ab, dauer=0.45: {"datei": A + "tippen_fehlerton.mp3", "ab": ab, "start": 0.8, "dauer": dauer, "lautstaerke": 1.2, "aus": 0.08}
fehler = lambda ab: {"datei": A + "fehlerton.mp3", "ab": ab, "dauer": 0.6, "lautstaerke": 0.85}
uhr = lambda ab, dauer: {"datei": A + "uhr_ticken.mp3", "ab": ab, "start": 0.3, "dauer": dauer, "lautstaerke": 1.1, "aus": 0.2}
lofi = lambda ab: {"datei": "../../musik/06_runway_lofi_ruhig.mp3", "ab": ab, "lautstaerke": 0.6, "ein": 0.1}
T = lambda wort, y, ab=None, farbe="weiss", groesse=110: {k: v for k, v in
     {"wort": wort, "y": y, "ab": ab, "farbe": farbe, "groesse": groesse}.items() if v is not None}

HOOKS = {
 "h01_bezug_ki": dict(typ="Fehler-Callout", passt="01 Ampel, 02 Excel-Fehler",
   szene=dict(quelle="ki_blick", dauer=1.8, ab=0, tempo=0.8, von=[540, 920, 1000], nach=[540, 880, 850],
              text=[T("#BEZUG!", 1150, 0.3, "rot", 200), T("2 Tage vor Abgabe.", 1310, 0.9, groesse=105)]),
   ton=[tippen(0, 0.35), fehler(0.3), uhr(0.6, 1.2)]),
 "h02_fehler_jede": dict(typ="Fehler-Callout", passt="02 Excel-Fehler, Steuerrückstellung allgemein",
   szene=dict(quelle="tabelle", dauer=2.6, ab=1.9,
              text=[T("Diesen Fehler hat", 380, 0.3, groesse=115), T("fast jede", 510, 0.5, groesse=115),
                    T("Steuerrückstellung.", 1400, 0.9, "gelb", 110)]),
   ton=[tippen(0, 0.4), fehler(0.73)]),
 "h03_hebesatz_excel": dict(typ="Frage / Spannung", passt="02 Excel-Fehler, Split-Screen",
   szene=dict(quelle="tabelle", dauer=2.8, ab=1.2,
              text=[T("Hebesatz geändert.", 400, 0.3, groesse=115), T("Und jetzt?", 1400, 1.45, "rot", 150)]),
   ton=[tippen(0.4, 0.6), fehler(1.43)]),
 "h04_17_sekunden": dict(typ="Zahl / Ergebnis", passt="01 Ampel, 02 Split-Screen, Tool-Demo",
   szene=dict(quelle="tool", dauer=2.6, ab=1.2,
              text=[T("Hebesatz ändern:", 400, 0.3, groesse=115), T("1,7 Sekunden.", 1400, 1.9, "gruen", 160)]),
   ton=[tippen(0.4, 0.6), lofi(1.83)]),
 "h05_hinzurechnung": dict(typ="Frage", passt="03 GewSt-Hinzurechnung",
   szene=dict(quelle="gewst", dauer=2.4, ab=0.8, von=[540, 700, 1080], nach=[540, 660, 920],
              text=[T("GewSt-Hinzurechnung", 300, 0.3, groesse=110), T("ohne Excel?", 450, 0.8, "gelb", 150)]),
   ton=[tippen(1.2, 0.45)]),
 "h06_noch_nicht": dict(typ="Frage / Status", passt="01 Ampel, Abschluss-Checkliste",
   szene=dict(quelle="ampel", dauer=2.5, ab=0.3, von=[540, 960, 1080], nach=[450, 920, 900],
              text=[T("Abschluss fertig?", 330, 0.3, groesse=120), T("Noch nicht.", 480, 1.0, "gelb", 150)]),
   ton=[]),
 "h07_von_hand": dict(typ="Frage / Schmerz", passt="03 GewSt, 02 Excel-Fehler, allgemein",
   szene=dict(quelle="ki_hand", dauer=2.6, ab=0.5, tempo=0.9,
              text=[T("Rechnest du das", 330, 0.3, groesse=120), T("noch von Hand?", 470, 0.8, "gelb", 120)]),
   ton=[tippen(0.1, 0.5), tippen(1.3, 0.5)]),
 "h08_freitagabend": dict(typ="Deadline / Schmerz", passt="01 Ampel, 04 Mein Weg",
   szene=dict(quelle="ki_buero", dauer=2.6, ab=0.5, tempo=0.9,
              text=[T("Freitagabend.", 330, 0.3, groesse=130), T("Abgabe Montag, 8 Uhr.", 480, 1.0, "rot", 105)]),
   ton=[uhr(0, 2.6)]),
 "h09_zeile_4000": dict(typ="Schmerz / Suche", passt="02 Excel-Fehler (kein Prüfpfad, #BEZUG!)",
   szene=dict(quelle="ki_tabelle", dauer=2.6, ab=0.5, tempo=0.9,
              text=[T("Irgendwo ist ein Fehler.", 330, 0.3, groesse=110), T("Zeile 1 von 4.000.", 480, 1.0, "gelb", 115)]),
   ton=[uhr(0.4, 2.2)]),
 "h10_frueher_heute": dict(typ="Vorher / Nachher", passt="01 Ampel, 04 Mein Weg",
   szene=dict(quelle="ampel", dauer=2.6, ab=13.6, von=[540, 960, 1080], nach=[410, 900, 820],
              text=[T("Früher: 2 Tage.", 330, 0.3, groesse=120), T("Heute: abschlussreif.", 470, 1.0, "gruen", 105)]),
   ton=[lofi(1.0)]),
}

def bauen(name):
    h = HOOKS[name]; q = h["szene"]["quelle"]
    if not (hier / Q[q]).exists():
        print("–", name, "übersprungen, Quelle fehlt:", Q[q]); return
    k = {"ausgabe": f"../hooks/{name}.mp4", "fps": 30, "ton": h["ton"],
         "quellen": {q: {"video": Q[q]}}, "szenen": [h["szene"]]}
    datei = hier / "schnitt" / "hooks" / f"{name}.json"
    datei.write_text(json.dumps(k, ensure_ascii=False, indent=1))
    subprocess.run([sys.executable, str(hier / "montage.py"), str(datei)], check=True)

if __name__ == "__main__":
    wahl = sys.argv[1:] or list(HOOKS)
    for n in HOOKS:
        if any(n.startswith(w) for w in wahl): bauen(n)
