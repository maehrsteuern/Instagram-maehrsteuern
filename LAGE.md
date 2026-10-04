# 🧭 Lage – maehrsteuern auf Instagram

_Automatisch erzeugt von `automatik/lage.py` – nicht von Hand bearbeiten (Notizen: `automatik/lage_notizen.md`). Stand: letzte Änderung So 04.10. 14:52 Uhr._

**Als Nächstes online:** 🎬 Reel `01-reel-ampel` am **So 04.10. 19:30 Uhr** – 🟢 freigegeben (geht automatisch online)

## 📝 Gerade in Arbeit

- Neustart läuft: Start-Storys + Vorfreude (30.09.) und Neuvorstellung (Do 01.10. 18:30, von Hand) sind online. Nach 2 h: 26 erreicht, 6× geteilt, 0 neue Follower. Angepinnt ✓ (03.10.). Offen von Hand: Highlight „Start 👋“.
- Wochenrhythmus ab Okt. steht im Prompt der Content-Fabrik (Mo + Do 08:47, max. 4 Beiträge pro Lauf): Di/Do Karussell + Teaser, Mi Begleit-Reel, Fr Wissens-Reel oder Stimm-Reel, So Reel + Teaser, täglich 12:15 Story.
- Content-Fabrik nutzt ab Mo 05.10. die Lernpunkte aus `strategie/wettbewerb.md` (über Abschnitt in `08_hooks.md`): pro Lauf ≥ 1 Hook „konkreter Fall“ oder „Prüfer/Finanzamt“, Lernpunkt im Freigabe-Issue vermerkt. Routine-Prompt selbst unverändert (nur aus ihrer eigenen Sitzung änderbar).
- Bis 10.10. alles freigegeben: Reel Ampel mit Stimme (So 04.10.), Excel-Fehler (Di 06.10.), Split-Reel als Begleit-Reel (Mi 07.10., vorgezogen), latente Steuern (Do 08.10.), Wissens-Reel KSt-Staffel (Fr 09.10.). So 11.10. ist frei → Fabrik am Mo 05.10.
- Latente Steuern bitte fachlich gegenlesen (`pruefzettel.md` im Post-Ordner; Bildunterschrift schon auf „Spätestens im Abschluss 2026“ angepasst). Änderungen bis Mi 07.10. abends.
- Sprachnachricht zu „Fr 09.10.“ aus `posts/sprechtexte.md` bis Do 08.10. → ersetzt dann das Wissens-Reel durch das Stimm-Reel.
- Reel „Mein Weg“ (20.10.): **Loris baut die Konzeption selbst um (03.10.)** – bis dahin gilt Variante B (`drehbuch_markenweg.md`) nicht als gesetzt, keine Sprachnachricht anfordern, nichts schneiden. Status bleibt `wartet_auf_sprachnachricht`, bis das neue Konzept da ist. **KI-Hinweis** (falls KI-Karten bleiben): Hinweis in der Bildunterschrift, Label nach dem Posten in der App prüfen.
- DM-Strecke läuft über **ManyChat** (Kommentar/Story-Antwort/DM mit Tool/TOOL/tool/tol → DM mit Demo-Link, Follow-up nach 23 h). Stichwörter nur in `automatik/interaktion.json` pflegen – Abweichungen meldet LAGE.md. Die eigenen Skripte schicken nie DMs.
- Interaktion läuft (Radar 50 Konten, Kommentar-Hilfe, LinkedIn-Pakete). **Sprint 1 (03.10.):** Wächter-Issue, Stichwort-Abgleich, Radar-Pflege montags, Erste-Stunde-Checkliste. **Kalender-Sync live (03.10.):** Termine gehen direkt in den Google-Kalender „maehrsteuern Autopilot“ (nur Postzeiten „beschäftigt“ für Reclaim, To-dos/LinkedIn „frei“; Farben + Pop-ups je Art). `kalender.ics` entfällt. **Wochenbericht** ab So 04.10. ca. 18:00 als Issue – Demos/ManyChat per Kommentar nachtragen. Demo-Buchungen + Herkunft: Apps-Script „maehrsteuern Demo-Kopie“ kopiert sie stündlich nach „maehrsteuern Autopilot“ – eingerichtet und per Echttest bestätigt (03.10.). Reclaim: Pflichtfeld „Woher kennst du mich?“, Titel „Demo + Erstgespräch – Name“, nur noch dieser eine Link. ManyChat-Zahlen bleiben von Hand (API nur Pro) – siehe `strategie/13_backlog.md`.
- **Automatik gehärtet (03.10., mit #23 in `claude/instagram`):** kein Doppel-Post bei Push-Konflikt, „stop“ greift auch während des Wartens, kein Schlüssel in Fehlermeldungen, keine verlorenen „go“-Antworten, Schlüssel-Verlängerung mit Reserve-Takt – Details `strategie/13_backlog.md`.
- Externer Takt fürs Posten läuft (cron-job.org, alle 15 Min.). Schlüssel `cron-posten` läuft am **29.09.2027** ab → vorher erneuern.
- Tax-Calc-Repo: PR #2 (Delta-Plakette beim Tippen) und PR #3 (Reel-Datensatz `?demo=reel`) warten auf Review.
- **Chrome-Claude-Module** (`strategie/14_chrome_module.md`): Erinnerungen im Kalender „maehrsteuern Autopilot“ – So 04.10. 11:00 einmalig A·2·3, jeden So 18:45 Modul 1 (ManyChat → Wochenbericht), 1. Mo im Monat 18:00 Module 4+6, LinkedIn-Upload (Modul 5) automatisch je Karussell am Werktag danach 08:00.
- **So 04.10. erster Wochenbericht (ca. 18:00):** prüfen, ob ManyChat-Kommentar (Chrome Modul 1, 18:45), Demo-Kopien und Herkunft richtig im Issue landen. Probelauf mit Testdaten am 03.10. ok. Dabei behoben: Kalender ohne unzuverlässige Volltextsuche (alle Seiten), leere Herkunft rutscht nicht mehr in die nächste Zeile, Nachträge zählen nur am Zeilenanfang/nach Komma (zitierte Zeilen und „Gesamtstand ManyChat …“ zählen nicht).
- **Radar-Nachträge (03.10.):** Meta-Drosselung (429/Code 4, 17, 32, 613) → Backoff 30/90/270 s, bei anhaltender Drosselung wird abgebrochen. Gedrosselte oder kurz gestörte Konten landen nicht mehr als 🧹 „nicht abrufbar“ in der Pflege; aufgeräumt werden nur dauerhaft kaputte Konten oder Konten ohne Beitrag seit 30 Tagen (montags, nur abgehakt). Art neuer Konten wird auch aus Wörtern wie „Steuerberaterin“, „Prüfung“, „Akademie“ erkannt; fehlende oder unbekannte Art erscheint als Hinweis im Radar-Issue.
- **Fristen** (`automatik/erinnerungen.json` → „Braucht dich“ + Kalender): LinkedIn #18 Mi 07.10. 08:00 (Termin kommt schon automatisch) · Reel-Vergleich Ampel/Split → Anzeigen-Start ca. Mo 12.10. (Chrome Modul 2 am 04.10. nur vorbereiten) · **ManyChat-Trial endet Fr 16.10.** → Entscheidung Loris (Erinnerung Mi 14.10.).
- **Meta-App „maehrsteuern Autopilot“** bleibt im Entwicklungsmodus. Die laufenden IG-Schlüssel und die Statistik sind davon nicht betroffen (eigenes Konto mit App-Rolle). Nur die Hashtag-Suche braucht die Freigabe → Checkliste [#26](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/26).
- **Reclaim-Hinweis:** Claudes Reclaim-Zugang (Connector) zeigt auf **Konto B (Outlook, Lite)**, nicht auf das Demo-Konto. Für die Automatik nicht nutzen; Demo-Buchungen kommen nur über das Apps-Script „maehrsteuern Demo-Kopie“.
- **Lage als Seite (04.10.):** `LAGE.html` mit Kacheln, Kalender, Diagrammen und filterbarem Protokoll, wird mit LAGE.md neu geschrieben und über GitHub Pages veröffentlicht (https://maehrsteuern.github.io/Instagram-maehrsteuern/). Einmalig von Hand: Settings → Pages → Source „GitHub Actions“.

## 👉 Braucht dich

- 🟡 **Freigeben** `04-story-frage` (Mo 19.10. 12:15) – „go“ oder „stop“ im Issue (Issue kommt, sobald `04-reel-mein-weg` fertig ist)
- ⏳ **Wartet auf sprachnachricht** `04-reel-mein-weg` (Di 20.10. 19:30) – Konzept wird von Loris umgebaut (03.10.) – Variante B (drehbuch_markenweg.md) vorerst nicht gesetzt, keine Sprachnachricht anfordern; bei KI-Karten: Hinweis in der Bildunterschrift, KI-Label nach dem Posten in der App prüfen
- 🎵 **Musik fehlt** `04-reel-mein-weg` (Di 20.10. 19:30)
- 🟡 **Freigeben** `04-story-teaser` (Di 20.10. 19:35) – „go“ oder „stop“ im Issue (Issue kommt, sobald `04-reel-mein-weg` fertig ist)

## ⏭️ Nächste 7 Tage

| Wann | Was | Status | Hinweis |
|---|---|---|---|
| So 04.10. 19:30 | 🎬 Reel `01-reel-ampel` | 🟢 freigegeben (geht automatisch online) | Loris erzählt (Sprachnachricht): 2 Tage vor Frist, #BEZUG!/#NAME?/#WERT! → Lösung mit Code, echte Programm-Aufnahme; Untertitel wörtlich, Musik ganz leise, CTA TOOL per DM, 26 s · [Freigabe #7](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/7) |
| So 04.10. 19:35 | 📱 Story `01-story-teaser` | 🟢 freigegeben (geht automatisch online) |  |
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

## 🗓️ Danach

| Wann | Was | Status | Hinweis |
|---|---|---|---|
| Mo 12.10. 12:15 | 📱 Story `03-story-quiz` | 🟢 freigegeben (geht automatisch online) |  |
| Di 13.10. 19:30 | 🖼️ Karussell `03-gewst-hinzurechnung` | 🟢 freigegeben (geht automatisch online) |  |
| Di 13.10. 19:35 | 📱 Story `03-story-teaser` | 🟢 freigegeben (geht automatisch online) |  |
| Mi 14.10. 19:30 | 🎬 Reel `07-reel-hinzurechnung` | 🟢 freigegeben (geht automatisch online) | Begleit-Reel zum Karussell vom 13.10. (12,8 s, echte Programm-Aufnahme, ohne Stimme) – neuer Mittwochs-Reel-Slot · [Freigabe #14](https://github.com/maehrsteuern/Instagram-maehrsteuern/issues/14) |
| Fr 16.10. 12:15 | 📱 Story `03-story-aufloesung` | 🟢 freigegeben (geht automatisch online) |  |
| Mo 19.10. 12:15 | 📱 Story `04-story-frage` | 🟡 Entwurf (wartet auf Freigabe) |  |
| Di 20.10. 19:30 | 🎬 Reel `04-reel-mein-weg` | ⏳ wartet auf sprachnachricht | Konzept wird von Loris umgebaut (03.10.) – Variante B (drehbuch_markenweg.md) vorerst nicht gesetzt, keine Sprachnachricht anfordern; bei KI-Karten: Hinweis in der Bildunterschrift, KI-Label nach dem Posten in der App prüfen |
| Di 20.10. 19:35 | 📱 Story `04-story-teaser` | 🟡 Entwurf (wartet auf Freigabe) |  |

## ✅ Zuletzt veröffentlicht (Autopilot)

- Sa 03.10. 12:15 · 📱 Story `08-story-tipp` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3999709094836161880) (online 2026-10-03 12:15)
- Fr 02.10. 12:15 · 📱 Story `01-story-frage` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3998984318181825905) (online 2026-10-02 12:15)
- Do 01.10. 18:30 · 🖼️ Karussell `00-neuvorstellung` · [ansehen](https://www.instagram.com/p/Dd9V5HAAhcL/) (online 2026-10-01 18:30)
- Mi 30.09. 19:30 · 📱 Story `00-vorfreude` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3997727075650058524) (online 2026-09-30 18:37)
- Mi 30.09. 12:32 · 📱 Story `00-start-3` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3997545080966344429) (online 2026-09-30 12:35)
- Mi 30.09. 12:31 · 📱 Story `00-start-2` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3997544897742372327) (online 2026-09-30 12:35)
- Mi 30.09. 12:30 · 📱 Story `00-start-1` · [ansehen](https://www.instagram.com/stories/maehrsteuern/3997544707312529712) (online 2026-09-30 12:35)

## 📈 Zahlen (täglich ca. 08:45)

**351 Follower** · 2 Beiträge im Profil (Abruf 2026-10-04) · **+0** seit 2026-10-03
Reichweite pro Tag: 01.10. **68** · 02.10. **79** · 03.10. **63** · 04.10. **9**

| Beitrag (letzte 14 Tage) | Aufrufe | Erreicht | Likes | Komm. | Gespeichert | Geteilt |
|---|---|---|---|---|---|---|
| Do 01.10. 18:30 [Neu hier? Dann kurz zu mir 👋](https://www.instagram.com/p/Dd9V5HAAhcL/) | 297 (+17) | 106 | 7 | 2 | 2 | 16 |
| Di 29.09. 15:42 [Steuern × Code. ⚡](https://www.instagram.com/reel/Dd34F9RtucT/) | 278 (+7) | 165 | 6 | 2 | 2 | 7 |

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
| Wochenbericht | sonntags ca. 18:00 (ein Issue) | – |
| Musik holen | nur von Hand | ✅ ok |

## 📜 Protokoll – jede Änderung

🤖 Autopilot · ✅ Freigabe · 📈 Statistik · 🎵 Musik · 🔀 Merge · ✍️ von Hand / Claude

**So 04.10.2026**
- 14:52 📈 Statistik 2026-10-04 ([`e5a407c`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e5a407c19b52d51642910375205b1c48b17183e1))
  - `automatik/statistik`
- 13:07 📡 Radar 2026-10-04: 8 Beiträge, 0 DM-Entwürfe ([`996fe74`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/996fe74d4dbf888d86c5d28492b53f48b2ec0864))
  - `automatik/interaktion`
- 08:59 ✍️ Tagesbericht 04.10.; Vortagsvergleich jetzt Morgen gegen Morgen (Schnappschuss je Bericht) ([`4d41c01`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4d41c016723ad265a0331f9ab1350a2f5acbda92))
  - `automatik/berichte`, `automatik/tagesbericht.py`
- 08:47 📈 Statistik 2026-10-04 ([`91fa33b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/91fa33b5962d62e23d7996789d41c1b65de38ed2))
  - `automatik/statistik`
- 07:02 📡 Radar 2026-10-04: 8 Beiträge, 0 DM-Entwürfe ([`9ee31d0`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/9ee31d0805fd2abb5e1444972821876d9f5f3dd8))
  - `automatik/interaktion`
- 01:03 ✍️ Lage-Seite: Veröffentlichung darf scheitern, ohne die Lage rot zu färben ([`015c30e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/015c30e3dbcf0bef7616834ed5c397900c529435))
  - `.github/workflows`
- 01:03 ✍️ Lage als Seite: LAGE.html mit Kacheln, Kalender, Diagrammen und Protokoll, Veröffentlichung über GitHub Pages ([`110b299`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/110b29958834522e6296662811988d45acc5aa14))
  - `.claude/skills/lage/SKILL.md`, `.github/workflows`, `CLAUDE.md`, `LAGE.html`, `README.md`, `automatik/lage.py`, `…`

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
- 10:58 ✍️ Latente Steuern: Bildunterschrift „Spätestens im Abschluss 2026“ ([`517eed6`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/517eed626f47d00007d4a1c63450ed845d5c2dda))
  - `automatik/lage_notizen.md`, `posts/05_2026-10-08_latente_steuern`
- 10:55 🔀 Merge claude/instagram ([`f4b8248`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f4b82489c0731ed02aebcf2960f65a244732385f))
- 10:55 ✍️ Automatik gehärtet: kein Doppel-Post, kein Schlüssel im Repo, keine verlorenen Antworten ([`b90716b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/b90716bb466a8a9e959e81d505c6e17df9ad7b83))
  - `.github/workflows`, `automatik/fb_schluessel_verlaengern.py`, `automatik/freigabe.py`, `automatik/kommentare.py`, `automatik/lage_notizen.md`, `automatik/linkedin.py`, `…`
- 10:47 ✍️ Kalender-Sync optimiert: nur Postzeiten blocken Reclaim, Farben + Pop-ups je Art ([`0ed7b42`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/0ed7b42725646e2f4bf95e63dd5f29f15e9d8128))
  - `.github/workflows`, `EINRICHTUNG.md`, `README.md`, `automatik/kalender.py`, `automatik/kalender_sync.py`, `automatik/lage_notizen.md`, `…`
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
  - Plan: `04-reel-mein-weg` status: wartet_auf_clips → wartet_auf_sprachnachricht
- 08:32 ✍️ Demo-Kopie: Echttest bestanden, Doku nachgezogen ([`cc33a15`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/cc33a15b97d6a74a8e99ba1aabddd15415b8a537))
  - `automatik/lage_notizen.md`, `strategie/13_backlog.md`
- 08:24 ✍️ Marken-Assets und Drehbuch-Variante B für Reel „Mein Weg“ ([`104945c`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/104945c07cee0c65eb3a533c23dff933dc699350))
  - `README.md`, `assets/marke/karte_1_aktuell_9x16.png`, `assets/marke/karte_2_ki_portrait_9x16.png`, `assets/marke/karte_3_ki_avatar_2025_9x16.png`, `assets/marke/loris_aktuell_freisteller.png`, `assets/marke/loris_ki_avatar_2025.jpg`, `…`
- 08:00 ✍️ Demo-Kopie: Herkunft robuster erkennen ([`40f0db5`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/40f0db5b44fba06a7906b2f7624a4443c9d48d94))
  - `automatik/apps_script`
- 07:52 ✍️ Demo-Buchungen: Apps-Script kopiert sie anonymisiert in den Autopilot-Kalender ([`eb930d7`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/eb930d7d8a6bfb81c9d69653fd01373ce2cfccea))
  - `EINRICHTUNG.md`, `README.md`, `automatik/apps_script`, `automatik/lage_notizen.md`, `automatik/wochenbericht.py`, `strategie/13_backlog.md`
- 07:20 ✍️ Wochenbericht: Demo-Buchungen und Herkunft automatisch aus dem Autopilot-Kalender ([`65d201b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/65d201b9befc3f700f2d9c5b9d5508b5e0f3dd17))
  - `.github/workflows`, `automatik/lage_notizen.md`, `automatik/wochenbericht.py`, `strategie/13_backlog.md`
- 07:05 ✍️ Wochenbericht sonntags + kalender.ics entfernt ([`c91f227`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c91f2275870664f901ed455c62e3a9a6de699df2))
  - `.github/workflows`, `EINRICHTUNG.md`, `README.md`, `automatik/kalender.py`, `automatik/kalender_sync.py`, `automatik/lage.py`, `…`
- 07:02 📡 Radar 2026-10-03: 8 Beiträge, 0 DM-Entwürfe ([`a9e2318`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a9e23183c84d6febc68ee8e5269b4f0f61f183f8))
  - `automatik/interaktion`
- 07:01 ✍️ Kalender-Sync: Plan-Termine direkt in den Google-Kalender „maehrsteuern Autopilot“ ([`b471b14`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/b471b147904d2f8b5c3b2a9fd65a6330ff54d788))
  - `.github/workflows`, `EINRICHTUNG.md`, `README.md`, `automatik/kalender.py`, `automatik/kalender_sync.py`, `automatik/lage.py`, `…`
- 06:42 🔑 Schlüssel: Ablaufdaten aktualisiert ([`e739f8b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e739f8ba33ac734584bedc573df49d77e48e7a95))
  - `automatik/schluessel_ablauf.json`
- 06:41 ✍️ Sprint 1: Wächter, Stichwort-Abgleich, Radar-Pflege, Erste-Stunde-Checkliste ([`76f93ad`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/76f93adf3889d22af2feb576cca9c6ef36037ec8))
  - `.github/workflows`, `README.md`, `automatik/ablauf.py`, `automatik/fb_schluessel_verlaengern.py`, `automatik/lage.py`, `automatik/lage_notizen.md`, `…`
- 06:35 📈 Statistik 2026-10-03 ([`c02d4c7`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c02d4c7c62bf7bdb390785debd9726ef23a832fe))
  - `automatik/statistik`
- 06:33 ✍️ Abläufe: Actions auf Node 24 (checkout@v7, setup-python@v7), Runner fest auf ubuntu-24.04 ([`c31d663`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c31d663ae51d08bb5c2ec6ac6332a84bce42b15f))
  - `.github/workflows`
- 00:41 📡 Radar: TaxTech-Konten ergänzt, ManyChat-Stichwörter angeglichen ([`399ed14`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/399ed142cfa2d8e65c476fae102f690bada38347))
  - `automatik/interaktion.json`
- 00:29 📡 Radar: Excel/DATEV-Konten ergänzt ([`c824346`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c824346653277cd05bbe1e04ac265fe73417cfd1))
  - `automatik/interaktion.json`

**Fr 02.10.2026**
- 21:05 💼 LinkedIn-Pakete: 02-excel-fehler, 05-latente-steuern, 03-gewst-hinzurechnung ([`5214c46`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/5214c460db8ac7cc9206d8649a67b97413765715))
  - `posts/02_2026-10-06_excel_fehler`, `posts/03_2026-10-13_gewst_hinzurechnung`, `posts/05_2026-10-08_latente_steuern`
- 21:04 📡 Radar 2026-10-02: 8 Beiträge, 0 DM-Entwürfe ([`8955b76`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/8955b76d24593880e98cf6b3035a561c81c4a749))
  - `automatik/interaktion`
- 20:55 📡 Radar: Konten eingetragen ([`0e7b547`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/0e7b5474da4cf4a29873d372c46e6adc6e14859f))
  - `automatik/interaktion.json`
- 16:12 ✍️ Auswertung: aktive Zeiten der ganzen Woche (auf deutsche Zeit umgerechnet) – 19:30 passt, Sonntag stärkster Abend ([`a2f31a3`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a2f31a30f1fd371ecc9e4895d59dac6e254bc376))
  - `strategie/06_auswertung.md`
- 15:11 📈 Statistik 2026-10-02 ([`c3f893b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c3f893b5c2d3bb9f56c0b7b3646ae9679ac7990b))
  - `automatik/statistik`
- 13:18 ✍️ Lage-Notizen: Interaktion gemergt, offen sind Secrets und Kontenliste ([`a54983d`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a54983d43696c5264401b31bfd0d104f40971bbb))
  - `automatik/lage_notizen.md`
- 13:18 🔀 Merge: Zweite Säule Interaktion (Radar, Kommentar-Hilfe, LinkedIn-Pakete) ([`47638f3`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/47638f3a174a1652349a3026025805e6a6024553))
- 13:14 ✍️ Zweite Säule Interaktion: Radar, Kommentar-Hilfe, LinkedIn-Pakete ([`cbe6029`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/cbe6029322456f13146cef5c89d2ece58c5b28fb))
  - `.github/workflows`, `EINRICHTUNG.md`, `README.md`, `automatik/fb_schluessel_verlaengern.py`, `automatik/interaktion.json`, `automatik/ki.py`, `…`
- 12:15 🤖 Autopilot: 01-story-frage veroeffentlicht ([`3b2259f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/3b2259fe3586af7149a5ff06981c0f95d9e2190c))
  - Plan: `01-story-frage` status: freigegeben → veroeffentlicht; `01-story-frage` online: https://www.instagram.com/stories/maehrsteuern/3998984318181825905
- 11:00 🤖 Autopilot: Dateien fuer 01-story-frage vorbereitet ([`7789e51`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/7789e5125a87885287c3cc34acbce3910159a8c6))
  - `posts/01_2026-10-04_reel_ampel`
- 08:47 📈 Statistik 2026-10-02 ([`60c4aa6`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/60c4aa67f643e11d4d6ef46ef453c4a2c18202b3))
  - `automatik/statistik`

**Do 01.10.2026**
- 23:56 ✍️ Lage: Neuvorstellung als veroeffentlicht eingetragen, Notizen auf Stand 01.10. abends ([`805d54b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/805d54b688b007b543fe592ea32cf008054844a9))
  - Plan: `00-neuvorstellung` status: manuell → veroeffentlicht; `00-neuvorstellung` online: https://www.instagram.com/p/Dd9V5HAAhcL/
- 23:42 ✅ Freigabe 08: go – Wissens-Reel KSt-Staffel Fr 09.10. 19:30 (Einstieg neu mit 30-%-Tabelle) und Storys 03./09./10.10. ([`408aec1`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/408aec19b17bf969055638edeb99707edf4cb3b2))
  - `posts/08_2026-10-09_reel_kst_staffel`, `vorlagen/system/aufnahmen/tabelle_30prozent.html`, `vorlagen/system/schnitt/p08_reel_kst_staffel.json`
- 23:33 ✍️ DM-Strecke: ManyChat erst ab mehr DMs (Schwelle festgehalten) ([`a24df07`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a24df07835a8e97cc929e291aac789076cad780e))
  - `strategie/04_dm_strecke.md`
- 23:31 ✍️ Redaktionsplan: Regel fuer Hinter-dem-Code-Beitraege (kein Jargon, immer Aha im Kanzleialltag) ([`1c5285f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1c5285f0548874863ba8d4ae67e3c3f90dc23fb6))
  - `strategie/03_redaktionsplan.md`
- 22:55 ✍️ Split-Reel als Begleit-Reel auf Mi 07.10. 19:30 vorgezogen (Teaser 19:35), Bildunterschrift oben/unten korrigiert ([`9c487b5`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/9c487b500d1fbec910db609568aa549348dfb7e1))
  - Plan: `06-reel-split` zeit: 2026-10-11 19:30 → 2026-10-07 19:30; `06-story-teaser` zeit: 2026-10-11 19:35 → 2026-10-07 19:35
- 21:39 ✅ Freigabe #15: go ([`a1c37f2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a1c37f287f46c60263bc0763f2c74dac956146fe))
  - Plan: `08-story-tipp` status: entwurf → freigegeben; `08-story-heute` status: entwurf → freigegeben; `08-reel-kst-staffel` status: entwurf → freigegeben; `08-story-rueckblick` status: entwurf → freigegeben
- 20:53 ✅ Freigabe angefragt (1 Beitrag/Beiträge) ([`c9bc6a3`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c9bc6a3ea3cace2cbeeaf1eba8b7b2a70df90e0f))
  - Plan: `08-story-tipp` → Freigabe-Issue #15; `08-story-heute` → Freigabe-Issue #15; `08-reel-kst-staffel` → Freigabe-Issue #15; `08-story-rueckblick` → Freigabe-Issue #15
- 20:53 ✍️ Content-Fabrik: Wissens-Reel KSt-Staffel (Fr 09.10.) und Mittags-Storys 03./09./10.10. als Entwurf ([`57cc299`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/57cc299dca2fa36a99febde1189bac5ab0d85e5b))
  - Plan: neu `08-story-tipp` (2026-10-03 12:15, entwurf); neu `08-story-heute` (2026-10-09 12:15, entwurf); neu `08-reel-kst-staffel` (2026-10-09 19:30, entwurf); neu `08-story-rueckblick` (2026-10-10 12:15, entwurf)
- 20:49 📈 Statistik 2026-10-01 ([`03c29c8`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/03c29c89d0c80c5955295b2a456dd03d72540461))
  - `automatik/statistik`
- 18:32 ✍️ Kalender: Drehbuch-Link im To-do für fehlende Clips ([`e66ed4c`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e66ed4c28a0945cbba3b786ace32c49667f66a4f))
  - `automatik/kalender.py`, `kalender.ics`
- 18:02 🔀 Merge branch 'claude/busy-shannon-s341nd' into claude/instagram ([`1edc40b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1edc40b064d9335d593884fadc7d23edf2da9b8e))
- 18:01 ✍️ Kalender-Feed: kalender.ics aus plan.json (Beiträge, Freigaben, fehlende Clips/Musik), wird mit der Lage automatisch neu geschrieben ([`41c3f6e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/41c3f6e6046a45f36542b9dece14a75f99015307))
  - `.github/workflows`, `EINRICHTUNG.md`, `README.md`, `automatik/kalender.py`, `automatik/lage_notizen.md`, `kalender.ics`
- 15:55 📈 Statistik 2026-10-01 ([`9d77f59`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/9d77f59e10b8afeba9e3c83383dceaae114eedc1))
  - `automatik/statistik`
- 15:11 ✅ Freigabe #14: go ([`5e2e5d0`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/5e2e5d0c889aa1954b0ec25064e0c9edca349afa))
  - Plan: `07-reel-hinzurechnung` status: entwurf → freigegeben
- 10:22 ✅ Freigabe angefragt (1 Beitrag/Beiträge) ([`fa3bf2a`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/fa3bf2a24cefa9c9f35c72b95661646f609a3e39))
  - Plan: `07-reel-hinzurechnung` → Freigabe-Issue #14
- 10:21 ✍️ Strategie: Karussell vs. Reel am Abend ergänzt; Neuvorstellung bleibt Karussell ([`a4d5abd`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a4d5abd328a414c99dee685d50a5df6cc87fe857))
  - `strategie/11_wissen_instagram.md`
- 10:11 ✍️ Plan: 3 Reels pro Woche (Mi/Fr/So) – Begleit-Reel Hinzurechnung Mi 14.10. als Entwurf, Sprechtexte für Fr 09.10. und 16.10. ([`b74ebc3`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/b74ebc3d4ec29d7655f46b313b584b65ffa66508))
  - Plan: neu `07-reel-hinzurechnung` (2026-10-14 19:30, entwurf)
- 10:01 ✍️ Strategie: Video Sebiforce (Verkaufen ohne Kaltakquise) eingearbeitet, Entscheidungen 2–3 Reels/Woche und Werbebudget nur für laufende Beiträge ([`f1b05cc`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f1b05ccb0128933da2ecf6638ff3722b84122e9e))
  - `automatik/lage_notizen.md`, `strategie/11_wissen_instagram.md`
- 09:48 ✍️ Strategie: Instagram-Wissen aus 5 Artikeln gesammelt (Algorithmus, Teilen/Speichern, Suche, Serien, Saison) und in Redaktionsplan/Reel-Regeln verlinkt ([`6398d4e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/6398d4e1a4a781a0e285577dacb8d842ebc3313a))
  - `README.md`, `automatik/lage_notizen.md`, `strategie/03_redaktionsplan.md`, `strategie/09_reel_regeln.md`, `strategie/11_wissen_instagram.md`
- 09:43 ✍️ Lage-Notizen aktualisiert: Ampel-Reel freigegeben, Content-Fabrik 01.10. ergänzt, Neustart-Schritte für heute ([`14ea872`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/14ea8723269b97ca7c0353ad85c3a6985f47e3bd))
  - `automatik/lage_notizen.md`
- 09:38 ✅ Freigabe #12: go ([`af139c9`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/af139c9b3518ba304516edbb193f44d9d6e376ec))
  - Plan: `05-story-frage` status: entwurf → freigegeben; `05-latente-steuern` status: entwurf → freigegeben; `05-story-teaser` status: entwurf → freigegeben
- 09:37 ✅ Freigabe #13: go ([`3768a94`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/3768a9419c370c50ecd16a89a879e98556b0138d))
  - Plan: `06-reel-split` status: entwurf → freigegeben; `06-story-teaser` status: entwurf → freigegeben
- 09:29 ✅ Freigabe angefragt (2 Beitrag/Beiträge) ([`260979f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/260979f24133388d2d7cc77b878d811d9a21e817))
  - Plan: `05-story-frage` → Freigabe-Issue #12; `05-latente-steuern` → Freigabe-Issue #12; `05-story-teaser` → Freigabe-Issue #12; `06-reel-split` → Freigabe-Issue #13; `06-story-teaser` → Freigabe-Issue #13
- 09:29 ✅ Freigabe #7: go – Reel Ampel (Stimme) So 04.10. 19:30 ([`349ebba`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/349ebbacc7d52731a96720c7d7538bb4a75e6fb4))
  - Plan: `01-reel-ampel` status: entwurf → freigegeben
- 09:13 🔀 Merge: Freigabe robust gegen fehlgeschlagenes Speichern ([`559aec1`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/559aec18abc324cf8b1f9488de5654154fade0e7))
- 09:12 ✅ Freigabe: push mit Wiederholung, go/stop findet Beiträge auch ohne gespeicherte Issue-Nummer (über den Titel) ([`3070a04`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/3070a04173765d6ea35cef39ea0e9c998d095b39))
  - `automatik/freigabe.py`
- 08:56 ✍️ Content-Fabrik 01.10.: Karussell latente Steuern (08.10.) mit Storys, Split-Reel Excel gegen Tool (11.10.) als Entwuerfe ([`4646f25`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4646f252f71029dfe7526ee2119864032710affe))
  - Plan: neu `05-story-frage` (2026-10-07 12:15, entwurf); neu `05-latente-steuern` (2026-10-08 19:30, entwurf); neu `05-story-teaser` (2026-10-08 19:35, entwurf); neu `06-reel-split` (2026-10-11 19:30, entwurf); neu `06-story-teaser` (2026-10-11 19:35, entwurf)
- 08:21 📈 Statistik 2026-10-01 ([`431db3b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/431db3b1b6bbe22e73c56dd1258a827b7ec2d175))
  - `automatik/statistik`
- 08:18 ✍️ Schluessel verlaengern: Workflow neu anmelden (war bei GitHub nicht registriert) ([`94eb587`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/94eb5875c40243fdacc3da6695390902f39d463d))
  - `.github/workflows`

**Mi 30.09.2026**
- 19:45 🔀 Merge: Statistik täglich ca. 08:45 + Tagesbericht ([`b427de9`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/b427de99d250726c8bfffe750bfd24e6b15513cf))
- 19:45 📈 Statistik täglich ca. 08:45 (Anstoß über Lage-Lauf, Reserve-Zeitplan) + Tagesbericht in LAGE.md ([`6f3a270`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/6f3a2708cc7ab144af63059f669c7d49bc5f164a))
  - `.github/workflows`, `EINRICHTUNG.md`, `README.md`, `automatik/lage.py`, `automatik/statistik.py`
- 18:49 ✅ Freigabe: eigene Warteschlange, damit der 15-Min.-Posten-Takt wartende Freigabe-Läufe nicht mehr verdrängt ([`4372d22`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4372d220840705e09262ad0782074a1e59e464f5))
  - `.github/workflows`
- 18:38 ✅ Freigabe angefragt (1 Beitrag/Beiträge) ([`0d81948`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/0d819486c988f0b002726307f089a428466b688b))
  - Plan: `01-reel-ampel` → Freigabe-Issue #7
- 18:37 🤖 Autopilot: 00-vorfreude veroeffentlicht ([`2ec2f9d`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/2ec2f9d4eaaccbdc37a9e3f5a93d7f7cf920d167))
  - Plan: `00-vorfreude` status: freigegeben → veroeffentlicht; `00-vorfreude` online: https://www.instagram.com/stories/maehrsteuern/3997727075650058524
- 18:24 ✍️ Bildunterschrift Reel Ampel an die Fassung mit Loris' Stimme angepasst (Excel-Fehler, Code, lokal) ([`c371f6f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c371f6fef6723840031efba88ec160c88d9c50f0))
  - `posts/01_2026-10-04_reel_ampel`
- 18:22 ✍️ Plan: Reel Ampel (Fassung mit Stimme) neu zur Freigabe – Status entwurf, neues Freigabe-Issue ([`9aeceb2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/9aeceb2bd9fcd106c0524d3f6fbd161305dae4c9))
  - Plan: `01-reel-ampel` status: pause → entwurf
- 18:19 🔀 Merge: Reel Ampel testet die Fassung mit Loris' Stimme (reel_stimme.mp4), Status pause bleibt ([`8106eb9`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/8106eb9823c4d5e707f40c833010ee30c6050ef1))
- 18:18 ✍️ Plan: Reel Ampel (04.10.) testet die Fassung mit Loris' Stimme (reel_stimme.mp4) ([`080e966`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/080e96623844e913c20ed71c112e26e1338f4c08))
  - `automatik/plan.json`
- 18:15 🤖 Autopilot: Dateien fuer 00-vorfreude vorbereitet ([`de366fa`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/de366fa96f1339ddeac43467097ab50bc0c008a3))
  - `posts/extra_2026-09-30_vorfreude`
- 17:47 ✍️ Ampel-Reel mit neuer Sprachaufnahme: Untertitel wörtlich, Stimme vorn, Musik und Atmo leise; Learnings in den Reel-Regeln ([`2bff54b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/2bff54b9897e26d4431e642caa8fc8b21e191132))
  - `posts/01_2026-10-04_reel_ampel`, `strategie/09_reel_regeln.md`, `vorlagen/system/schnitt/p01_reel_ampel_stimme.json`
- 17:31 ✍️ Ampel-Reel: neue Fassung mit Loris' Stimme (Ich-Geschichte, wörtliche Untertitel, keine Lo-Fi-Musik) ([`8860eac`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/8860eac08352f9cfdf258950a3df20d914dd378c))
  - `posts/01_2026-10-04_reel_ampel`, `vorlagen/system/montage.py`, `vorlagen/system/schnitt/p01_reel_ampel_stimme.json`
- 17:16 ✍️ Reel-Regeln: Feedback zum Ampel-Reel – zu professionell/generisch, mehr persönliches Drama statt Screen-Demo mit Lo-Fi ([`b10373c`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/b10373c626e2f520c314bd668296b2b28f2292bf))
  - `strategie/09_reel_regeln.md`
- 16:09 🔀 Merge remote-tracking branch 'origin/claude/instagram' into claude/instagram ([`befde8f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/befde8f42c6c366748595166c8106b10ae22702e))
- 16:08 🔀 Merge: Reels aus echten Programm-Aufnahmen, Hook-Bibliothek, Reel-Ampel auf reel_hook.mp4 (Status pause bleibt) ([`e048af2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e048af2954e4154ba3bb16ffef04852f9271bf51))
- 16:07 🔀 Merge: Lage ohne Dauer-Commits ([`e7e5dfa`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e7e5dfabe79cba20f5164613645778ece0cb96ba))
- 16:07 🔀 Merge remote-tracking branch 'origin/claude/instagram' into claude/admiring-ramanujan-2dwc7k ([`12606f7`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/12606f7ff905a81186369517ecdc71cf31772ae8))
- 15:28 📈 Statistik 2026-09-30 ([`a4bab94`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a4bab94532ab349b4f2d5f23572b90447d272c10))
  - `automatik/statistik`
- 15:26 ✍️ Lage: Stand ohne eigene Lage-Commits (verhindert Commit alle 15 Minuten) ([`5c69bdd`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/5c69bddf24fc338217ec0736bfd5f418bb681b7e))
  - `automatik/lage.py`
- 15:26 ✍️ Plan: Ampel-Reel postet die Hook-Version mit echter Programm-Aufnahme (reel_hook.mp4) ([`4242076`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4242076191ff34c4c5839600bf9c6c6abcde79bd))
  - `automatik/plan.json`
- 13:28 ✍️ Hook-Bibliothek: zehn fertige Reel-Einstiege (1,8-2,8 s) mit Bauskript ([`cbfc192`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/cbfc1920d55787b310d0bd61918e87fcd7e8b446))
  - `musik/QUELLEN.md`, `vorlagen/hooks/README.md`, `vorlagen/hooks/bausteine/karte_oben_tabelle.mp4`, `vorlagen/hooks/bausteine/karte_unten_tool.mp4`, `vorlagen/hooks/bausteine/ki_buero_abend.mp4`, `vorlagen/hooks/bausteine/ki_taschenrechner.mp4`, `…`
- 13:01 ✍️ Post 02: untere Hälfte mit echter Delta-Plakette (+87.500) neu aufgenommen ([`defb906`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/defb9069e7cdf692414b87e0945704638c52ffa9))
  - `posts/02_2026-10-06_excel_fehler`, `strategie/10_software_reel_konzept.md`, `vorlagen/system/aufnahmen/split_excel_tool.mjs`
- 12:50 ✅ Freigabe #2: stop ([`6f673c3`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/6f673c3f8ae35d0bfbcd75cbed1e447959f9d73b))
  - Plan: `01-reel-ampel` status: entwurf → pause
- 12:47 🔀 Merge: externer Posten-Takt eingerichtet ([`00f0756`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/00f07568055445b6a012dc4c6e97a299c7798495))
- 12:47 ✍️ Externer Posten-Takt eingerichtet (cron-job.org, Test 204), Ablaufdaten notiert ([`258f5fd`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/258f5fd049079208bf84903c532f607ba19bc945))
  - `EINRICHTUNG.md`, `automatik/lage_notizen.md`
- 12:38 ✍️ Post 02: Split-Screen-Reel Tabelle gegen Tool (Hebesatz 400 -> 450) ([`ec1c4df`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ec1c4dff3fb411294c9838cec27393e04e110ea1))
  - `posts/02_2026-10-06_excel_fehler`, `strategie/10_software_reel_konzept.md`, `vorlagen/system/aufnahmen/excel_attrappe.html`, `vorlagen/system/aufnahmen/rekorder.mjs`, `vorlagen/system/aufnahmen/split_excel_tool.mjs`, `vorlagen/system/schnitt/p02_reel_split.json`
- 12:37 🔀 Merge: externer Takt fürs Posten (EINRICHTUNG Schritt 5) ([`16bec95`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/16bec95ba152bf98778aca0645155f06b09868f9))
- 12:37 ✍️ Einrichtung: externer 15-Min.-Takt fürs Posten über cron-job.org (GitHub-Zeitplan fällt aus) ([`3c4f377`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/3c4f377564522f803a179e379deef606bd14b87d))
  - `EINRICHTUNG.md`, `automatik/lage_notizen.md`
- 12:35 🤖 Autopilot: 00-start-3 veroeffentlicht ([`aab43f3`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/aab43f30e4bf740fabc2c30ae765cafa24f8d674))
  - Plan: `00-start-3` status: freigegeben → veroeffentlicht; `00-start-3` online: https://www.instagram.com/stories/maehrsteuern/3997545080966344429
- 12:35 🤖 Autopilot: Dateien fuer 00-start-3 vorbereitet ([`cc6bd34`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/cc6bd342f9607e5d0f875ed3a36cc0a940918a3b))
  - `assets/storys/start/_jpg/start_3.jpg`
- 12:35 🤖 Autopilot: 00-start-2 veroeffentlicht ([`2cda9a5`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/2cda9a5ac7a96d23f9f4cf211043e4a30dc300b7))
  - Plan: `00-start-2` status: freigegeben → veroeffentlicht; `00-start-2` online: https://www.instagram.com/stories/maehrsteuern/3997544897742372327
- 12:35 🤖 Autopilot: Dateien fuer 00-start-2 vorbereitet ([`18a5f5d`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/18a5f5d5d793d2c6bdae93462eceb706bd347425))
  - `assets/storys/start/_jpg/start_2.jpg`
- 12:35 🤖 Autopilot: 00-start-1 veroeffentlicht ([`c104979`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c104979ca545a77571a71aebff738a648c936600))
  - Plan: `00-start-1` status: freigegeben → veroeffentlicht; `00-start-1` online: https://www.instagram.com/stories/maehrsteuern/3997544707312529712
- 12:34 🤖 Autopilot: Dateien fuer 00-start-1 vorbereitet ([`422d822`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/422d8223d998e79f7ed7d26cece1437a1029bc4f))
  - `assets/storys/start/_jpg/start_1.jpg`
- 11:55 ✍️ Post 03: Begleit-Reel GewSt-Hinzurechnung aus echter Programm-Aufnahme ([`c457e10`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c457e10cbc35bac47e0f62590f78929d62552c39))
  - `posts/03_2026-10-13_gewst_hinzurechnung`, `strategie/10_software_reel_konzept.md`, `vorlagen/system/aufnahmen/ampel_gelb_gruen.mjs`, `vorlagen/system/aufnahmen/gewst_hinzurechnung.mjs`, `vorlagen/system/aufnahmen/rekorder.mjs`, `vorlagen/system/schnitt/p03_reel_hinzurechnung.json`
- 11:55 ✍️ Beitrag 03: Hook „Werden Mieten voll hinzugerechnet?“ ([`f4d49f4`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f4d49f446f5ca2dff902da7c8efcee75258c7ad3))
  - `posts/03_2026-10-13_gewst_hinzurechnung`, `strategie/03_redaktionsplan.md`, `strategie/08_hooks.md`, `vorlagen/system/jobs/p03_gewst.json`
- 11:54 🔀 Merge remote-tracking branch 'origin/claude/instagram' into claude/focused-darwin-3hmeil ([`79b6d5c`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/79b6d5c558810a5a458075d41f3d0834c2a09617))
- 11:54 ✍️ Hook-Sammlung: strategie/08_hooks.md ([`ab7ce12`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ab7ce12bc907b5474012662116e864122e104ef6))
  - `README.md`, `strategie/03_redaktionsplan.md`, `strategie/08_hooks.md`
- 11:54 🔀 Merge: Lage – laufender Überblick LAGE.md + Skill ([`1a0cc59`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1a0cc5962a47730a3061b5144954ba4d7ebf0e92))
- 11:01 ✍️ Ampel-Reel: echte Programm-Aufnahme Gelb -> Grün statt Standbilder ([`e5d6794`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e5d67948e33f5623a7c741bd68b7ac1f0bbbe4d3))
  - `posts/01_2026-10-04_reel_ampel`, `strategie/10_software_reel_konzept.md`, `vorlagen/system/aufnahmen/ampel_gelb_gruen.mjs`, `vorlagen/system/montage.py`, `vorlagen/system/schnitt/p01_reel_ampel_hook.json`
- 10:55 ✍️ Lage: laufender Überblick LAGE.md (Plan, offene Punkte, Automatik, Protokoll jeder Änderung) + Skill ([`ce1dfd3`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ce1dfd370f6ad1e09c2cc8145d38945ddc49219e))
  - `.claude/skills/lage/SKILL.md`, `.github/workflows`, `CLAUDE.md`, `README.md`, `automatik/lage.py`, `automatik/lage_notizen.md`
- 10:50 ✍️ Start-Story 1: Hook „Wir müssen ehrlich über Excel reden.“ ([`d5290d5`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/d5290d549c6f4af12c5828ce371869601b0313a1))
  - `assets/storys/start/start_1.png`, `vorlagen/system/jobs/start_storys.json`
- 10:37 ✍️ Strategie: eigenes Reel-Konzept für Software (Split-Screen, Satisfying Software, Gesicht + Screen) ([`457cf54`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/457cf541e93c8ed58913cd587bdd30923cacbed4))
  - `strategie/09_reel_regeln.md`, `strategie/10_software_reel_konzept.md`
- 10:34 ✍️ Ampel-Reel: ruhiger Hook mit Atmo statt Musik, Lo-Fi erst ab der Lösung ([`11d8e74`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/11d8e748f39d0af80e9343520d879aa9412326c1))
  - `musik/06_runway_lofi_ruhig.mp3`, `musik/QUELLEN.md`, `musik/atmo/fehlerton.mp3`, `musik/atmo/tippen_fehlerton.mp3`, `musik/atmo/uhr_ticken.mp3`, `posts/01_2026-10-04_reel_ampel`, `…`
- 10:26 ✍️ Ampel-Reel: schnelle Hook-Montage mit KI-Clip, Effekten und Outline-Texten ([`74d38e3`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/74d38e3c39a438a8b7252a1e4dfa177011827a18))
  - `posts/01_2026-10-04_reel_ampel`, `vorlagen/system/montage.py`, `vorlagen/system/schnitt/p01_reel_ampel_hook.json`, `vorlagen/system/schriften/Outfit-Bold.ttf`, `vorlagen/system/schriften/Outfit-OFL.txt`
- 10:09 ✍️ Ampel-Reel: Runway-Deep-House-Titel, Drop auf Schnitt bei 1,3 s ([`ce63bcc`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ce63bcc13f7291956e4c402a24d492784d23ae22))
  - `musik/05_runway_deephouse.mp3`, `musik/QUELLEN.md`, `posts/01_2026-10-04_reel_ampel`, `vorlagen/system/schnitt/p01_reel_ampel_musik.json`
- 10:02 ✍️ reel.py: Option musik_start (Titel versetzt starten); ungenutzten Workflow entfernt ([`8a81bdb`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/8a81bdbb98e89d73aba0c5196c9e917f64034dc3))
  - `.github/workflows`, `vorlagen/system/reel.py`
- 09:54 ✍️ Workflow „Musik von URL“; Reel Ampel zurück auf Autopilot ([`177435b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/177435bad3a8aab05af82d211ca5c56b1735985b))
  - Plan: `01-reel-ampel` status: manuell → entwurf
- 09:50 ✍️ Reel Ampel: manuell mit Instagram-Musik statt eingebauter Musik ([`48dd8a7`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/48dd8a7987a9e8dc62150305b141ef42e41cdd75))
  - Plan: `01-reel-ampel` status: entwurf → manuell
- 09:49 ✍️ Reel Ampel: Hinweis „läuft lokal“ in Aufruf-Leiste und Bildunterschrift ([`bc4b807`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/bc4b8073c68cbcc79851ff51be5eb62e847d958a))
  - `posts/01_2026-10-04_reel_ampel`, `vorlagen/system/jobs/p01_reel_ampel.json`
- 09:47 ✍️ Reel Ampel: neuer Einstieg #BEZUG!, Ampel Rot→Gelb→Grün, 11 s ohne Abspann ([`d96a6c1`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/d96a6c176dfac57d3660a520479e0567574c2a13))
  - `README.md`, `automatik/plan.json`, `posts/01_2026-10-04_reel_ampel`, `strategie/03_redaktionsplan.md`, `strategie/08_demo_reel_formel.md`, `vorlagen/system/ampel.html`, `…`
- 08:56 📈 Statistik 2026-09-30 ([`068d3fb`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/068d3fb9dc3d508d04ffcd6340aee0e4432052db))
  - `automatik/statistik`
- 07:31 ✅ Freigabe #1: go ([`32bac43`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/32bac432abd6a15141b6d74da0e5516a09bab628))
  - Plan: `00-vorfreude` status: entwurf → freigegeben
- 06:03 ✅ Freigabe angefragt (2 Beitrag/Beiträge) ([`1cd5370`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1cd53708b890f895560b4078d677fbbfd1c9fa28))
  - Plan: `00-vorfreude` → Freigabe-Issue #1; `01-reel-ampel` → Freigabe-Issue #2
- 06:02 ✍️ Entwuerfe: Vorfreude-Story heute 19:30, Ampel-Reel automatisch mit Musik ([`4e4d043`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4e4d0435e8360c7b138a9d9d40c1925db82c0a1e))
  - Plan: neu `00-vorfreude` (2026-09-30 19:30, entwurf); `01-reel-ampel` status: manuell → entwurf
- 05:58 ✍️ Plan: 3 Start-Storys heute 12:30-12:32 automatisch ([`dfd885f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/dfd885f00d09730777291bbe33a07c29ec27d975))
  - Plan: neu `00-start-1` (2026-09-30 12:30, freigegeben); neu `00-start-2` (2026-09-30 12:31, freigegeben); neu `00-start-3` (2026-09-30 12:32, freigegeben)
- 05:49 ✍️ DM-Strecke: Stand 30.09. abends (nur Sofortantwort, tool2 Berechnungen, Tests) ([`7922a53`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/7922a53fdbd2b00e3ab36e9edb3c577b51202dd7))
  - `strategie/04_dm_strecke.md`
- 05:41 ✍️ Reel Ampel: neuer Einstieg mit Excel-Chaos und hartem Schnitt aufs Dashboard ([`b0da689`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/b0da689efbda5be42c868dba08db25a6cb375326))
  - `posts/01_2026-10-04_reel_ampel`, `vorlagen/system/excel_chaos.html`, `vorlagen/system/jobs/p01_reel_ampel.json`, `vorlagen/system/render.mjs`, `vorlagen/system/schnitt/p01_reel_ampel.json`
- 05:27 ✍️ DM-Strecke: Schnellantworten nach Gruppe (tool1-5, termin), Automatik TOOL in der App ([`c5199cb`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/c5199cb514c03c9b31a2e6c46b00d77f64ac9bac))
  - `strategie/04_dm_strecke.md`
- 05:23 ✍️ DM-Strecke: Sofortantwort aktiv, danach manuell ([`a01471c`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a01471c265dbc3227415f2aeac8e758d7c4d4d37))
  - `strategie/04_dm_strecke.md`
- 04:49 ✍️ Neuvorstellung: alle App-Einstellungen zum Neu-Einplanen ([`bac74a7`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/bac74a7ff1a17d4331c563a901c8be2e84656a81))
  - `posts/00_2026-10-01_neuvorstellung`
- 04:48 ✍️ Neuvorstellung: flexible Folie 6 und Bildunterschrift zum Neu-Einplanen ([`2ae0cd9`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/2ae0cd9a8714fba93c24a61aed295b775757662c))
  - `posts/00_2026-10-01_neuvorstellung`, `vorlagen/system/jobs/p00_neuvorstellung.json`
- 04:43 ✍️ Neustart: Examens-Community als Zielgruppe, Bildunterschrift Neuvorstellung, Themenspeicher, Demo-Drehbuch, DM-Tracking anonymisiert ([`a1b4eee`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a1b4eee53141dbd066c7bb3cbe7d4e0e01856efd))
  - `posts/00_2026-10-01_neuvorstellung`, `strategie/01_positionierung.md`, `strategie/03_redaktionsplan.md`, `strategie/04_dm_strecke.md`, `strategie/06_auswertung.md`, `strategie/07_demo_video.md`, `…`
- 04:38 ✍️ Auswertung: Ausgangswert 352 echte Follower ([`f8214ec`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f8214ec5af15642d577522b92b10e7d17fea6aab))
  - `strategie/06_auswertung.md`
- 04:32 📈 Statistik 2026-09-30 ([`8a0d526`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/8a0d5264729060fb801fbce85e9113d261c0337d))
  - `automatik/statistik`
- 04:28 ✍️ Neuvorstellung: alte Folie 6 bleibt (so geplant in der App) ([`5e4450e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/5e4450e0eac5740d3214da11770e3eaaeab34d1f))
  - `posts/00_2026-10-01_neuvorstellung`, `vorlagen/system/jobs/p00_neuvorstellung.json`
- 04:24 ✍️ Neuvorstellung: flexibel mindestens 1-2 Beitraege pro Woche, meist 19:30 ([`e392ff5`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e392ff53af778cb1bf0814c98e1e9b27db2a0474))
  - `posts/00_2026-10-01_neuvorstellung`, `vorlagen/system/jobs/p00_neuvorstellung.json`
- 04:24 ✍️ Neuvorstellung: Folie 6 und Text auf mindestens 3 Beitraege, Di/Do/So 19:30 ([`3144e0e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/3144e0ec45e16ce041383d70c387c4ebdde97b62))
  - `posts/00_2026-10-01_neuvorstellung`, `vorlagen/system/jobs/p00_neuvorstellung.json`
- 04:22 ✍️ Postingzeit ab 04.10. auf 19:30 (Follower-Hoch um 20 Uhr laut Statistik) ([`d0a9d62`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/d0a9d6244436b98f00617641479df6c135b7cd37))
  - Plan: `01-reel-ampel` zeit: 2026-10-04 18:30 → 2026-10-04 19:30; `01-story-teaser` zeit: 2026-10-04 18:35 → 2026-10-04 19:35; `02-excel-fehler` zeit: 2026-10-06 18:30 → 2026-10-06 19:30; `02-story-teaser` zeit: 2026-10-06 18:35 → 2026-10-06 19:35; `03-gewst-hinzurechnung` zeit: 2026-10-13 18:30 → 2026-10-13 19:30; `03-story-teaser` zeit: 2026-10-13 18:35 → 2026-10-13 19:35; `04-reel-mein-weg` zeit: 2026-10-20 18:30 → 2026-10-20 19:30; `04-story-teaser` zeit: 2026-10-20 18:35 → 2026-10-20 19:35
- 04:19 ✍️ Auswertung: Eigen-Push und gekaufte Reichweite 2025 beruecksichtigt ([`a6cd5e2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a6cd5e22dc694e0eda7108dc4602c91f77a96219))
  - `strategie/06_auswertung.md`
- 04:15 ✍️ Auswertung Instagram-Insights 30.09.2026 ([`f5d676a`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/f5d676a42f0b8d3f8df334d7df6bd7e28aa99995))
  - `automatik/insights_voll.py`, `strategie/06_auswertung.md`
- 04:13 ✍️ Insights: Verlauf nur bis Kontostart Mai 2025 ([`fb262b9`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/fb262b902e9305ddb9c4fae891de40fc5f8f2123))
  - `automatik/insights_voll.py`
- 04:12 📈 Statistik 2026-09-30 ([`d66b955`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/d66b9557b86ab3fabc3ff0706cc873590c0bb324))
  - `automatik/statistik`
- 04:08 ✍️ Insights: leere Aufschluesselungen abfangen ([`4cb094b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4cb094b730ef5c3734f8ddd941a70921209e45aa))
  - `automatik/insights_voll.py`
- 04:00 📈 Statistik: doppelter Lauf am selben Tag endet ohne Fehler ([`73e74fe`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/73e74fe01cfaa7251a923d2ec19ccd636674599a))
  - `automatik/statistik.py`
- 04:00 📈 Statistik: vollstaendige Insights (Zielgruppe, Verlauf, Reel-Kennzahlen, Kommentare) ([`ed7753b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/ed7753bcbfda194568f15946ec8c61e162337bc0))
  - `.github/workflows`, `automatik/insights_voll.py`, `automatik/statistik.py`
- 03:48 🎵 Musik: Rausch-Titel entfernt, Reihenfolge nach Eignung ([`10a183e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/10a183ed4f746845c8e109cdf9e6af6b45e5113b))
  - `musik/05_gt577noisesurfer_rainteardrops_01_noises.mp3`, `musik/QUELLEN.md`, `musik/README.md`
- 03:48 🎵 Musik: gemeinfreie Titel (CC0) aus dem Internet Archive ([`69e6aa2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/69e6aa23790d3c8a0a25157ef9557f30ae34992c))
  - `musik/01_productionloopsandsamplesvol12009_2011_0.mp3`, `musik/02_variousartists_tastersvinegar3_03_a_n_k.mp3`, `musik/03_plantasia_garfield_park_conservatory_02.mp3`, `musik/04_tomorrows_harbest_raw_wav_a1_gemini.mp3`, `musik/05_gt577noisesurfer_rainteardrops_01_noises.mp3`, `musik/QUELLEN.md`
- 03:44 🎵 Musik holen: Laengenangaben im Format mm:ss verstehen ([`810338b`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/810338b846468e63c4afb2678ad839485b9780ba))
  - `automatik/musik_holen.py`
- 03:42 🎵 Musik holen: einfachere Suchabfragen ([`e10ff49`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e10ff494ae8c9267e32a3b3ca1225d32832ab617))
  - `automatik/musik_holen.py`
- 03:41 🎵 Musik holen: Quelle Internet Archive (CC0), FreePD ist geschlossen ([`a9c3d69`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/a9c3d6928e349b17d9b7b3e8120fc4d6fbd244d8))
  - `.github/workflows`, `automatik/musik_holen.py`
- 03:41 🎵 Musik holen: breitere Suche und Protokoll ([`fb67903`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/fb67903ec9316d97452f0ccf07400359891c0e40))
  - `automatik/musik_holen.py`
- 03:40 🎵 Musik holen: gemeinfreie Titel (CC0) von FreePD per Workflow ([`cbfb80a`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/cbfb80ade71abbdc926a8dbe5d4a4db5af43d0fc))
  - `.github/workflows`, `automatik/musik_holen.py`
- 03:34 🤖 Autopilot: Dateien fuer Probelauf 02-excel-fehler vorbereitet ([`dead862`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/dead862461ca2f7721903e10621d07c584ffd98a))
  - `posts/02_2026-10-06_excel_fehler`
- 03:33 ✍️ Posting-Lauf alle 15 Minuten statt stuendlich (ausgefallene GitHub-Zeitplaene abfangen) ([`2be796f`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/2be796fd90418a2852c5d1b9839316d07644ab4c))
  - `.github/workflows`
- 03:32 ✍️ Vollautomatik: Freigabe per Issue (go/stop), Storys ohne Sticker, Reels mit eingebauter Musik, 3 Beitraege pro Woche ([`4093d29`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/4093d29d4662bbe896a68d8b9cb98f4e93985ca6))
  - Plan: neu `01-story-frage` (2026-10-02 12:15, freigegeben); neu `02-story-umfrage` (2026-10-05 12:15, freigegeben); neu `03-story-quiz` (2026-10-12 12:15, freigegeben); neu `04-story-frage` (2026-10-19 12:15, entwurf)
- 03:27 🤖 Autopilot: Probelauf-Modus (hochladen ohne Veroeffentlichen) und Freigabe 04.10.-16.10. ([`892f85e`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/892f85e0414e1c0acf8ac1cda780a4a993ca0514))
  - Plan: `01-story-teaser` status: entwurf → freigegeben; `02-excel-fehler` status: entwurf → freigegeben; `02-story-teaser` status: entwurf → freigegeben; `03-gewst-hinzurechnung` status: entwurf → freigegeben; `03-story-teaser` status: entwurf → freigegeben; `03-story-aufloesung` status: entwurf → freigegeben
- 03:22 📈 Statistik 2026-09-30 ([`7a0815d`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/7a0815da20aac7c4641e29249d87e04aab9977db))
  - `automatik/statistik`
- 03:21 ✍️ Modify comment for workflow trigger clarity ([`9e128d1`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/9e128d175328a4f9d7fb9122d109e6f4da1e3048))
  - `.github/workflows`

**Di 29.09.2026**
- 22:47 ✍️ Neuvorstellung manuell in der App geplant, Teaser-Story entfaellt ([`eef8768`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/eef87684b6c812c3da006927c0da28b9dc21df85))
  - Plan: `00-neuvorstellung` status: entwurf → manuell; `00-story-teaser` status: entwurf → entfaellt
- 20:23 ✍️ Reel Ampel neu geschnitten: Haken ab dem ersten Bild ueber laufendem Dashboard, 14 s ([`0984d52`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/0984d527f5bee77f31947e246846f634d800ea80))
  - `posts/01_2026-10-04_reel_ampel`, `vorlagen/system/einblendung.html`, `vorlagen/system/jobs/p01_reel_ampel.json`, `vorlagen/system/reel.py`, `vorlagen/system/schnitt/p01_reel_ampel.json`
- 20:17 ✍️ DM-Tracking: erster Kontakt aus Kaltakquise ([`5c91e80`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/5c91e800c012ebf7a717dfa4727c7897b5089554))
  - `strategie/dm_tracking.csv`
- 20:14 ✍️ Leitspruch bleibt Steuern x Code, KI als Qualifikation; Bio, Terminlink und Start-Storys aktualisiert ([`42abd34`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/42abd3437316350355126e2dbff9d7b921c10a7b))
  - `README.md`, `assets/storys/start/start_1.png`, `posts/00_2026-10-01_neuvorstellung`, `posts/01_2026-10-04_reel_ampel`, `posts/02_2026-10-06_excel_fehler`, `posts/04_2026-10-20_reel_mein_weg`, `…`
- 20:09 ✍️ Leitspruch Steuern x KI: Vorlagen, Storys, Bio und Strategie angepasst ([`e4a6372`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/e4a63728fbf080782131ff9752f50986244794e0))
  - `README.md`, `assets/storys/start/start_1.png`, `posts/01_2026-10-04_reel_ampel`, `posts/02_2026-10-06_excel_fehler`, `posts/04_2026-10-20_reel_mein_weg`, `posts/extra_2026-09-29_countdown`, `…`
- 20:06 ✍️ Neuvorstellung: Werdegang (Diplom-Finanzwirt, IHK KI-Transformation) und Ausrichtung KI x Steuern ([`12420d2`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/12420d28e25d1407338d432540da8e7dd145fcbb))
  - `posts/00_2026-10-01_neuvorstellung`, `vorlagen/system/jobs/p00_neuvorstellung.json`
- 19:25 ✍️ Startwoche vorgezogen: Neuvorstellung Do 01.10., Reel So 04.10., danach dienstags ([`1e942af`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/1e942aff6edf7d31fd9e61cef194e3b942b163a6))
  - Plan: `00-neuvorstellung` zeit: 2026-10-04 18:30 → 2026-10-01 18:30; `00-story-teaser` zeit: 2026-10-04 18:35 → 2026-10-01 18:35; `01-reel-ampel` status: entwurf → manuell; `01-reel-ampel` zeit: 2026-10-06 18:30 → 2026-10-04 18:30; `01-story-teaser` zeit: 2026-10-06 18:35 → 2026-10-04 18:35; `02-excel-fehler` zeit: 2026-10-13 18:30 → 2026-10-06 18:30; `02-story-teaser` zeit: 2026-10-13 18:35 → 2026-10-06 18:35; `03-gewst-hinzurechnung` zeit: 2026-10-20 18:30 → 2026-10-13 18:30; `03-story-teaser` zeit: 2026-10-20 18:35 → 2026-10-13 18:35; `03-story-aufloesung` zeit: 2026-10-23 12:15 → 2026-10-16 12:15; `04-reel-mein-weg` zeit: 2026-10-27 18:30 → 2026-10-20 18:30; `04-story-teaser` zeit: 2026-10-27 18:35 → 2026-10-20 18:35
- 19:22 ✍️ Countdown-Story fuer den Neustart ([`77eb295`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/77eb29502816e4b10ba4de995b5b1bc4945601c5))
  - `posts/extra_2026-09-29_countdown`, `vorlagen/system/jobs/extra_countdown.json`
- 19:21 ✍️ Repo-Name Instagram-maehrsteuern eingetragen ([`8390edf`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/8390edf95db04982e136d36a618472e858c702ea))
  - `EINRICHTUNG.md`
- 19:17 ✍️ Instagram-Autopilot: Vorlagen, Beitraege Okt. 2026 und automatisches Posten ([`d04f975`](https://github.com/maehrsteuern/Instagram-maehrsteuern/commit/d04f97515051945cf5190af915df1281805d2b44))
  - Plan: neu `00-neuvorstellung` (2026-10-04 18:30, entwurf); neu `00-story-teaser` (2026-10-04 18:35, entwurf); neu `01-reel-ampel` (2026-10-06 18:30, entwurf); neu `01-story-teaser` (2026-10-06 18:35, entwurf); neu `02-excel-fehler` (2026-10-13 18:30, entwurf); neu `02-story-teaser` (2026-10-13 18:35, entwurf); neu `03-gewst-hinzurechnung` (2026-10-20 18:30, entwurf); neu `03-story-teaser` (2026-10-20 18:35, entwurf); neu `03-story-aufloesung` (2026-10-23 12:15, entwurf); neu `04-reel-mein-weg` (2026-10-27 18:30, wartet_auf_clips); neu `04-story-teaser` (2026-10-27 18:35, entwurf)
