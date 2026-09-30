# 3 · Redaktionsplan – 3 Beiträge pro Woche

## Wochenrhythmus (ab Oktober 2026)
| Tag | Was | Wer |
|---|---|---|
| **Montag 08:47** | Content-Fabrik baut die nächsten Beiträge → Freigabe-Issue mit Vorschau | Claude |
| **Montag 19:00** | Kurzer Check: `go` oder `stop` im Freigabe-Issue (Kalender erinnert) | du, 2 Min. |
| **Dienstag 19:30** | Karussell (Praxis oder Wissen) + Teaser-Story 19:35 | Autopilot |
| **Donnerstag 08:47** | Content-Fabrik, zweite Runde | Claude |
| **Donnerstag 19:30** | Karussell + Teaser-Story; abends Check der neuen Freigaben | Autopilot / du |
| **Sonntag 19:30** | Reel (Demo aus Screenshots, Musik fest eingebaut) + Teaser | Autopilot |
| **täglich 12:15** | eine Story: Frage „Antworte auf diese Story“, Auflösung oder Tipp | Autopilot |
| laufend | Kommentare und DMs beantworten | du |

Säulen rotieren über die drei Slots: Demo (So), Praxis und Wissen (Di/Do), „Hinter dem Code“ alle 2–3 Wochen statt einer Demo.

Nach Feierabend sind Berufstätige und Studierende gleichzeitig online, Begründung in `05_veroeffentlichung.md`. Nach 4 Wochen die Uhrzeit anhand der Statistik prüfen.

**Startwoche:** Neuvorstellung **Do 01.10.** (18:30, in der App geplant), Reel Ampel **So 04.10.**, danach jeden Dienstag 19:30.

## Plan Oktober – November 2026

| Woche | Datum | Säule | Format | Thema / Haken | Story davor | Status |
|---|---|---|---|---|---|---|
| 1 | So 04.10. | Demo | Reel | **„Ertragsteuer-Ampel: 3 Sekunden statt 3 Stunden“** – Dashboard zeigt Rot/Gelb/Grün je Position | Frage: „Wie lange dauert bei euch die Steuerrückstellung?“ | **fertig** (`posts/01_…`) |
| 2 | 06.10. | Praxis | Karussell | **„5 Excel-Fehler in deiner Steuerrückstellung“** | Umfrage: „Hattest du schon mal #BEZUG! kurz vor Abgabe?“ | **fertig** (`posts/02_…`) |
| 3 | 13.10. | Wissen | Karussell | **„Gewerbesteuer-Hinzurechnung in 7 Folien – mit Rechenbeispiel“** (Demo-Zahlen) | Quiz: „Werden Mieten voll hinzugerechnet?“ | **fertig** (`posts/03_…`) |
| 4 | 20.10. | Hinter dem Code | Reel (Gesicht) | **„Vom Steuer-Studium zum eigenen Tool“** – 3 Stationen in 20 s | Frage: „Was willst du über mich wissen?“ | Bausteine fertig, **Clips von dir bis 15.10.** (`posts/04_…/drehbuch.md`) |
| 5 | 27.10. | Demo | Reel | **„Prüfpfad: Jede Zahl bis zur Quelle klicken“** | Umfrage: „Wie viele Tabellenblätter hat eure größte Steuer-Datei?“ | offen |
| 6 | 03.11. | Praxis | Karussell | **„Excel vs. Standardsoftware vs. eigenes Tool – ehrlich verglichen“** (knüpft an die Umfrage im angepinnten Reel an) | Umfrage: „Team Code oder Team Excel?“ | offen |
| 7 | 10.11. | Wissen | Karussell | **„Jahresabschluss: 7 Steuer-Punkte, die du jetzt schon vorbereiten kannst“** (speichern!) | Frage: „Was ist dein größter Zeitfresser im Abschluss?“ | offen |
| 8 | 17.11. | Hinter dem Code | Reel | **„Ihr habt abgestimmt – ich baue das Feature“** (Ergebnis aus Woche 6) | Umfrage: „Welches Feature zuerst?“ | offen |

## Themenspeicher (für freie Slots der Content-Fabrik)
| Säule | Thema / Haken | Zielgruppe | Hinweis |
|---|---|---|---|
| Wissen | **„Latente Steuern im Abschluss 2026: Welcher Steuersatz gilt?“** – KSt sinkt ab 2028 jährlich um 1 Punkt (2028: 14 %, 2029: 13 %, 2030: 12 %, 2031: 11 %, ab 2032: 10 %; Investitionssofortprogramm 2025). Differenzen nach dem Jahr ihrer Umkehr bewerten (§ 274 Abs. 2 HGB). Rechenbeispiel Demo-Zahlen, GewSt 400 %: 2027 = 29,83 %, 2032 = 24,55 %. | Steuerabteilungen | Knüpft an Excel-Fehler Nr. 1 („fest eingetippter Steuersatz“) an. Rechtsstand vor Freigabe prüfen. |
| Praxis | **„Steuersatz-Staffel 2028–2032 in Excel: So baust du sie richtig“** (Parameter-Tabelle statt Festwert) | Steuerabteilungen, Kanzleien | Folgebeitrag, Aufruf „TOOL“ |
| Praxis | **„Was im Examen keiner sagt: So sieht die Steuerrückstellung in der Praxis aus“** | Ex-Examens-Community, heute Berater | Brücken-Thema, zählt nicht zur Examens-Quote |

**Nach Woche 4 und 8:** Kennzahlen aus `01_positionierung.md` eintragen, schwächste Säule anpassen, nächste 4 Wochen planen.

## Ablauf pro Beitrag (Checkliste)
1. Thema aus der Tabelle nehmen, Haken in einem Satz formulieren (Muster und Regeln: `08_hooks.md`)
2. Texte in eine Job-Datei schreiben, z. B. `vorlagen/system/jobs/p05_….json` (Vorlage: `p02_excel_fehler.json` kopieren)
3. Bilder erzeugen: im Ordner `vorlagen/system` → `node render.mjs jobs/p05_….json`
4. Bei Reels aus Screenshots: Schnittliste wie `schnitt/p01_reel_ampel.json`, dann `python3 reel.py schnitt/….json`
5. Bildunterschrift nach Muster unten
6. Beitrag für Di 19:30 einplanen, Story-Teaser direkt danach

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
