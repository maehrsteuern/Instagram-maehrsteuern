# 3 · Content calendar – 5 Reels + 2 carousels + daily stories

All times **US Eastern (ET, America/New_York)**. Loris lives in Germany: Berlin = ET + 6 h (exception: Oct 25 – Oct 31, 2026 and Mar 14 – Mar 27, 2027 it is ET + 5 h, because Europe and the US switch daylight saving time on different dates). The autopilot always posts in ET, so this only matters for Loris' own reminders.

## Weekly rhythm (from Oct 12, 2026)
| Day | 9:00 AM ET | 12:30 PM ET | 7:30 PM ET | Who |
|---|---|---|---|---|
| **Mon** | Story (poll/question) | **Reel** | – | autopilot (sticker story: Loris) |
| **Tue** | – | **Reel** | **Carousel** + teaser story 7:35 PM | autopilot |
| **Wed** | Story | **Reel** | – | autopilot / Loris |
| **Thu** | Story | **Reel** | **Carousel** + teaser story 7:35 PM | autopilot / Loris |
| **Fri** | Story | **Reel** | – | autopilot / Loris |
| **Sat** | Story (recap / quiz answer) | – | – | autopilot |
| **Sun** | – | – | (free – the Content Factory fills it only with a strong Reel) | – |

Production and approval around it:
| When | What | Who |
|---|---|---|
| **Mon + Thu 8:47 AM Berlin** (2:47 AM ET) | Content Factory builds the next posts → approval issue with preview (`15_content_factory.md`) | Claude |
| **Mon + Thu 7:00 PM Berlin** (1:00 PM ET) | quick check: `go` or `stop` in the approval issue (calendar reminds you) | Loris, 5 min |
| daily | answer comments and DMs; ManyChat handles "TOOL" instantly | Loris |
| daily, morning Berlin | radar issue: comment on 5–8 US posts (`12_interaction.md`) | Loris, 10 min |

Why these slots:
- **12:30 PM ET** = lunch scroll on the East Coast and 9:30 AM on the West Coast; 6:30 PM in Berlin, so Loris can sit in the first hour of every Reel.
- **7:30 PM ET** = evening scroll, when professionals have time to swipe and save a carousel. It is 1:30 AM in Berlin – the first hour is covered by ManyChat (TOOL) and the comment helper; Loris answers the rest the next morning. Check after 4 weeks whether evening carousels lose to the Reels; fallback slot: 8:00 AM ET (2:00 PM Berlin).
- **9:00 AM ET** stories = morning check-in; sticker stories (poll, question, quiz) cannot be posted through the API → status `manual`, Loris posts them in the app between 9:00 AM and noon ET (3–6 PM Berlin).

**Volume:** 5 Reels + 2 carousels per week (Reel-first, see `16_us_growth_playbook.md`). Pillars rotate over the slots:
- Reels Mon–Fri: at least 2 × **Satisfying software** (pillar 5), 1 × **Demo** (1), 1 × **number Reel** (3), 1 × companion Reel to the carousel or **Behind the code** (4, at least every 2 weeks)
- Carousels Tue/Thu: **Spreadsheet pain → fix** (2) and **Tax know-how** (3), alternating

## Launch plan Oct 11–25, 2026
All entries start as `draft` in `automation/plan.json`. Nothing posts before Loris approves in the approval issue ("go").

