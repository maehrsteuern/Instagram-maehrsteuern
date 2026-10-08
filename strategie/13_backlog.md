# 13 · Backlog Automatisierung

Stand 03.10.2026. Bewertung und Freigabe durch Loris, Umsetzung durch Claude.

## ✅ Umgesetzt (Sprint 1, 03.10.)
- **Wächter** – ein offenes Issue „🚨 Wächter“, kommentiert nur bei rotem Workflow oder Schlüssel < 14 Tage (`automatik/waechter.py`, läuft im Lage-Lauf)
- **Stichwort-Abgleich** – `automatik/interaktion.json` ist die einzige Quelle; Abweichungen in Bildunterschriften erscheinen in `LAGE.md` unter „Braucht dich“
- **Radar-Pflege** – montags im Radar-Issue: 🧹 entfernen / ➕ aufnehmen, übernommen wird nur, was abgehakt ist
- **Erste-Stunde-Checkliste** – nach jedem Feed-Beitrag als Kommentar im Freigabe-Issue
- Actions auf Node 24, Runner fest `ubuntu-24.04`

## ✅ Umgesetzt (Sprint 2, 03.10.)
- **#3 Wochenbericht + #9 Herkunft der Demos** – sonntags ein Issue (`automatik/wochenbericht.py`); Demos/ManyChat/Herkunft per Kommentar von Hand (Variante a), zusätzlich gezählt aus `strategie/dm_tracking.csv` (Variante b, Spalte `termin_gebucht` = ja); Werte in `automatik/statistik/woche.csv`. Automatisch: Reclaim bucht fest in den Hauptkalender → Apps-Script `automatik/apps_script/demo_kopie.gs` (Loris' Google-Konto) kopiert nur Demo-Buchungen ohne Namen/E-Mails nach „maehrsteuern Autopilot“, Herkunft aus dem Pflichtfeld „Woher kennst du mich?“ (Variante C, 03.10.; Echttest 03.10. bestanden: Kopie „📅 Demo gebucht (Instagram)“ erschienen, nach Absage gelöscht; Herkunft mit allen 5 Optionen gegen das echte Reclaim-Format geprüft). Abgelehnt: Dienstkonto liest Hauptkalender (Variante B, zu weit). Nicht genutzt: UTM (Reclaim speichert ihn nicht sicher), eigene Links je Quelle (Feld ist genauer), ManyChat-API (nur Pro), Reclaim-Webhooks (nur Business).
- **`kalender.ics` entfernt** – ersetzt durch den Direkt-Sync
- **#1 Kalender-Direktsync** – Google-Kalender „maehrsteuern Autopilot“ per Dienstkonto (nur dieser Kalender, Scope `calendar.events`), jeder Lage-Lauf, idempotent, Postzeiten „beschäftigt“ für Reclaim, To-dos „frei“, Farben je Art (`automatik/kalender_sync.py`)

## ✅ Umgesetzt (Robustheit, 03.10.)
- **Kein Doppel-Post:** `posten.py` pusht den Status mit Wiederholung; nach dem Warten wird der Plan neu gelesen („stop“, neue Zeit, „entfaellt“ greifen noch); kurze API-Aussetzer (Verbindung, 5xx) 3× wiederholt – `media_publish` nie; fehlender Link nach dem Veröffentlichen markiert den Beitrag nicht mehr als „fehler“
- **Kein Schlüssel im Repo/Log:** IG_TOKEN wird aus Fehlermeldungen in `plan.json` entfernt; neuer Schlüssel beim Verlängern maskiert und per stdin an `gh secret set`; Ablaufdatum erst nach erfolgreichem Ersetzen
- **Keine verlorenen Antworten:** „go“/„K12 ok“/Nachträge laufen je Kommentar in eigener Concurrency-Gruppe (vorher konnte ein neuer Kommentar einen wartenden Lauf verdrängen)
- **Push-Wiederholung** mit `rebase --abort` in allen Skripten, Statistik-Push mit Wiederholung, LinkedIn-Paket bricht ohne Push ab
- **Reserve-Takt:** Lage stößt die Schlüssel-Verlängerung an, wenn < 30 Tage übrig; Statistik-Neuversuch nach 30 Min.
- **posten.yml:** Eingaben nur als Umgebungsvariable (keine Befehlseinschleusung)
- Offen (klein): `insights_voll.py` holt täglich die ganze Historie neu; `lage.py`-Protokoll liest das ganze Git-Log; Push-Schleifen in ein Modul zusammenführen

