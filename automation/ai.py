"""Shared access to Claude for radar, comments, LinkedIn and the weekly report (text suggestions – never
posted automatically). Without ANTHROPIC_API_KEY, json_answer() returns None and the scripts continue
without suggestions.

Cost: about 3–8 cents per call; with 2–3 calls a day roughly $2–6 a month.
"""
import json, os

MODEL = "claude-opus-5-5"

# Applies to every text Claude writes for @maehrtax
VOICE = """You write for Loris, Instagram @maehrtax ("Tax × Code – tax know-how that computes").
Loris is a German-trained tax pro (trained in the German tax administration, Diplom-Finanzwirt) and a Certified
AI Manager (IHK, German Chamber of Commerce). He builds AI + code tools for US tax teams.
Audience: in-house tax teams (ASC 740 / tax provision, compliance), CPA firms and tax preparers, small business
owners, accounting students. Write US English (US spelling and formats: $1,250.50, 10/15/2026, 7:30 PM ET).
Style: talk to "you", friendly and concrete, short sentences, at most one emoji, no hashtags.
Hard rules:
- Educational only. Never give individual tax, legal or accounting advice. If someone asks about their own
  situation, say it depends on the facts and to talk to their CPA about their case.
- Never claim or imply that Loris is a CPA, EA, tax attorney or former IRS employee.
- No ads, no links, no "DM TOOL", no "check my profile", no self-promotion (unless the task explicitly allows it).
- Nothing about Loris' employer, no real company or client data.
- Only state tax facts you are sure about; when in doubt, ask a question instead of claiming something.
- Never generic ("Great post!") – always refer to the specific content."""


def json_answer(task, data, schema, max_tokens=8000):
    """One call, answer as JSON following `schema`. None if there is no key or something goes wrong."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Note: ANTHROPIC_API_KEY missing – continuing without AI suggestions.")
        return None
    try:
        import anthropic
    except ImportError:
        print("Note: anthropic package not installed – continuing without AI suggestions.")
        return None
    try:
        answer = anthropic.Anthropic().beta.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            system=VOICE,
            output_config={"effort": "medium", "format": {"type": "json_schema", "schema": schema}},
            messages=[{"role": "user", "content": f"{task}\n\n<data>\n{json.dumps(data, ensure_ascii=False, indent=1)}\n</data>"}],
        )
    except anthropic.APIError as err:
        print(f"Note: Claude not reachable ({err.__class__.__name__}) – continuing without AI suggestions.")
        return None
    if answer.stop_reason != "end_turn":
        print(f"Note: Claude did not finish ({answer.stop_reason}) – continuing without AI suggestions.")
        return None
    try:
        return json.loads(next(b.text for b in answer.content if b.type == "text"))
    except (StopIteration, ValueError):
        print("Note: Claude's answer was not valid JSON – continuing without AI suggestions.")
        return None
