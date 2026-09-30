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

## Wie es danach läuft
| Wann | Was passiert | Wer |
|---|---|---|
| **Mo + Do 08:47** | Content-Fabrik baut die nächsten Beiträge und trägt sie als Entwurf ein | Claude |
| direkt danach | GitHub öffnet je Beitrag ein **Freigabe-Issue** mit Vorschau (Bilder, Reel-Link, Text) | Autopilot |
| **Mo + Do 19:00** | Kalender-Erinnerung → im Issue **`go`** oder **`stop`** antworten | du |
| Di / Do / So 19:30, täglich 12:15 | Beiträge und Storys gehen automatisch online | Autopilot |
| **Montag früh** | Statistik wird abgeholt | Autopilot |
| **1. des Monats** | Monatsbericht, Instagram-Schlüssel wird verlängert (braucht `GH_PAT`) | Claude + Autopilot |

**Freigaben:** https://github.com/maehrsteuern/Instagram-maehrsteuern/issues?q=is%3Aopen+label%3Afreigabe
Nur deine eigenen Kommentare zählen. `go` = einplanen, `stop` = pausieren, alles andere wird ignoriert.
**Notbremse:** Actions → *Instagram posten* → ⋯ → *Disable workflow* (stoppt auch die Starts von cron-job.org).
**Fehler:** stehen in `automatik/plan.json` beim Eintrag (`"status": "fehler"`), GitHub schickt dir eine Mail.
**Probelauf:** Actions → *Instagram posten* → *Run workflow* → Feld „test“ = Eintrags-ID → lädt hoch, veröffentlicht nichts.
