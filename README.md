# maehrsteuern – Instagram

**Autopilot:** `automatik/plan.json` ist der Veröffentlichungsplan. GitHub Actions postet freigegebene Einträge zur geplanten Zeit (`.github/workflows/posten.yml`), holt täglich ca. 08:45 die Statistik (Tagesbericht in `LAGE.md`) verlängert monatlich den Instagram-Schlüssel, legt jeden Morgen ein Radar-Issue zum Kommentieren an und meldet neue Kommentare mit Antwortvorschlag (`strategie/12_interaktion.md`). Einrichtung: `EINRICHTUNG.md`.

**Überblick:** `LAGE.md` – was als Nächstes online geht, was du tun musst, Automatik-Status und Protokoll jeder Änderung. Wird automatisch nach jedem Push und jedem Automatik-Lauf neu geschrieben (`automatik/lage.py`, `.github/workflows/lage.yml`); Notizen dazu in `automatik/lage_notizen.md`.

**Kalender:** Direkt-Sync in den Google-Kalender „maehrsteuern Autopilot“ (`automatik/kalender_sync.py`, jeder Lage-Lauf): Postzeiten, offene Freigaben, von Hand posten, fehlende Clips/Musik – als „beschäftigt“ für Reclaim. Einrichtung: `EINRICHTUNG.md` Schritt 6.

Leitspruch: „Steuern × Code“ – KI ist Qualifikation und Werkzeug, Code ist der Unterschied: Lösungen, die wirklich laufen.

