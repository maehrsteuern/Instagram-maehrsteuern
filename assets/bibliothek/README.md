# Bibliothek – fertige Assets auf Vorrat

Aus dem Claude-Design-Katalog „maehrsteuern Brand Kit“ (Runden 1–7) übernommen und mit dem Vorlagen-System erzeugt. **Nichts davon ist im Plan** – die Content-Fabrik oder Loris nimmt sich hier Beiträge, kopiert sie nach `posts/<Nr>_<Datum>_<Thema>/` und trägt sie in `automatik/plan.json` ein.

**996 Bilder** in 142 Job-Dateien.

- **Alle Zahlen sind Demo-Werte.** Rechtsstand und Normen vor der Freigabe fachlich prüfen (Stand der Texte: Okt. 2026).
- Texte ändern: Job-Datei in `vorlagen/system/jobs/bibliothek/` anpassen, dann im Ordner `vorlagen/system` → `node render.mjs jobs/bibliothek/<datei>.json`. Danach optional verlustfrei verkleinern: `pip install pyoxipng` und `python3 -c "import oxipng,sys; [oxipng.optimize(f, level=3) for f in sys.argv[1:]]" <png …>`.
- `leiste_*.png` und `haken_ueber_*.png` sind transparent (Overlay fürs Reel).

| Ordner | Inhalt |
|---|---|
| `karussell/<serie>/folie_0N.png` | Karussells 1080×1350 |
| `storys/` | Storys 1080×1920 (Quiz + Auflösung, Umfragen, Teaser, Tipps, Zahl des Tages, FAQ) |
| `reels/<reel>/titelbild.png` | Reel-Titelbilder 1080×1920 |
| `bausteine/` | Reel-Einblendungen (haken, haken_ueber, leiste, abspann) und Ampel-Nahaufnahmen |
| `einzelposts/` | Einzelposts 1:1 „Zahl mit Norm“ 1080×1080 |
| `highlights/` | Highlight-Titelbilder |
| `linkedin/` | LinkedIn-Banner 1584×396 |

## Runde 1

| Job | Inhalt | Bilder | Dateien |
|---|---|---|---|
| `r1_01_vergleich_wege.json` | Karussell · Woche 6 · Praxis – „Excel vs. Standardsoftware vs. eigenes Tool“ | 7 | `karussell/vergleich_wege/` |
| `r1_02_jahresabschluss_7.json` | Karussell · Woche 7 · Wissen – „Jahresabschluss: 7 Steuer-Punkte“ | 4 | `karussell/jahresabschluss_7/` |
| `r1_03_themenspeicher.json` | Karussell · Themenspeicher – „Steuersatz-Staffel in Excel“ & „Was im Examen keiner sagt“ (Anfänge, Rest folgt) | 3 | `karussell/examen/`, `karussell/staffel/` |
| `r1_04_storys_faq.json` | Storys · Highlight „FAQ ❓“ (Texte aus 02_bio_highlights.md) | 4 | `storys/faq_1.png`, `storys/faq_2.png`, `storys/faq_3.png`, `storys/faq_4.png` |
| `r1_05_storys_woche_5_8.json` | Storys · Woche 5–8 (Frage, Umfrage, Teaser, Tipp) | 6 | `storys/` – w5_umfrage, w6_umfrage, w6_teaser, w7_frage, w8_umfrage, tipp_hebesatz_zelle |
| `r1_06_reel_titel.json` | Reel-Titelbilder (Text im mittleren 3:4-Bereich) | 3 | `reels/reel_pruefpfad/titelbild.png`, `reels/reel_excel_vs_tool/titelbild.png`, `reels/reel_abgestimmt/titelbild.png` |
| `r1_07_einblendungen_pruefpfad.json` | Reel-Einblendungen · W5 „Prüfpfad“ (haken, leiste, abspann) | 3 | `bausteine/haken_pruefpfad.png`, `bausteine/leiste_pruefpfad.png`, `bausteine/abspann_pruefpfad.png` |
| `r1_08_highlights.json` | Highlight-Titelbilder · neu: Demo, Termin, Ampel | 3 | `highlights/hl_demo.png`, `highlights/hl_termin.png`, `highlights/hl_ampel.png` |
| `r1_09_linkedin.json` | LinkedIn-Banner 1584×396 (links unten frei fürs Profilbild) | 1 | `linkedin/banner.png` |

## Runde 2

