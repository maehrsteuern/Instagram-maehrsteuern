# Autopilot einrichten (einmalig, ca. 30 Minuten)

## 1 · Repo ✅ erledigt
https://github.com/maehrsteuern/Instagram-maehrsteuern (öffentlich)

## 2 · Instagram-Schnittstelle freischalten (ca. 15 Min.)
Dein Konto ist schon professionell, das ist die Voraussetzung.
1. https://developers.facebook.com → mit Facebook anmelden → einmalig als Entwickler registrieren
2. **Meine Apps → App erstellen**
   - Anwendungsfall: **„Nachrichten und Inhalte auf Instagram verwalten“**
   - App-Name: `maehrsteuern Autopilot` → kein Business-Portfolio nötig → *App erstellen*
3. Links **Anwendungsfälle** → Instagram-API → **Anpassen** → **API-Einrichtung mit Instagram-Login**
4. Bei **„Zugriffstoken generieren“** → *Konto hinzufügen* → mit **@maehrsteuern** anmelden → alle Berechtigungen erlauben
   - Falls eine Tester-Einladung verlangt wird: *App-Rollen → Rollen → Instagram-Tester hinzufügen* → dann in der Instagram-App *Einstellungen → Website-Berechtigungen → Apps und Websites → Tester-Einladungen* → annehmen
5. Du siehst jetzt zwei Werte – **beide kopieren**:
   - den **Zugriffsschlüssel** (langer Text, beginnt oft mit `IG…`)
   - die **Instagram-Konto-ID** (eine lange Zahl)

Die App bleibt im Entwicklungsmodus. Für dein eigenes Konto reicht das, eine Prüfung durch Meta ist nicht nötig.

## 3 · Werte sicher bei GitHub hinterlegen (3 Min.)
Repo **Instagram-maehrsteuern** → **Settings → Secrets and variables → Actions → New repository secret**:

| Name | Wert |
|---|---|
| `IG_TOKEN` | der Zugriffsschlüssel |
| `IG_USER_ID` | die Instagram-Konto-ID |
| `GH_PAT` *(optional, empfohlen)* | ein GitHub-Schlüssel, damit der Instagram-Schlüssel sich selbst erneuert: https://github.com/settings/personal-access-tokens → *Generate new token* → Repository **Instagram-maehrsteuern** → Berechtigung **Secrets: Read and write** |

Diese Werte sieht niemand, auch nicht im öffentlichen Repo. **Schick sie nie im Chat.**

## 4 · Testen (1 Min.)
Repo → **Actions → Instagram-Statistik → Run workflow**. Grüner Haken = Verbindung steht. Dieser Test liest nur und postet nichts.

## 5 · Zuverlässiger Takt für das Posten (10 Min., dringend empfohlen)
GitHub führt Zeitpläne (`schedule`) bei kleinen Repos oft verspätet oder gar nicht aus – am 30.09. lief „Instagram posten“ ab 09:30 nicht mehr, die Start-Storys mussten von Hand angestoßen werden. Ein externer Taktgeber startet den Lauf deshalb zusätzlich alle 15 Minuten. Doppelte Starts schaden nicht: Läufe warten aufeinander, und gepostet wird nur, was `freigegeben` und fällig ist.

**a) Eigenen GitHub-Schlüssel nur dafür anlegen** (nicht `GH_PAT` wiederverwenden – der darf Secrets ändern)
1. https://github.com/settings/personal-access-tokens → **Generate new token** (fine-grained)
2. Name `cron-posten`, Ablauf **1 Jahr** (Kalender-Erinnerung zum Erneuern setzen)
3. Repository access: **Only select repositories → Instagram-maehrsteuern**
4. Permissions → Repository permissions → **Actions: Read and write** (sonst nichts)
5. *Generate token* → Schlüssel kopieren (beginnt mit `github_pat_…`) – **nicht im Chat schicken**

**b) Takt bei cron-job.org einrichten**
1. https://cron-job.org → kostenlos registrieren → **Create cronjob**
2. Title `Instagram posten`, URL:
   `https://api.github.com/repos/maehrsteuern/Instagram-maehrsteuern/actions/workflows/posten.yml/dispatches`
3. Execution schedule: **Every 15 minutes**
4. Reiter **Advanced**:
   - Request method: **POST**
   - Headers:
     | Key | Value |
     |---|---|
     | `Authorization` | `Bearer github_pat_…` (dein Schlüssel aus a) |
     | `Accept` | `application/vnd.github+json` |
     | `X-GitHub-Api-Version` | `2022-11-28` |
     | `User-Agent` | `cron-job-maehrsteuern` |
   - Request body: `{"ref":"claude/instagram"}`
5. Speichern → **Test run**: Antwort **204** = passt. Unter Actions → *Instagram posten* erscheint ein neuer Lauf „workflow_dispatch“.

✅ Eingerichtet am 30.09.2026 (Schlüssel gültig bis 29.09.2027). Die API-Version `2022-11-28` gilt laut GitHub noch bis März 2028 – vorher im Header auf eine neuere Version umstellen.

Bei Fehlern: 401 = Schlüssel falsch/abgelaufen · 403/404 = Berechtigung „Actions: Read and write“ oder Repo-Auswahl fehlt · 422 = Body/Branch falsch.

