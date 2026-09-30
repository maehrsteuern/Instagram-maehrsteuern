# Eigenes Reel-Konzept für Software (Stand 30.09.2026)

**Warum ein eigenes Konzept?** Schnelle Bau-Montagen (Gerba-Stil: harte Schnitte, Blitze, Shake) funktionieren im Handwerk,
weil jeder Schnitt echten, physischen Fortschritt zeigt. Software hat keinen Staub und keine Funken, dort wirkt dasselbe Tempo
nur hektisch (Test Ampel-Reel, 30.09.). Unser „Wow“ entsteht aus **Kontrast** (Chaos → Ruhe) und **sichtbarer Veränderung
auf dem Bildschirm** (Zahl springt, Ampel wird grün, Fehler verschwindet).

Ausgangslage (Insights 29./30.09.): 68 % Überspringrate, 7 s Sehdauer, 0 Klicks auf den Bio-Link.
→ Der Einstieg muss in 1 s klar machen, *worum es geht*, und das Reel muss Vertrauen aufbauen.
Regeln für Tempo, Ton und Text: `09_reel_regeln.md`.

## Die drei Formate

### A · Vorher/Nachher im Split-Screen (7–10 s)
- Oben Excel (rot getönt, Fehlerzellen), unten das Tool (grün). **Gleiche Aufgabe, zwei Timer.**
- Oben läuft die Zeit („2 Tage …“), unten steht nach 3 s „fertig“ – und bleibt ruhig stehen.
- Ton: oben Tippen und Uhr, sobald unten „fertig“ steht, setzt die Musik ein.
- Hook-Text: „Gleiche Aufgabe. Links Excel, rechts mein Tool.“ bzw. „Wer ist schneller?“
- Baubar aus vorhandenem Material (Excel-Chaos, App-Screens). Mit echten Aufnahmen noch stärker.

### B · Satisfying Software (8–12 s)
- **Echte Bildschirmaufnahme**, weiche Auto-Zooms, die dem Cursor folgen (wie bei SaaS-Demos), leise Klick-Sounds.
- Genau **ein** befriedigender Moment als Höhepunkt: Zahl zählt hoch, Ampel springt Rot → Grün, Fehlerliste leert sich.
- Keine Glitches, keine Blitze. Die Bewegung kommt aus Zoom und Kamerafahrt, nicht aus Effekten.
- Loop-fähig: Das Ende läuft nahtlos in den Anfang (erhöht die Sehdauer).
- **Braucht Aufnahmen vom Tool** (Liste unten).

### C · Gesicht + Screen (10–20 s)
- 2–3 s Loris vor der Kamera als Hook („Das hat mich früher 2 Tage gekostet.“), dann Screen (Format A oder B).
- Stärkstes Format für Vertrauen und DMs, weil eine echte Person dahinter steht (Bio-Link bisher 0 Klicks).
- **Kein KI-Gesicht als Ersatz** – KI-Mimik wirkt übertrieben (siehe `09_reel_regeln.md`).
- Umsetzung, sobald Handy-Clips da sind (Post 04 ist schon so geplant).

## Zuordnung zu den nächsten Posts

| Post | Datum | Format | Idee |
|---|---|---|---|
| 01 Ampel-Reel | 04.10. | B (jetzt aus Screens) | Aktuelle Version `reel_hook.mp4`. Mit echter Aufnahme später als B-Variante neu. |
| 02 Excel-Fehler (Karussell) | 06.10. | **A** als Begleit-Reel / Story | „Fehler Nr. 2: #BEZUG!“ – oben Excel bricht, unten das Tool zeigt die Quelle. |
| 03 GewSt-Hinzurechnung (Karussell) | 13.10. | **B** als Begleit-Reel / Story | Posten eintippen → Hinzurechnung rechnet sich live, Freibetrag, ein Viertel, Ergebnis zählt hoch. |
| 04 Mein Weg (Reel) | 20.10. | **C** | Drehbuch steht (`posts/04_…/drehbuch.md`), Loris filmt die Clips. |

Karussells bleiben Karussells (sie sammeln Speicherungen). Das Begleit-Reel zieht neue Leute auf das Karussell.

## Aufnahmeliste für Bildschirmaufnahmen (Format A/B)

Nur **Demodaten**, nichts vom Arbeitgeber. Auflösung mindestens 1920×1080, Browser-Zoom 125–150 %, Mauszeiger groß,
langsame, ruhige Bewegungen (Zooms mache ich im Schnitt). Pro Clip 20–60 s, Namen wie angegeben.

| Datei | Was aufnehmen | Für |
|---|---|---|
| `ampel_rot_gruen.mp4` | Abschlussreife steht auf Rot → fehlenden Hebesatz eintragen → Gelb → Rückstellung buchen → Grün | 01, B |
| `dashboard_klick.mp4` | Dashboard öffnen, Kennzahlen laden, über Karten fahren, auf eine Zahl klicken → Herleitung/Prüfpfad | 01/02, A |
| `bezug_quelle.mp4` | Eine Zahl anklicken → Quelle/Import sichtbar (statt #BEZUG!) | 02, A |
| `gewst_hinzurechnung.mp4` | Mieten, Zinsen, Leasing eintragen → Hinzurechnung, Freibetrag, ein Viertel, Ergebnis | 03, B |
| `excel_scroll.mp4` (optional) | Beispiel-Excel mit Fehlern scrollen, auf #BEZUG!-Zelle klicken | A (oben) |

Ablage: `posts/<post>/clips/` auf Zweig `claude/instagram` (wie beim Drehbuch von Post 04).
Aufnahme z. B. mit OBS oder Windows+G.

## Automatische Aufnahmen (ohne dass Loris aufnehmen muss)
Das Ertragsteuer-Programm läuft im Browser. Claude kann es selbst bedienen und aufnehmen:
- Runder Reel-Datensatz: `steuerberechnung/index.html?demo=reel` (Repo Tax-Calc-App-by-Loris, Branch `claude/reel-demodaten`).
  Ergebnis vor Steuern 10 Mio., Hebesatz 400 %, KSt 750.000, GewSt 700.000, laufende Steuer 1.491.250.
- Handy-Ansicht 540×960 bei doppelter Pixeldichte → gestochen scharfe 1080×1920, dunkles Design.
- Sichtbarer Mauszeiger mit Klick-Welle, echtes Tippen, weiches Scrollen.
- Technik gemeinsam in `vorlagen/system/aufnahmen/rekorder.mjs`, je Klickstrecke ein kurzes Skript:
  `ampel_gelb_gruen.mjs` (Post 01, Breite 540) und `gewst_hinzurechnung.mjs` (Post 03, Breite 600, damit die Rechentabelle ganz ins Bild passt).
- Post 03: Begleit-Reel `posts/03_…/reel_hinzurechnung.mp4` (Schnitt `schnitt/p03_reel_hinzurechnung.json`) mit denselben Zahlen wie Folie 5
  (150.000 / 100.000 / 400.000 / 80.000 → 390.000 ./. 200.000 → ein Viertel = 47.500 €).
- **Ehrlichkeit:** Die Ampel des Programms wird bei fehlenden Pflichtangaben **gelb**, rot nur bei echten Fehlern
  (z. B. falscher SAP-Ledger). Wir zeigen nur Zustände, die das Programm wirklich so anzeigt. Rot liefert der Excel-Hook.
