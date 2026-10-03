# 13 · Backlog Automatisierung

Stand 03.10.2026. Bewertung und Freigabe durch Loris, Umsetzung durch Claude.

## ✅ Umgesetzt (Sprint 1, 03.10.)
- **Wächter** – ein offenes Issue „🚨 Wächter“, kommentiert nur bei rotem Workflow oder Schlüssel < 14 Tage (`automatik/waechter.py`, läuft im Lage-Lauf)
- **Stichwort-Abgleich** – `automatik/interaktion.json` ist die einzige Quelle; Abweichungen in Bildunterschriften erscheinen in `LAGE.md` unter „Braucht dich“
- **Radar-Pflege** – montags im Radar-Issue: 🧹 entfernen / ➕ aufnehmen, übernommen wird nur, was abgehakt ist
- **Erste-Stunde-Checkliste** – nach jedem Feed-Beitrag als Kommentar im Freigabe-Issue
- Actions auf Node 24, Runner fest `ubuntu-24.04`

## ✅ Umgesetzt (Sprint 2, 03.10.)
- **#3 Wochenbericht + #9 Herkunft der Demos** – sonntags ein Issue (`automatik/wochenbericht.py`); Demos/ManyChat/Herkunft per Kommentar von Hand (Variante a), zusätzlich gezählt aus `strategie/dm_tracking.csv` (Variante b, Spalte `termin_gebucht` = ja); Werte in `automatik/statistik/woche.csv`. Automatisch: Reclaim-Buchungen „Demo + Erstgespräch“ im Kalender „maehrsteuern Autopilot“ + Buchungsfeld „Woher kennst du mich?“ (sobald Reclaim dort einträgt, Chrome-Check 03.10.). Nicht genutzt: UTM (Reclaim speichert ihn nicht sicher), eigene Links je Quelle (Feld ist genauer), ManyChat-API (nur Pro), Reclaim-Webhooks (nur Business).
- **`kalender.ics` entfernt** – ersetzt durch den Direkt-Sync
- **#1 Kalender-Direktsync** – Google-Kalender „maehrsteuern Autopilot“ per Dienstkonto (nur dieser Kalender, Scope `calendar.events`), jeder Lage-Lauf, idempotent, Termine „beschäftigt“ für Reclaim (`automatik/kalender_sync.py`)


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