## 6 · Instagram-Plan im Google Kalender ✅ eingerichtet (03.10.)
Direkt-Sync statt Abo: Jeder Lage-Lauf (alle 15 Min.) schreibt die Termine aus dem Plan in den Google-Kalender **„maehrsteuern Autopilot“** (`automatik/kalender_sync.py`). Termine sind „beschäftigt“ → Reclaim legt keine Demo darauf.
- Zugang: Google-Cloud-Projekt `maehrsteuern-autopilot` (nur Calendar API, keine Abrechnung), Dienstkonto `kalender-sync@…` ohne Projekt-Rollen, nur dieser eine Kalender ist mit ihm geteilt („Änderungen an Terminen vornehmen“). Scope im Code: nur `calendar.events`.
- Secrets: `GOOGLE_SA_KEY` (Dienstkonto-JSON), `GOOGLE_CALENDAR_ID`.
- Der Sync fasst nur eigene Termine an (Markierung `maehrsteuern=1`), feste Event-IDs → kein Doppeln.
- **Zugang sperren:** Google Cloud → Dienstkonten → kalender-sync → Schlüssel löschen, oder Freigabe im Kalender entfernen.
- `kalender.ics` wird weiter erzeugt (Fallback zum Abonnieren per URL `https://raw.githubusercontent.com/maehrsteuern/Instagram-maehrsteuern/claude/instagram/kalender.ics`); kann entfallen, wenn der Sync zuverlässig läuft.

## 7 · Interaktion: Radar, Kommentar-Hilfe, LinkedIn (ca. 25 Min.)
Erklärung: `strategie/12_interaktion.md`. Alles läuft auch ohne diesen Schritt weiter, nur ohne Radar und Vorschläge.

**a) Claude-Schlüssel (für Kommentar- und DM-Vorschläge, ca. 2–5 €/Monat)**
https://console.anthropic.com → *Billing* 10 € aufladen, Limit 10 €/Monat setzen → *API Keys → Create Key* → Secret `ANTHROPIC_API_KEY`.

**b) Facebook-Zugang (nur für den Radar – fremde Profile lesen)**
Die bisherige Instagram-Schnittstelle kann keine fremden Profile lesen. Dafür braucht es den Weg über eine Facebook-Seite:
1. Facebook-Seite „maehrsteuern“ anlegen (falls noch keine da ist) und in der Instagram-App verbinden: *Profil bearbeiten → Seite → verbinden*.
2. developers.facebook.com → deine App `maehrsteuern Autopilot` → *Anwendungsfall hinzufügen* → **„Alles auf deiner Seite verwalten“** (oder „Instagram-API mit Facebook-Login“).
3. *Tools → Graph API Explorer* → oben deine App wählen → *Berechtigungen*: `instagram_basic`, `pages_show_list`, `pages_read_engagement`, `business_management` → **Generate Access Token** → mit Facebook bestätigen.
4. Im Explorer abfragen: `me/accounts?fields=instagram_business_account` → die Zahl bei `instagram_business_account.id` kopieren → Secret **`FB_IG_USER_ID`**.
5. Schlüssel langlebig machen: *Tools → Zugriffsschlüssel-Debugger* → Schlüssel einfügen → **„Zugriffsschlüssel verlängern“** → neuen Schlüssel kopieren → Secret **`FB_TOKEN`** (gilt 60 Tage).
6. Damit er sich selbst verlängert: *App-Einstellungen → Allgemeines* → **App-ID** → Secret `FB_APP_ID`, **App-Geheimcode** → Secret `FB_APP_SECRET` (braucht `GH_PAT` aus Schritt 3).
7. Konten eintragen: 20–40 Instagram-Namen in `automatik/interaktion.json` → `radar.konten` (oder Claude schicken).

**c) Testen:** Actions → *Radar* → *Run workflow*. Danach liegt ein Issue „📡 Radar …“ da. Actions → *Kommentare* → *Run workflow* legt beim ersten neuen Kommentar das Issue „💬 Kommentare beantworten“ an.

**ManyChat** beantwortet Kommentare mit „TOOL“ und alle DMs. Die Skripte hier schicken nie eine DM.

## Wie es danach läuft
| Wann | Was passiert | Wer |
|---|---|---|
| **Mo + Do 08:47** | Content-Fabrik baut die nächsten Beiträge und trägt sie als Entwurf ein | Claude |
| direkt danach | GitHub öffnet je Beitrag ein **Freigabe-Issue** mit Vorschau (Bilder, Reel-Link, Text) | Autopilot |
| **Mo + Do 19:00** | Kalender-Erinnerung → im Issue **`go`** oder **`stop`** antworten | du |
| Di / Do / So 19:30, täglich 12:15 | Beiträge und Storys gehen automatisch online | Autopilot |
| **täglich ca. 08:45** | Statistik wird abgeholt, Tagesbericht in `LAGE.md` | Autopilot |
| **täglich ca. 07:00** | Radar-Issue: Beiträge zum Kommentieren, DM-Entwürfe, montags Collab; LinkedIn-Pakete für neue Karussells | Autopilot + du (15 Min.) |
| alle 15 Min. | neue Kommentare mit Antwortvorschlag ins Issue „💬 Kommentare“ – `K12 ok` postet die Antwort | Autopilot + du |
| **1. des Monats** | Monatsbericht, Instagram-Schlüssel wird verlängert (braucht `GH_PAT`) | Claude + Autopilot |

**Freigaben:** https://github.com/maehrsteuern/Instagram-maehrsteuern/issues?q=is%3Aopen+label%3Afreigabe
Nur deine eigenen Kommentare zählen. `go` = einplanen, `stop` = pausieren, alles andere wird ignoriert.
**Notbremse:** Actions → *Instagram posten* → ⋯ → *Disable workflow* (stoppt auch die Starts von cron-job.org).
**Fehler:** stehen in `automatik/plan.json` beim Eintrag (`"status": "fehler"`), GitHub schickt dir eine Mail.
**Probelauf:** Actions → *Instagram posten* → *Run workflow* → Feld „test“ = Eintrags-ID → lädt hoch, veröffentlicht nichts.
