# Autopilot einrichten (einmalig, ca. 30 Minuten)

## 1 · Repo anlegen (2 Min.)
1. https://github.com/new öffnen
2. Name: **instagram** · **Public** · *nichts* ankreuzen (kein README) → **Create repository**
3. Claude Zugriff geben: https://github.com/apps/claude/installations/select_target → **maehrsteuern** → unter *Repository access* das Repo **instagram** hinzufügen (falls dort „Only select repositories“ steht) → *Save*
4. Mir Bescheid sagen, dann lade ich alles hoch.

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
Repo **instagram** → **Settings → Secrets and variables → Actions → New repository secret**:

| Name | Wert |
|---|---|
| `IG_TOKEN` | der Zugriffsschlüssel |
| `IG_USER_ID` | die Instagram-Konto-ID |
| `GH_PAT` *(optional, empfohlen)* | ein GitHub-Schlüssel, damit der Instagram-Schlüssel sich selbst erneuert: https://github.com/settings/personal-access-tokens → *Generate new token* → Repository **instagram** → Berechtigung **Secrets: Read and write** |

Diese Werte sieht niemand, auch nicht im öffentlichen Repo. **Schick sie nie im Chat.**

## 4 · Testen (1 Min.)
Repo → **Actions → Instagram-Statistik → Run workflow**. Grüner Haken = Verbindung steht. Dieser Test liest nur und postet nichts.

## Wie es danach läuft
| Wann | Was passiert | Wer |
|---|---|---|
| **Mittwoch** | Ich baue den Beitrag für den übernächsten Dienstag, du bekommst eine Push-Nachricht mit Vorschau | Claude |
| bis Sonntag | Du schaust drüber und schreibst in der Sitzung **„freigeben“** oder was geändert werden soll | du |
| **Dienstag 18:30** | Beitrag geht automatisch online, 18:35 die Teaser-Story | Autopilot |
| Montag / Freitag 12:15 | Kalender-Erinnerung für die Sticker-Story, die du von Hand postest | du |
| **Montag früh** | Statistik wird abgeholt | Autopilot |
| **1. des Monats** | Monatsbericht mit Empfehlungen, Instagram-Schlüssel wird verlängert | Claude + Autopilot |

**Selbst freigeben ohne Claude:** In `automatik/plan.json` beim Eintrag `"status": "entwurf"` auf `"freigegeben"` ändern (am Handy: Datei öffnen → Stift → *Commit changes*).
**Notbremse:** Status auf `"pause"` setzen. Oder *Actions → Instagram posten → ⋯ → Disable workflow*.
**Fehler:** Wenn etwas schiefgeht, steht beim Eintrag `"status": "fehler"` mit Grund, und GitHub schickt dir eine Mail.
