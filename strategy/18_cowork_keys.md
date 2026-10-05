# 18 · Cowork prompt – fix the keys once (IG_USER_ID, self-refresh, expiry dates)

Paste the block below into a **Claude Cowork** session with Claude in Chrome (logged in to Facebook/Meta for Developers and GitHub as Loris). Written in German because Loris runs it. Background: the stats found that the secret `IG_USER_ID` holds an ID that does not belong to @maehrtax (the scripts work around it by reading the ID from the token, but every run logs a warning), and `FB_TOKEN` was a short-lived token until 10/5.

```text
Moin! Wir bringen einmal alle Schlüssel für die Instagram-Automatik von @maehrtax in Ordnung.
Repo: https://github.com/maehrsteuern/maehrtax---instagram (Secrets: Settings → Secrets and variables → Actions).
Meta-App: „maehrsteuern Autopilot“ auf developers.facebook.com. Mit mir redest du Deutsch.
Arbeite die Schritte 1–5 der Reihe nach ab und frag vor jedem Schritt kurz: „Schritt X starten?“

══════════ GRUNDREGELN ══════════
- Login, 2-Faktor, Passwort-Abfragen: STOPP – das mache ich.
- Schlüssel/Tokens (IG_TOKEN, FB_TOKEN, App-Secret, GitHub-Tokens) NIE in den Chat schreiben, nicht vorlesen,
  nicht in Notizen ablegen. Wenn einer angezeigt wird: STOPP, ich kopiere ihn selbst ins Secret.
- Die Instagram-Konto-ID und die App-ID sind keine Geheimnisse – die darfst du kopieren und eintragen.
- Nichts löschen, keine App-Einstellungen ändern, keine Berechtigungen entfernen, nichts bei Meta zur Prüfung einreichen.
- Nichts am deutschen Repo Instagram-maehrsteuern oder am Konto @maehrsteuern ändern.

══════════ SCHRITT 1 – Richtige Instagram-Konto-ID → Secret IG_USER_ID ══════════
1. developers.facebook.com/apps → „maehrsteuern Autopilot“ → Anwendungsfälle → Instagram-API → Anpassen →
   „API-Einrichtung mit Instagram-Login“ → Abschnitt „Zugriffstoken generieren“.
2. Dort steht das Konto @maehrtax mit einer langen Zahl daneben – die Instagram-Konto-ID (nicht die ID der
   Facebook-Seite, nicht die App-ID). Wenn mehrere Konten gelistet sind: nur die Zahl in der Zeile @maehrtax.
3. GitHub-Repo → Settings → Secrets and variables → Actions → IG_USER_ID → „Update“ → diese Zahl eintragen → speichern.
   (Den Token-Button daneben NICHT drücken – IG_TOKEN funktioniert schon.)
Bericht: ID gefunden in Zeile @maehrtax ja/nein · IG_USER_ID aktualisiert ja/nein.

══════════ SCHRITT 2 – Selbst-Verlängerung: FB_APP_ID, FB_APP_SECRET, GH_PAT prüfen ══════════
1. GitHub → Settings → Secrets and variables → Actions: Liste der Secret-NAMEN ansehen (Werte sieht man nicht).
   Notiere, welche dieser Namen existieren: IG_TOKEN, IG_USER_ID, GH_PAT, FB_TOKEN, FB_IG_USER_ID, FB_APP_ID,
   FB_APP_SECRET, ANTHROPIC_API_KEY, GOOGLE_SA_KEY, GOOGLE_CALENDAR_ID.
2. Fehlt FB_APP_ID: developers.facebook.com → App → App-Einstellungen → Allgemeines → „App-ID“ kopieren →
   neues Secret FB_APP_ID anlegen.
3. Fehlt FB_APP_SECRET: auf derselben Seite „App-Geheimcode“ → „Anzeigen“ → STOPP. Ich kopiere ihn selbst ins
   neue Secret FB_APP_SECRET. Du wartest, bis ich „erledigt“ sage.
4. Fehlt GH_PAT: STOPP und mir sagen – den lege ich selbst an (SETUP.md, Tabelle der Secrets: fine-grained Token,
   nur Repo maehrtax---instagram, Berechtigung „Secrets: Read and write“).
Bericht: vorhandene Secret-Namen · FB_APP_ID neu ja/nein · FB_APP_SECRET (von mir) ja/nein · GH_PAT vorhanden ja/nein.

══════════ SCHRITT 3 – Ablaufdaten der Schlüssel ablesen ══════════
Ich öffne dafür die Schlüssel – du liest NUR die Datumszeilen ab, nicht den Schlüssel selbst.
1. developers.facebook.com/tools/debug/accesstoken öffnen. Ich füge den aktuellen FB_TOKEN ein und klicke „Debug“.
   Du liest ab: „Expires“ (Datum) und „Valid: True/False“. Danach Feld leeren.
2. Dasselbe mit dem Instagram-Schlüssel (IG_TOKEN) – falls der Debugger ihn nicht erkennt: „nicht prüfbar“ notieren.
Bericht: FB_TOKEN gültig bis <Datum> · IG_TOKEN gültig bis <Datum oder „nicht prüfbar“>.

══════════ SCHRITT 4 – Testlauf ══════════
1. GitHub-Repo → Actions → „Instagram stats“ → „Run workflow“ (Branch main) → starten.
2. Warten, bis der Lauf fertig ist (ca. 1 Min.), Lauf öffnen → Job „stats“ → Schritt „Fetch“ aufklappen.
3. Prüfen: grüner Haken? Steht im Log noch „IG_USER_ID does not match IG_TOKEN“? (Soll NICHT mehr erscheinen.)
4. Dasselbe mit Actions → „Radar“ → „Run workflow“: grüner Haken? Steht im Log „FB_TOKEN is expired or invalid“?
   (Soll NICHT erscheinen.)
Bericht: Stats grün ja/nein, Warnung weg ja/nein · Radar grün ja/nein.

══════════ SCHRITT 5 – Abschluss ══════════
Gib mir diesen Text zum Kopieren für Claude Code aus und setz die Berichte ein:
„Moin Claude Code, Schlüssel für @maehrtax sind erledigt:
<BERICHTE 1–4>
Bitte trag die Ablaufdaten in automation/key_expiry.json ein (FB_TOKEN, IG_TOKEN), prüf die letzten Läufe von
Stats und Radar und sag mir, ob die Selbst-Verlängerung jetzt vollständig ist.“
```

## After Cowork
- Claude Code writes the expiry dates into `automation/key_expiry.json` (the watchdog warns 14 days before), checks the runs, and confirms the monthly refresh (`token.yml`) has everything it needs: `IG_TOKEN` + `GH_PAT` for Instagram, `FB_TOKEN` + `FB_APP_ID` + `FB_APP_SECRET` + `GH_PAT` for the radar.
