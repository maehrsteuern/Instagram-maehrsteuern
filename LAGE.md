# 🧭 Lage – maehrsteuern auf Instagram

_Automatisch erzeugt von `automatik/lage.py` – nicht von Hand bearbeiten (Notizen: `automatik/lage_notizen.md`). Stand: letzte Änderung Mo 05.10. 09:13 Uhr._

**Als Nächstes online:** 📱 Story `02-story-umfrage` am **Mo 05.10. 12:15 Uhr** – 🟢 freigegeben (geht automatisch online)

## 📝 Gerade in Arbeit

- Neustart läuft: Start-Storys + Vorfreude (30.09.) und Neuvorstellung (Do 01.10. 18:30, von Hand) sind online. Nach 2 h: 26 erreicht, 6× geteilt, 0 neue Follower. Angepinnt ✓ (03.10.). Offen von Hand: Highlight „Start 👋“.
- Wochenrhythmus ab Okt. steht im Prompt der Content-Fabrik (Mo + Do 08:47, max. 4 Beiträge pro Lauf): Di/Do Karussell + Teaser, Mi Begleit-Reel, Fr Wissens-Reel oder Stimm-Reel, So Reel + Teaser, täglich 12:15 Story.
- Content-Fabrik nutzt ab Mo 05.10. die Lernpunkte aus `strategie/wettbewerb.md` (über Abschnitt in `08_hooks.md`): pro Lauf ≥ 1 Hook „konkreter Fall“ oder „Prüfer/Finanzamt“, Lernpunkt im Freigabe-Issue vermerkt. Routine-Prompt selbst unverändert (nur aus ihrer eigenen Sitzung änderbar).
- **So 04.10. umgebaut:** Statt Ampel-Reel geht 19:30 das Community-Reel „5 Sachen, die ich aus Excel rausgeschmissen hab“ online (Loris' Sprachnachricht, 41 s, keine Werbung, CTA: Zahl 1–5 in die Kommentare) + neue Teaser-Story 19:35. Ampel-Reel und alter Teaser stehen auf `pause` – kann später wieder eingeplant werden. Die Kommentar-Antworten (welche Nummer?) sind die Themen für die nächsten Reels.
- **Doppel-Post 04.10. behoben:** Das 5-Dinge-Reel ging zweimal raus (DeFLK53ALSs = im Plan, DeFLSBNFUXy = Duplikat, von Loris am 04.10. gelöscht ✓). Ursache: Ein Lauf startet mit dem Stand vom Startzeitpunkt und hat den Plan nur nach dem Warten neu geladen. `posten.py` holt jetzt direkt vor jedem Posten den neuesten Plan; klappt das nicht, wird nicht gepostet (nächster Lauf holt nach).
- Bis 10.10. alles freigegeben: 5-Dinge-Reel (So 04.10.), Excel-Fehler (Di 06.10.), Split-Reel als Begleit-Reel (Mi 07.10., vorgezogen), latente Steuern (Do 08.10.), Wissens-Reel KSt-Staffel (Fr 09.10.). So 11.10. ist frei → Fabrik am Mo 05.10.
- Latente Steuern: Prüfzettel Punkte 1–5 am 05.10. mit Quellen geprüft ✓ – Box Folie 6 präzisiert (kleine KapGes: von § 274 befreit, passive Latenzen ggf. als Rückstellung), fachlich nichts mehr offen (`pruefzettel.md` im Post-Ordner; „Abschluss 2026“ am 05.10. überall auf „spätestens jetzt“ geändert – Folien 1+7, Bildunterschrift, Teaser, LinkedIn-Text + PDF). Änderungen bis Mi 07.10. abends.
- Sprachnachricht zu „Fr 09.10.“ aus `posts/sprechtexte.md` bis Do 08.10. → ersetzt dann das Wissens-Reel durch das Stimm-Reel.
- Reel „Mein Weg“ (20.10.): **Loris baut die Konzeption selbst um (03.10.)** – bis dahin gilt Variante B (`drehbuch_markenweg.md`) nicht als gesetzt, keine Sprachnachricht anfordern, nichts schneiden. Status bleibt `wartet_auf_sprachnachricht`, bis das neue Konzept da ist. **KI-Hinweis** (falls KI-Karten bleiben): Hinweis in der Bildunterschrift, Label nach dem Posten in der App prüfen.
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
- **Bibliothek aus dem Brand Kit (Claude Design) gebaut (02.10.):** 365 fertige Bilder in `assets/bibliothek/` (Übersicht `README.md` dort), Texte als Job-Dateien in `vorlagen/system/jobs/bibliothek/`. Neue Vorlagen `zahl.html` + `banner.html`, Highlight-Symbole, Vergleichstabelle/Checkliste im Karussell. Nichts davon ist eingeplant. **Gegengelesen (05.10.):** 10 Fehler korrigiert, 25 Zweifelsfälle mit Loris entschieden und umgesetzt → `assets/bibliothek/PRUEFBERICHT.md`. Offen nur: Zinsschranke-Caption mit Hinweis auf Untergang des Zinsvortrags. **Erste Bibliothek-Beiträge eingeplant (05.10., als Entwurf → Freigabe-Issue):** Rückstellung in 6 Schritten Do 15.10. (Quiz SolZ Mi 14.10., Auflösung Do 15.10. 12:15, Teaser 19:35) · E-Rechnung-Fahrplan Do 22.10. (Umfrage Mi 21.10., Teaser 19:35). Content-Fabrik: diese Slots sind belegt. **Runde 4 ergänzt (05.10.):** +217 Bilder (jetzt 582) – GmbH/Gesellschafter, Bilanz, USt, Lohn, ErbSt/GrESt, Paragraf als Formel, Steuerkalender, GoBD, Mythos/Glossar Teil 2, Einzelposts, Storys, Reel-Titel, Einblendungen, Highlights, Ampeln (`r4_*.json`), nichts eingeplant. 6 Korrekturen vor dem Rendern, 4 Zweifelsfälle + Platzhalter „312 Testfälle“ / § 8c-Quoten 48/62 % offen → Prüfbericht Abschnitt „Runde 4“.
- **Lage als Seite (04.10.):** `LAGE.html` mit Kacheln, Kalender, Diagrammen und filterbarem Protokoll, wird mit LAGE.md neu geschrieben und über GitHub Pages veröffentlicht (https://maehrsteuern.github.io/Instagram-maehrsteuern/). Pages eingeschaltet ✓ (04.10.), Seite läuft und aktualisiert sich bei jeder neuen Lage automatisch.

## 👉 Braucht dich

- ⏳ **Wartet auf sprachnachricht** `09-reel-monatsbericht` (So 11.10. 19:30) – Folge-Reel zu Nummer 1 aus dem 5-Dinge-Reel (04.10.): Monatsbericht in 3 Schritten (SuSa einlesen → abstimmen → PDF), Code-Ausschnitte zum Nachbauen, keine Werbung. Sprechtext „So 11.10.“ in posts/sprechtexte.md – Sprachnachricht bis Fr 09.10.
- 🟡 **Freigeben** `09-story-teaser` (So 11.10. 19:35) – „go“ oder „stop“ im Issue (Issue kommt, sobald `09-reel-monatsbericht` fertig ist)
- 🟡 **Freigeben** `09-story-quiz` (Mi 14.10. 12:15) – „go“ oder „stop“ im Issue (Issue kommt, sobald `09-reel-monatsbericht` fertig ist)
- 🟡 **Freigeben** `09-story-aufloesung` (Do 15.10. 12:15) – „go“ oder „stop“ im Issue (Issue kommt, sobald `09-reel-monatsbericht` fertig ist)
- 🟡 **Freigeben** `09-rueckstellung` (Do 15.10. 19:30) – „go“ oder „stop“ im Issue (Issue kommt, sobald `09-reel-monatsbericht` fertig ist)
- 🟡 **Freigeben** `09-story-teaser` (Do 15.10. 19:35) – „go“ oder „stop“ im Issue (Issue kommt, sobald `09-reel-monatsbericht` fertig ist)
- 🟡 **Freigeben** `04-story-frage` (Mo 19.10. 12:15) – „go“ oder „stop“ im Issue (Issue kommt, sobald `04-reel-mein-weg` fertig ist)
- ⏳ **Wartet auf sprachnachricht** `04-reel-mein-weg` (Di 20.10. 19:30) – Konzept wird von Loris umgebaut (03.10.) – Variante B (drehbuch_markenweg.md) vorerst nicht gesetzt, keine Sprachnachricht anfordern; bei KI-Karten: Hinweis in der Bildunterschrift, KI-Label nach dem Posten in der App prüfen
- 🎵 **Musik fehlt** `04-reel-mein-weg` (Di 20.10. 19:30)
- 🟡 **Freigeben** `04-story-teaser` (Di 20.10. 19:35) – „go“ oder „stop“ im Issue (Issue kommt, sobald `04-reel-mein-weg` fertig ist)
- ⏰ **💼 LinkedIn-Karussell „Excel-Fehler“ posten (Issue #18)** (Mi 07.10. 08:00) – PDF + Text im Issue #18, danach 1 h Kommentare beantworten und #18 schließen. Termin steht schon automatisch im Kalender (Chrome Modul 5).

## ⏭️ Nächste 7 Tage

| Wann | Was | Status | Hinweis |
|---|---|---|---|
| Mo 05.10. 12:15 | 📱 Story `02-story-umfrage` | 🟢 freigegeben (geht automatisch online) |  |
| Di 06.10. 19:30 | 🖼️ Karussell `02-excel-fehler` | 🟢 freigegeben (geht automatisch online) |  |
| Di 06.10. 19:35 | 📱 Story `02-story-teaser` | 🟢 freigegeben (geht automatisch online) |  |
| Mi 07.10. 12:15 | 📱 Story `05-story-frage` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #12](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/12) |
| Mi 07.10. 19:30 | 🎬 Reel `06-reel-split` | 🟢 freigegeben (geht automatisch online) | Begleit-Reel zum Karussell Excel-Fehler vom Di 06.10. (Split-Screen Excel gegen Tool), auf Loris' Wunsch am 01.10. von So 11.10. auf Mi 07.10. vorgezogen. · [Freigabe #13](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/13) |
| Mi 07.10. 19:35 | 📱 Story `06-story-teaser` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #13](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/13) |
| Do 08.10. 19:30 | 🖼️ Karussell `05-latente-steuern` | 🟢 freigegeben (geht automatisch online) | Rechtsstand: KSt-Staffel 2028–2032 laut Investitionssofortprogramm 2025, § 274 Abs. 2 HGB – bitte fachlich gegenlesen · [Freigabe #12](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/12) |
| Do 08.10. 19:35 | 📱 Story `05-story-teaser` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #12](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/12) |
| Fr 09.10. 12:15 | 📱 Story `08-story-heute` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #15](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/15) |
| Fr 09.10. 19:30 | 🎬 Reel `08-reel-kst-staffel` | 🟢 freigegeben (geht automatisch online) | Wissens-Reel (These + Zahl, 10 s) zum Karussell latente Steuern vom 08.10. Wer schickt das an wen: Steuerabteilung an den Kollegen mit der Excel, in der noch 30 % steht. Suchbegriffe: latente Steuern, Steuersatz 2028, KSt-Senkung. Keine Sprachnachricht da – liegt bis Do 08.10. eine zum Sprechtext Fr 09.10. vor, ersetzt das Stimm-Reel dieses. · [Freigabe #15](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/15) |
| Sa 10.10. 12:15 | 📱 Story `08-story-rueckblick` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #15](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/15) |
| So 11.10. 19:30 | 🎬 Reel `09-reel-monatsbericht` | ⏳ wartet auf sprachnachricht | Folge-Reel zu Nummer 1 aus dem 5-Dinge-Reel (04.10.): Monatsbericht in 3 Schritten (SuSa einlesen → abstimmen → PDF), Code-Ausschnitte zum Nachbauen, keine Werbung. Sprechtext „So 11.10.“ in posts/sprechtexte.md – Sprachnachricht bis Fr 09.10. |
| So 11.10. 19:35 | 📱 Story `09-story-teaser` | 🟡 Entwurf (wartet auf Freigabe) |  |

## 🗓️ Danach

| Wann | Was | Status | Hinweis |
|---|---|---|---|
| Mo 12.10. 12:15 | 📱 Story `03-story-quiz` | 🟢 freigegeben (geht automatisch online) |  |
| Di 13.10. 19:30 | 🖼️ Karussell `03-gewst-hinzurechnung` | 🟢 freigegeben (geht automatisch online) |  |
| Di 13.10. 19:35 | 📱 Story `03-story-teaser` | 🟢 freigegeben (geht automatisch online) |  |
| Mi 14.10. 12:15 | 📱 Story `09-story-quiz` | 🟡 Entwurf (wartet auf Freigabe) | Aus der Bibliothek: Quiz SolZ als Einstieg zum Rückstellungs-Karussell |
| Mi 14.10. 19:30 | 🎬 Reel `07-reel-hinzurechnung` | 🟢 freigegeben (geht automatisch online) | Begleit-Reel zum Karussell vom 13.10. (12,8 s, echte Programm-Aufnahme, ohne Stimme) – neuer Mittwochs-Reel-Slot · [Freigabe #14](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/14) |
| Do 15.10. 12:15 | 📱 Story `09-story-aufloesung` | 🟡 Entwurf (wartet auf Freigabe) |  |
| Do 15.10. 19:30 | 🖼️ Karussell `09-rueckstellung` | 🟡 Entwurf (wartet auf Freigabe) | Aus der Bibliothek (gegengelesen 05.10., Demo-Zahlen 1 Mio. €, Hebesatz 400 %) |
| Do 15.10. 19:35 | 📱 Story `09-story-teaser` | 🟡 Entwurf (wartet auf Freigabe) |  |
| Fr 16.10. 12:15 | 📱 Story `03-story-aufloesung` | 🟢 freigegeben (geht automatisch online) |  |
| Mo 19.10. 12:15 | 📱 Story `04-story-frage` | 🟡 Entwurf (wartet auf Freigabe) |  |
| Di 20.10. 19:30 | 🎬 Reel `04-reel-mein-weg` | ⏳ wartet auf sprachnachricht | Konzept wird von Loris umgebaut (03.10.) – Variante B (drehbuch_markenweg.md) vorerst nicht gesetzt, keine Sprachnachricht anfordern; bei KI-Karten: Hinweis in der Bildunterschrift, KI-Label nach dem Posten in der App prüfen |
| Di 20.10. 19:35 | 📱 Story `04-story-teaser` | 🟡 Entwurf (wartet auf Freigabe) |  |
| Mi 21.10. 12:15 | 📱 Story `10-story-umfrage` | 🟢 freigegeben (geht automatisch online) | Aus der Bibliothek: Umfrage E-Rechnung als Einstieg · [Freigabe #31](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/31) |
| Do 22.10. 19:30 | 🖼️ Karussell `10-e-rechnung` | 🟢 freigegeben (geht automatisch online) | Aus der Bibliothek (gegengelesen 05.10., Rechtsstand Okt. 2026: § 27 Abs. 38 UStG) · [Freigabe #31](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/31) |
| Do 22.10. 19:35 | 📱 Story `10-story-teaser` | 🟢 freigegeben (geht automatisch online) |  · [Freigabe #31](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/31) |

## ✅ Zuletzt veröffentlicht (Autopilot)

- So 04.10. 19:35 · 📱 Story `01-story-teaser-5dinge` · [ansehen](https://www.instagram.com/stories/maehrsteuern/4000661016565086455) (online 2026-10-04 19:46)
- So 04.10. 19:30 · 🎬 Reel `01-reel-5dinge` · [ansehen](https://www.instagram.com/reel/DeFLK53ALSs/) (online 2026-10-04 19:30)
- Sa 03.10. 12:15 · 📱 Story `08-story-tipp` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3999709094836161880) (online 2026-10-03 12:15)
- Fr 02.10. 12:15 · 📱 Story `01-story-frage` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3998984318181825905) (online 2026-10-02 12:15)
- Do 01.10. 18:30 · 🖼️ Karussell `00-neuvorstellung` · [ansehen](https://www.instagram.com/p/Dd9V5HAAhcL/) (online 2026-10-01 18:30)
- Mi 30.09. 19:30 · 📱 Story `00-vorfreude` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3997727075650058524) (online 2026-09-30 18:37)
- Mi 30.09. 12:32 · 📱 Story `00-start-3` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3997545080966344429) (online 2026-09-30 12:35)
- Mi 30.09. 12:31 · 📱 Story `00-start-2` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3997544897742372327) (online 2026-09-30 12:35)
- Mi 30.09. 12:30 · 📱 Story `00-start-1` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3997544707312529712) (online 2026-09-30 12:35)

## 📈 Zahlen (täglich ca. 08:45)

**352 Follower** · 3 Beiträge im Profil (Abruf 2026-10-05) · **+1** seit 2026-10-04
Reichweite pro Tag: 01.10. **68** · 02.10. **79** · 03.10. **63** · 04.10. **418**

| Story (letzte 24 h) | Aufrufe | Erreicht | Antworten | Profilbesuche | Follows |
|---|---|---|---|---|---|
| So 04.10. 19:46 | 51 | 44 | 0 | 0 | 0 |
| So 04.10. 19:50 | 53 | 40 | 0 | 1 | 1 |

| Beitrag (letzte 14 Tage) | Aufrufe | Erreicht | Likes | Komm. | Gespeichert | Geteilt |
|---|---|---|---|---|---|---|
| So 04.10. 19:30 [5 Dinge, die ich aus Excel rausgeschmiss](https://www.instagram.com/reel/DeFLK53ALSs/) | 519 (+296) | 406 | 5 | 2 | 8 | 3 |
| Do 01.10. 18:30 [Neu hier? Dann kurz zu mir 👋](https://www.instagram.com/p/Dd9V5HAAhcL/) | 302 (+4) | 110 | 8 | 2 | 2 | 16 |
| Di 29.09. 15:42 [Steuern × Code. ⚡](https://www.instagram.com/reel/Dd34F9RtucT/) | 281 (+3) | 167 | 6 | 2 | 2 | 7 |

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

**Mo 05.10.2026**
- 09:13 ✅ Freigabe #31: go ([`fc33faf`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/fc33faf70167f966ac3f31f801fbb370ec70f21e))
  - Plan: `10-story-umfrage` status: entwurf → freigegeben; `10-e-rechnung` status: entwurf → freigegeben; `10-story-teaser` status: entwurf → freigegeben
- 09:06 ✍️ Stand claude/instagram übernommen ([`53b4eaf`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/53b4eaf085e3b802e2b0e1698a2b6d6a4eedf704))
- 09:06 ✍️ Reel 11.10. Monatsbericht: Bilder (3 Schritte), Titelbild, Teaser, Bildunterschrift, Drehbuch ([`b197f71`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/b197f7113caee3b60e3dc3c002797a50e42b5b7c))
  - `LAGE.html`, `posts/09_2026-10-11_reel_monatsbericht`, `posts/sprechtexte.md`, `vorlagen/system/fuenf_dinge.html`, `vorlagen/system/jobs/p09_reel_monatsbericht.json`
- 09:05 ✅ Freigabe angefragt (1 Beitrag/Beiträge) ([`8ca2ae2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/8ca2ae236f636b31dfadd9054c658953f92cc3a4))
  - Plan: `10-story-umfrage` → Freigabe-Issue #31; `10-e-rechnung` → Freigabe-Issue #31; `10-story-teaser` → Freigabe-Issue #31
- 09:05 🔀 Merge remote-tracking branch 'origin/claude/instagram' into ccr-e6f8d1b2-zd8pzn ([`c77b202`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c77b2029d7d18815b0e9539038a26353f2166d13))
- 09:05 ✍️ Erste Bibliothek-Beiträge eingeplant: Rückstellung (15.10.) und E-Rechnung (22.10.) ([`14efa48`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/14efa482bd2af59d6966f30dc6ae35c5eca2a9f1))
  - Plan: neu `09-story-quiz` (2026-10-14 12:15, entwurf); neu `09-story-aufloesung` (2026-10-15 12:15, entwurf); neu `09-rueckstellung` (2026-10-15 19:30, entwurf); neu `09-story-teaser` (2026-10-15 19:35, entwurf); neu `10-story-umfrage` (2026-10-21 12:15, entwurf); neu `10-e-rechnung` (2026-10-22 19:30, entwurf); neu `10-story-teaser` (2026-10-22 19:35, entwurf)
- 09:03 ✍️ Reel So 11.10. eingeplant: „Nummer 1: Der Monatsbericht“ (wartet auf Sprachnachricht) ([`dc36957`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/dc369579b6a2ad1835017ac59cf1e0fe1137e099))
  - Plan: neu `09-reel-monatsbericht` (2026-10-11 19:30, wartet_auf_sprachnachricht); neu `09-story-teaser` (2026-10-11 19:35, entwurf)
- 09:03 ✍️ Lage-Notiz: globaler Reclaim-Puffer 10 Min. entschieden ([`384fa87`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/384fa8755b9dfe73c4f34ad54f00d77a0846f180))
  - `LAGE.html`, `automatik/lage_notizen.md`
- 09:02 🔀 Merge remote-tracking branch 'origin/claude/instagram' into claude/instagram ([`ff02a11`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ff02a11e25af47725737b0578a24172525306ca7))
- 09:02 ✍️ Lage-Notiz: Chrome-Check Sprint 2 eingetragen – nur Testbuchung und Puffer offen ([`4afac31`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4afac31f1821607173ab39a0fc86320728a251c1))
  - `LAGE.html`, `automatik/lage_notizen.md`
- 09:02 🔀 Merge remote-tracking branch 'origin/claude/instagram' into claude/instagram ([`322e9a0`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/322e9a0f68abb1e6c8cfc94fd5c361e53fe38a23))
- 09:02 💼 LinkedIn Excel-Fehler: Punkt 1 um KSt-Senkung ab 2028 ergänzt ([`e2566fb`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e2566fb480b207cb97497a659f0e616290ba79e0))
  - `LAGE.html`, `posts/02_2026-10-06_excel_fehler`
- 09:01 🔀 Merge remote-tracking branch 'origin/claude/instagram' into instagram-merge ([`93ebbbf`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/93ebbbfad07e8fe0dd9864ffd9c6151db587c386))
- 09:01 ✍️ Bibliothek: 25 Zweifelsfälle entschieden und umgesetzt ([`9c2dcd6`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/9c2dcd64d6c93ec74e5adb0491d2ef39c2f32014))
  - `LAGE.html`, `assets/bibliothek/PRUEFBERICHT.md`, `assets/bibliothek/bausteine/haken_8b.png`, `assets/bibliothek/karussell/bewirtung/folie_05.png`, `assets/bibliothek/karussell/e_rechnung/folie_03.png`, `assets/bibliothek/karussell/examen/folie_01.png`, `…`
- 08:56 ✍️ Latente Steuern Folie 6: Hinweis zu kleinen Kapitalgesellschaften präzisiert ([`e0329b6`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e0329b680ce9146b3c3876400c272a2511656c16))
  - `LAGE.html`, `automatik/lage_notizen.md`, `posts/05_2026-10-08_latente_steuern`, `vorlagen/system/jobs/p05_latente_steuern.json`
- 08:54 ✍️ Prüfzettel latente Steuern: Punkte 4–5 geprüft, Box Folie 6 zur Entscheidung ([`f92e962`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f92e96267a45ac4725e3f0247683590b002cd476))
  - `LAGE.html`, `automatik/lage_notizen.md`, `posts/05_2026-10-08_latente_steuern`
- 08:51 ✍️ Prüfzettel latente Steuern: Punkte 1–3 mit Quellen geprüft ([`ac252f8`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ac252f80ce0dc6a0d87aa1d8b5c975bd4fa4a80a))
  - `LAGE.html`, `automatik/lage_notizen.md`, `posts/05_2026-10-08_latente_steuern`
- 08:47 📈 Statistik 2026-10-05 ([`db0069d`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/db0069da35cb6b2d766db3757f07a80d67c9001c))
  - `automatik/statistik`
- 08:47 🔀 Merge: Bibliothek gegengelesen (10 Korrekturen, Prüfbericht) ([`686ac1b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/686ac1bfb2362e5b9bf0745eb19ff13b6ac1c796))
- 08:39 ✍️ Bibliothek gegengelesen: 10 Korrekturen, 25 Zweifelsfälle im Prüfbericht ([`d3ee26f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/d3ee26f6780915231a438dacbce0b5cddb704709))
  - `LAGE.html`, `assets/bibliothek/PRUEFBERICHT.md`, `assets/bibliothek/einzelposts/zahl_zinsen.png`, `assets/bibliothek/karussell/e_rechnung/folie_03.png`, `assets/bibliothek/karussell/forschungszulage/folie_03.png`, `assets/bibliothek/karussell/gewst_zahlen/folie_04.png`, `…`
- 08:31 ✍️ Lage-Notiz: latente Steuern auf „spätestens jetzt“ umgestellt ([`fde2ac9`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/fde2ac984d3a7f1056f4f3cbec8c577b76ac6f81))
  - `LAGE.html`, `automatik/lage_notizen.md`
- 08:29 🔀 Merge remote-tracking branch 'origin/claude/instagram' into claude/instagram ([`a465237`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a4652376cdd635f24d23f9d1da551b6e32c8da58))
- 08:29 💼 LinkedIn-Paket latente Steuern: „Abschluss 2026“ → „spätestens jetzt“ ([`f3959e2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f3959e2020519cf14d0f0930ddac914db5066b55))
  - `LAGE.html`, `posts/05_2026-10-08_latente_steuern`
- 08:29 ✍️ Lage-Notiz: Puffer 10 Min. am Demo-Link als offener Chrome-Schritt ([`b444ec7`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/b444ec7b5dcc7c5b647219ede693ccc5b9bf8f35))
  - `LAGE.html`, `automatik/lage_notizen.md`
- 08:29 🔀 Merge remote-tracking branch 'origin/claude/instagram' into claude/instagram ([`c364a4e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c364a4eacdad154f62e5d7b8663483c242213f4f))
- 08:28 🔀 Merge branch 'claude/instagram' of https://github.com/maehrsteuern/Instagram-maehrsteuern into claude/instagram ([`85a1dfd`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/85a1dfd6974909865ccd70e2981a3796672f54a3))
- 08:27 ✍️ Wochenbericht: Demo-Zahlen aus Reclaim-Pflichtfeld + Kalender, dm_tracking nicht mehr angezeigt ([`714b0eb`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/714b0eb0b4c9cc35d73cb7f9a5ac3d874d340d3b))
  - `LAGE.html`, `automatik/lage_notizen.md`, `automatik/wochenbericht.py`
- 08:28 🔀 Merge branch 'claude/instagram' of https://github.com/maehrsteuern/Instagram-maehrsteuern into claude/instagram ([`34127cc`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/34127ccd7ac5d0ba8fc5e8a126eef22d65c9de45))
- 08:28 🔀 Merge remote-tracking branch 'origin/claude/instagram' into claude/instagram ([`ee6e233`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ee6e2334b3f6301f88ebcc09a627054c16554281))
- 08:28 🔀 Merge remote-tracking branch 'origin/claude/instagram' into claude/instagram ([`99bf365`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/99bf3657a014fa18a807313182eea9e1e49e5385))
- 08:28 ✍️ Lage-Notiz: GitHub Pages eingeschaltet, Lage-Seite läuft (erledigt) ([`be6765d`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/be6765d918528c33a51ad1a07e4a9caab5ad19ff))
  - `LAGE.html`, `automatik/lage_notizen.md`
- 08:28 ✍️ Latente Steuern: „Abschluss 2026“ → „spätestens jetzt“ ([`f8fda58`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f8fda5850ec94d37c8b92b989248f2e4360936d7))
  - `LAGE.html`, `posts/05_2026-10-08_latente_steuern`, `vorlagen/system/jobs/p05_latente_steuern.json`
- 08:28 ✍️ Wochenbericht: Sonntags-Reels zählen in der Folgewoche als neu; Reel-Vergleich auf „5 Dinge“ vs. Split ([`3cb33fe`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/3cb33fe0780585282727634cb1951bc61d819ce7))
  - `LAGE.html`, `automatik/erinnerungen.json`, `automatik/lage_notizen.md`, `automatik/wochenbericht.py`
- 08:27 🔀 Merge pull request #16 from maehrsteuern/claude/upbeat-goodall-huo6u7 ([`262ed48`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/262ed487ed9b2c5f9a63c5e7d9950047851bda2d))
- 08:27 🔀 Merge claude/instagram in Bibliothek-Branch: Konflikte gelöst ([`0581783`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/058178316c96c700026777ee6023c075a8d81354))
- 08:27 🔀 Merge: Lage-Notizen Kalender-Prüfung – Autopilot-Kalender in Reclaim verbunden, Freigabe/Auslöser noch gegenprüfen ([`0deb532`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/0deb532118e3e94d8151e674981da7063d1b4099))
- 08:26 ✍️ Lage: Duplikat des 5-Dinge-Reels gelöscht ([`c09d6c5`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c09d6c5fa749cc10f86e3b418b0f06e4964b98fe))
  - `LAGE.html`, `automatik/lage_notizen.md`
- 07:03 📡 Radar 2026-10-05: 8 Beiträge, 0 DM-Entwürfe ([`c7af627`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c7af627103cd7673c90dbc18c53d97522c1b2062))
  - `automatik/interaktion`

**So 04.10.2026**
- 21:28 📈 Statistik 2026-10-04 ([`1e9ea9e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1e9ea9ea7c92280cb4d24c0b8a6636c28d6fa5fb))
  - `automatik/statistik`
- 21:04 ✍️ Reel-Regeln: Listen-Reels hoechstens 3 Punkte, unter 20 s (Erkenntnis 5-Dinge-Reel) ([`4878531`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/48785317faa85863a94d49e61e1aab4b027e1cbe))
  - `strategie/09_reel_regeln.md`
- 20:38 📈 Statistik 2026-10-04 ([`1096968`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1096968c6b9b9a9b9156e5f097d3f95312fba9bb))
  - `automatik/statistik`
- 19:48 🤖 Autopilot: vor jedem Posten neuesten Plan holen – verhindert Doppel-Posts ([`5738537`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/5738537125e7e824964b436914029f8446af3573))
  - `LAGE.html`, `automatik/lage_notizen.md`, `automatik/posten.py`
- 19:46 🤖 Autopilot: 01-story-teaser-5dinge veroeffentlicht ([`a850704`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a850704aa2a081fcd149efb9a8f2a15bbd8df45a))
  - Plan: `01-story-teaser-5dinge` status: freigegeben → veroeffentlicht; `01-story-teaser-5dinge` online: https://www.instagram.com/stories/maehrsteuern/4000661016565086455
- 19:46 🤖 Autopilot: Dateien fuer 01-story-teaser-5dinge vorbereitet ([`3b9e1ab`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/3b9e1ab11b4c811de1de4d0d4e98ed69cfa2910c))
  - Plan: neu `00-start-1` (2026-09-30 12:30, veroeffentlicht); neu `00-start-2` (2026-09-30 12:31, veroeffentlicht); neu `00-start-3` (2026-09-30 12:32, veroeffentlicht); neu `00-vorfreude` (2026-09-30 19:30, veroeffentlicht); neu `00-neuvorstellung` (2026-10-01 18:30, veroeffentlicht); neu `00-story-teaser` (2026-10-01 18:35, entfaellt); neu `01-story-frage` (2026-10-02 12:15, veroeffentlicht); neu `08-story-tipp` (2026-10-03 12:15, veroeffentlicht); neu `01-reel-ampel` (2026-10-04 19:30, pause); neu `01-story-teaser` (2026-10-04 19:35, pause); neu `01-reel-5dinge` (2026-10-04 19:30, veroeffentlicht); neu `01-story-teaser-5dinge` (2026-10-04 19:35, freigegeben); neu `02-story-umfrage` (2026-10-05 12:15, freigegeben); neu `02-excel-fehler` (2026-10-06 19:30, freigegeben); neu `02-story-teaser` (2026-10-06 19:35, freigegeben); neu `05-story-frage` (2026-10-07 12:15, freigegeben); neu `06-reel-split` (2026-10-07 19:30, freigegeben); neu `06-story-teaser` (2026-10-07 19:35, freigegeben); neu `05-latente-steuern` (2026-10-08 19:30, freigegeben); neu `05-story-teaser` (2026-10-08 19:35, freigegeben); neu `08-story-heute` (2026-10-09 12:15, freigegeben); neu `08-reel-kst-staffel` (2026-10-09 19:30, freigegeben); neu `08-story-rueckblick` (2026-10-10 12:15, freigegeben); neu `03-story-quiz` (2026-10-12 12:15, freigegeben); neu `03-gewst-hinzurechnung` (2026-10-13 19:30, freigegeben); neu `03-story-teaser` (2026-10-13 19:35, freigegeben); neu `07-reel-hinzurechnung` (2026-10-14 19:30, freigegeben); neu `03-story-aufloesung` (2026-10-16 12:15, freigegeben); neu `04-story-frage` (2026-10-19 12:15, entwurf); neu `04-reel-mein-weg` (2026-10-20 19:30, wartet_auf_sprachnachricht); neu `04-story-teaser` (2026-10-20 19:35, entwurf)
- 00:13 ✍️ LAGE.md vom Ziel-Branch übernommen (wird nach dem Merge automatisch neu erzeugt) ([`5c7f63c`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/5c7f63cd3015f373ddca653ec4c90f4b63605c28))
- 00:13 🔀 Merge claude/instagram in Bibliothek-Branch: Konflikte gelöst ([`978f730`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/978f730edd04156b2f0426f0b2e68001f153f180))

**Sa 03.10.2026**
- 19:52 🔀 Merge: Radar drosselfest, Wochenbericht geprüft, Fristen in Lage + Kalender ([`01b05e7`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/01b05e73e2d2ae3c6aef2f8e5390e6d4ea2defbe))
- 16:35 📡 Radar drosselfest, Wochenbericht geprüft, Fristen in Lage + Kalender ([`2598e31`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/2598e310de3f079372f545e40dbf050c5415fe85))
  - `automatik/erinnerungen.json`, `automatik/kalender.py`, `automatik/kalender_sync.py`, `automatik/lage.py`, `automatik/lage_notizen.md`, `automatik/radar.py`, `…`
- 14:02 📈 Statistik 2026-10-03 ([`4e9a81f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4e9a81f04f6335ce3440326acfdef106dd264738))
  - `automatik/statistik`
- 12:25 📡 Radar 2026-10-03: 8 Beiträge, 0 DM-Entwürfe, Konten −0/+10 (abgehakt) ([`d9cc42b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/d9cc42b16e0f8541602b616f118d6075f54a3430))
  - `automatik/interaktion.json`, `automatik/interaktion`
- 12:15 🤖 Autopilot: 08-story-tipp veroeffentlicht ([`e36ea97`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e36ea9729d02b9bcd9389c289c388ee439254b91))
  - Plan: `08-story-tipp` status: freigegeben → veroeffentlicht; `08-story-tipp` online: https://www.instagram.com/stories/maehrsteuern/3999709094836161880
- 12:01 ✍️ Kalender-Sync optimiert + Automatik gehärtet (#23) ([`c918b6b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c918b6b08d85b6e622d80fee6e6125368bdb0ba1))
- 11:18 🔀 Merge: Neuvorstellung angepinnt, Mein Weg umkonzipieren ([`a53f609`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a53f6092c90496057f06f91c320ef6a2118c9b4d))
- 11:18 ✍️ Neuvorstellung angepinnt (erledigt), Reel „Mein Weg“: Konzept baut Loris um – keine Sprachnachricht anfordern ([`c4e6cbc`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c4e6cbc75b479ad12d03f38c4afbbb5e35327d41))
  - `automatik/lage.py`, `automatik/lage_notizen.md`, `automatik/plan.json`
- 11:00 🤖 Autopilot: Dateien fuer 08-story-tipp vorbereitet ([`568830e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/568830e81361f28c724dd67e42f296ad2615006a))
  - `posts/08_2026-10-09_reel_kst_staffel`
- 10:59 🔀 Merge claude/instagram (LAGE.md vom Ziel-Branch übernommen) ([`cec8375`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/cec837549e12513f9d9faa1a0c53032f068c0896))
- 10:58 ✍️ Lage-Notizen: Autopilot-Kalender in Reclaim noch nicht verbunden, Freigabe/Auslöser gegenprüfen ([`072d0e8`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/072d0e80655779c70ac91964e7ce2c09ec1f3949))
  - `automatik/lage_notizen.md`
- 10:58 ✍️ Latente Steuern: Bildunterschrift „Spätestens im Abschluss 2026“ ([`517eed6`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/517eed626f47d00007d4a1c63450ed845d5c2dda))
  - `automatik/lage_notizen.md`, `posts/05_2026-10-08_latente_steuern`
- 10:55 🔀 Merge claude/instagram ([`f4b8248`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f4b82489c0731ed02aebcf2960f65a244732385f))
- 10:55 ✍️ Automatik gehärtet: kein Doppel-Post, kein Schlüssel im Repo, keine verlorenen Antworten ([`b90716b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/b90716bb466a8a9e959e81d505c6e17df9ad7b83))
  - `.github/workflows`, `automatik/fb_schluessel_verlaengern.py`, `automatik/freigabe.py`, `automatik/kommentare.py`, `automatik/lage_notizen.md`, `automatik/linkedin.py`, `…`
- 10:47 ✍️ Kalender-Sync optimiert: nur Postzeiten blocken Reclaim, Farben + Pop-ups je Art ([`0ed7b42`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/0ed7b42725646e2f4bf95e63dd5f29f15e9d8128))
  - Plan: neu `00-start-1` (2026-09-30 12:30, veroeffentlicht); neu `00-start-2` (2026-09-30 12:31, veroeffentlicht); neu `00-start-3` (2026-09-30 12:32, veroeffentlicht); neu `00-vorfreude` (2026-09-30 19:30, veroeffentlicht); neu `00-neuvorstellung` (2026-10-01 18:30, veroeffentlicht); neu `00-story-teaser` (2026-10-01 18:35, entfaellt); neu `01-story-frage` (2026-10-02 12:15, veroeffentlicht); neu `08-story-tipp` (2026-10-03 12:15, freigegeben); neu `01-reel-ampel` (2026-10-04 19:30, freigegeben); neu `01-story-teaser` (2026-10-04 19:35, freigegeben); neu `02-story-umfrage` (2026-10-05 12:15, freigegeben); neu `02-excel-fehler` (2026-10-06 19:30, freigegeben); neu `02-story-teaser` (2026-10-06 19:35, freigegeben); neu `05-story-frage` (2026-10-07 12:15, freigegeben); neu `06-reel-split` (2026-10-07 19:30, freigegeben); neu `06-story-teaser` (2026-10-07 19:35, freigegeben); neu `05-latente-steuern` (2026-10-08 19:30, freigegeben); neu `05-story-teaser` (2026-10-08 19:35, freigegeben); neu `08-story-heute` (2026-10-09 12:15, freigegeben); neu `08-reel-kst-staffel` (2026-10-09 19:30, freigegeben); neu `08-story-rueckblick` (2026-10-10 12:15, freigegeben); neu `03-story-quiz` (2026-10-12 12:15, freigegeben); neu `03-gewst-hinzurechnung` (2026-10-13 19:30, freigegeben); neu `03-story-teaser` (2026-10-13 19:35, freigegeben); neu `07-reel-hinzurechnung` (2026-10-14 19:30, freigegeben); neu `03-story-aufloesung` (2026-10-16 12:15, freigegeben); neu `04-story-frage` (2026-10-19 12:15, entwurf); neu `04-reel-mein-weg` (2026-10-20 19:30, wartet_auf_sprachnachricht); neu `04-story-teaser` (2026-10-20 19:35, entwurf)
- 10:44 ✍️ Content-Fabrik: Lernpunkte aus dem Wettbewerbs-Check in die Hook-Regeln ([`639b98d`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/639b98dbb2ca0cba0b13f2f590e63e5e6f6d4424))
  - `automatik/lage_notizen.md`, `strategie/08_hooks.md`, `strategie/wettbewerb.md`
- 10:35 📡 Radar: Art neuer Konten aus der Vorschlagszeile übernehmen ([`e76ef09`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e76ef095f26b45caeeec04de1ed23659919c17d2))
  - `automatik/radar.py`
- 10:32 ✍️ Wettbewerbs-Check Oktober 2026 ([`fb00717`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/fb007179e4cbbc084bed1e937fc0b81b877835ed))
  - `strategie/wettbewerb.md`
- 10:00 ✍️ Chrome-Module: Gesamtprompt im Repo + LinkedIn-Erinnerungen im Kalender ([`4eccdd2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4eccdd2bec52c33150e9a7bfdceb5f5db7fa4660))
  - `README.md`, `automatik/kalender.py`, `automatik/lage_notizen.md`, `strategie/14_chrome_module.md`
- 09:58 🔀 Merge branch 'claude/instagram' of https://github.com/maehrsteuern/Instagram-maehrsteuern into claude/instagram ([`7e9ecfe`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/7e9ecfebcc3690be006282adb22a8b468546884e))
- 09:58 ✍️ Reel-Entwurf „Mein Weg rückwärts“ zum Review und Prüfzettel latente Steuern ([`ab5fc1f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ab5fc1f8fdd6db7b591e13a8e384c84a61bb1139))
  - `posts/04_2026-10-20_reel_mein_weg`, `posts/05_2026-10-08_latente_steuern`, `vorlagen/system/schnitt/p04_reel_markenweg_entwurf.json`
- 09:52 ✍️ Tagesbericht als Bild: Kennzahlen, Reichweite pro Tag, Beitraege mit Vortagsvergleich und Methoden-Check ([`ad5c8ad`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ad5c8ad64e3d0c9902b294a4dbe229ef86a858c2))
  - `automatik/berichte`, `automatik/tagesbericht.py`
- 09:51 📡 Radar: Häkchen auch in eigenen Kommentaren im Radar-Issue zählen ([`72d79a5`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/72d79a53ba0cec60f21f1c2491f1eca24c2d22c5))
  - `automatik/radar.py`
- 08:59 ✍️ Auswertung: eigene Frage-Story schlaegt geteilte Story, Karussell waechst ueber 2 Tage ([`f9d3771`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f9d37710e292a1875e55d1d3b1c104ef8db8276d))
  - `strategie/06_auswertung.md`
- 08:37 🔀 Merge remote-tracking branch 'origin/claude/instagram' into ccr-9d4fa6dd-1kqi9l ([`09d9a7f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/09d9a7f09ee103b9151cea0c4b72ec7d7027113e))
- 08:37 ✍️ Reel „Mein Weg“: Variante B über den Autopiloten, KI-Hinweis in der Bildunterschrift ([`7eca616`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/7eca6167f7e62a3493798598751f7d944ef20585))
  - `automatik/lage_notizen.md`, `automatik/plan.json`, `posts/04_2026-10-20_reel_mein_weg`
- 08:34 ✍️ Zwischenstand: Reel „Mein Weg“ auf Variante B (Markenweg) umgestellt ([`36f5416`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/36f54165c1e7c0e94aca36a544501e686645dad7))
  - Plan: neu `00-start-1` (2026-09-30 12:30, veroeffentlicht); neu `00-start-2` (2026-09-30 12:31, veroeffentlicht); neu `00-start-3` (2026-09-30 12:32, veroeffentlicht); neu `00-vorfreude` (2026-09-30 19:30, veroeffentlicht); neu `00-neuvorstellung` (2026-10-01 18:30, veroeffentlicht); neu `00-story-teaser` (2026-10-01 18:35, entfaellt); neu `01-story-frage` (2026-10-02 12:15, veroeffentlicht); neu `08-story-tipp` (2026-10-03 12:15, freigegeben); neu `01-reel-ampel` (2026-10-04 19:30, freigegeben); neu `01-story-teaser` (2026-10-04 19:35, freigegeben); neu `02-story-umfrage` (2026-10-05 12:15, freigegeben); neu `02-excel-fehler` (2026-10-06 19:30, freigegeben); neu `02-story-teaser` (2026-10-06 19:35, freigegeben); neu `05-story-frage` (2026-10-07 12:15, freigegeben); neu `06-reel-split` (2026-10-07 19:30, freigegeben); neu `06-story-teaser` (2026-10-07 19:35, freigegeben); neu `05-latente-steuern` (2026-10-08 19:30, freigegeben); neu `05-story-teaser` (2026-10-08 19:35, freigegeben); neu `08-story-heute` (2026-10-09 12:15, freigegeben); neu `08-reel-kst-staffel` (2026-10-09 19:30, freigegeben); neu `08-story-rueckblick` (2026-10-10 12:15, freigegeben); neu `03-story-quiz` (2026-10-12 12:15, freigegeben); neu `03-gewst-hinzurechnung` (2026-10-13 19:30, freigegeben); neu `03-story-teaser` (2026-10-13 19:35, freigegeben); neu `07-reel-hinzurechnung` (2026-10-14 19:30, freigegeben); neu `03-story-aufloesung` (2026-10-16 12:15, freigegeben); neu `04-story-frage` (2026-10-19 12:15, entwurf); neu `04-reel-mein-weg` (2026-10-20 19:30, wartet_auf_sprachnachricht); neu `04-story-teaser` (2026-10-20 19:35, entwurf)
- 08:32 ✍️ Demo-Kopie: Echttest bestanden, Doku nachgezogen ([`cc33a15`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/cc33a15b97d6a74a8e99ba1aabddd15415b8a537))
  - Plan: neu `00-start-1` (2026-09-30 12:30, veroeffentlicht); neu `00-start-2` (2026-09-30 12:31, veroeffentlicht); neu `00-start-3` (2026-09-30 12:32, veroeffentlicht); neu `00-vorfreude` (2026-09-30 19:30, veroeffentlicht); neu `00-neuvorstellung` (2026-10-01 18:30, veroeffentlicht); neu `00-story-teaser` (2026-10-01 18:35, entfaellt); neu `01-story-frage` (2026-10-02 12:15, veroeffentlicht); neu `08-story-tipp` (2026-10-03 12:15, freigegeben); neu `01-reel-ampel` (2026-10-04 19:30, freigegeben); neu `01-story-teaser` (2026-10-04 19:35, freigegeben); neu `02-story-umfrage` (2026-10-05 12:15, freigegeben); neu `02-excel-fehler` (2026-10-06 19:30, freigegeben); neu `02-story-teaser` (2026-10-06 19:35, freigegeben); neu `05-story-frage` (2026-10-07 12:15, freigegeben); neu `06-reel-split` (2026-10-07 19:30, freigegeben); neu `06-story-teaser` (2026-10-07 19:35, freigegeben); neu `05-latente-steuern` (2026-10-08 19:30, freigegeben); neu `05-story-teaser` (2026-10-08 19:35, freigegeben); neu `08-story-heute` (2026-10-09 12:15, freigegeben); neu `08-reel-kst-staffel` (2026-10-09 19:30, freigegeben); neu `08-story-rueckblick` (2026-10-10 12:15, freigegeben); neu `03-story-quiz` (2026-10-12 12:15, freigegeben); neu `03-gewst-hinzurechnung` (2026-10-13 19:30, freigegeben); neu `03-story-teaser` (2026-10-13 19:35, freigegeben); neu `07-reel-hinzurechnung` (2026-10-14 19:30, freigegeben); neu `03-story-aufloesung` (2026-10-16 12:15, freigegeben); neu `04-story-frage` (2026-10-19 12:15, entwurf); neu `04-reel-mein-weg` (2026-10-20 19:30, wartet_auf_clips); neu `04-story-teaser` (2026-10-20 19:35, entwurf)

**Fr 02.10.2026**
- 17:40 ✍️ Lage: Neuvorstellung angepinnt (erledigt), ManyChat läuft ([`433d9dd`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/433d9ddfa08f42fc6450fc6ac72b4538d5d8fbc0))
  - `automatik/lage_notizen.md`, `automatik/plan.json`
- 16:36 🔀 Merge remote-tracking branch 'origin/claude/instagram' into claude/upbeat-goodall-huo6u7 ([`9f1937f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/9f1937f8cacd4c46086ac72ebc469ad709bc8d3b))
- 16:31 ✍️ Bibliothek aus dem Brand Kit (Claude Design): 365 fertige Assets ([`1f6ffc4`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1f6ffc4940575300f26391be0fb53ec83b501a21))
  - `README.md`, `assets/bibliothek/README.md`, `assets/bibliothek/bausteine/abspann_copy_paste.png`, `assets/bibliothek/bausteine/abspann_mehr_abschluss.png`, `assets/bibliothek/bausteine/abspann_pruefpfad.png`, `assets/bibliothek/bausteine/abspann_quote.png`, `…`
- 16:12 ✍️ Auswertung: aktive Zeiten der ganzen Woche (auf deutsche Zeit umgerechnet) – 19:30 passt, Sonntag stärkster Abend ([`a2f31a3`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a2f31a30f1fd371ecc9e4895d59dac6e254bc376))
  - `strategie/06_auswertung.md`
- 15:11 📈 Statistik 2026-10-02 ([`c3f893b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c3f893b5c2d3bb9f56c0b7b3646ae9679ac7990b))
  - `automatik/statistik`
- 13:18 ✍️ Lage-Notizen: Interaktion gemergt, offen sind Secrets und Kontenliste ([`a54983d`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a54983d43696c5264401b31bfd0d104f40971bbb))
  - `automatik/lage_notizen.md`
- 13:18 🔀 Merge: Zweite Säule Interaktion (Radar, Kommentar-Hilfe, LinkedIn-Pakete) ([`47638f3`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/47638f3a174a1652349a3026025805e6a6024553))
- 13:14 ✍️ Zweite Säule Interaktion: Radar, Kommentar-Hilfe, LinkedIn-Pakete ([`cbe6029`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/cbe6029322456f13146cef5c89d2ece58c5b28fb))
  - `.github/workflows`, `EINRICHTUNG.md`, `README.md`, `automatik/fb_schluessel_verlaengern.py`, `automatik/interaktion.json`, `automatik/ki.py`, `…`
- 08:47 📈 Statistik 2026-10-02 ([`60c4aa6`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/60c4aa67f643e11d4d6ef46ef453c4a2c18202b3))
  - `automatik/statistik`