| ID | When (ET) | Type | Folder `posts/…` | Pillar | Topic / hook |
|---|---|---|---|---|---|
| 00-launch-1..3 | Sun 10/11 9:00/9:01/9:02 AM | Story ×3 | `00_2026-10-11_launch_stories` | 4 | Hi, I'm Loris · What I build · How the free demo works |
| 03-story-poll | Mon 10/12 9:00 AM | Story | `03_2026-10-13_excel_mistakes` | – | poll: "How many spreadsheets feed your provision?" |
| 01-reel-ref-error | Mon 10/12 12:30 PM | Reel | `01_2026-10-12_reel_ref_error` | 1 | "3 days to the Oct 15 deadline. Then this: #REF!" → red → tool → green |
| 00-intro | Mon 10/12 7:30 PM | Carousel | `00_2026-10-12_intro` | 4 | "New here? Quick intro 👋" (pin) |
| 00-story-teaser | Mon 10/12 7:35 PM | Story | `00_2026-10-12_intro` | – | teaser intro |
| 02-reel-split | Tue 10/13 12:30 PM | Reel | `02_2026-10-13_reel_split` | 1 | Split screen: spreadsheet (2 h) vs. tool (17 s) |
| 03-excel-mistakes | Tue 10/13 7:30 PM | Carousel | `03_2026-10-13_excel_mistakes` | 2 | "5 spreadsheet mistakes in your tax provision" |
| 03-story-teaser | Tue 10/13 7:35 PM | Story | `03_2026-10-13_excel_mistakes` | – | teaser |
| 04-story-question | Wed 10/14 9:00 AM | Story | `04_2026-10-14_reel_hardcoded_rate` | – | "Your worst #REF! story?" |
| 04-reel-hardcoded-rate | Wed 10/14 12:30 PM | Reel | `04_2026-10-14_reel_hardcoded_rate` | 5 | "21% typed into 400 cells" → one parameter → all cells update (satisfying) |
| 05-story-deadline | Thu 10/15 9:00 AM | Story | `05_2026-10-15_reel_deadline_night` | – | poll "Filing today?" |
| 05-reel-deadline-night | Thu 10/15 12:30 PM | Reel | `05_2026-10-15_reel_deadline_night` | 5 | "Oct 15, 11:48 PM. Still in Excel?" – chaos → clean |
| 06-163j-ebitda | Thu 10/15 7:30 PM | Carousel | `06_2026-10-15_163j_ebitda` | 3 | "§ 163(j) is back on EBITDA – your interest limit just grew" |
| 06-story-teaser | Thu 10/15 7:35 PM | Story | `06_2026-10-15_163j_ebitda` | – | teaser |
| 06-story-quiz | Fri 10/16 9:00 AM | Story | `06_2026-10-15_163j_ebitda` | – | quiz: "$4M interest, $14M EBITDA – how much is deductible?" |
| 07-reel-163j-number | Fri 10/16 12:30 PM | Reel | `07_2026-10-16_reel_163j_number` | 3 | number Reel: "+$1,000,000 deductible. One line changed." |
| 06-story-answer | Sat 10/17 9:00 AM | Story | `06_2026-10-15_163j_ebitda` | – | quiz answer: all $4.0M |
| 10-story-question | Mon 10/19 9:00 AM | Story | `10_2026-10-20_174a_deferred_taxes` | – | "Did you capitalize R&D in 2022–2024?" |
| 08-reel-4000-rows | Mon 10/19 12:30 PM | Reel | `08_2026-10-19_reel_4000_rows` | 5 | "4,000 rows. One click." (satisfying loop) |
| 09-reel-my-story | Tue 10/20 12:30 PM | Reel | `09_2026-10-20_reel_my_story` | 4 | "From the German tax office to building tax tools" – **waits for Loris' concept + English voice note** |
| 10-174a-deferred-taxes | Tue 10/20 7:30 PM | Carousel | `10_2026-10-20_174a_deferred_taxes` | 3 | "§ 174A: R&D expensing is back – what it does to your deferred taxes" |
| 10-story-teaser | Tue 10/20 7:35 PM | Story | `10_2026-10-20_174a_deferred_taxes` | – | teaser |
| 12-story-poll | Wed 10/21 9:00 AM | Story | `12_2026-10-22_reel_ai_vs_code` | – | poll "AI or code for tax math?" |
| 11-reel-163j-demo | Wed 10/21 12:30 PM | Reel | `11_2026-10-21_reel_163j_demo` | 1 | screen recording: 163(j) calculator, EBIT → EBITDA, 12 s |
| 12-reel-ai-vs-code | Thu 10/22 12:30 PM | Reel | `12_2026-10-22_reel_ai_vs_code` | 2 | "Why ChatGPT shouldn't do your tax math" |
| 13-automate-first | Thu 10/22 7:30 PM | Carousel | `13_2026-10-22_automate_first` | 2 | "3 tax workflows I'd automate first" + checklist lead magnet |
| 13-story-teaser | Thu 10/22 7:35 PM | Story | `13_2026-10-22_automate_first` | – | teaser |
| 13-story-cta | Fri 10/23 9:00 AM | Story | `13_2026-10-22_automate_first` | – | "DM TOOL → checklist + demo" |
| 14-reel-174a-number | Fri 10/23 12:30 PM | Reel | `14_2026-10-23_reel_174a_number` | 3 | "+$378,000 cash in year 1. Same R&D." |

