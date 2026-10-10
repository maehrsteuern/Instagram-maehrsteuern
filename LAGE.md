# 🧭 Lage – maehrsteuern auf Instagram

_Automatisch erzeugt von `automatik/lage.py` – nicht von Hand bearbeiten (Notizen: `automatik/lage_notizen.md`). Stand: letzte Änderung Sa 10.10. 08:49 Uhr._

**Als Nächstes online:** 🎬 Reel `12-reel-zeile` am **Sa 10.10. 19:30 Uhr** – ✋ manuell (postest du in der App)

## 📝 Gerade in Arbeit

- Neustart läuft: Start-Storys + Vorfreude (30.09.) und Neuvorstellung (Do 01.10. 18:30, von Hand) sind online. Nach 2 h: 26 erreicht, 6× geteilt, 0 neue Follower. Angepinnt ✓ (03.10.). Offen von Hand: Highlight „Start 👋“.
- Wochenrhythmus ab Okt. steht im Prompt der Content-Fabrik (Mo + Do 08:47, max. 4 Beiträge pro Lauf): Di/Do Karussell + Teaser, Mi Begleit-Reel, Fr Wissens-Reel oder Stimm-Reel, So Reel + Teaser, täglich 12:15 Story.
- Content-Fabrik nutzt ab Mo 05.10. die Lernpunkte aus `strategie/wettbewerb.md` (über Abschnitt in `08_hooks.md`): pro Lauf ≥ 1 Hook „konkreter Fall“ oder „Prüfer/Finanzamt“, Lernpunkt im Freigabe-Issue vermerkt. Routine-Prompt selbst unverändert (nur aus ihrer eigenen Sitzung änderbar).
- **So 04.10. umgebaut:** Statt Ampel-Reel geht 19:30 das Community-Reel „5 Sachen, die ich aus Excel rausgeschmissen hab“ online (Loris' Sprachnachricht, 41 s, keine Werbung, CTA: Zahl 1–5 in die Kommentare) + neue Teaser-Story 19:35. Ampel-Reel und alter Teaser stehen auf `pause` – kann später wieder eingeplant werden. Die Kommentar-Antworten (welche Nummer?) sind die Themen für die nächsten Reels.
- **Doppel-Post 04.10. behoben:** Das 5-Dinge-Reel ging zweimal raus (DeFLK53ALSs = im Plan, DeFLSBNFUXy = Duplikat, von Loris am 04.10. gelöscht ✓). Ursache: Ein Lauf startet mit dem Stand vom Startzeitpunkt und hat den Plan nur nach dem Warten neu geladen. `posten.py` holt jetzt direkt vor jedem Posten den neuesten Plan; klappt das nicht, wird nicht gepostet (nächster Lauf holt nach).
- **Di 06.10. 19:30 Reel „Nummer 1: Der Monatsbericht“ (Version 3)** freigegeben (go von Loris im Chat, 06.10.): dritte Aufnahme, Atmer raus, Pausen mit Raumton, 30 s. Karussell Excel-Fehler Mi 07.10., LinkedIn #18 Do 08.10., Split-Reel So 11.10.
- **Reels laufen sehr gut, Meta Verified (08.10.) → ab jetzt jeden Abend ein Reel 19:30**, alle von Loris eingesprochen (Aufnahmen 08.10. in `aufnahmen/`), von Claude fertig geschnitten (Stimme −18 LUFS, wörtliche Untertitel, Atmo + leise Runway-Musik) und als Status `manuell` eingeplant – **Loris lädt jedes über Edits hoch und plant es dort** (Anleitung `EDITS.md` im Ordner): Do 08 Split (Stimme neu) · Fr 09 Nr. 2 Zeile · Sa 10 Steuersatz 2028 · So 11 Verknüpfung · Mo 12 Nr. 3 final_final_v3 · Di 13 Nr. 4 Rechnungsnummern · Mi 14 Hinzurechnung (Autopilot) · Do 15 Nr. 5 Listen · Fr 16 Mein Weg (KI-Label!). Karussells am selben Tag auf 12:30 (latente Steuern Fr 09., GewSt Di 13., Rückstellung Do 15.), Teaser 12:35. Offen: Sa 17.10. frei – Thema aus den Kommentaren (`17-reel-kommentare` steht noch auf Sa 24.10.). Schnitt: `vorlagen/system/schnitt/reels_0810_bauen.py` (Stimme `vorlagen/system/stimme.py`, Transkript `automatik/transkribieren.py`). Neue Musik 07–12 (Runway) in `musik/`. **Umplanung 10.10.:** Nr. 2 lief Fr 09.10. nicht (Schnitt „300 oder Zeilen“) → neu geschnitten, Sa 10.10. 19:30; danach alles +1 Tag: So 11 Steuersatz („gestern“ rausgeschnitten) · Mo 12 Verknüpfung · Di 13 Nr. 3 · Mi 14 Nr. 4 · Do 15 Hinzurechnung (Autopilot) · Fr 16 Nr. 5 · Sa 17 Mein Weg (KI-Label). `stimme.py`: raus-Kanten jetzt hart (nichts aus dem Ausgeschnittenen, danach 0,14 s Luft) – Kanten am Pegel messen und per Whisper gegenhören.
- **Stumme Reels behoben (06.10.):** `montage.py` erzeugte bei bestimmten Tonspuren (Atmo/Musik ohne Stimme) eine Tonspur mit kaputten Zeitstempeln → im MP4 stumm. Betroffen: Split-Reel und KSt-Staffel-Reel – beide neu gerendert (−18,5 / −19,7 LUFS). Fix: `asetpts=N/SR/TB` nach `amix` + jede Spur auf volle Länge. Ab jetzt nach jedem Render Lautheit prüfen (sollte ca. −18 LUFS sein, −70 = stumm).
- **Edits-Test (06.10.):** Split-Reel Do 08.10. 19:30 baut Loris selbst in Edits und plant es dort (Status `manuell`, Paket in `posts/02_2026-10-06_excel_fehler/edits_paket/`, Anleitung als Google Doc im Drive). Grund: laut Mosseri (Aug. 2025) kleiner Reichweiten-Bonus für Edits-Reels, nur bei echtem Schnitt in Edits, „nicht für immer“ – aktueller Stand unbelegt, daher Test über 2–3 Reels gegen Autopilot-Reels. Woche dafür verschoben: latente Steuern Fr 09.10., KSt-Reel + „Heute 19:30“-Story Sa 10.10., Rückblick-Story So 11.10.
- Bis 10.10. alles freigegeben: 5-Dinge-Reel (So 04.10.), Excel-Fehler (Di 06.10.), Split-Reel als Begleit-Reel (Mi 07.10., vorgezogen), latente Steuern (Do 08.10.), Wissens-Reel KSt-Staffel (Fr 09.10.). So 11.10. ist frei → Fabrik am Mo 05.10.
- Latente Steuern: Prüfzettel Punkte 1–5 am 05.10. mit Quellen geprüft ✓ – Box Folie 6 präzisiert (kleine KapGes: von § 274 befreit, passive Latenzen ggf. als Rückstellung), fachlich nichts mehr offen (`pruefzettel.md` im Post-Ordner; „Abschluss 2026“ am 05.10. überall auf „spätestens jetzt“ geändert – Folien 1+7, Bildunterschrift, Teaser, LinkedIn-Text + PDF). Änderungen bis Mi 07.10. abends.
- Reel „Mein Weg“: Loris hat Variante B am 08.10. eingesprochen → fertig, Fr 16.10. 19:30 (Edits, `manuell`). **KI-Label beim Posten einschalten** (Karte 2 + 3 KI), Hinweis steht in der Bildunterschrift. Variante-A-Dateien als `*_variante_a.*` im Ordner.
- DM-Strecke läuft über **ManyChat** (Kommentar/Story-Antwort/DM mit Tool/TOOL/tool/tol → DM mit Demo-Link, Follow-up nach 23 h). Stichwörter nur in `automatik/interaktion.json` pflegen – Abweichungen meldet LAGE.md. Die eigenen Skripte schicken nie DMs.
- Interaktion läuft (Radar 50 Konten, Kommentar-Hilfe, LinkedIn-Pakete). **Sprint 1 (03.10.):** Wächter-Issue, Stichwort-Abgleich, Radar-Pflege montags, Erste-Stunde-Checkliste. **Kalender-Sync live (03.10.):** Termine gehen direkt in den Google-Kalender „maehrsteuern Autopilot“ (nur Postzeiten „beschäftigt“ für Reclaim, To-dos/LinkedIn „frei“; Farben + Pop-ups je Art). In Reclaim verbunden ✓, Freigabe nur Dienstkonto (nicht öffentlich, nicht im Hauptkalender) ✓ (Chrome 05.10.). `kalender.ics` entfällt. **Wochenbericht** ab So 04.10. ca. 18:00 als Issue – Demos/ManyChat per Kommentar nachtragen. Demo-Zahlen (entschieden 03.10.): Reclaim-Pflichtfeld „Woher kennst du mich?“ → Apps-Script „maehrsteuern Demo-Kopie“ kopiert Buchungen stündlich ohne Namen nach „maehrsteuern Autopilot“ → Wochenbericht zählt sie; UTM/Webhooks scheiden aus (Starter), `dm_tracking.csv` nicht mehr im Bericht. **Chrome 05.10.:** Pflichtfeld (Dropdown, Pflicht) ✓, Reclaim-Vorlagen weg ✓ (zweiter Link „Demo + Intro Call“ für @maehrtax bleibt, wird nicht gezählt), Apps-Script = GitHub-Stand, 1 Trigger stündlich :40, 0 % Fehler ✓. **Offen:** Testbuchung (loris_jm@gmx.de, Herkunft Instagram → Kopie prüfen → absagen) + Beschreibungsausschnitt an Claude; Puffer: global 10 Min. nach jedem Meeting (gilt auch für @maehrtax, entschieden 05.10.) – setzt Chrome zusammen mit der Testbuchung. ManyChat-Zahlen bleiben von Hand (API nur Pro) – siehe `strategie/13_backlog.md`.
- **Automatik gehärtet (03.10., mit #23 in `claude/instagram`):** kein Doppel-Post bei Push-Konflikt, „stop“ greift auch während des Wartens, kein Schlüssel in Fehlermeldungen, keine verlorenen „go“-Antworten, Schlüssel-Verlängerung mit Reserve-Takt – Details `strategie/13_backlog.md`.
- Externer Takt fürs Posten läuft (cron-job.org, alle 15 Min.). Schlüssel `cron-posten` läuft am **29.09.2027** ab → vorher erneuern.
- Tax-Calc-Repo: PR #2 (Delta-Plakette beim Tippen) und PR #3 (Reel-Datensatz `?demo=reel`) warten auf Review.
- **Chrome-Claude-Module** (`strategie/14_chrome_module.md`): Erinnerungen im Kalender „maehrsteuern Autopilot“ – So 04.10. 11:00 einmalig A·2·3, jeden So 18:45 Modul 1 (ManyChat → Wochenbericht), 1. Mo im Monat 18:00 Module 4+6, LinkedIn-Upload (Modul 5) automatisch je Karussell am Werktag danach 08:00.
- **Wochenbericht KW 40 ist da ([#29](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/29), So 18:01, Reserve-Lauf 21:26 hat dasselbe Issue nur aktualisiert):** Zahlen geprüft (575 Aufrufe = Zuwachs der 2 neuen Beiträge, Radar 2 Kommentare aus #22, Kalender verbunden – 0 Demos). **Offen: ManyChat-Zeile fehlt** (Chrome Modul 1 lief nicht) → im Issue `manychat x/y` + Zeile `Gesamtstand ManyChat: gesendet X / Klicks Y` kommentieren. Behoben (05.10.): Sonntags-Reels (19:30, nach dem Bericht) zählen jetzt im Bericht der Folgewoche als neu – „neu“ = gepostet So–Sa.
- **Radar-Nachträge (03.10.):** Meta-Drosselung (429/Code 4, 17, 32, 613) → Backoff 30/90/270 s, bei anhaltender Drosselung wird abgebrochen. Gedrosselte oder kurz gestörte Konten landen nicht mehr als 🧹 „nicht abrufbar“ in der Pflege; aufgeräumt werden nur dauerhaft kaputte Konten oder Konten ohne Beitrag seit 30 Tagen (montags, nur abgehakt). Art neuer Konten wird auch aus Wörtern wie „Steuerberaterin“, „Prüfung“, „Akademie“ erkannt; fehlende oder unbekannte Art erscheint als Hinweis im Radar-Issue.
- **Fristen** (`automatik/erinnerungen.json` → „Braucht dich“ + Kalender): LinkedIn #18 Mi 07.10. 08:00 (Termin kommt schon automatisch) · Reel-Vergleich „5 Dinge“/Split → Anzeigen-Start ca. Mo 12.10. (Chrome Modul 2 am 04.10. nur vorbereiten) · **ManyChat-Trial endet Fr 16.10.** → Entscheidung Loris (Erinnerung Mi 14.10.).
- **Meta-App „maehrsteuern Autopilot“** bleibt im Entwicklungsmodus. Die laufenden IG-Schlüssel und die Statistik sind davon nicht betroffen (eigenes Konto mit App-Rolle). Nur die Hashtag-Suche braucht die Freigabe → Checkliste [#26](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/26).
- **Reclaim-Hinweis:** Claudes Reclaim-Zugang (Connector) zeigt auf **Konto B (Outlook, Lite)**, nicht auf das Demo-Konto. Für die Automatik nicht nutzen; Demo-Buchungen kommen nur über das Apps-Script „maehrsteuern Demo-Kopie“.
- **Bibliothek aus dem Brand Kit (Claude Design) gebaut (02.10.):** 365 fertige Bilder in `assets/bibliothek/` (Übersicht `README.md` dort), Texte als Job-Dateien in `vorlagen/system/jobs/bibliothek/`. Neue Vorlagen `zahl.html` + `banner.html`, Highlight-Symbole, Vergleichstabelle/Checkliste im Karussell. Nichts davon ist eingeplant. **Gegengelesen (05.10.):** 10 Fehler korrigiert, 25 Zweifelsfälle mit Loris entschieden und umgesetzt → `assets/bibliothek/PRUEFBERICHT.md`. Offen nur: Zinsschranke-Caption mit Hinweis auf Untergang des Zinsvortrags. **Erste Bibliothek-Beiträge eingeplant (05.10., als Entwurf → Freigabe-Issue):** Rückstellung in 6 Schritten Do 15.10. (Quiz SolZ Mi 14.10., Auflösung Do 15.10. 12:15, Teaser 19:35) · E-Rechnung-Fahrplan Do 22.10. (Umfrage Mi 21.10., Teaser 19:35). Content-Fabrik: diese Slots sind belegt. **Runde 4 ergänzt (05.10.):** +217 Bilder (jetzt 582) – GmbH/Gesellschafter, Bilanz, USt, Lohn, ErbSt/GrESt, Paragraf als Formel, Steuerkalender, GoBD, Mythos/Glossar Teil 2, Einzelposts, Storys, Reel-Titel, Einblendungen, Highlights, Ampeln (`r4_*.json`), nichts eingeplant. 6 Korrekturen vor dem Rendern, 4 Zweifelsfälle + Platzhalter „312 Testfälle“ / § 8c-Quoten 48/62 % offen → Prüfbericht Abschnitt „Runde 4“. **Runde 7 (07.10.):** 14 MBS-Reel-Bilder (10 Titel `reels/mbs_*`, 4 Einblendungen `bausteine/mbs_*`, Abspann „Demo buchen“), `einblendung.html` kann jetzt `chip`/`kicker` im Abspann. **Runden 5+6 (07.10.):** +400 Bilder (jetzt 996) – Kleinunternehmer, Firmenwagen, Gebäude-AfA, USt-Sätze, Minijob/Reisekosten 2026, Grundwerte 2026, Kapitalerträge, Vermietung, AO-Fristen, OSS u. a. 10 Korrekturen, 32 Umbenennungen gegen Überschreiben, Zweifelsfälle → Prüfbericht „Runden 5 und 6“.
- **Lage als Seite (04.10.):** `LAGE.html` mit Kacheln, Kalender, Diagrammen und filterbarem Protokoll, wird mit LAGE.md neu geschrieben und über GitHub Pages veröffentlicht (https://maehrsteuern.github.io/Instagram-maehrsteuern/). Pages eingeschaltet ✓ (04.10.), Seite läuft und aktualisiert sich bei jeder neuen Lage automatisch.

## 👉 Braucht dich

- ✋ **Von Hand posten** `12-reel-zeile` (Sa 10.10. 19:30) – 10.10.: Fr 09.10. nicht gepostet (Schnitt bei 16 s klang wie „300 oder Zeilen“) → neu geschnitten (harte Kanten am Pegel, „Egal ob 3 oder 300 Zeilen.“), heute 19:30; alle folgenden Reels +1 Tag. · Serie Nummer 2: Zeile eingefügt, Summe weg. Vorgezogen vom 12.10. (08.10., Reels laufen gut → täglich 19:30). Einstieg „Jutta hat schon wieder …“ bleibt drin (erfundene Person, Wunsch Loris 08.10.). · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner.
- ✋ **Von Hand posten** `08-reel-kst-staffel` (So 11.10. 19:30) – 10.10.: +1 Tag (So 11.10.), „gestern“ aus „Den Rechenweg habe ich gestern ins Karussell gepackt“ geschnitten (Karussell lief Fr 09.10.). · Stimm-Reel „Der Steuersatz, der ab 2028 falsch ist“ ersetzt das stumme Wissens-Reel (08.10.). Tag nach dem Karussell latente Steuern („gestern ins Karussell“). · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner.
- ✋ **Von Hand posten** `13-reel-verknuepfung` (Mo 12.10. 19:30) – #BEZUG! zwei Tage vor Abgabe – Verknüpfung auf die alte Datei. Vorgezogen vom 16.10. · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner.
- ✋ **Von Hand posten** `14-reel-versionen` (Di 13.10. 19:30) – Serie Nummer 3: final_final_v3. Vorgezogen vom 18.10. · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner.
- 🟡 **Freigeben** `09-story-quiz` (Mi 14.10. 12:15) – „go“ oder „stop“ im Issue ([Freigabe #35](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/35))
- ✋ **Von Hand posten** `15-reel-rechnungsnummern` (Mi 14.10. 19:30) – Serie Nummer 4: doppelte Rechnungsnummer. Vorgezogen vom 20.10. · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner.
- 🟡 **Freigeben** `09-story-aufloesung` (Do 15.10. 12:15) – „go“ oder „stop“ im Issue ([Freigabe #35](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/35))
- 🟡 **Freigeben** `09-rueckstellung` (Do 15.10. 12:30) – „go“ oder „stop“ im Issue ([Freigabe #35](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/35))
- 🟡 **Freigeben** `09-story-teaser` (Do 15.10. 12:35) – „go“ oder „stop“ im Issue ([Freigabe #35](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/35))
- ✋ **Von Hand posten** `16-reel-listen` (Fr 16.10. 19:30) – Serie Nummer 5: zwei Listen, SVERWEIS. Vorgezogen vom 22.10. – Serie damit durch. · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner.
- ✋ **Von Hand posten** `04-reel-mein-weg` (Sa 17.10. 19:30) – Mein Weg rückwärts (Variante B, Loris hat den Text am 08.10. eingesprochen). Vorgezogen vom 27.10. KI-LABEL in Edits/Instagram einschalten (Karte 2 + 3 KI), Hinweis steht in der Bildunterschrift. Variante-A-Dateien: *_variante_a.* · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner.
- ⏳ **Wartet auf sprachnachricht** `17-reel-kommentare` (Sa 24.10. 19:30) – Thema aus den Kommentaren der Serie (wird nach Auswertung bis ca. 20.10. festgelegt). Reel-Takt alle 2 Tage (06.10.). Upload über Edits: Claude baut das Reel komplett fertig (mit Musik, Untertiteln) und schickt es im Chat, Loris lädt es über Edits hoch und plant/postet selbst – der Autopilot postet NICHT (Status nach dem Schnitt: manuell). Sprechtext in posts/sprechtexte.md.
- ⏰ **📣 Reel-Vergleich „5 Dinge“ vs. Split → Anzeige starten (ca. 12.10.)** (Mo 12.10. 18:00) – „5 Dinge“ (So 04.10., ersetzt das Ampel-Reel) gegen Split (Mi 07.10.) vergleichen: (Speichern + Teilen) / Reichweite in LAGE.md bzw. im Wochenbericht.
- ⏰ **💳 ManyChat-Trial endet Fr 16.10. – entscheiden** (Mi 14.10. 18:00) – Entscheidung Loris: weiter (Kosten?) oder kündigen. Grundlage: ManyChat gesendet/Klicks und Demos aus den Wochenberichten KW 40 + 41.

## ⏭️ Nächste 7 Tage

| Wann | Was | Status | Hinweis |
|---|---|---|---|
| Sa 10.10. 19:30 | 🎬 Reel `12-reel-zeile` | ✋ manuell (postest du in der App) | 10.10.: Fr 09.10. nicht gepostet (Schnitt bei 16 s klang wie „300 oder Zeilen“) → neu geschnitten (harte Kanten am Pegel, „Egal ob 3 oder 300 Zeilen.“), heute 19:30; alle folgenden Reels +1 Tag. · Serie Nummer 2: Zeile eingefügt, Summe weg. Vorgezogen vom 12.10. (08.10., Reels laufen gut → täglich 19:30). Einstieg „Jutta hat schon wieder …“ bleibt drin (erfundene Person, Wunsch Loris 08.10.). · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner. |
| So 11.10. 12:15 | 📱 Story `08-story-heute` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #15](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/15) |
| So 11.10. 19:30 | 🎬 Reel `08-reel-kst-staffel` | ✋ manuell (postest du in der App) | 10.10.: +1 Tag (So 11.10.), „gestern“ aus „Den Rechenweg habe ich gestern ins Karussell gepackt“ geschnitten (Karussell lief Fr 09.10.). · Stimm-Reel „Der Steuersatz, der ab 2028 falsch ist“ ersetzt das stumme Wissens-Reel (08.10.). Tag nach dem Karussell latente Steuern („gestern ins Karussell“). · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner. · [Freigabe #15](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/15) |
| Mo 12.10. 12:15 | 📱 Story `03-story-quiz` | 🟢 freigegeben (geht automatisch online) |  |
| Mo 12.10. 18:00 | 📱 Story `08-story-rueckblick` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #15](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/15) |
| Mo 12.10. 19:30 | 🎬 Reel `13-reel-verknuepfung` | ✋ manuell (postest du in der App) | #BEZUG! zwei Tage vor Abgabe – Verknüpfung auf die alte Datei. Vorgezogen vom 16.10. · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner. |
| Di 13.10. 12:30 | 🖼️ Karussell `03-gewst-hinzurechnung` | 🟢 freigegeben (geht automatisch online) |  |
| Di 13.10. 12:35 | 📱 Story `03-story-teaser` | 🟢 freigegeben (geht automatisch online) |  |
| Di 13.10. 19:30 | 🎬 Reel `14-reel-versionen` | ✋ manuell (postest du in der App) | Serie Nummer 3: final_final_v3. Vorgezogen vom 18.10. · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner. |
| Mi 14.10. 12:15 | 📱 Story `09-story-quiz` | 🟡 Entwurf (wartet auf Freigabe) | Ja/Nein zum Antippen (08.10.): Antwort per Emoji-Schnellreaktion 👏 = Ja · 😮 = Nein – ein Tipp statt Tippen. Besser noch: in der App zusätzlich Quiz-Sticker Ja/Nein setzen (richtig: Ja). Aus der Bibliothek, Einstieg zum Rückstellungs-Karussell · [Freigabe #35](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/35) |
| Mi 14.10. 19:30 | 🎬 Reel `15-reel-rechnungsnummern` | ✋ manuell (postest du in der App) | Serie Nummer 4: doppelte Rechnungsnummer. Vorgezogen vom 20.10. · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner. |
| Do 15.10. 12:15 | 📱 Story `09-story-aufloesung` | 🟡 Entwurf (wartet auf Freigabe) |  · [Freigabe #35](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/35) |
| Do 15.10. 12:30 | 🖼️ Karussell `09-rueckstellung` | 🟡 Entwurf (wartet auf Freigabe) | Aus der Bibliothek (gegengelesen 05.10., Demo-Zahlen 1 Mio. €, Hebesatz 400 %) · [Freigabe #35](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/35) |
| Do 15.10. 12:35 | 📱 Story `09-story-teaser` | 🟡 Entwurf (wartet auf Freigabe) |  · [Freigabe #35](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/35) |
| Do 15.10. 19:30 | 🎬 Reel `07-reel-hinzurechnung` | 🟢 freigegeben (geht automatisch online) | Begleit-Reel zum Karussell vom 13.10. (12,8 s, echte Programm-Aufnahme, ohne Stimme) – neuer Mittwochs-Reel-Slot · [Freigabe #14](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/14) |
| Fr 16.10. 12:15 | 📱 Story `03-story-aufloesung` | 🟢 freigegeben (geht automatisch online) |  |
| Fr 16.10. 18:00 | 📱 Story `04-story-frage` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #44](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/44) |
| Fr 16.10. 19:30 | 🎬 Reel `16-reel-listen` | ✋ manuell (postest du in der App) | Serie Nummer 5: zwei Listen, SVERWEIS. Vorgezogen vom 22.10. – Serie damit durch. · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner. |

## 🗓️ Danach

| Wann | Was | Status | Hinweis |
|---|---|---|---|
| Sa 17.10. 19:30 | 🎬 Reel `04-reel-mein-weg` | ✋ manuell (postest du in der App) | Mein Weg rückwärts (Variante B, Loris hat den Text am 08.10. eingesprochen). Vorgezogen vom 27.10. KI-LABEL in Edits/Instagram einschalten (Karte 2 + 3 KI), Hinweis steht in der Bildunterschrift. Variante-A-Dateien: *_variante_a.* · Upload über Edits (08.10.): Loris lädt reel.mp4 + titelbild.png in Edits, Bildunterschrift aus bildunterschrift.txt, plant dort auf die Planzeit – der Autopilot postet NICHT. Stimme Loris (Aufnahme 08.10.), wörtliche Untertitel, Musik Runway (musik/QUELLEN.md). Anleitung: EDITS.md im Ordner. |
| Sa 17.10. 19:35 | 📱 Story `04-story-teaser` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #44](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/44) |
| Do 22.10. 12:15 | 📱 Story `10-story-umfrage` | 🟢 freigegeben (geht automatisch online) | Aus der Bibliothek: Umfrage E-Rechnung als Einstieg · [Freigabe #31](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/31) |
| Fr 23.10. 19:30 | 🖼️ Karussell `10-e-rechnung` | 🟢 freigegeben (geht automatisch online) | Aus der Bibliothek (gegengelesen 05.10., Rechtsstand Okt. 2026: § 27 Abs. 38 UStG) · 06.10.: auf Fr 23.10. geschoben (Reel-Takt alle 2 Tage). · [Freigabe #31](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/31) |
| Fr 23.10. 19:35 | 📱 Story `10-story-teaser` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #31](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/31) |
| Sa 24.10. 19:30 | 🎬 Reel `17-reel-kommentare` | ⏳ wartet auf sprachnachricht | Thema aus den Kommentaren der Serie (wird nach Auswertung bis ca. 20.10. festgelegt). Reel-Takt alle 2 Tage (06.10.). Upload über Edits: Claude baut das Reel komplett fertig (mit Musik, Untertiteln) und schickt es im Chat, Loris lädt es über Edits hoch und plant/postet selbst – der Autopilot postet NICHT (Status nach dem Schnitt: manuell). Sprechtext in posts/sprechtexte.md. |

## ✅ Zuletzt veröffentlicht (Autopilot)

- Fr 09.10. 12:35 · 📱 Story `05-story-teaser` · [ansehen](https://www.instagram.com/stories/maehrsteuern/4004067818916764813) (online 2026-10-09 12:35)
- Fr 09.10. 12:30 · 🖼️ Karussell `05-latente-steuern` · [ansehen](https://www.instagram.com/p/DeRTLb4EYwd/) (online 2026-10-09 12:31)
- Do 08.10. 19:35 · 📱 Story `06-story-teaser` · [ansehen](https://www.instagram.com/stories/maehrsteuern/4003554454352185254) (online 2026-10-08 19:35)
- Mi 07.10. 19:35 · 📱 Story `02-story-teaser` · [ansehen](https://www.instagram.com/stories/maehrsteuern/4002829658245043420) (online 2026-10-07 19:35)
- Mi 07.10. 19:30 · 🖼️ Karussell `02-excel-fehler` · [ansehen](https://www.instagram.com/p/DeM5u1vGLsR/) (online 2026-10-07 19:32)
- Mi 07.10. 12:15 · 📱 Story `05-story-frage` · [ansehen](https://www.instagram.com/stories/maehrsteuern/4002608197877985940) (online 2026-10-07 12:15)
- Di 06.10. 19:35 · 📱 Story `11-story-teaser` · [ansehen](https://www.instagram.com/stories/maehrsteuern/4002104878277412503) (online 2026-10-06 19:35)
- Di 06.10. 19:30 · 🎬 Reel `11-reel-monatsbericht` · [ansehen](https://www.instagram.com/reel/DeKUuvPgA1W/) (online 2026-10-06 19:30)
- Mo 05.10. 12:15 · 📱 Story `02-story-umfrage` · [ansehen](https://www.instagram.com/stories/maehrsteuern/4001158648931891388) (online 2026-10-05 12:15)
- So 04.10. 19:35 · 📱 Story `01-story-teaser-5dinge` · [ansehen](https://www.instagram.com/stories/maehrsteuern/4000661016565086455) (online 2026-10-04 19:46)

## 📈 Zahlen (täglich ca. 08:45)

**359 Follower** · 7 Beiträge im Profil (Abruf 2026-10-10) · **+1** seit 2026-10-09
Reichweite pro Tag: 06.10. **220** · 07.10. **136** · 08.10. **216** · 09.10. **66**

| Story (letzte 24 h) | Aufrufe | Erreicht | Antworten | Profilbesuche | Follows |
|---|---|---|---|---|---|
| Fr 09.10. 12:35 | 33 | 29 | 0 | 0 | 0 |
| Fr 09.10. 12:54 | 34 | 26 | 0 | 0 | 0 |

| Beitrag (letzte 14 Tage) | Aufrufe | Erreicht | Likes | Komm. | Gespeichert | Geteilt |
|---|---|---|---|---|---|---|
| Fr 09.10. 12:31 [Hör auf, 30 % fest einzutippen. 📉](https://www.instagram.com/p/DeRTLb4EYwd/) | 112 (+40) | 43 | 6 | 0 | 6 | 84 |
| Do 08.10. 19:30 [Gleiche Aufgabe, zwei Wege: Hebesatz von](https://www.instagram.com/reel/DePeYymNG2K/) | 286 (+11) | 222 | 7 | 0 | 8 | 25 |
| Mi 07.10. 19:32 [5 Excel-Fehler, die fast jede Steuerrück](https://www.instagram.com/p/DeM5u1vGLsR/) | 186 (+6) | 73 | 5 | 0 | 4 | 0 |
| Di 06.10. 19:30 [Zwei Stunden. Jeden Monat. Nur Copy-Past](https://www.instagram.com/reel/DeKUuvPgA1W/) | 375 (+1) | 284 | 11 | 2 | 10 | 8 |
| So 04.10. 19:30 [5 Dinge, die ich aus Excel rausgeschmiss](https://www.instagram.com/reel/DeFLK53ALSs/) | 915 (+4) | 674 | 13 | 10 | 15 | 16 |
| Do 01.10. 18:30 [Neu hier? Dann kurz zu mir 👋](https://www.instagram.com/p/Dd9V5HAAhcL/) | 354 (+3) | 132 | 10 | 2 | 2 | 17 |
| Di 29.09. 15:42 [Steuern × Code. ⚡](https://www.instagram.com/reel/Dd34F9RtucT/) | 326 (+0) | 187 | 10 | 2 | 4 | 7 |

Rohdaten: `automatik/statistik/`, Auswertung: `strategie/06_auswertung.md`

## ⚙️ Automatik

| Ablauf | Wann | Letzter Lauf |
|---|---|---|
| Lage + Google-Kalender | alle 15 Min. (LAGE.md, Kalender-Sync, Wächter) | ✅ ok |
| Posten | alle 15 Min. (postet freigegebene Einträge) | ✅ ok |
| Freigabe | bei neuen Entwürfen / Antwort im Issue | ✅ ok |
| Statistik | täglich ca. 08:45 | ✅ ok |
| Schlüssel verlängern | am 1. des Monats ca. 06:27 | ✅ ok |
| Radar + LinkedIn | täglich ca. 07:00 (Issue mit Arbeitsliste) | ✅ ok |
| Kommentare | nach jedem Posten-Takt (Vorschläge ins Issue) | ✅ ok |
| Wochenbericht | sonntags ca. 18:00 (ein Issue) | ✅ ok |
| Musik holen | nur von Hand | ✅ ok |

## 📜 Protokoll – jede Änderung

🤖 Autopilot · ✅ Freigabe · 📈 Statistik · 🎵 Musik · 🔀 Merge · ✍️ von Hand / Claude

**Sa 10.10.2026**
- 08:49 📈 Statistik 2026-10-10 ([`5fd657b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/5fd657b3c7b3798ffd911c6e243dc193a231de35))
  - `automatik/statistik`
- 07:04 📡 Radar 2026-10-10: 8 Beiträge, 0 DM-Entwürfe ([`f626328`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f626328688858f48feed9c8023210206cf3929a6))
  - `automatik/interaktion`

**Fr 09.10.2026**
- 15:47 📈 Statistik 2026-10-09 ([`79346c6`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/79346c66cf32cc4fb3a54b81827749e3e7b01bbe))
  - `automatik/statistik`
- 13:56 📡 Radar 2026-10-09: 8 Beiträge, 0 DM-Entwürfe ([`6837bf4`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/6837bf4cc8cc9607c1938351b4a04f397df157cf))
  - `automatik/interaktion`
- 12:35 🤖 Autopilot: 05-story-teaser veroeffentlicht ([`ff09f34`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ff09f3462a5439fd1a77b18400d1e643ba27b88f))
  - Plan: `05-story-teaser` status: freigegeben → veroeffentlicht; `05-story-teaser` online: https://www.instagram.com/stories/maehrsteuern/4004067818916764813
- 12:32 🤖 Autopilot: Dateien fuer 05-story-teaser vorbereitet ([`606887a`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/606887a622f73b7997e3b21789fe055ca873777f))
  - `posts/05_2026-10-08_latente_steuern`
- 12:31 🤖 Autopilot: 05-latente-steuern veroeffentlicht ([`afefee6`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/afefee6abd0848ee8dd8f942b12ce1abb8428d36))
  - Plan: `05-latente-steuern` status: freigegeben → veroeffentlicht; `05-latente-steuern` online: https://www.instagram.com/p/DeRTLb4EYwd/
- 11:15 🤖 Autopilot: Dateien fuer 05-latente-steuern vorbereitet ([`7e99d1f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/7e99d1f35b6ee4e5bace79c97ba157adf8023f33))
  - `posts/05_2026-10-08_latente_steuern`
- 08:48 📈 Statistik 2026-10-09 ([`177eda4`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/177eda42043631c50f2998d39d777203aafded82))
  - `automatik/statistik`
- 07:05 📡 Radar 2026-10-09: 8 Beiträge, 0 DM-Entwürfe ([`0c9c6fc`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/0c9c6fc3bc9e991c600d222579b7668cf1aba5c4))
  - `automatik/interaktion`

**Do 08.10.2026**
- 19:35 🤖 Autopilot: 06-story-teaser veroeffentlicht ([`7cfed5a`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/7cfed5abd434681ce018f0a123c80eb0491cf57b))
  - Plan: `06-story-teaser` status: freigegeben → veroeffentlicht; `06-story-teaser` online: https://www.instagram.com/stories/maehrsteuern/4003554454352185254
- 19:08 ✍️ Testmonat-Auswertung im Tagesbericht, plan.json mit stimme/hook, Fabrik 3× pro Woche ([`6dcd8c7`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/6dcd8c7968a14def4aa8cfc32248471bac62075b))
  - `LAGE.html`, `automatik/berichte`, `automatik/insights_voll.py`, `automatik/plan.json`, `automatik/tagesbericht.py`, `strategie/06_auswertung.md`, `…`
- 19:05 ✍️ Story-Quiz zum Antippen, Bio-Vorschlag mit Nutzen-Satz, Highlight „Start“ ([`582aabb`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/582aabb34e1bf44982ef8bd91f90189188ed7e89))
  - `LAGE.html`, `automatik/plan.json`, `posts/09_2026-10-15_rueckstellung`, `strategie/02_bio_highlights.md`, `vorlagen/system/jobs/p09_story_quiz_tippen.json`
- 19:03 ✍️ Routine Tagesbericht: neues Prompt mit Zugangsschritt, Kalender-Hinweis und Commit-Regel ([`ae0777f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ae0777fc08b87f56cdd5028499638a2259597158))
  - `automatik/routinen`
- 18:40 ✅ Freigabe #44: go ([`390a66d`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/390a66d43e28766dca308d7cc17a1895ec1b215e))
  - Plan: `04-story-frage` status: entwurf → freigegeben; `04-story-teaser` status: entwurf → freigegeben
- 18:31 🤖 Autopilot: Dateien fuer 06-story-teaser vorbereitet ([`6385791`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/63857917ff22592ef62b18671eddd2ec800ab2cb))
  - `posts/02_2026-10-06_excel_fehler`
- 16:05 📈 Statistik 2026-10-08 ([`55edf34`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/55edf34f548269184f9d3f6591adc15b0fa278db))
  - `automatik/statistik`
- 15:51 ✅ Freigabe angefragt (1 Beitrag/Beiträge) ([`16ff123`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/16ff12330f13313cdcc95c89bc9c5e1678a73dc5))
  - Plan: `04-story-frage` → Freigabe-Issue #44; `04-story-teaser` → Freigabe-Issue #44
- 15:50 ✍️ Tagesbericht: Methoden-Check erst ab 48 h, Reel-Länge, Heute-geplant-Liste ([`66cd01e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/66cd01eeed24ffb7d1e20811b6ed4e75635cdb1d))
  - `automatik/berichte`, `automatik/tagesbericht.py`
- 15:49 🔀 Merge pull request #43 from maehrsteuern/claude/focused-shannon-hrtyy7 ([`776c97e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/776c97e9409d714980d146efb4985e72337dd4f3))
- 15:41 🔀 Merge claude/instagram (Radar 08.10.), Lage neu erzeugt ([`79694ed`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/79694edad1b8dd49d7dd25953fabff045db1f649))
- 14:55 ✍️ Split-Reel in Edits geplant (Do 08.10. 19:30) ([`c90e7bb`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c90e7bb0f50dfe1d7d148cb9fe5f45e83073ea1f))
  - `LAGE.html`, `automatik/plan.json`
- 14:30 ✍️ Reel Nr. 2 Zeile: Einstieg „Jutta hat schon wieder …“ wieder drin ([`a41e46c`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a41e46c5119a4b5bbd1b7de8d949e786cd365b45))
  - `LAGE.html`, `automatik/plan.json`, `posts/12_2026-10-09_reel_zeile`, `vorlagen/system/schnitt/p12_reel_zeile_0810.json`, `vorlagen/system/schnitt/reels_0810_bauen.py`
- 14:03 📡 Radar 2026-10-08: 8 Beiträge, 0 DM-Entwürfe ([`a059875`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a059875b857f4f56170661b32248ffd76e3404a9))
  - `automatik/interaktion`
- 11:20 ✍️ Reels mit Loris' Stimme fertig: 8 Reels, ab heute täglich 19:30 (Edits, manuell) ([`eadde9e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/eadde9ec7f24e21028ced687f424ad20eedf2851))
  - Plan: `05-latente-steuern` zeit: 2026-10-09 19:30 → 2026-10-09 12:30; `05-story-teaser` zeit: 2026-10-09 19:35 → 2026-10-09 12:35; `12-reel-zeile` status: wartet_auf_sprachnachricht → manuell; `12-reel-zeile` zeit: 2026-10-12 19:30 → 2026-10-09 19:30; `08-reel-kst-staffel` status: freigegeben → manuell; `13-reel-verknuepfung` status: wartet_auf_sprachnachricht → manuell; `13-reel-verknuepfung` zeit: 2026-10-16 19:30 → 2026-10-11 19:30; `14-reel-versionen` status: wartet_auf_sprachnachricht → manuell; `14-reel-versionen` zeit: 2026-10-18 19:30 → 2026-10-12 19:30; `03-gewst-hinzurechnung` zeit: 2026-10-13 19:30 → 2026-10-13 12:30; `03-story-teaser` zeit: 2026-10-13 19:35 → 2026-10-13 12:35; `15-reel-rechnungsnummern` status: wartet_auf_sprachnachricht → manuell; `15-reel-rechnungsnummern` zeit: 2026-10-20 19:30 → 2026-10-13 19:30; `09-rueckstellung` zeit: 2026-10-15 19:30 → 2026-10-15 12:30; `09-story-teaser` zeit: 2026-10-15 19:35 → 2026-10-15 12:35; `04-story-frage` zeit: 2026-10-26 12:15 → 2026-10-15 18:00; `16-reel-listen` status: wartet_auf_sprachnachricht → manuell; `16-reel-listen` zeit: 2026-10-22 19:30 → 2026-10-15 19:30; `04-reel-mein-weg` status: wartet_auf_sprachnachricht → manuell; `04-reel-mein-weg` zeit: 2026-10-27 19:30 → 2026-10-16 19:30; `04-story-teaser` zeit: 2026-10-27 19:35 → 2026-10-16 19:35
- 10:53 ✍️ Add files via upload ([`57a5004`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/57a5004dc3b20c04644e78bcb86e3b07fd2ff393))
  - `08.10.2026 10.38.mp3`, `08.10.2026 10.39.mp3`, `08.10.2026 10.41.mp3`, `08.10.2026 10.42(2).mp3`, `08.10.2026 10.42.mp3`, `08.10.2026 10.43(2).mp3`, `…`
- 10:51 ✍️ Lage neu erzeugt (Sitzungsstart 08.10.) ([`9baf27e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/9baf27eb474eb8da24c86eda1ebd0a45fdec6343))
  - `LAGE.html`
- 08:48 📈 Statistik 2026-10-08 ([`7abdbc6`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/7abdbc6f628d3ff57b68e0630f6c833f8da9bff0))
  - `automatik/statistik`
- 07:05 📡 Radar 2026-10-08: 8 Beiträge, 0 DM-Entwürfe ([`24a5a4f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/24a5a4ffd0c8dc898c67f078a9bce7f64a4ba470))
  - `automatik/interaktion`

**Mi 07.10.2026**
- 19:35 🤖 Autopilot: 02-story-teaser veroeffentlicht ([`e476372`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e476372f52ceb6d0bc4bee2debcd9b34867e3ac9))
  - Plan: `02-story-teaser` status: freigegeben → veroeffentlicht; `02-story-teaser` online: https://www.instagram.com/stories/maehrsteuern/4002829658245043420
- 19:32 🤖 Autopilot: Dateien fuer 02-story-teaser vorbereitet ([`abc4d88`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/abc4d88f198aa0cf7fba3cb751486cb4235ce6ab))
  - `posts/02_2026-10-06_excel_fehler`
- 19:32 🤖 Autopilot: 02-excel-fehler veroeffentlicht ([`1e9ba27`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1e9ba27479847ba2022ae3b4cd03e91954f8155a))
  - Plan: `02-excel-fehler` status: freigegeben → veroeffentlicht; `02-excel-fehler` online: https://www.instagram.com/p/DeM5u1vGLsR/
- 16:34 ✍️ Bibliothek Runden 5 und 6: 400 Assets (jetzt 996) ([`722b914`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/722b9140f6ff0cbcc8fce8cb4eec2087cdad236f))
  - `LAGE.html`, `README.md`, `assets/bibliothek/PRUEFBERICHT.md`, `assets/bibliothek/README.md`, `assets/bibliothek/bausteine/abspann_frist.png`, `assets/bibliothek/bausteine/abspann_plausi.png`, `…`
- 16:02 ✍️ Bibliothek Runde 7: MBS-Reels (10 Titel, 4 Einblendungen) ([`070fd3b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/070fd3b4a71c53a5b19c0cdf439b18642f30e189))
  - `LAGE.html`, `README.md`, `assets/bibliothek/README.md`, `assets/bibliothek/bausteine/mbs_abspann_demo.png`, `assets/bibliothek/bausteine/mbs_haken_baum.png`, `assets/bibliothek/bausteine/mbs_haken_ueber_ampel.png`, `…`
- 15:57 📈 Statistik 2026-10-07 ([`4a88e46`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4a88e46e8170ddfc9874c707f10498163fa293fa))
  - `automatik/statistik`
- 13:48 📡 Radar 2026-10-07: 8 Beiträge, 0 DM-Entwürfe ([`60f7657`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/60f76576125ce2bb92dcf47d8139fbd84f33690b))
  - `automatik/interaktion`
- 12:15 🤖 Autopilot: 05-story-frage veroeffentlicht ([`9709ca9`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/9709ca9674c2c5decabc5e417c2cabe3ec52fed2))
  - Plan: `05-story-frage` status: freigegeben → veroeffentlicht; `05-story-frage` online: https://www.instagram.com/stories/maehrsteuern/4002608197877985940
- 11:00 🤖 Autopilot: Dateien fuer 05-story-frage vorbereitet ([`a8342f2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a8342f2bcef7afa73ebcde2c8b2e0e4b17cf81ec))
  - `posts/05_2026-10-08_latente_steuern`
- 08:47 📈 Statistik 2026-10-07 ([`281779f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/281779f62c7d99ba9a9f36191ffec48836d91250))
  - `automatik/statistik`
- 07:05 📡 Radar 2026-10-07: 8 Beiträge, 0 DM-Entwürfe ([`b4bb83c`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/b4bb83c7f8f93671ce6847808a8dc4b36ec6b407))
  - `automatik/interaktion`

**Di 06.10.2026**
- 21:10 ✍️ Titelbild-Vorlage „Excel vs. Code“ (titel_split.html) für das Split-Reel – Varianten zur Auswahl ([`45579b6`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/45579b6ad03fb20a6d2c3452a98444a2a89f3800))
  - `posts/02_2026-10-06_excel_fehler`, `vorlagen/system/render.mjs`, `vorlagen/system/titel_split.html`
- 21:07 ✍️ montage.py: stumme Tonspur behoben – Split- und KSt-Reel mit Ton neu gerendert ([`1413df2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1413df2f4329f7f252b56cdf8ce5d3f77e9f012b))
  - `LAGE.html`, `automatik/lage_notizen.md`, `posts/02_2026-10-06_excel_fehler`, `posts/08_2026-10-09_reel_kst_staffel`, `vorlagen/system/montage.py`
- 20:50 ✍️ Reel-Serie: komplett fertig liefern (inkl. Musik), Loris lädt über Edits hoch ([`e490c8d`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e490c8d24f38c8e94696626468fed05fcd5c2718))
  - `LAGE.html`, `automatik/lage_notizen.md`, `automatik/plan.json`
- 20:49 ✍️ Stand claude/instagram übernommen ([`a1fda23`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a1fda236acc2b7523259e14a26b6d07a183bf706))
- 20:49 ✍️ Reel-Takt alle 2 Tage bis 24.10.: 6 neue Reel-Slots + 5 Sprechtexte (Serie Nummer 2–5 + Verknüpfung) ([`ac88455`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ac884553c77ec5411a0e2dc8ce4ee97ac4ed083f))
  - Plan: neu `12-reel-zeile` (2026-10-12 19:30, wartet_auf_sprachnachricht); neu `13-reel-verknuepfung` (2026-10-16 19:30, wartet_auf_sprachnachricht); neu `14-reel-versionen` (2026-10-18 19:30, wartet_auf_sprachnachricht); neu `15-reel-rechnungsnummern` (2026-10-20 19:30, wartet_auf_sprachnachricht); neu `16-reel-listen` (2026-10-22 19:30, wartet_auf_sprachnachricht); neu `17-reel-kommentare` (2026-10-24 19:30, wartet_auf_sprachnachricht); `10-story-umfrage` zeit: 2026-10-21 12:15 → 2026-10-22 12:15; `10-e-rechnung` zeit: 2026-10-22 19:30 → 2026-10-23 19:30; `10-story-teaser` zeit: 2026-10-22 19:35 → 2026-10-23 19:35; `04-story-frage` zeit: 2026-10-19 12:15 → 2026-10-26 12:15; `04-reel-mein-weg` zeit: 2026-10-20 19:30 → 2026-10-27 19:30; `04-story-teaser` zeit: 2026-10-20 19:35 → 2026-10-27 19:35
- 20:45 📈 Statistik: Schnellabruf einzelner Beiträge (nur Protokoll, keine Dateien) ([`a028389`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a028389fd39fec8aeefb0d76ec5acecd5ee5fb2c))
  - `.github/workflows`, `automatik/beitrag_jetzt.py`
- 20:44 ✍️ Edits-Test: Split-Reel Do 08.10. von Loris in Edits (manuell), Woche verschoben ([`ea2ce8f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ea2ce8fa74a159a7beb35cbfcc8accc9c6499de3))
  - Plan: `06-reel-split` status: freigegeben → manuell; `06-reel-split` zeit: 2026-10-11 19:30 → 2026-10-08 19:30; `06-story-teaser` zeit: 2026-10-11 19:35 → 2026-10-08 19:35; `05-latente-steuern` zeit: 2026-10-08 19:30 → 2026-10-09 19:30; `05-story-teaser` zeit: 2026-10-08 19:35 → 2026-10-09 19:35; `08-story-heute` zeit: 2026-10-09 12:15 → 2026-10-10 12:15; `08-reel-kst-staffel` zeit: 2026-10-09 19:30 → 2026-10-10 19:30; `08-story-rueckblick` zeit: 2026-10-10 12:15 → 2026-10-11 12:15
- 19:35 🤖 Autopilot: 11-story-teaser veroeffentlicht ([`461142e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/461142eef2e2d6b5a0a87e5afc8355fe1aef4e4d))
  - Plan: `11-story-teaser` status: freigegeben → veroeffentlicht; `11-story-teaser` online: https://www.instagram.com/stories/maehrsteuern/4002104878277412503
- 19:33 🤖 Autopilot: Dateien fuer 11-story-teaser vorbereitet ([`ee11a38`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ee11a38228eba20470b2a90f856cc2ef92c0ad70))
  - `posts/11_2026-10-07_reel_monatsbericht`
- 19:30 🤖 Autopilot: 11-reel-monatsbericht veroeffentlicht ([`cc1c6cd`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/cc1c6cdf9569ac208f740249a8bce31a07f9392e))
  - Plan: `11-reel-monatsbericht` status: freigegeben → veroeffentlicht; `11-reel-monatsbericht` online: https://www.instagram.com/reel/DeKUuvPgA1W/
- 18:15 🤖 Autopilot: Dateien fuer 11-reel-monatsbericht vorbereitet ([`1ffae8c`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1ffae8c0517ab28cf932f749de5a62628339f0f3))
  - `posts/11_2026-10-07_reel_monatsbericht`
- 15:39 📈 Statistik 2026-10-06 ([`7b45a11`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/7b45a114620537823b44d3d9103db877910dbc23))
  - `automatik/statistik`
- 14:03 📡 Radar 2026-10-06: 8 Beiträge, 0 DM-Entwürfe ([`53d5ace`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/53d5acee2585587251978ea768430868550bbc18))
  - Plan: neu `00-start-1` (2026-09-30 12:30, veroeffentlicht); neu `00-start-2` (2026-09-30 12:31, veroeffentlicht); neu `00-start-3` (2026-09-30 12:32, veroeffentlicht); neu `00-vorfreude` (2026-09-30 19:30, veroeffentlicht); neu `00-neuvorstellung` (2026-10-01 18:30, veroeffentlicht); neu `00-story-teaser` (2026-10-01 18:35, entfaellt); neu `01-story-frage` (2026-10-02 12:15, veroeffentlicht); neu `08-story-tipp` (2026-10-03 12:15, veroeffentlicht); neu `01-reel-ampel` (2026-10-04 19:30, pause); neu `01-reel-5dinge` (2026-10-04 19:30, veroeffentlicht); neu `01-story-teaser` (2026-10-04 19:35, pause); neu `01-story-teaser-5dinge` (2026-10-04 19:35, veroeffentlicht); neu `02-story-umfrage` (2026-10-05 12:15, veroeffentlicht); neu `11-reel-monatsbericht` (2026-10-06 19:30, freigegeben); neu `11-story-teaser` (2026-10-06 19:35, freigegeben); neu `05-story-frage` (2026-10-07 12:15, freigegeben); neu `02-excel-fehler` (2026-10-07 19:30, freigegeben); neu `02-story-teaser` (2026-10-07 19:35, freigegeben); neu `05-latente-steuern` (2026-10-08 19:30, freigegeben); neu `05-story-teaser` (2026-10-08 19:35, freigegeben); neu `08-story-heute` (2026-10-09 12:15, freigegeben); neu `08-reel-kst-staffel` (2026-10-09 19:30, freigegeben); neu `08-story-rueckblick` (2026-10-10 12:15, freigegeben); neu `06-reel-split` (2026-10-11 19:30, freigegeben); neu `06-story-teaser` (2026-10-11 19:35, freigegeben); neu `03-story-quiz` (2026-10-12 12:15, freigegeben); neu `03-gewst-hinzurechnung` (2026-10-13 19:30, freigegeben); neu `03-story-teaser` (2026-10-13 19:35, freigegeben); neu `09-story-quiz` (2026-10-14 12:15, entwurf); neu `07-reel-hinzurechnung` (2026-10-14 19:30, freigegeben); neu `09-story-aufloesung` (2026-10-15 12:15, entwurf); neu `09-rueckstellung` (2026-10-15 19:30, entwurf); neu `09-story-teaser` (2026-10-15 19:35, entwurf); neu `03-story-aufloesung` (2026-10-16 12:15, freigegeben); neu `04-story-frage` (2026-10-19 12:15, entwurf); neu `04-reel-mein-weg` (2026-10-20 19:30, wartet_auf_sprachnachricht); neu `04-story-teaser` (2026-10-20 19:35, entwurf); neu `10-story-umfrage` (2026-10-21 12:15, freigegeben); neu `10-e-rechnung` (2026-10-22 19:30, freigegeben); neu `10-story-teaser` (2026-10-22 19:35, freigegeben)
