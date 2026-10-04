"""Ablaufdaten der Zugangsschlüssel merken – nur das Datum, nie den Schlüssel. Liest der Wächter (waechter.py)."""
import json
from datetime import date, timedelta
from pathlib import Path

DATEI = Path(__file__).resolve().parent / "schluessel_ablauf.json"


def ablauf_merken(name, sekunden):
    daten = json.loads(DATEI.read_text()) if DATEI.exists() else {}
    daten[name] = (date.today() + timedelta(seconds=sekunden)).isoformat()
    DATEI.write_text(json.dumps(daten, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