Demo numbers are fixed in `00_us_brief.md` (§ 163(j), § 174A, provision example "Northwind Manufacturing Inc.") – all posts use exactly those.

**After the launch (from Mon 10/26):** the Content Factory fills the weekly rhythm from the backlog below. **Week 3 = paid boost starts** (best Reel by (saves + shares) / reach → click-to-DM ad, USD 5/day, see `12_interaction.md`).

## Idea backlog November 2026 – January 2027 (for the Content Factory)
Every tax-law post gets a `fact_check.md` (source, as-of date, what Loris must double-check). Items marked ⚠️ need extra care before approval.

### November – year-end provision season starts
| Pillar | Format | Topic / hook | Group | Note |
|---|---|---|---|---|
| 3 | Carousel | "Year-end provision: 7 things you can prep in November" (save this) | Tax teams | Evergreen, strong save candidate |
| 1 | Reel | "Deferred tax rollforward. One click." – opening balance → movements → closing balance, ties out | Tax teams | Demo company Northwind |
| 2 | Carousel + companion Reel | "Why your rate reconciliation never ties – 5 usual suspects" | Tax teams, CPA firms | Hook pattern "real case" |
| 3 | Number Reel | "100% bonus depreciation is permanent again" – one asset, one number | Tax teams, SMB | ⚠️ OBBBA: property acquired after Jan 19, 2025 |
| 5 | Satisfying Reel | "47 tabs → one dashboard" (tabs collapse into one clean view, loop) | Everyone | |
| 3 | Carousel | "Sales tax economic nexus: the $100,000 line (and why it's not the same everywhere)" | SMB, CPA firms | ⚠️ thresholds vary by state – show one example state, link no list |
| 5 | Satisfying Reel | "600 vendors. 3 missing TINs. Found in 2 seconds." (1099 vendor check, list turns green) | CPA firms, SMB | |
| 3 | Number Reel | "The 1099-NEC threshold just moved from $600 to $2,000" | SMB, freelancers | ⚠️ OBBBA, payments made after Dec 31, 2025 – verify before approval |
| 4 | Reel | "What the German tax office taught me about audit trails" | Everyone | personal story, voice note |
| 2 | Carousel | "Spreadsheet vs. tax software vs. small tool – an honest comparison" | Tax teams | ends with poll story "Team code or team Excel?" |
| – | – | **Thanksgiving week (Thu 11/26):** keep Mon–Wed, Thu/Fri light (one satisfying Reel, no carousel) | – | US audience is offline |

### December – close, Q4 estimates, busy-season prep
| Pillar | Format | Topic / hook | Group | Note |
|---|---|---|---|---|
| 3 | Number Reel | "Jan 15: your Q4 estimated tax – one number to check today" | SMB, freelancers | ⚠️ deadline Fri 1/15/2027; no individual advice |
| 2 | Carousel | "The provision spreadsheet that breaks every December – and how to fix it" | Tax teams | |
| 2 | Carousel | "3 workflows to automate before busy season" | CPA firms | lead magnet tie-in (checklist) |
| 5 | Satisfying Reel | "Tie-out: 1,200 rows, 0 differences" (red cells clear one by one) | Everyone | loop |
| 1 | Reel | "SOX question: where does this number come from? – one click to the source" | Tax teams | audit-trail demo |
| 4 | Reel | "I built a 1099 checker in a weekend – here's what broke" | Everyone | Behind the code |
| 3 | Carousel | "§ 174A: 5 questions for your year-end provision" (follow-up to 10/20) | Tax teams | ⚠️ catch-up / transition rules – fact-check |
| – | – | **Dec 24 – Jan 1:** reduce to 3 Reels/week, no carousels; schedule evergreen satisfying Reels | – | holiday dip |

