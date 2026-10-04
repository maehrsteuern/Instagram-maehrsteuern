# 16 · US growth playbook

How @maehrtax grows from zero to leads in the US. Source of truth: `00_us_brief.md`. This file explains the *why* and the decision rules; the weekly slots are in `03_content_calendar.md`, the Reel craft in `08`–`10`.

## 1 · Why Reel-first in the US
- **US users consume more short video** and react strongly to **satisfying, fast, visual content**. A new account has no followers to show carousels to – Reels are the only format that reaches non-followers at scale.
- **The algorithm rewards sends and watch time** (`11_instagram_knowledge.md`). Short, loopable Reels with a visible transformation produce both.
- **Carousels still convert** (trust, saves, inquiries) – so they stay at 2 per week, each with a companion Reel that pulls new people to it.
- Result: **5 Reels (Mon–Fri 12:30 PM ET) + 2 carousels (Tue/Thu 7:30 PM ET) + 1 story per day.** The German account posts ~2 Reels a week; the US plan is deliberately more aggressive.

## 2 · The 5 pillars
| # | Pillar | Job in the funnel | Format | CTA | Weekly share |
|---|---|---|---|---|---|
| 1 | **Demo** – tool in action | Leads | Reel 8–25 s | DM TOOL | 1 Reel |
| 2 | **Spreadsheet pain → fix** | Trust, leads | Carousel 6–8 slides + companion Reel | DM TOOL | 1 carousel (+ Reel) |
| 3 | **Tax know-how that computes** | Reach, saves | Carousel or number Reel (one thesis + one number, 8–12 s) | Save this | 1 Reel, 1 carousel |
| 4 | **Behind the code** – person & story | Likability, follows | Reel with face/voice | Follow | every 2 weeks |
| 5 | **Satisfying software** | Reach, shares | Loopable Reel 6–12 s, no talking | Follow / DM TOOL | ≥ 2 Reels |

## 3 · Satisfying software – principles
The format that is new for the US. Built for **shares and rewatches**, not for explanation. Full recipes: `10_software_reel_concept.md`, format S.
1. **One motion, one payoff** – a single continuous transformation, no story, no talking.
2. **"Before" readable in 0.5 s** – red cells, `#REF!`, 47 tabs, 4,000 unsorted rows.
3. **Physical-looking payoff** – cascade, wave of green, counter rolling to an exact number, rows snapping into place.
4. **Perfect loop** – last frame flows into the first; rewatches push watch time past 100 %.
5. **Sound is half of it** – soft clicks synced to every change, one clean "done" sound, no voice.
6. **Calm framing** – centered, big type, dark brand background, green glow on the "after".
7. **Hold the "after" ~1 s** before the loop.
8. **Hook ≤ 5 words** – "4,000 rows. One click." / "Before. After."
9. **Small CTA bar** in the last second, never a static end card.
10. **Honest** – only states the tool really shows.

## 4 · Hook formulas (≤ 1.5 s, on screen from frame 1)
| Formula | Example |
|---|---|
| Deadline + pain | "3 days to Oct 15. Then this: #REF!" |
| Time vs. time | "2 hours in Excel. 17 seconds in code." |
| Count + click | "4,000 rows. One click." |
| Number + change | "+$1,000,000 deductible. One line changed." |
| Stop doing X | "Stop typing 21% into 400 cells." |
| Hot take | "ChatGPT shouldn't do your tax math." |
| Auditor angle | "Your auditor asks: where's this number from?" |
| Identity callout | "If you own the tax provision, watch this." |
| German angle | "Trained by the most rule-obsessed tax office on earth." |
Rules and full library: `08_hooks.md`.

## 5 · Conversion funnel – numbers to watch
```
Reel reach ──► profile visit ──► "TOOL" (comment/DM) ──► ManyChat DM ──► link click ──► booked demo ──► project
                                         └──────────────► checklist PDF (not ready to talk) ──► later demo
```
| Step | Metric | Starting target (assumption – calibrate after 4 weeks) | Where |
|---|---|---|---|
| Reach → attention | Skip rate · avg. watch time | < 50 % · ≥ 70 % of length | Reel insights |
| Attention → value | (saves + shares) / reach | ≥ 2 % | Reel insights |
| Reach → profile | Profile visits / reach | ≥ 1 % | account insights |
| Reach → lead | TOOL per 1,000 reach | ≥ 1 | ManyChat + `dm_tracking.csv` |
| Lead → click | Link clicks / DMs sent | ≥ 30 % | ManyChat insights |
| Click → demo | Bookings / clicks | ≥ 10 % | Reclaim (via demo copy in the calendar) |
| Ad | Cost per started conversation | ≤ $3 | Ads Manager |
Track weekly in `06_analytics.md`. If a step is far below target, fix that step first (e.g. many TOOL DMs but no clicks → DM text; many clicks but no bookings → booking page).