## Struktur (neu)
| Datei | Inhalt |
|---|---|
| `strategie/01_positionierung.md` | Kernsatz, Zielgruppen mit Rangfolge, 4 Content-Säulen, Formate, Kennzahlen |
| `strategie/02_bio_highlights.md` | Name, Bio, Kategorie, Link, Highlight-Reihe inkl. FAQ-Texte |
| `strategie/03_redaktionsplan.md` | Wochenrhythmus (1 Beitrag/Woche) und Plan Okt.–Nov. 2026 |
| `strategie/04_dm_strecke.md` | Nachrichten für „TOOL“ → Demo + Erstgespräch, Technik |
| `strategie/05_veroeffentlichung.md` | **Fahrplan mit Uhrzeiten, Anleitung zum Einplanen, Prüfliste** |
| `strategie/08_hooks.md` | Hook-Regeln, angepasste Auswahl nach 6 Bausteinen, Varianten für die geplanten Beiträge |
| `strategie/08_demo_reel_formel.md` | Aufbau für Demo-Reels (Schmerz → Schnitt → Höhepunkt → Aufruf) |
| `strategie/09_reel_regeln.md` | Reel-Regeln aus Feedback: Hook, KI-Clips, Ton, Safe-Zone, Farben |
| `strategie/10_software_reel_konzept.md` | Eigenes Reel-Konzept für Software (Split-Screen, Satisfying Software, Gesicht + Screen), Bildschirmaufnahmen |
| `strategie/11_wissen_instagram.md` | Gesammeltes Instagram-Wissen: Algorithmus-Signale, Teilen/Speichern, Suche, Serien, Saison, offene Entscheidungen |
| `strategie/13_backlog.md` | Backlog Automatisierung: umgesetzt, Sprint 2, zurückgestellt, abgelehnt |
| `strategie/linkedin/` | **LinkedIn-Strang (Aufbau):** `01_wissen_linkedin.md` (Algorithmus, Formate, Takt – Entwurf zum Prüfen), `02_erstanalyse_*.md` (Ausgangswerte), `03_profil.md` (Headline, Info, Erfahrung), `prompts/` (Prompts für Claude in Chrome, nur lesen/vorbereiten); Titelbild `assets/linkedin/` |
| `strategie/12_interaktion.md` | **Zweite Säule Interaktion:** Radar, DM-Entwürfe, Kommentar-Hilfe, Click-to-DM-Anzeige, Collabs, LinkedIn, Grenzen |
| `vorlagen/hooks/` | Hook-Bibliothek: zehn fertige Reel-Einstiege (1,8–2,8 s), Übersicht in `README.md` |
| `automatik/` | `plan.json` (Plan + Status), `posten.py`, `statistik.py`, `schluessel_verlaengern.py`, `statistik/*.csv` |
| `automatik/interaktion.json` | Einstellungen Radar/Kommentare (Konten, Hashtags, Grenzen); Stand in `automatik/interaktion/` |
| `automatik/wochenbericht.py` | Sonntags ein Issue „📊 Woche KW xx“ (Follower, Aufrufe, Top 3, Radar, Trichter); Nachtrag `demos 2` / `manychat 14/6` / `herkunft …`; Werte in `automatik/statistik/woche.csv` |
| `automatik/apps_script/demo_kopie.gs` | Apps-Script (läuft in Loris' Google-Konto): kopiert Reclaim-Demo-Buchungen ohne Namen/E-Mails in „maehrsteuern Autopilot“ – Quelle für den Wochenbericht |
| `automatik/kalender_sync.py` | Termine aus dem Plan direkt in den Google-Kalender „maehrsteuern Autopilot“ (Dienstkonto, nur dieser Kalender, idempotent) |
| `automatik/waechter.py` | Ein Issue „🚨 Wächter“ bei rotem Workflow oder Schlüssel < 14 Tage (Ablaufdaten in `schluessel_ablauf.json`) |
| `automatik/radar.py`, `kommentare.py`, `linkedin.py`, `ki.py` | Radar-Issue, Kommentar-Hilfe, LinkedIn-Pakete, gemeinsamer Claude-Zugang |
| `strategie/dm_tracking.csv` | Liste zum Nachverfolgen der Anfragen |
| `posts/<Nr>_<Datum>_<Thema>/` | fertige Beiträge: Folien bzw. Reel, Titelbild, Storys, `bildunterschrift.txt` |

## Vorlagen-System (`vorlagen/system/`)
- `karussell.html` (1080×1350; Typen `titel`, `inhalt` mit Text/Liste/Tabelle, `cta`), `story.html` (1080×1920; `info`, `frage`, `teaser`), `reel_titel.html`, `highlight.html` (`start`, `wissen`, `faq`), `einblendung.html` (Reel: `haken`, `leiste`, `abspann`), `ampel.html` (Ampel-Nahaufnahme `rot`/`gelb`/`gruen`, Stil der App)
- Farben und Schriften zentral in `basis.css`; `*Wort*` im Text wird grün, `\n` bricht um; zu lange Überschriften werden automatisch verkleinert
- Texte stehen in Job-Dateien unter `jobs/`. Bilder erzeugen: im Ordner `vorlagen/system` → `node render.mjs jobs/p02_excel_fehler.json`
- Reels aus Standbildern: Schnittliste in `schnitt/`, dann `python3 reel.py schnitt/p01_reel_ampel.json` (braucht `pip install pillow imageio-ffmpeg`)
- Ergebnisse landen in `posts/` bzw. `assets/` (`highlights/`, `storys/start/`)

## Marke
- Botschaft: **Steuern × Code** – „Steuerwissen, das rechnet.“ Diplom-Finanzwirt und KI-Manager (IHK), baut KI- und Steuer-Tools – vom Tool bis zum ganzen Prozess.
- Aufruf: **Schreib „TOOL“ per DM**
- Farben: Hintergrund `#0B110E` (Verlauf nach `#153A31`), Akzent Grün `#53C3A2`, Text `#EAF1EC`, Nebentext `#8FA398`
- Schriften: IBM Plex Serif (Überschriften), IBM Plex Sans (Text), IBM Plex Mono (Kicker, Handle) – eingebettet in `vorlagen/schriften.css`
- Stil: dunkel, grünes Leuchten, ruhig und hochwertig

## Profil (Stand)
- 9 Beiträge, 353 Follower; Reel „Mein eigenes Steuer-Tool“ angepinnt
- Bio: „Steuern × Code · Bereit für die Zukunft deines Workflows? · Schreib „TOOL“ per DM“
- Highlights: „Tools ⚙️“, „Feedbacks 🙏“ – Titelbilder in `assets/`

## Dateien
| Datei | Inhalt |
|---|---|
| `assets/maehrsteuern_Reel_15s.mp4` | fertiges Reel 9:16, 15 s, mit Musik |
| `assets/maehrsteuern_Reel_Titelbild.png` | Titelbild des Reels |
| `assets/maehrsteuern_Highlight_*.png` | Highlight-Symbole |
| `assets/app_9x16.png` | Dashboard-Screenshot (nur Demo-Daten) |
| `assets/ende_9x16.png` | Abspann-Karte |
| `assets/marke/*` | Marken-Bilder: Originale (Freisteller heute, KI-Porträt, KI-Avatar 2025) + 9:16-Karten im Markenstil (Hintergrund `#0B110E` → `#153A31`, Gesicht in der Safe-Zone) |
| `vorlagen/*.html` + `*.mjs` | Vorlagen; Bild erzeugen mit `node cover.mjs` usw. im Ordner `vorlagen` (Playwright, Chromium unter /opt/pw-browsers) |

## Regeln
- Keine echten Zahlen, Namen oder Logos vom Arbeitgeber, nur Demo-Daten; Arbeitgeber nie als Ort oder Marke markieren.
- Realistische KI-Personen im Video → KI-Label in Instagram einschalten.
- Schrift nie von der KI-Videoerzeugung schreiben lassen – Text als eigenes Bild vorgeben oder nachträglich einsetzen.