| Job | Inhalt | Bilder | Dateien |
|---|---|---|---|
| `r2_01_rueckstellung.json` | Karussell · Wissen – „Die Steuerrückstellung in 6 Schritten“ | 7 | `karussell/rueckstellung/` |
| `r2_02_gewst_zahlen.json` | Karussell · Wissen – „Gewerbesteuer in 5 Zahlen“ | 7 | `karussell/gewst_zahlen/` |
| `r2_03_verlustvortrag.json` | Karussell · Wissen – „Verluste 2026: 70 % oder 60 %?“ | 6 | `karussell/verlustvortrag/` |
| `r2_04_afa_degressiv.json` | Karussell · Wissen – „Die degressive AfA ist zurück“ | 5 | `karussell/afa_degressiv/` |
| `r2_05_solz.json` | Karussell · Wissen – „Warum 15,825 %?“ | 4 | `karussell/solz/` |
| `r2_06_vga.json` | Karussell · Wissen – „5 Klassiker der vGA“ | 7 | `karussell/vga/` |
| `r2_07_excel_formeln.json` | Karussell · Praxis – „5 Excel-Formeln für Steuerleute“ | 7 | `karussell/excel_formeln/` |
| `r2_08_ki_steuer.json` | Karussell · KI × Steuern – „5 Aufgaben, die KI heute schon übernimmt“ | 5 | `karussell/ki_steuer/` |
| `r2_09_so_entsteht.json` | Karussell · Hinter dem Code – „Von der Excel-Datei zum Tool“ | 7 | `karussell/so_entsteht/` |
| `r2_10_iab.json` | Karussell · Wissen – „Investitionsabzugsbetrag“ | 5 | `karussell/iab/` |
| `r2_11_storys_quiz_und_aufloesung.json` | Storys · Quiz und Auflösung | 8 | `storys/` – quiz_gewst_ba, quiz_gewst_ba_aufloesung, quiz_hebesatz, quiz_hebesatz_aufloesung, quiz_verlust, quiz_verlust_aufloesung, quiz_solz, quiz_solz_aufloesung |
| `r2_12_storys_fragen_und_umfragen.json` | Storys · Fragen und Umfragen | 8 | `storys/` – frage_gesellschaften, frage_pruefung, frage_ki, frage_hebesaetze, frage_naechstes, frage_blaetter, frage_freitag, frage_formel |
| `r2_13_storys_neuer_beitrag.json` | Storys · Teaser „Neuer Beitrag“ | 7 | `storys/` – teaser_rueckstellung, teaser_gewst, teaser_verlust, teaser_afa, teaser_vga, teaser_formeln, teaser_ki |
| `r2_14_storys_tipps_einblicke_begruessung.json` | Storys · Tipps, Einblicke, Begrüßung | 9 | `storys/` – tipp_umkehrjahr, tipp_hinzurechnung, tipp_vorauszahlung, tipp_namen, mythos_ki, einblick_ampel, dm_danke, willkommen, rueckblick_woche1 |
| `r2_15_reel_titel.json` | Reel-Titelbilder | 12 | `reels/reel_afa/`, `reels/reel_ampel_springt/`, `reels/reel_bezug/`, `reels/reel_formeln/`, `reels/reel_freitag/`, `reels/reel_hebesatz/`, `reels/reel_ki/`, `reels/reel_rueckstellung/`, `reels/reel_solz/`, `reels/reel_verlust/`, `reels/reel_vga/`, `reels/reel_weg/` – titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild |
| `r2_16_einblendungen.json` | Reel-Einblendungen (haken, haken_ueber, leiste, abspann) | 12 | `bausteine/` – haken_zeile4000, haken_von_hand, haken_17s, haken_freitag, haken_ueber_rot, haken_ueber_pruefpfad, leiste_einlesen, leiste_regeln, leiste_ampel, leiste_gebucht, abspann_rechnet, abspann_copy_paste |
| `r2_17_highlights.json` | Highlight-Titelbilder · Prüfpfad, Rechner, DM, Excel | 4 | `highlights/hl_pruefpfad.png`, `highlights/hl_rechner.png`, `highlights/hl_dm.png`, `highlights/hl_excel.png` |
| `r2_18_ampel.json` | Ampel-Nahaufnahmen · Gewerbesteuer-Hinzurechnung (Stil der App) | 3 | `bausteine/ampel_hinz_rot.png`, `bausteine/ampel_hinz_gelb.png`, `bausteine/ampel_hinz_gruen.png` |

## Runde 3

