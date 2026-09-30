# Hook-Bibliothek

Fertige Einstiege für Reels: je **1,8–2,8 s**, 1080×1920, Outline-Text ab 0,3 s, **nur Atmo, keine Musik**.
Sie passen vor jedes Reel; die Musik setzt dann mit dem eigentlichen Inhalt ein (Regeln: `strategie/09_reel_regeln.md`).
Alle zehn am Stück: `uebersicht.mp4` (25 s).

| Datei | Länge | Text | Typ | Bild | passt zu |
|---|---|---|---|---|---|
| `h01_bezug_ki.mp4` | 1.8 s | #BEZUG! / 2 Tage vor Abgabe. | Fehler-Callout | KI-Clip (Runway): ruhiger Blick | 01 Ampel, 02 Excel-Fehler |
| `h02_fehler_jede.mp4` | 2.6 s | Diesen Fehler hat / fast jede / Steuerrückstellung. | Fehler-Callout | Tabellen-Attrappe (Karte) | 02 Excel-Fehler, Steuerrückstellung allgemein |
| `h03_hebesatz_excel.mp4` | 2.8 s | Hebesatz geändert. / Und jetzt? | Frage / Spannung | Tabellen-Attrappe (Karte) | 02 Excel-Fehler, Split-Screen |
| `h04_17_sekunden.mp4` | 2.6 s | Hebesatz ändern: / 1,7 Sekunden. | Zahl / Ergebnis | Programm-Aufnahme (Karte, Stoppuhr) | 01 Ampel, 02 Split-Screen, Tool-Demo |
| `h05_hinzurechnung.mp4` | 2.4 s | GewSt-Hinzurechnung / ohne Excel? | Frage | Programm-Aufnahme GewSt | 03 GewSt-Hinzurechnung |
| `h06_noch_nicht.mp4` | 2.5 s | Abschluss fertig? / Noch nicht. | Frage / Status | Programm-Aufnahme Dashboard | 01 Ampel, Abschluss-Checkliste |
| `h07_von_hand.mp4` | 2.6 s | Rechnest du das / noch von Hand? | Frage / Schmerz | KI-Clip (Runway): Hände, Taschenrechner | 03 GewSt, 02 Excel-Fehler, allgemein |
| `h08_freitagabend.mp4` | 2.6 s | Freitagabend. / Abgabe Montag, 8 Uhr. | Deadline / Schmerz | KI-Clip (Runway): leeres Büro abends | 01 Ampel, 04 Mein Weg |
| `h09_zeile_4000.mp4` | 2.6 s | Irgendwo ist ein Fehler. / Zeile 1 von 4.000. | Schmerz / Suche | KI-Clip (Runway): über die Schulter auf Tabelle | 02 Excel-Fehler (kein Prüfpfad, #BEZUG!) |
| `h10_frueher_heute.mp4` | 2.6 s | Früher: 2 Tage. / Heute: abschlussreif. | Vorher / Nachher | Programm-Aufnahme Dashboard | 01 Ampel, 04 Mein Weg |

## Verwenden
Hook als erste Quelle in eine Schnittdatei (`vorlagen/system/montage.py`) übernehmen, z. B.
`"quellen": {"hook": {"video": "../hooks/h04_17_sekunden.mp4"}, …}` und als erste Szene
`{"quelle": "hook", "dauer": 2.6, "ab": 0}`. Den Ton des Hooks in `"ton"` mit `"ab": 0` übernehmen
(Atmo liegt unter `musik/atmo/`, die Spuren stehen in `vorlagen/system/schnitt/hooks/<name>.json`).

## Ändern und neu bauen
Alle Hooks sind in `vorlagen/system/hooks_bauen.py` beschrieben (Quelle, Ausschnitt, Text, Ton).
`python3 hooks_bauen.py` baut alle, `python3 hooks_bauen.py h04 h07` nur einzelne.

## Bausteine (`bausteine/`)
- `karte_*.mp4`: die Hälften aus dem Split-Screen von Post 02, mittig auf dunklem Grund (y 620–1260).
- `ki_*.mp4`: drei Runway-Clips (eigene KI-Generierung, 30.09.2026), bewusst **ohne Gesichter** –
  KI-Mimik wirkt übertrieben. `ki_buero_abend.mp4`: die Wanduhr zeigt etwa 21:45, deshalb „Freitagabend“ statt Uhrzeit;
  auf dem Monitor ist klein ein Herstellerlogo zu sehen.
- Programm-Aufnahmen stammen aus dem Reel-Datensatz (nur Demozahlen), die Tabelle ist eine Attrappe.
