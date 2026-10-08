# Routine „Instagram Tagesbericht 9 Uhr“ – Prompt (Stand 08.10.2026)

Das Prompt einer Routine kann nur aus **ihrem eigenen Chat** geändert werden. Dort einfügen:
„Ersetze dein Routine-Prompt durch den folgenden Text“ + den Block unten.

Zusätzlich in den Routine-Einstellungen (claude.ai/code → Routinen → „Instagram Tagesbericht 9 Uhr“):
- **Quelle/Repo:** `maehrsteuern/Instagram-maehrsteuern` mit Schreibzugriff eintragen.
- **Connector:** Google Calendar hinzufügen (der Fireflies- und der Posteingang-Routine ist er schon zugeordnet, dieser fehlt er).
- **GitHub:** github.com → Settings → Applications → Claude → Repository access: `Instagram-maehrsteuern` freigeben.
  Hinweis: Das Repo heißt auf GitHub `Instagram-maehrsteuern` (großes I); `instagram-maehrsteuern` wird nur umgeleitet.

```text
Täglicher Insights-Bericht für @maehrsteuern. Loris will ihn jeden Morgen um 9 Uhr hier im Chat UND im Google Kalender – ausführlich, visuell (Bild mit Tabellen) und mit deiner direkten Einschätzung, ob unsere Methoden greifen.

0. Zugang (IMMER zuerst, auch wenn der Ordner schon existiert – sonst antwortet der Git-Proxy beim Push mit 403 „repository is not in this session's authorized repository set“): add_repo mit owner maehrsteuern, repo Instagram-maehrsteuern, access "push". Vorhandenen Klon weiter nutzen, sonst wie von add_repo angegeben klonen. Zweig claude/instagram, git pull --rebase.

1. Prüfen, ob automatik/statistik/insights_<heute>.json existiert. Fehlt sie: Workflow statistik.yml auf claude/instagram per GitHub-MCP starten, mit einer until-Schleife (max. 5 Min.) auf den Commit „Statistik <heute>" warten, dann pullen.
2. `python3 automatik/tagesbericht.py` → automatik/berichte/tagesbericht_<heute>.png/.html/.json (Kacheln, Reichweite pro Tag, Beiträge mit Alter in h, Reels mit Skip · Ø Sehdauer / Länge = Anteil gesehen, Storys, Methoden-Check mit n, „Heute geplant“). Der Methoden-Check bewertet nur Beiträge ab 48 h; jüngere stehen als ⏳ „zu früh“ – nie als ❌ werten. PNG ansehen (Read), prüfen, dass nichts abgeschnitten/falsch ist; bei Fehlern das Skript reparieren.
3. PNG in den Scratchpad kopieren und mit SendUserFile (display "render", status "proactive") senden.
4. Chat-Bericht (Deutsch, klar gegliedert):
   a) Tabelle Konto (Heute | Vortag | Δ) und alle Beiträge seit 29.09. mit Δ zum Vortag; bei Reels Skip, Ø Sehdauer und Anteil an der Länge (JSON beitraege[].anteil).
   b) **Greifen unsere Methoden?** – jede Zeile mit Status, Ursache in 1–2 Sätzen und ob die Datenlage reicht (n; < 48 h = zu früh). Formate vergleichen (Karussell/Reel/Story, Stimme ja/nein, Slot 12:15/19:30) erst ab n ≥ 3 je Gruppe.
   c) **Was wir ändern** – 1–3 Maßnahmen mit Bezug auf geplante Beiträge (ID/Datum). Nur vorschlagen, nicht eigenmächtig ändern.
   d) Heute geplant (JSON heute_online, inkl. „von Hand posten“ / „wartet auf Sprachnachricht“), Einträge mit status "fehler", offene Freigabe-Issues, was Loris heute tun muss.
   2025er Zahlen nicht als Maßstab nehmen.
5. Google Kalender (create_event, Primärkalender): heute 09:00–09:10 Europe/Berlin, availability FREE, useDefaultReminders false. Titel „📈 Instagram-Tagesbericht: <Follower> Follower (<±Δ>) · <wichtigste Zahl>". Beschreibung HTML (Konto, Beiträge, Methoden-Check, Einschätzung, Was wir ändern, Heute geplant) + Link https://github.com/maehrsteuern/Instagram-maehrsteuern/blob/claude/instagram/automatik/berichte/tagesbericht_<heute>.png . Keine Kontaktnamen. Fehlen die Kalender-Tools (auch per ToolSearch), als erste Zeile des Berichts: „⚠️ Kalendereintrag fehlt: Google-Calendar-Connector ist in dieser Routine nicht eingebunden“.
6. automatik/berichte/* committen; wirklich neue Erkenntnisse knapp in strategie/06_auswertung.md. Commit-Regel (Loris, 08.10.2026): Autor „Loris M. <mkwloris@googlemail.com>“ per --author; Committer bleibt die signierende Identität aus git config (Claude <noreply@anthropic.com>), sonst „Unverified“ und der Stop-Hook schlägt an; deutsche Nachricht; am Ende die Co-Authored-By-Zeile für Claude. pull --rebase, push. Schlägt der Push fehl: genauen Fehler im Bericht nennen.
```

## Dieselbe Commit-Regel in den anderen Routinen
„Instagram Content-Fabrik (in Session)“ und „Instagram Monatsbericht“ verlangen noch „kein Co-Authored-By, keine Nennung von Claude, Committer Loris M.“.
Im jeweiligen Routine-Chat Punkt 5 ersetzen durch: *Autor „Loris M. <mkwloris@googlemail.com>“ per --author, Committer = signierende Identität aus git config, Co-Authored-By-Zeile für Claude am Ende.*
