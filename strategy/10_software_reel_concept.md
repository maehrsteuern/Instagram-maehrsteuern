# 10 · Our own Reel concept for software

**Why our own concept?** Fast construction montages (hard cuts, flashes, shake) work for trades because every cut shows real, physical progress. Software has no dust and no sparks – the same pace just looks hectic (test on the German account, 9/30/2026). Our "wow" comes from **contrast** (chaos → calm) and **visible change on screen** (number jumps, status light turns green, error disappears, 400 cells update at once).

Starting point from the German account: 68 % skip rate, 7 s watch time, 0 link clicks on the first demo Reel.
→ The opening must make clear in 1 s *what this is about*, and the Reel must build trust. For the US: hook ≤ 1.5 s, transformation visible before second 8.
Rules for pace, sound and text: `09_reel_rules.md`. Growth strategy: `16_us_growth_playbook.md`.

## The four formats

### A · Before/after split screen (7–14 s)
- Top: spreadsheet (red tint, error cells), bottom: the tool (green). **Same task, two timers.**
- Top: the clock keeps running ("2 hours …"), bottom: "done" after 3 s – and stays calm.
- Sound: top typing and clock; as soon as the bottom says "done", music starts.
- Hook text: "Same task. Spreadsheet vs. tool." or "Who's faster?"
- Launch: `02-reel-split` (Tue 10/13): spreadsheet 2 h vs. tool 17 s.

### B · Demo screen recording (8–12 s)
- **Real screen recording**, soft auto-zooms that follow the cursor (like SaaS demos), quiet click sounds.
- Exactly **one** satisfying moment as the payoff: number counts up, status light jumps to green, error list empties.
- No glitches, no flashes. Motion comes from zoom and camera move, not from effects.
- Launch: `01-reel-ref-error` (10/12), `11-reel-163j-demo` (10/21).

### C · Face + screen (10–20 s)
- 2–3 s of Loris on camera as the hook ("This used to take me two days."), then screen (format A or B).
- Strongest format for trust and DMs, because a real person is behind it.
- **No AI face as a substitute** – AI expressions look exaggerated (`09_reel_rules.md`).
- Launch: `09-reel-my-story` (10/20), waiting for Loris' concept + English voice note.

### S · Satisfying software (new for the US, pillar 5, 6–12 s)
The US audience reacts strongly to satisfying, fast, visual content. This format is built **for shares and rewatches**, not for explanation.

**Principles**
1. **One motion, one payoff.** A single continuous transformation – no story, no talking, no feature list.
2. **Readable "before" in 0.5 s.** The chaos must be obvious at a glance: red cells, `#REF!`, 47 tabs, unsorted rows.
3. **The payoff is physical-looking:** a cascade (cells flip one after another), a wave of green, a counter rolling to an exact number, rows snapping into order.
4. **Perfect loop.** The last frame flows into the first (cut back to "before" on a beat, or the "after" dissolves into the next "before"). Rewatches raise watch time above 100 %.
5. **Sound is half the satisfaction:** soft clicks synced to every change, one clean "done" sound at the payoff, no voice. Music optional, quiet.
6. **Symmetry and calm framing:** centered grid, big font, dark brand background, green glow on the "after".
7. **Hold the "after" for ~1 s** before looping – the brain needs the moment of rest.
8. **Hook as minimal text** (≤ 5 words): "4,000 rows. One click." · "Before. After." · "21% → one cell."
9. **CTA as a small bar** in the last second ("DM TOOL"), never a static end card.
10. Only states the tool really shows – honesty beats effect.

**Recipes**
| Recipe | Before | Payoff | Launch / backlog |
|---|---|---|---|
| Parameter cascade | "21%" hard-coded in 400 cells | one parameter cell changes → all 400 cells update in a wave | `04-reel-hardcoded-rate` (10/14) |
| Deadline night | messy workbook at 11:48 PM, clock ticking | one click → clean summary, clock stops | `05-reel-deadline-night` (10/15) |
| Row sort | 4,000 unsorted rows with red errors | one click → rows snap into order, errors go green | `08-reel-4000-rows` (10/19) |
| Tab collapse | 47 tabs scroll by | tabs fold into one dashboard | backlog Nov |
| Tie-out | red difference cells | they clear one by one, total difference "0.00" | backlog Dec |
| Vendor check | 600 vendors, 3 missing TINs flagged | list turns green, 3 highlighted | backlog Nov |
| Counter | "Disallowed interest: $1,000,000" | counts down to $0 (EBIT → EBITDA) | variant of `07`/`11` |

