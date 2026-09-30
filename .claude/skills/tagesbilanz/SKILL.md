---
name: tagesbilanz
description: Tagesbilanz für Loris – was wurde heute in allen Repos geschafft, wie viele Claude-Sitzungen, Punktwert mit Ampel (wenig/okay/viel). Nutzen bei „/tagesbilanz“, „Tagesbilanz“, „was habe ich heute geschafft“, „wie viel habe ich heute gemacht“.
---

# Tagesbilanz

1. Sitzungen von heute zählen: `list_sessions` (claude-code-remote, `mine: true`, ggf. per ToolSearch laden) aufrufen und die Sitzungen zählen, die heute (deutsche Zeit) erstellt oder zuletzt aktiv waren. Nicht erreichbar → 0 und das dazu sagen.
2. `python3 automatik/tagesbilanz.py --sitzungen N --speichern` ausführen (für einen anderen Tag `--datum JJJJ-MM-TT`).
3. Loris kurz sagen: Punktwert + Ampel, pro Repo in 1–2 Sätzen was erledigt wurde (Commit-Liste zusammenfassen, nicht abtippen), dazu die Titel der Sitzungen. Vergleich mit den letzten Tagen aus `automatik/tagesbilanz.md`.
4. `automatik/tagesbilanz.md` committen („Tagesbilanz JJJJ-MM-TT“) und pushen.

Chats in claude.ai (außerhalb von Claude Code) sind nicht abrufbar – wenn Loris nennt, wie viele es waren, zu `--sitzungen` dazuzählen.