## ✅ Umgesetzt (Nachträge, 03.10. nachmittags)
- **Radar:** Backoff bei Meta-Drosselung (HTTP 429, Codes 4/17/32/613/8000x; 30/90/270 s, `Retry-After` beachtet), Abbruch statt Dauerfeuer; nur dauerhafte Fehler führen zu 🧹-Vorschlägen; 1 s Pause je Konto; Art-Erkennung mit mehr Stichwörtern, fehlende/unbekannte Art als Hinweis im Issue
- **Wochenbericht:** Demo-Kopien ohne `q`-Suche und mit Blättern gelesen, Herkunft-Regex bleibt in der Zeile, Nachträge nur am Zeilenanfang/nach Komma (keine Treffer in Zitaten oder in „Gesamtstand ManyChat …“)
- **Einmalige Erinnerungen:** `automatik/erinnerungen.json` → „Braucht dich“ in LAGE.md + Termin im Autopilot-Kalender (Art `erinnerung`, „frei“)


## 🔧 Content-Fabrik für 2 Beiträge pro Tag (08.10.)
**Problem:** Die Fabrik baut höchstens 4 Beiträge pro Lauf an 2 Tagen, also 8 pro Woche. Der Testmonat braucht 14 Feed-Beiträge pro Woche.
**Lösung (Loris hat zugestimmt):**
- ✅ **Zeitplan:** 3 Läufe pro Woche, **Mo, Mi, Fr 08:47** (umgestellt am 08.10.; vorher Mo/Do).
- ⏳ **Prompt** (nur im Chat der Routine „Instagram Content-Fabrik (in Session)“ änderbar). Punkt 2 dort ersetzen:
  > Leere Slots von übermorgen bis +7 Tage füllen, **höchstens 6 Feed-Beiträge pro Lauf** (Teaser-/Frage-Storys zählen nicht).
  > Slots: 12:15 und 19:30 (Feed), Storys 12:45 und 19:35. Reihenfolge der Slots und Formate nach `strategie/15_plan_2_pro_tag.md`,
  > sobald es die Datei gibt. Bis dahin: mittags Karussell, abends Reel.
  > Stimm-Reels nur mit Sprachnachricht (sonst `wartet_auf_sprachnachricht`). Pro Beitrag `"stimme": true/false` und `"hook": "fall"|"zahl"` setzen.
  > Lieber ein Slot leer als ein schwacher Beitrag.

  Punkt 5 (Commit) ersetzen: Autor „Loris M.“ per `--author`, Committer = signierende Identität aus git config, Co-Authored-By-Zeile für Claude.
- **Rechnung:** 3 × 6 = 18 Plätze für 14 Beiträge. Das lässt Puffer für Slots, die bewusst leer bleiben, und für Loris' manuelle Reels.
- **Engpass ist nicht die Fabrik, sondern die Freigabe.** 14 Freigaben pro Woche heißt 2 pro Tag. Freigabe-Issues deshalb bündeln (ein Issue je Lauf statt je Beitrag), wenn das zu viel wird.

## ⏸️ Zurückgestellt bis ca. 15 Beiträge
Vorher fehlen die Daten, um daraus etwas Belastbares abzuleiten.
- **#4 Rückmeldung an die Content-Fabrik** – 48 h nach jedem Beitrag Speichern/Teilen pro Reichweite bewerten, Ergebnis in `strategie/was_funktioniert.md`, die Fabrik liest es mit
- **#5 Themenliste aus Kommentaren und Radar** – wöchentlich Fragen und häufige Begriffe sammeln (Claude, ca. 0,50 €/Monat) → `strategie/themen.md`
- **#10 Beste Uhrzeiten monatlich** – Empfehlung aus den Aktiv-Zeiten der Follower, nie automatisch umstellen
- **#11 Collab nachfassen** – 7 Tage nach abgehakter Anfrage ohne Antwort ein Hinweis im Radar

## ❌ Abgelehnt
- **#12 LinkedIn per API posten** – Dokument-Posts brauchen die freigabepflichtige Community-Management-API; 2 Min. von Hand sind günstiger

## Grundsätze
- Nie automatisch posten, kommentieren, folgen, liken oder DMs senden. DMs nur über ManyChat.
- Benachrichtigungen niedrig halten, lieber bündeln (ein Issue je Zweck, Status im Issue-Text statt neuer Kommentare).
- Kosten, Upgrades, neue Zugänge: erst fragen.