Build: either a scripted recording (`templates/system/recordings/`) or rendered stills/animations (`templates/system/excel_chaos.html`, `traffic_light.html`) cut with `reel.py` / `montage.py`. **At least one satisfying Reel per Content Factory run** (`15_content_factory.md`).

## Mapping to the launch posts
| Post | Date | Format | Idea |
|---|---|---|---|
| 01 Reel #REF! | 10/12 | B | Spreadsheet `#REF!` red → tool → status green |
| 02 Reel split | 10/13 | A | Spreadsheet 2 h vs. tool 17 s, same task |
| 04 Reel hard-coded rate | 10/14 | S | parameter cascade |
| 05 Reel deadline night | 10/15 | S | chaos → clean, clock stops |
| 07 Reel § 163(j) number | 10/16 | number Reel (pillar 3) | "+$1,000,000 deductible" |
| 08 Reel 4,000 rows | 10/19 | S | row sort loop |
| 09 Reel my story | 10/20 | C | waits for Loris |
| 11 Reel 163(j) demo | 10/21 | B | calculator EBIT → EBITDA, 12 s |
| 12 Reel AI vs. code | 10/22 | C or A | AI answer vs. code answer side by side |
| 14 Reel § 174A number | 10/23 | number Reel (pillar 3) | "+$378,000 cash in year 1" |

Carousels stay carousels (they collect saves). The companion Reel pulls new people to the carousel.

## Recording list (formats A/B/S)
**Demo data only**, nothing from the employer. Resolution at least 1920×1080 (or phone view 540×960 at 2× pixel density → sharp 1080×1920), browser zoom 125–150 %, big cursor, slow, calm movements (zooms are done in the edit). Demo numbers exactly as in `00_us_brief.md`.

| File | What to record | For |
|---|---|---|
| `status_red_green.mp4` | provision status yellow/red → fill missing input → green | 01, B |
| `dashboard_click.mp4` | open dashboard, hover over cards, click a number → audit trail | 01/07 video, B |
| `split_spreadsheet_tool.mp4` | same task in the spreadsheet mock (top) and the tool (bottom), two timers | 02, A |
| `rate_cascade.mp4` | parameter "21%" changes → 400 cells update | 04, S |
| `rows_sort.mp4` | 4,000 rows → one click → sorted, errors green | 08, S |
| `interest_limit_163j.mp4` | 163(j) calculator: EBIT $10.0M → EBITDA $14.0M, disallowed $1.0M → $0 | 07/11, B/S |

Storage: `posts/<post>/clips/`.

## Automatic recordings (no manual recording needed)
The demo tool runs in the browser. Claude can operate and record it itself:
- Shared recorder: `templates/system/recordings/recorder.mjs` (visible cursor with click ripple, real typing, smooth scrolling); one short script per click path (e.g. `interest_limit_163j.mjs`, `split_excel_tool.mjs`, `traffic_light_yellow_green.mjs`).
- English demo tool mock: `templates/system/recordings/demo_tool.html` (fictional "Northwind Manufacturing Inc."); spreadsheet mocks `excel_mock.html`, `table_old_rate.html` – generic, no real program, no logo.
- Phone view 540×960 at 2× pixel density → 1080×1920, dark design. Split screen: both halves 1080×640 so everything sits between y 210 and 1500 (safe zone).
- **Honesty:** we only show states the tool really displays. If the tool shows "yellow" for missing inputs, the red comes from the spreadsheet hook, not from the tool.
- Learned on the German account: recording the real tool found a real bug (a delta badge compared against an intermediate value while typing). Watch every recording once frame by frame before using it.
