# Hook library (English, @maehrtax)

Ready-made Reel openers: **1.8–2.8 s**, 1080×1920, 30 fps, outline text (Outfit Bold). The first line is readable in
frame 1, the second pops in by ~1 s. **Ambience only** (typing, error beep, clock) – music only where the hook already
shows the solution – so a hook fits in front of any Reel (rules: `strategy/09_reel_rules.md`, brief: `strategy/00_us_brief.md`).
All text sits inside the safe zone (y 250–1500, right 150 px free). Demo data only (fictional "Northwind Manufacturing Inc.").

| File | Length | Hook text | Pattern | Picture | Use for pillar | AI footage |
|---|---|---|---|---|---|---|
| `h01_ref_deadline.mp4` | 2.0 s | #REF! / 3 days before the deadline. | Error callout | Spreadsheet mock, errors piling up | 1 Demo · 2 In practice | no |
| `h02_every_provision.mp4` | 2.6 s | This error is in / almost every provision. | Error callout | Spreadsheet half of the split screen (card) | 2 In practice | no |
| `h03_400_cells.mp4` | 2.4 s | 21% typed / into 400 cells. | Number / pain | Demo tool, rate view (400 red cells) | 5 Satisfying · 2 In practice | no |
| `h04_17_seconds.mp4` | 2.7 s | Full provision check: / 17 seconds. | Number / result | Tool half of the split screen, stopwatch "✓ 17 s" | 1 Demo | no |
| `h05_interest_limit.mp4` | 2.4 s | Your interest limit / just grew. | Reveal | Demo tool, § 163(j) view | 3 Know-how · 1 Demo | no |
| `h06_ready_to_book.mp4` | 2.5 s | Ready to book? / Not yet. | Question / status | Demo tool, provision check on red | 1 Demo | no |
| `h07_by_hand.mp4` | 2.6 s | Still doing this / by hand? | Question / pain | Runway clip: hands, calculator | 2 In practice · 3 Know-how | **yes** |
| `h08_friday_night.mp4` | 2.6 s | Friday, 9:45 PM. / Due Monday, 8 AM. | Deadline / pain | Runway clip: empty office at night (wall clock ≈ 9:45) | 2 In practice · 4 Behind the code | **yes** |
| `h09_row_4000.mp4` | 2.6 s | There's an error somewhere. / Row 1 of 4,000. | Pain / search | Runway clip: over the shoulder onto a spreadsheet | 2 In practice | **yes** |
| `h10_one_click.mp4` | 2.8 s | 4,000 messy rows. / One click. | Before / after | Demo tool, cleanup view | 5 Satisfying | no |

**AI footage = yes:** the clip is an own Runway generation with a realistic person or scene → switch on Instagram's AI label
("AI info") when posting and add `Contains AI-generated footage.` to the caption. The clips show no faces on purpose
(AI facial expressions look exaggerated). On-screen text is never AI-generated – it is set by `montage.py`.

## Use a hook in a Reel
Take the hook as the first source of a cut list (`templates/system/montage.py`), e.g.
`"sources": {"hook": {"video": "../hooks/h04_17_seconds.mp4"}, …}` with the first scene
`{"source": "hook", "duration": 2.7, "start": 0}`. Copy the hook's audio tracks from `templates/system/cuts/hooks/<name>.json`
into the Reel's `"audio"` (with `"at"` unchanged). Or rebuild the hook text inside the Reel's own first scene.

## Change and rebuild
All hooks are described in `templates/system/build_hooks.py` (source, crop, text, audio).
`cd templates/system && python3 build_hooks.py` builds all, `python3 build_hooks.py h04 h07` only some.
The cut lists land in `templates/system/cuts/hooks/`.

## Sources
- `clips/ai_office_evening.mp4`, `clips/ai_calculator.mp4`, `clips/ai_over_shoulder.mp4` – three Runway video clips
  (own AI generation, Sept 30, 2026), no faces. `ai_office_evening`: the wall clock shows about 9:45 PM, a small
  monitor brand logo is visible – crop it (`"from"/"to"`) if that matters.
- `clips/card_top_table.mp4`, `clips/card_bottom_tool.mp4` – the halves of the English split-screen recording
  (`posts/02_…/clips/rec_split.mp4`), centred on the dark background (y 654–1266).
- Demo-tool and spreadsheet recordings live in the Reel folders (`posts/<reel>/clips/rec_*.mp4`) and can be re-recorded any time:
  `templates/system/recordings/*.mjs` (deterministic Playwright recorder, see `recorder.mjs`).
- `overlays/cta_dm_tool.png`, `overlays/cta_checklist.png` – transparent CTA boxes 'DM "TOOL"' (render job `templates/system/jobs/r00_overlays.json`).