### January – deadlines as hooks, busy season
| Pillar | Format | Topic / hook | Group | Note |
|---|---|---|---|---|
| 5 | Satisfying Reel | "5 spreadsheet habits to quit in 2027" (each one deleted on screen) | Everyone | New Year hook |
| 3 | Number Reel | "Jan 15. Q4 estimates. Still guessing?" | SMB, freelancers | post Mon 1/11 or Tue 1/12 |
| 3 | Carousel | "1099-NEC & W-2: what's due and when" | SMB, CPA firms | ⚠️ Jan 31, 2027 is a Sunday → due **Mon 2/1/2027** – verify |
| 1 | Reel | "1099 prep: vendor list → clean file in 17 seconds" | CPA firms | demo |
| 2 | Carousel | "Busy season survival: 5 recurring calcs that should never be manual" | CPA firms | DM TOOL |
| 3 | Carousel | "Mar 15 is closer than you think – partnerships & S corps checklist" | CPA firms | post late January |
| 2 | Reel | "AI vs. code, part 2: let AI read the K-1, let code do the math" | Tax teams, CPA firms | series |
| 1 | Reel | "Q4 provision for the 10-K: the 3 numbers your auditor checks first" | Tax teams | ⚠️ keep general, no audit advice |

### Evergreen (any time a slot is free)
- Series "Spreadsheet mistake #1, #2, #3 …" (hard-coded rates, broken links, manual rounding, copy-paste years, hidden rows)
- Series "AI vs. code" (where AI helps: reading, classifying, drafting · where code must calculate)
- "Trained by the German tax office" mini-stories (pillar 4): one German rule-obsession moment → what it means for US audit trails
- State apportionment explained with one example (pillar 3, ⚠️ fact-check)

**After week 4 (11/8) and week 8 (12/6):** fill in the KPIs from `01_positioning.md` in `06_analytics.md`, adjust the weakest pillar, plan the next 4 weeks.

## Workflow per post (checklist)
1. Take the topic from the tables, write the hook in one sentence (patterns and rules: `08_hooks.md`)
   – clarify: **Who sends this to whom?** and which **search terms** belong on slide 1 / in the first caption line / in the spoken text (`11_instagram_knowledge.md`)
2. Write the texts into a job file, e.g. `templates/system/jobs/p15_….json` (copy an existing job as a template)
3. Render images: `node templates/system/render.mjs templates/system/jobs/p15_….json`
4. Reels: cut list like `templates/system/cuts/p02_reel_split.json`, then `python3 templates/system/reel.py templates/system/cuts/….json`
5. Caption with the template below; tax law → `fact_check.md` in the post folder
6. Add the entry to `automation/plan.json` as `draft` (teaser story 5 minutes after every carousel)

## Caption template
```
[Hook from slide 1 / the Reel, one line – with the search term]

[2–4 short lines: problem → what the tool / the know-how solves – one number]

[CTA by pillar:]
Demo / In practice:  💬 Comment or DM "TOOL" – I'll send you the demo + the free checklist.
Know-how:            📌 Save this for your next close.
Behind the code:     ➕ Follow for more Tax × Code.
Satisfying:          ➕ Follow for more – or DM "TOOL" if your spreadsheet looks like the "before".

Educational content – not tax, legal or accounting advice.

#taxprofessional #accounting #excel #taxautomation #asc740
```
Hashtags: 3–5 are enough. Base set plus 1–2 for the topic (e.g. `#cpa`, `#salestax`, `#accountingstudent`, `#busyseason`, `#taxprovision`). Max. 30 different hashtags in 7 days.