## 6 · Lead magnet: "The Spreadsheet-to-Code Checklist for Tax Teams"
For people who aren't ready to talk. Delivered by ManyChat with every TOOL DM (`04_dm_funnel.md`). 2–3 pages PDF in brand design, US English, demo data only, footer `Educational content – not tax, legal or accounting advice.`

Content outline (12 checks – "how many can you tick?"):
1. Every input has **one** source (no copy-paste from the trial balance)
2. Tax rates are **parameters**, never typed into cells
3. **No external links** between workbooks
4. Every number is **traceable** to its source in one click (audit trail)
5. **Version history** and a change log exist
6. **Tie-outs are built in** and turn red on a difference
7. **Rounding rules** are explicit and in one place
8. Inputs, calculations and outputs are **separated**
9. Next period **rolls forward** without a rebuild
10. Review and sign-off are **documented** (SOX-ready)
11. **AI reads, classifies and drafts – code calculates** (clear line)
12. You know **which workflow to automate first**: score = frequency × hours × error risk

Scoring: 10–12 ✅ you're ahead · 6–9 ✅ pick one workflow and fix it · 0–5 ✅ start with checks 2, 3 and 6 this month. Last page: "Want to see it for your workflow? DM TOOL or book the free 20-min demo" + booking link.
To do: build the PDF (template in `templates/system/`, rendered like the carousels), host it, put the link into ManyChat. Teased in carousel `13-automate-first` (10/22) and story `13-story-cta` (10/23).

## 7 · Paid boost rules (from week 3, Mon 10/26)
- **Pick:** the Reel with the best **(saves + shares) / reach** of the last 14 days, minimum 500 reach. Never a pillar-4 Reel (personal stories don't sell to strangers). Loris confirms.
- **Setup:** click-to-DM ad, **USD 5/day, United States only**, age 25–55, interests accounting, tax, CPA, corporate finance; placement Instagram feed + Reels; prefilled "TOOL" → ManyChat. Details: `12_interaction.md` section 5, Chrome module 2.
- **Loris pays and submits himself.** Claude/Chrome only prepare.
- **One ad at a time.** Monthly cap $150 – anything above: ask Loris first.
- **Ad text** carries the compliance footer.
- **7-day check:** cost per started conversation ≤ $3 → keep; $3–5 → narrow the audience (only "CPA" / "tax"); > $5 → swap the Reel. 0 bookings after 14 days → swap the Reel or pause.
- **To research:** whether Meta asks for a special ad category (e.g. financial products and services) for this kind of ad – that would limit targeting options.

## 8 · Collab strategy
- **Who:** US tax/accounting creators and small CPA firms with 1,000–50,000 followers (small accounts say yes more often). Never competitors' brand accounts, never government accounts.
- **How:** comment honestly 2–3 times first (radar), then one request per week (radar issue, Mondays). Drafts in `12_interaction.md`.
- **Formats that fit us:** "CPA vs. code" (they explain the rule, Loris shows the calculation), satisfying duet (their messy demo workbook → cleaned up), guest slide, story Q&A, later a 20-min live.
- **Goal:** borrowed trust + their audience. A collab post (both as authors) counts double: reach on both profiles.
- Never pay for a collab without asking Loris. No invented collaboration claims.

## 9 · What to stop (or change) after 4 weeks (review 11/8/2026)
Decide with numbers from `06_analytics.md`, not by gut. Stop or change:
| Signal after 4 weeks | Action |
|---|---|
| A pillar with (saves + shares) / reach < 1 % **and** 0 TOOL | halve it (every 2 weeks), test a new hook pattern |
| Satisfying Reels with skip rate > 60 % | change the recipe (stronger "before", shorter, faster payoff) |
| Evening carousels reach < 50 % of the Reels' median **and** < 10 saves | move carousels to 8:00 AM ET or 12:30 PM on a non-Reel day |
| Ad: cost per conversation > $5 after 2 Reels tested | pause the ad, put the budget on hold |
| Sticker stories with < 3 replies each | cut to 3 per week |
| Hashtags with no measurable reach | drop to 3 per post |
| A hook pattern that never beats the median | retire it from `08_hooks.md` |
| ManyChat follow-up with < 5 % clicks | rewrite message ④ |
Never stop: compliance footer, fact checks, the TOOL keyword, demo data only.