| Job | Inhalt | Bilder | Dateien |
|---|---|---|---|
| `r3_01_hinzurechnung.json` | Karussell · Wissen – „Hinzurechnung: vier Quoten, ein Freibetrag“ | 7 | `karussell/hinzurechnung/` |
| `r3_02_par8b.json` | Karussell · Wissen – „Dividenden unter GmbHs: 95 % steuerfrei“ | 6 | `karussell/par8b/` |
| `r3_03_zinsschranke.json` | Karussell · Wissen – „Die Zinsschranke in 60 Sekunden“ | 6 | `karussell/zinsschranke/` |
| `r3_04_organschaft.json` | Karussell · Wissen – „Organschaft: fünf Voraussetzungen“ | 7 | `karussell/organschaft/` |
| `r3_05_latente_basics.json` | Karussell · Wissen – „Latente Steuern: aktiv oder passiv?“ | 6 | `karussell/latente_basics/` |
| `r3_06_rst_steuerlich.json` | Karussell · Wissen – „Rückstellungen: Was das Finanzamt streicht“ | 6 | `karussell/rst_steuerlich/` |
| `r3_07_gwg.json` | Karussell · Wissen – „GWG oder Sammelposten?“ | 5 | `karussell/gwg/` |
| `r3_08_bewirtung.json` | Karussell · Wissen – „Geschäftsessen und Geschenke“ | 6 | `karussell/bewirtung/` |
| `r3_09_e_rechnung.json` | Karussell · Praxis – „E-Rechnung: der Fahrplan bis 2028“ | 6 | `karussell/e_rechnung/` |
| `r3_10_fristen_ao.json` | Karussell · Wissen – „Fristen und Zuschläge“ | 7 | `karussell/fristen_ao/` |
| `r3_11_aufbewahrung.json` | Karussell · Wissen – „Aufbewahrung: 8 Jahre statt 10“ | 5 | `karussell/aufbewahrung/` |
| `r3_12_mindeststeuer.json` | Karussell · Wissen – „Globale Mindeststeuer: 15 %“ | 6 | `karussell/mindeststeuer/` |
| `r3_13_forschungszulage.json` | Karussell · Wissen – „Forschungszulage“ | 6 | `karussell/forschungszulage/` |
| `r3_14_kst_staffel.json` | Karussell · Wissen – „Die KSt sinkt: 15 % → 10 %“ | 6 | `karussell/kst_staffel/` |
| `r3_15_mythen.json` | Karussell · Mythos oder Fakt – „6 Steuer-Irrtümer“ | 8 | `karussell/mythen/` |
| `r3_16_examen_praxis.json` | Karussell · Examen → Praxis – „4 Unterschiede“ | 6 | `karussell/examen_praxis/` |
| `r3_17_glossar_1.json` | Karussell · Glossar – „5 Begriffe für den Abschluss“ | 7 | `karussell/glossar_1/` |
| `r3_18_bp_vorbereitung.json` | Karussell · Praxis – „Betriebsprüfung: 4 Dinge vorab“ | 6 | `karussell/bp_vorbereitung/` |
| `r3_19_excel_suenden.json` | Karussell · Praxis – „Die 7 Todsünden der Steuer-Excel“ | 6 | `karussell/excel_suenden/` |
| `r3_20_kuerzungen.json` | Karussell · Wissen – „Kürzungen nach § 9 GewStG“ | 6 | `karussell/kuerzungen/` |
| `r3_21_einzelposts.json` | Einzelposts 1:1 · „Zahl mit Norm“ | 12 | `einzelposts/` – zahl_gesamtsatz, zahl_2032, zahl_gwg, zahl_geschenke, zahl_zinsschranke, zahl_mindeststeuer, zahl_zinsen, zahl_belege, zahl_kleinunternehmer, zahl_forschung, zahl_hebesatz, zahl_eav |
| `r3_22_storys_quiz_und_aufloesung.json` | Storys · Quiz und Auflösung (Runde 3) | 12 | `storys/` – quiz_geschenke, quiz_geschenke_aufloesung, quiz_gwg, quiz_gwg_aufloesung, quiz_belege, quiz_belege_aufloesung, quiz_zinsschranke, quiz_zinsschranke_aufloesung, quiz_saeumnis, quiz_saeumnis_aufloesung, quiz_einspruch, quiz_einspruch_aufloesung |
| `r3_23_storys_zahl_des_tages.json` | Storys · Zahl des Tages | 8 | `storys/` – zdt_zinsen, zdt_8b, zdt_ebitda, zdt_viertel, zdt_mindeststeuer, zdt_bekanntgabe, zdt_bewirtung, zdt_verspaetung |
| `r3_24_storys_fragen_und_tipps.json` | Storys · Fragen und Tipps (Runde 3) | 12 | `storys/` – frage_verfahrensdoku, frage_erechnung, frage_dateiname, frage_organschaft, frage_reel, frage_dauer, tipp_geschenke_konto, tipp_bewirtungsbeleg, tipp_schachtel, tipp_eav, tipp_instandhaltung, tipp_grundsteuerwert |
| `r3_25_reel_titel.json` | Reel-Titelbilder (Runde 3) | 15 | `reels/reel_8b/`, `reels/reel_aufbewahrung/`, `reels/reel_bewirtung/`, `reels/reel_erechnung/`, `reels/reel_gwg/`, `reels/reel_hinzurechnung/`, `reels/reel_kst2032/`, `reels/reel_mindeststeuer/`, `reels/reel_organschaft/`, `reels/reel_prompt/`, `reels/reel_rst_ampel/`, `reels/reel_suenden/`, `reels/reel_tag/`, `reels/reel_zinsschranke/`, `reels/reel_zuschlaege/` – titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild, titelbild |
| `r3_26_einblendungen.json` | Reel-Einblendungen (Runde 3) | 15 | `bausteine/` – haken_formel, haken_datenzugriff, haken_vorjahr, haken_8b, haken_final, haken_ueber_hinz, haken_ueber_gelb, haken_ueber_gruen, leiste_konten, leiste_quoten, leiste_freibetrag, leiste_hinz_fertig, leiste_norm, abspann_mehr_abschluss, abspann_quote |
| `r3_27_highlights.json` | Highlight-Titelbilder · Quiz, Paragraf, Code, Prozent | 4 | `highlights/hl_quiz.png`, `highlights/hl_paragraf.png`, `highlights/hl_code.png`, `highlights/hl_prozent.png` |
| `r3_28_ampel.json` | Ampel-Nahaufnahmen · Zinsschranke, Organschaft, Rückstellung | 6 | `bausteine/` – ampel_zins_rot, ampel_zins_gruen, ampel_organ_gelb, ampel_organ_gruen, ampel_rst_rot, ampel_rst_gruen |

