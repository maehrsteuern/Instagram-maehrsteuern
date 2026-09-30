---
name: lage
description: Überblick über den Instagram-Content-Plan von maehrsteuern – was gerade läuft, was als Nächstes online geht, was von Hand zu tun ist und was zuletzt passiert ist. IMMER zu Beginn jeder Sitzung in diesem Repo nutzen und nach jeder Änderung an plan.json, posts/, strategie/ oder automatik/. Auch bei „Lage“, „Überblick“, „Stand“, „was läuft gerade“, „was kommt als Nächstes“, „was ist passiert“.
---

# Lage – der laufende Überblick

`LAGE.md` im Repo-Wurzelordner ist die eine Seite, auf der Loris jederzeit sieht, was auf Instagram passiert.
Sie wird von `automatik/lage.py` erzeugt und von `.github/workflows/lage.yml` nach **jedem Push**, nach **jedem Lauf**
von Posten/Freigabe/Statistik/Schlüssel/Musik und jeden Morgen neu geschrieben. Das Protokoll darin kommt aus dem
Git-Verlauf – jeder Commit (Autopilot und von Hand) steht dort automatisch, inkl. der Änderungen an `plan.json`.

## Zu Beginn jeder Sitzung
1. `git pull` auf `claude/instagram` bzw. den Arbeitsbranch, dann `python3 automatik/lage.py`.
2. `LAGE.md` lesen – vor allem **Braucht dich**, **Nächste 7 Tage** und **Automatik** (rote Einträge = Fehler).
3. Loris kurz sagen, was als Nächstes online geht und was offen ist, bevor anderes gemacht wird.

## Nach jeder Änderung
- Commit-Nachricht auf Deutsch und so, dass sie im Protokoll allein verständlich ist
  (z. B. „Plan: Reel Ampel auf Mo 19:30 verschoben (Feiertag)“). Das Protokoll zeigt nur Nachricht + Plan-Änderungen.
- Ändert sich, woran gerade gearbeitet wird oder wurde etwas entschieden: `automatik/lage_notizen.md` anpassen
  (kurze Stichpunkte, Veraltetes löschen). Das erscheint oben in LAGE.md unter „Gerade in Arbeit“.
- `python3 automatik/lage.py` ausführen und `LAGE.md` mit committen. (Die Action macht es sonst ohnehin nach dem Push.)
- `LAGE.md` nie von Hand bearbeiten – wird überschrieben. Fehlt dort etwas, `automatik/lage.py` erweitern.

## Status in plan.json (Bedeutung)
`entwurf` → Freigabe-Issue, „go“ → `freigegeben` → Autopilot postet → `veroeffentlicht` (mit Link).
`manuell` = Loris postet in der App · `wartet_*` = blockiert (z. B. Clips fehlen) · `fehler` = Posten fehlgeschlagen · `entfaellt`.
