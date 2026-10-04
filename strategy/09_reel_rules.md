# 9 · Reel rules

Adds to the formula in `08_demo_reel_formula.md`. Applies to every Reel from the Content Factory.
General knowledge (algorithm, sharing, length, cover, search): `11_instagram_knowledge.md`. US-specific growth strategy: `16_us_growth_playbook.md`.
Cut list templates: `templates/system/cuts/` (renderers `templates/system/reel.py` for stills, `templates/system/montage.py` for video montages).

## US baseline (from the brief)
- **Hook ≤ 1.5 s**, on-screen text from frame 1, works without sound.
- **Visible transformation** in every Reel: chaos → clean, red → green, 2 hours → 17 seconds.
- **CTA** in every Reel, on screen, no static end card (the Reel should loop).
- **Faster cut than in Germany** – but still calm and premium: speed comes from the payoff arriving early, not from effects.
- Satisfying Reels (pillar 5): 6–12 s, no talking, loopable – details in `10_software_reel_concept.md`.

## Learnings from the German account (feedback Loris, 9/30/2026)
- A polished screen demo felt **too professional** – like a product video for a website or an ad, **not like Instagram**.
- The pain point in the opening worked. **After that it went generic**: screen demo + lo-fi music is a standard pattern everybody has seen and doesn't hold.
- **What worked better:** a personal angle, **more drama, more trigger, the pain stays longer and is told personally** ("this happened to me …") instead of shown neutrally.
- Consequences for story Reels (pillars 1, 2, 4):
  - First person, a real small story (situation → the moment it blows up → turn), not "problem → tool demo".
  - The pain carries the Reel; the tool is the punchline at the end, not the main part.
  - Text as a thought or quote ("I thought the provision tied out."), not as an ad line ("Everything recalculates.").
  - No background music by default. Better original sound, silence, ambience, or a trending sound from the Instagram app (manual).
  - Polished vs. personal/raw – on Instagram, personal usually wins.
- Exception: **satisfying Reels** are deliberately clean and wordless – there the polish is the point, but they must loop and never look like an ad (no logo intro, no feature list).

## Voice and sound (Loris, 9/30)
- **Your own voice carries the Reel** (a phone voice note is enough). Outline the text, speak casually – in English; a light German accent is fine and part of the story.
- **Subtitles match the spoken words exactly** – word for word, so the Reel works without sound.
  All on-screen text follows this logic (keywords like "#REF!" only as reinforcement of what's said).
  Timestamps via speech recognition (faster-whisper, model "small"), proofread the wording by hand at the end.
- **Voice first:** music very quiet in the background, sound effects (clock, error beep, typing) also quiet.
  Guide values: voice approx. −18 LUFS, music ~0.13, ambience 0.2–0.3.
- Recording: keep distance from the phone mic (otherwise it sounds scratchy/clipped), quiet room.

## Hook (0–1.5 s, extended opening up to 3 s)
- **No rapid fire.** Max. 2 shots in the hook, not 4–5 eighth-note cuts. Each shot may stand 1.4–2 s – but the first text is there from 0.0–0.3 s.
- **Text from 0.3 s at the latest**, big with black outline, word by word or line by line. The hook must work **without sound**.
- **Error callout** fits @maehrtax: real pain ("#REF! – 3 days before Oct 15. Sound familiar?"), then the resolution.
- Hook wording: `08_hooks.md`. No claims the Reel doesn't deliver.
- Hook library with ready-made openings: `templates/hooks/`.

## AI clips (Runway)
- **Use only a short section.** AI faces exaggerate expressions (screaming, hands on the head). That looks fake, people don't like it.
- Good: the **quiet, tense moment** (staring at a red screen, a frown), slow camera move.
- Slow the clip down (speed 0.8 in the cut list), no glitch or shake effects on top.
- In the prompt ask for a calm expression ("subtle, restrained expression") instead of "shock" or "disbelief".
- **Realistic AI people → switch on Instagram's AI label.** Never let AI video generation write on-screen text – text is always our own overlay.

## Sound design
- **The music must match the emotion.** Pain moment ≠ deep house.
- In the hook **no music, but ambience**: typing → error beep (text pops on it) → clock ticking.
- **Music starts with the solution** (cut to the tool). The contrast silence → music carries the relief.
- Music for the solution: calm, confident (lo-fi, minimal), no party drop. Beat from second 0.
- Satisfying Reels: soft clicks, a satisfying "done" sound on the payoff, music optional.
- Ambience is in `music/ambience/`, tracks in `music/` (sources in `music/SOURCES.md`).

## Cuts and effects
- Effects **sparingly and on purpose**: one clean whip pan at the switch pain → solution is enough.
- Flash, glitch, zoom punch and shake (construction-montage style) get attention but quickly become too much and are saturated in the feed. At most one at a time, never all at once.
- **Construction montages work for trades, not for software.** There every cut shows real progress; with software the same pace just looks hectic. Our own concept: `10_software_reel_concept.md`.
- Darken busy screens behind text (dim value ~0.35 in the cut list).

## Text and safe zone (1080×1920)
- Nothing below **y ≈ 1500** (Instagram caption and buttons) and nothing above **y ≈ 200** (header).
- Keep ~150 px free on the right (like, comment and share buttons).
- Never put text over a face. With AI clips the text sits on the chest/shirt.
- Colors: red = error/pain, yellow = question, green = solution, white = everything else.
- Numbers in US format on screen: `$1,000,000`, `21%`, `10/15`.

## Hook inspiration (mistake/problem, applied to tax)
- "Everyone makes this mistake in the tax provision – here's the fix."
- "Stop doing this – it's only slowing you down." (spreadsheet links)
- "You know that moment when …?" (#REF! on deadline day)
- "3 mistakes you're probably making in your rate reconciliation."
- "This saved me hours – and it's ridiculously simple."
- "I used to make this mistake all the time."