## Runde 4

**Platzhalter – vor Verwendung ersetzen:** „312 Testfälle“ (`storys/einblick_test.png`, `reels/reel_tests/titelbild.png`, `bausteine/haken_ueber_test.png`) und die Beteiligungsquoten 48 %/62 % in `bausteine/ampel_8c_gelb.png` / `ampel_8c_rot.png` sind erfundene Demo-Werte.

| Job | Inhalt | Bilder | Dateien |
|---|---|---|---|
| `r4_01_ein_euro.json` | Karussell · Wissen – „Ein Euro Gewinn: Was bleibt?“ | 6 | `karussell/ein_euro/` |
| `r4_02_teileinkuenfte.json` | Karussell · Wissen – „Teileinkünfteverfahren: 60/40“ | 6 | `karussell/teileinkuenfte/` |
| `r4_03_holding.json` | Karussell · Wissen – „Holding: Warum 1,5 %?“ | 6 | `karussell/holding/` |
| `r4_04_thesaurierung.json` | Karussell · Wissen – „Thesaurierung nach § 34a EStG“ | 6 | `karussell/thesaurierung/` |
| `r4_05_betriebsaufspaltung.json` | Karussell · Wissen – „Betriebsaufspaltung“ | 6 | `karussell/betriebsaufspaltung/` |
| `r4_06_par8c.json` | Karussell · Wissen – „§ 8c KStG: Wann Verluste untergehen“ | 6 | `karussell/par8c/` |
| `r4_07_einlagekonto.json` | Karussell · Wissen – „Das steuerliche Einlagekonto“ | 6 | `karussell/einlagekonto/` |
| `r4_08_pension.json` | Karussell · Wissen – „Pensionsrückstellung: 6 % vs. HGB“ | 6 | `karussell/pension/` |
| `r4_09_teilwert.json` | Karussell · Wissen – „Teilwertabschreibung“ | 6 | `karussell/teilwert/` |
| `r4_10_reverse_charge.json` | Karussell · Umsatzsteuer – „Reverse-Charge: 5 Fälle“ | 6 | `karussell/reverse_charge/` |
| `r4_11_vorsteuer.json` | Karussell · Umsatzsteuer – „Vorsteuer: 4 Voraussetzungen“ | 7 | `karussell/vorsteuer/` |
| `r4_12_ust_va.json` | Karussell · Umsatzsteuer – „Voranmeldung: monatlich oder quartalsweise?“ | 6 | `karussell/ust_va/` |
| `r4_13_lohn_extras.json` | Karussell · Lohn – „Sieben steuerfreie Extras“ | 6 | `karussell/lohn_extras/` |
| `r4_14_homeoffice.json` | Karussell · Lohn – „Homeoffice und Arbeitszimmer“ | 6 | `karussell/homeoffice/` |
| `r4_15_erbst_bv.json` | Karussell · Wissen – „Unternehmensnachfolge: 85 % oder 100 %?“ | 6 | `karussell/erbst_bv/` |
| `r4_16_grest_share.json` | Karussell · Wissen – „Grunderwerbsteuer bei Share Deals“ | 5 | `karussell/grest_share/` |
| `r4_17_paragraf_formel.json` | Karussell · Praxis – „Wenn Paragrafen Excel-Formeln wären“ | 7 | `karussell/paragraf_formel/` |
| `r4_18_steuerkalender.json` | Karussell · Praxis – „Der Steuerkalender: Q4“ | 6 | `karussell/steuerkalender/` |
| `r4_19_gobd.json` | Karussell · Praxis – „GoBD in fünf Wörtern“ | 7 | `karussell/gobd/` |
| `r4_20_mythen_2.json` | Karussell · Mythos oder Fakt – Teil 2 | 8 | `karussell/mythen_2/` |
| `r4_21_glossar_2.json` | Karussell · Glossar – Teil 2 | 7 | `karussell/glossar_2/` |
| `r4_22_einzelposts.json` | Einzelposts 1:1 · „Zahl mit Norm“ (Runde 4) | 15 | `einzelposts/` – zahl_48, zahl_holding, zahl_34a, zahl_teileinkuenfte, zahl_pension, zahl_8c, zahl_ust_va, zahl_ist, zahl_kleinbetrag, zahl_betriebsfeier, zahl_homeoffice, zahl_verschonung, zahl_share_deal, zahl_stundung, zahl_reverse |
| `r4_23_storys_quiz_und_aufloesung.json` | Storys · Quiz und Auflösung (Runde 4) | 12 | `storys/` – quiz_euro, quiz_euro_aufloesung, quiz_holding, quiz_holding_aufloesung, quiz_sachbezug, quiz_sachbezug_aufloesung, quiz_pension, quiz_pension_aufloesung, quiz_ust, quiz_ust_aufloesung, quiz_8c, quiz_8c_aufloesung |
| `r4_24_storys_zahl_des_tages.json` | Storys · Zahl des Tages (Runde 4) | 8 | `storys/` – zdt_34a, zdt_pension, zdt_sachbezug, zdt_ehegatte, zdt_10tage, zdt_kleinbetrag, zdt_einlage, zdt_lohnsumme |
| `r4_25_storys_fragen_tipps_einblicke.json` | Storys · Fragen, Tipps, Einblicke (Runde 4) | 13 | `storys/` – frage_holding, frage_rc, frage_nachfolge, frage_glossar, frage_einlage, frage_extras, tipp_rc_hinweis, tipp_einlage_bescheinigung, tipp_option, tipp_freigrenze, tipp_adv, einblick_formel, einblick_test |
| `r4_26_reel_titel.json` | Reel-Titelbilder (Runde 4) | 14 | `reels/reel_ein_euro/`, `reels/reel_holding/`, `reels/reel_34a/`, `reels/reel_betriebsaufspaltung/`, `reels/reel_8c/`, `reels/reel_rc/`, `reels/reel_rechnung/`, `reels/reel_extras/`, `reels/reel_homeoffice/`, `reels/reel_nachfolge/`, `reels/reel_paragraf_formel/`, `reels/reel_gobd/`, `reels/reel_tests/`, `reels/reel_mythen2/` |
| `r4_27_einblendungen.json` | Reel-Einblendungen (Runde 4) | 14 | `bausteine/` – haken_52cent, haken_miete, haken_51, haken_rechnung, haken_test, haken_ueber_rc, haken_ueber_einlage, haken_ueber_test, leiste_rechnung_lesen, leiste_pflicht, leiste_13b, leiste_vorsteuer, abspann_paragraf, abspann_getestet |
| `r4_28_highlights.json` | Highlight-Titelbilder · Euro, Summe, Formel, USt | 4 | `highlights/hl_euro.png`, `highlights/hl_summe.png`, `highlights/hl_formel.png`, `highlights/hl_ust.png` |
| `r4_29_ampel.json` | Ampel-Nahaufnahmen · Vorsteuer, § 8c, Pensionen | 6 | `bausteine/` – ampel_vst_rot, ampel_vst_gruen, ampel_8c_gelb, ampel_8c_rot, ampel_pension_gelb, ampel_pension_gruen |

