"""Gemeinsamer Zugang zu Claude für Radar, Kommentare und LinkedIn (Textvorschläge, nie automatisch gepostet
außer der festen TOOL-Antwort). Ohne ANTHROPIC_API_KEY liefert json_antwort() None – die Skripte laufen dann
ohne Vorschläge weiter.

Kosten: ca. 3–8 Cent pro Aufruf, bei 2–3 Aufrufen am Tag ca. 2–5 € im Monat.
"""
import json, os

MODELL = "claude-opus-5-5"

# Gilt für jeden Text, den Claude für maehrsteuern schreibt
STIMME = """Du schreibst für Loris, Instagram @maehrsteuern: Diplom-Finanzwirt und KI-Manager (IHK), baut Steuer-Tools mit Code.
Leitspruch „Steuern × Code – Steuerwissen, das rechnet.“ Zielgruppen: Steuerabteilungen, Kanzleien/StB-Mitarbeitende, KMU, Studierende.
Stil: Du-Form, locker, aber fachlich sauber, kurze Sätze, höchstens ein Emoji, keine Hashtags.
Harte Regeln:
- Keine Werbung, keine Links, kein „Schreib TOOL“, kein „schau auf mein Profil“, keine Selbstdarstellung.
- Nichts über Loris' Arbeitgeber, keine echten Firmen- oder Mandantendaten.
- Fachlich nur, was sicher stimmt; im Zweifel eine Frage stellen statt etwas zu behaupten.
- Nie generisch („Toller Beitrag!“) – immer konkret auf den Inhalt eingehen."""


def json_antwort(aufgabe, daten, schema, max_tokens=8000):
    """Ein Aufruf, Antwort als JSON nach `schema`. None, wenn kein Schlüssel da ist oder etwas schiefgeht."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Hinweis: ANTHROPIC_API_KEY fehlt – ohne KI-Vorschläge.")
        return None
    import anthropic
    try:
        antwort = anthropic.Anthropic().beta.messages.create(
            model=MODELL,
            max_tokens=max_tokens,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            system=STIMME,
            output_config={"effort": "medium", "format": {"type": "json_schema", "schema": schema}},
            messages=[{"role": "user", "content": f"{aufgabe}\n\n<daten>\n{json.dumps(daten, ensure_ascii=False, indent=1)}\n</daten>"}],
        )
    except anthropic.APIError as fehler:
        print(f"Hinweis: Claude nicht erreichbar ({fehler.__class__.__name__}) – ohne KI-Vorschläge.")
        return None
    if antwort.stop_reason != "end_turn":
        print(f"Hinweis: Claude hat nicht fertig geantwortet ({antwort.stop_reason}) – ohne KI-Vorschläge.")
        return None
    return json.loads(next(b.text for b in antwort.content if b.type == "text"))
