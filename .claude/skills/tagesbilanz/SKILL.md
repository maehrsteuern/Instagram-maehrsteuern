---
name: tagesbilanz
description: Tagesbilanz für Loris – was wurde heute in allen Repos geschafft, wie viele Claude-Sitzungen, Punktwert mit Ampel (wenig/okay/viel), auch als Wochenbilanz über die letzten 7 Tage. Nutzen bei „/tagesbilanz“, „Tagesbilanz“, „Wochenbilanz“, „was habe ich heute/diese Woche geschafft“, „wie viel Workflow die letzten Tage“.
---

# Tagesbilanz

1. Sitzungen von heute zählen: `list_sessions` (claude-code-remote, `mine: true`, ggf. per ToolSearch laden) aufrufen und die Sitzungen zählen, die heute (deutsche Zeit) erstellt oder zuletzt aktiv waren. Nicht erreichbar → 0 und das dazu sagen.
2. `python3 automatik/tagesbilanz.py --sitzungen N --speichern` ausführen (für einen anderen Tag `--datum JJJJ-MM-TT`).
3. Loris kurz sagen: Punktwert + Ampel, pro Repo in 1–2 Sätzen was erledigt wurde (Commit-Liste zusammenfassen, nicht abtippen), dazu die Titel der Sitzungen. Vergleich mit den letzten Tagen aus `automatik/tagesbilanz.md`.
4. `automatik/tagesbilanz.md` committen („Tagesbilanz JJJJ-MM-TT“) und pushen.

## Wochenbilanz (letzte 7 Tage)

1. `list_sessions` (`mine: true`, `limit: 100`) aufrufen, Sitzungen je Tag nach `created_at` in deutscher Zeit zählen (Ausgabe ist groß → aus der gespeicherten Datei per Python auswerten).
2. `python3 automatik/tagesbilanz.py --woche --sitzungen-je-tag JJJJ-MM-TT=N,... --speichern` (Ende = `--datum`, Standard heute).
3. Loris sagen: Wochenpunkte, Ø pro Tag + Ampel, stärkster/schwächster Tag, pro Repo 1–2 Sätze (Themen bündeln, nicht abtippen). Vergleich mit Vorwochen aus `automatik/wochenbilanz.md`.
4. `automatik/tagesbilanz.md` + `automatik/wochenbilanz.md` committen („Wochenbilanz JJJJ-MM-TT“) und pushen.

Nicht gezählt: automatische Commits (Lage, Statistik, Radar, Status, Freigaben), Merges, derselbe Betreff ein zweites Mal (Cherry-Picks), Commits fremder Repos auf einem Branch (zählen beim Heimat-Repo) und Dateien über 5.000 geänderte Zeilen (Datenimporte).

Chats in claude.ai (außerhalb von Claude Code) sind nicht abrufbar – wenn Loris nennt, wie viele es waren, zu `--sitzungen` dazuzählen.

**Ohne Sitzung:** Die Tagesbilanz läuft auch als Artefakt direkt in claude.ai: https://claude.ai/artifact/XfjZPdFSHr37jTXdRd4Woo (Quelle `automatik/tagesbilanz.html`; Verlauf in der Artefakt-Datenbank, Sammlung `tage`). Nach Änderungen die Datei unter derselben URL neu veröffentlichen.