## Runde 7 · MAEHR Business Suite (MBS)

Reels 9:16 für die MBS (Stand: Beta/Demo). Aufruf überall „Demo buchen“ (Caption: https://app.reclaim.ai/m/maehrsteuern/demo). Der Abspann nutzt das neue optionale Feld `chip` in `einblendung.html` (Standard bleibt „Schreib TOOL per DM“).

| Job | Inhalt | Bilder | Ordner |
|---|---|---|---|
| `r7_01_mbs_reel_titel.json` | Titelbilder, ein Modul je Reel | 10 | `reels/mbs_*/` |
| `r7_02_mbs_einblendungen.json` | Wiederverwendbare Einblendungen (Haken, Ampel, Import-Leiste, Abspann) | 4 | `bausteine/mbs_*` |

## Runde 5

Keine erfundenen Werte – alle Zahlen sind Gesetzeswerte (Stand Okt. 2026). Vor Freigabe fachlich gegenlesen, besonders: E-Auto-Preisgrenze 100.000 € (Anschaffung ab 1.7.2025), Gastronomie 7 % ab 2026, Entfernungspauschale 0,38 € ab 2026, Minijob 603 €. RAP-Grenze im Design (1.000 €) auf 5.000 € korrigiert – siehe Prüfbericht.

| Job | Inhalt | Bilder | Dateien |
|---|---|---|---|
| `r5_01_kleinunternehmer.json` | Karussell · Umsatzsteuer – „Kleinunternehmer seit 2025“ | 6 | `karussell/kleinunternehmer/` |
| `r5_02_firmenwagen.json` | Karussell · Lohn – „Firmenwagen: 1 % oder Fahrtenbuch?“ | 7 | `karussell/firmenwagen/` |
| `r5_03_gebaeude_afa.json` | Karussell · Wissen – „Gebäude-AfA: 2, 3 oder 5 %?“ | 6 | `karussell/gebaeude_afa/` |
| `r5_04_par35.json` | Karussell · Wissen – „Gewerbesteuer-Anrechnung § 35 EStG“ | 6 | `karussell/par35/` |
| `r5_05_ausschuettung.json` | Karussell · Wissen – „GmbH-Ausschüttung: der Ablauf“ | 6 | `karussell/ausschuettung/` |
| `r5_06_ust_saetze.json` | Karussell · Umsatzsteuer – „7 % oder 19 %?“ | 7 | `karussell/ust_saetze/` |
| `r5_07_ig_lieferung.json` | Karussell · Umsatzsteuer – „Innergemeinschaftliche Lieferung“ | 6 | `karussell/ig_lieferung/` |
| `r5_08_dauerfrist.json` | Karussell · Umsatzsteuer – „Dauerfristverlängerung“ | 6 | `karussell/dauerfrist/` |
| `r5_09_minijob.json` | Karussell · Lohn – „Minijob 2026“ | 7 | `karussell/minijob/` |
| `r5_10_reisekosten.json` | Karussell · Lohn – „Reisekosten 2026“ | 6 | `karussell/reisekosten/` |
| `r5_11_schenkung.json` | Karussell · Wissen – „Schenkung: Freibeträge“ | 7 | `karussell/schenkung/` |
| `r5_12_par23.json` | Karussell · Wissen – „Private Veräußerung § 23 EStG“ | 7 | `karussell/par23/` |
| `r5_13_par17.json` | Karussell · Wissen – „Anteile verkaufen § 17 EStG“ | 6 | `karussell/par17/` |
| `r5_14_buchfuehrung.json` | Karussell · Wissen – „EÜR oder Bilanz?“ | 6 | `karussell/buchfuehrung/` |
| `r5_15_rap.json` | Karussell · Wissen – „Rechnungsabgrenzung“ | 6 | `karussell/rap/` |
| `r5_16_zufluss.json` | Karussell · Wissen – „Zufluss und Abfluss“ | 6 | `karussell/zufluss/` |
| `r5_17_excel_checks.json` | Karussell · Praxis – „Fünf Plausi-Checks für den Abschluss“ | 7 | `karussell/excel_checks/` |
| `r5_18_mythen_3.json` | Karussell · Mythos oder Fakt – „Teil 3“ | 7 | `karussell/mythen_3/` |
| `r5_19_glossar_3.json` | Karussell · Glossar – „Teil 3“ | 7 | `karussell/glossar_3/` |
| `r5_20_einzelposts.json` | Einzelposts 1:1 · „Zahl mit Norm“ (Runde 5) | 15 | `einzelposts/` – zahl_kleinunternehmer_2025, zahl_firmenwagen, zahl_e_auto, zahl_gebaeude, zahl_35, zahl_gewst_freibetrag, zahl_sondervz, zahl_zm, zahl_minijob, zahl_verpflegung, zahl_pendler, zahl_kinder, zahl_23_freigrenze, zahl_17, zahl_rap |
| `r5_21_storys_quiz_und_aufloesung.json` | Storys · Quiz und Auflösung (Runde 5) | 12 | `storys/` – quiz_kleinunternehmer, quiz_kleinunternehmer_aufloesung, quiz_arbeitsweg, quiz_arbeitsweg_aufloesung, quiz_enkel, quiz_enkel_aufloesung, quiz_vermietet, quiz_vermietet_aufloesung, quiz_minijob, quiz_minijob_aufloesung, quiz_schnitzel, quiz_schnitzel_aufloesung |
| `r5_22_storys_zahl_des_tages.json` | Storys · Zahl des Tages (Runde 5) | 10 | `storys/` – zdt_25000, zdt_e_auto, zdt_gebaeude, zdt_35, zdt_elftel, zdt_zm, zdt_verpflegung, zdt_038, zdt_20000, zdt_80000 |
| `r5_23_storys_fragen_und_tipps.json` | Storys · Fragen und Tipps (Runde 5) | 12 | `storys/` – frage_firmenwagen, frage_kleinunternehmer, frage_minijob, frage_dauerfrist, frage_reise, frage_mythen, tipp_fahrtenbuch, tipp_zm, tipp_ig_rechnung, tipp_entfernung, tipp_rap, tipp_zufluss |
| `r5_24_reel_titel.json` | Reel-Titelbilder (Runde 5) | 10 | `reels/reel_kleinunternehmer/`, `reels/reel_firmenwagen/`, `reels/reel_gebaeude/`, `reels/reel_35/`, `reels/reel_gastro/`, `reels/reel_minijob/`, `reels/reel_reise/`, `reels/reel_schenkung/`, `reels/reel_23/`, `reels/reel_plausi/` |
| `r5_25_einblendungen.json` | Reel-Einblendungen (Runde 5) | 10 | `bausteine/` – haken_kleinunternehmer, haken_fahrtenbuch, haken_schnitzel, haken_enkel, haken_ueber_zm, haken_ueber_plausi, leiste_susa, leiste_vorjahr, abspann_plausi, abspann_ust |
| `r5_26_highlights.json` | Highlight-Titelbilder · km, EU, Lohn, AfA, Kfz | 5 | `highlights/` – hl_km, hl_eu, hl_lohn, hl_afa, hl_kfz |
| `r5_27_ampel.json` | Ampel-Nahaufnahmen · EU-Lieferung, Kleinunternehmer | 4 | `bausteine/` – ampel_ig_rot, ampel_ig_gruen, ampel_ku_gelb, ampel_ku_gruen |

## Runde 6

Alle Zahlen sind Gesetzeswerte (Stand Okt. 2026), keine Platzhalter. Vor Freigabe gegenlesen, besonders: Grundwerte 2026 (12.348 € / 3.414 € / 259 €), Belegaufbewahrung 8 Jahre, Bekanntgabe 4 Tage, Mindestbesteuerung 70 % (2024–2027).

Umbenannt gegenüber dem Design, damit nichts aus Runden 2–4 überschrieben wird: Ordner `homeoffice_2`, `iab_2`, `verlustvortrag_2`, `aufbewahrung_2`, `reels/reel_homeoffice_tag/`; Dateien `zahl_homeoffice_tag`, `zahl_ist_2026`, `zahl_belege_8`, `quiz_rechnungen(_aufloesung)`, `frage_glossar_5`.

| Job | Inhalt | Bilder | Ordner |
|---|---|---|---|
| `r6_01_kapitalertraege.json` | Karussell · Wissen – „Kapitalerträge: fünf Regeln“ | 7 | `karussell/kapitalertraege/` |
| `r6_02_vermietung.json` | Karussell · Wissen – „Vermietung: fünf Grenzen“ | 7 | `karussell/vermietung/` |
| `r6_03_grundwerte_2026.json` | Karussell · Wissen – „Die Grundwerte 2026“ | 6 | `karussell/grundwerte_2026/` |
| `r6_04_spenden.json` | Karussell · Wissen – „Spenden richtig absetzen“ | 6 | `karussell/spenden/` |
| `r6_05_handwerker_35a.json` | Karussell · Wissen – „Handwerker und Haushalt“ | 7 | `karussell/handwerker_35a/` |
| `r6_06_werbungskosten.json` | Karussell · Lohn – „Werbungskosten für Arbeitnehmer“ | 6 | `karussell/werbungskosten/` |
| `r6_07_homeoffice.json` | Karussell · Lohn – „Homeoffice und Arbeitszimmer“ | 6 | `karussell/homeoffice_2/` |
| `r6_08_gewst_zerlegung.json` | Karussell · Wissen – „Gewerbesteuer-Zerlegung“ | 6 | `karussell/gewst_zerlegung/` |
| `r6_09_leistungsort.json` | Karussell · Umsatzsteuer – „Wo ist die Leistung steuerbar?“ | 7 | `karussell/leistungsort/` |
| `r6_10_oss.json` | Karussell · Umsatzsteuer – „One-Stop-Shop“ | 6 | `karussell/oss/` |
| `r6_11_par14c.json` | Karussell · Umsatzsteuer – „Falsche Steuer auf der Rechnung“ | 6 | `karussell/par14c/` |
| `r6_12_bauleistungen.json` | Karussell · Umsatzsteuer – „Reverse-Charge am Bau“ | 6 | `karussell/bauleistungen/` |
| `r6_13_istversteuerung.json` | Karussell · Umsatzsteuer – „Ist- oder Sollversteuerung“ | 6 | `karussell/istversteuerung/` |
| `r6_14_iab.json` | Karussell · Wissen – „Investitionsabzugsbetrag“ | 7 | `karussell/iab_2/` |
| `r6_15_verlustvortrag.json` | Karussell · Wissen – „Verluste richtig nutzen“ | 6 | `karussell/verlustvortrag_2/` |
| `r6_16_saeumnis.json` | Karussell · Wissen – „Zinsen und Säumniszuschläge“ | 6 | `karussell/saeumnis/` |
| `r6_17_einspruch.json` | Karussell · Wissen – „Einspruch einlegen“ | 6 | `karussell/einspruch/` |
| `r6_18_verjaehrung.json` | Karussell · Wissen – „Festsetzungsverjährung“ | 6 | `karussell/verjaehrung/` |
| `r6_19_aufbewahrung.json` | Karussell · Praxis – „Aufbewahrungsfristen“ | 6 | `karussell/aufbewahrung_2/` |
| `r6_20_mythen_4.json` | Karussell · Mythos oder Fakt – „Teil 4“ | 7 | `karussell/mythen_4/` |
| `r6_21_glossar_4.json` | Karussell · Glossar – „Teil 4“ | 7 | `karussell/glossar_4/` |
| `r6_22_einzelposts.json` | Einzelposts 1:1 · „Zahl mit Norm“ (Runde 6) | 15 | `einzelposts/` |
| `r6_23_storys_quiz_und_aufloesung.json` | Storys · Quiz und Auflösung (Runde 6) | 10 | `storys/` |
| `r6_24_storys_zahl_des_tages.json` | Storys · Zahl des Tages (Runde 6) | 12 | `storys/` |
| `r6_25_storys_fragen_und_tipps.json` | Storys · Fragen und Tipps (Runde 6) | 10 | `storys/` |
| `r6_26_reel_titel.json` | Reel-Titelbilder (Runde 6) | 8 | `reels/reel_homeoffice_tag/ u. a.` |
| `r6_27_einblendungen.json` | Reel-Einblendungen (Runde 6) | 7 | `bausteine/` |
| `r6_28_highlights.json` | Highlight-Titelbilder · AO, Kap, V+V | 3 | `highlights/` |
| `r6_29_ampel.json` | Ampel-Nahaufnahmen · Bescheidprüfung | 2 | `bausteine/` |
