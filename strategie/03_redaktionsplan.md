# 3 · Redaktionsplan – 1 Beitrag pro Woche

## Wochenrhythmus
| Tag | Was | Aufwand |
|---|---|---|
| **Montag** | Story mit Frage- oder Umfrage-Sticker zum Thema der Woche | 5 Min. |
| **Dienstag, 18:30** | **Beitrag der Woche** + Story-Teaser „Neuer Beitrag“ | Hauptarbeit |
| Dienstag bis Donnerstag | Kommentare und DMs beantworten (innerhalb von 24 h) | 10 Min./Tag |
| **Freitag** | Story: Antworten der Frage vom Montag auflösen oder Blick hinter die Kulissen | 5 Min. |

Nach Feierabend sind Berufstätige und Studierende gleichzeitig online, Begründung in `05_veroeffentlichung.md`. Nach 4 Wochen die Uhrzeit anhand der Statistik prüfen.

**Start:** Neuvorstellung (Karussell) am **So 04.10., 18:30**, danach anpinnen.

## Plan Oktober – November 2026

| Woche | Datum (Di) | Säule | Format | Thema / Haken | Story Montag | Status |
|---|---|---|---|---|---|---|
| 1 | 06.10. | Demo | Reel | **„Ertragsteuer-Ampel: 3 Sekunden statt 3 Stunden“** – Dashboard zeigt Rot/Gelb/Grün je Position | Frage: „Wie lange dauert bei euch die Steuerrückstellung?“ | **fertig** (`posts/01_…`) |
| 2 | 13.10. | Praxis | Karussell | **„5 Excel-Fehler in deiner Steuerrückstellung“** | Umfrage: „Hattest du schon mal #BEZUG! kurz vor Abgabe?“ | **fertig** (`posts/02_…`) |
| 3 | 20.10. | Wissen | Karussell | **„Gewerbesteuer-Hinzurechnung in 7 Folien – mit Rechenbeispiel“** (Demo-Zahlen) | Quiz: „Werden Mieten voll hinzugerechnet?“ | **fertig** (`posts/03_…`) |
| 4 | 27.10. | Hinter dem Code | Reel (Gesicht) | **„Vom Steuer-Studium zum eigenen Tool“** – 3 Stationen in 20 s | Frage: „Was willst du über mich wissen?“ | Bausteine fertig, **Clips von dir bis 22.10.** (`posts/04_…/drehbuch.md`) |
| 5 | 03.11. | Demo | Reel | **„Prüfpfad: Jede Zahl bis zur Quelle klicken“** | Umfrage: „Wie viele Tabellenblätter hat eure größte Steuer-Datei?“ | offen |
| 6 | 10.11. | Praxis | Karussell | **„Excel vs. Standardsoftware vs. eigenes Tool – ehrlich verglichen“** (knüpft an die Umfrage im angepinnten Reel an) | Umfrage: „Team Code oder Team Excel?“ | offen |
| 7 | 17.11. | Wissen | Karussell | **„Jahresabschluss: 7 Steuer-Punkte, die du jetzt schon vorbereiten kannst“** (speichern!) | Frage: „Was ist dein größter Zeitfresser im Abschluss?“ | offen |
| 8 | 24.11. | Hinter dem Code | Reel | **„Ihr habt abgestimmt – ich baue das Feature“** (Ergebnis aus Woche 6) | Umfrage: „Welches Feature zuerst?“ | offen |

**Nach Woche 4 und 8:** Kennzahlen aus `01_positionierung.md` eintragen, schwächste Säule anpassen, nächste 4 Wochen planen.

## Ablauf pro Beitrag (Checkliste)
1. Thema aus der Tabelle nehmen, Haken in einem Satz formulieren
2. Texte in eine Job-Datei schreiben, z. B. `vorlagen/system/jobs/p05_….json` (Vorlage: `p02_excel_fehler.json` kopieren)
3. Bilder erzeugen: im Ordner `vorlagen/system` → `node render.mjs jobs/p05_….json`
4. Bei Reels aus Screenshots: Schnittliste wie `schnitt/p01_reel_ampel.json`, dann `python3 reel.py schnitt/….json`
5. Bildunterschrift nach Muster unten
6. Beitrag für Di 18:30 einplanen, Story-Teaser direkt danach

## Muster Bildunterschrift
```
[Haken aus Folie 1, eine Zeile]

[2–3 kurze Sätze: Problem → was das Tool/Wissen löst]

[Aufruf je nach Säule:]
Demo/Praxis:   💬 Schreib mir „TOOL“ per DM – ich zeig dir die Demo.
Wissen:        📌 Speichern für den nächsten Abschluss.
Hinter d. Code: ➕ Folgen, wenn du Steuern × Code sehen willst.

#steuern #steuerrecht #excel #automatisierung #steuerabteilung
```
Hashtags: 3–5 passende reichen, immer dieselbe Grundmenge plus 1–2 zum Thema (z. B. `#gewerbesteuer`, `#jahresabschluss`).
