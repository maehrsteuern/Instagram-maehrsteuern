# 5 · Publishing – schedule, approval, checklist

> **Autopilot:** posts and teaser stories go live automatically once they are `approved` in `automation/plan.json` (setup: `SETUP.md`). Only sticker stories (question, poll, quiz) stay manual – calendar reminders in "maehrtax Autopilot" tell you when. The "Plan B: schedule in the Instagram app" section below is the fallback.

All files are ready in `posts/<nr>_<date>_<topic>/`. All times are **ET** (Berlin = ET + 6 h, Oct 25–31 and Mar 14–27: ET + 5 h).

## Posting times
| Slot | What | Why |
|---|---|---|
| **12:30 PM ET** Mon–Fri | Reel | Lunch scroll East Coast = 9:30 AM West Coast. Reels reach mostly non-followers; the hook and watch time matter more than the minute. 6:30 PM in Berlin → Loris can be online for the first hour. |
| **7:30 PM ET** Tue + Thu | Carousel + teaser story 7:35 PM | Evening scroll – professionals have time to swipe and save. 1:30 AM Berlin → ManyChat + comment helper cover the first hour, Loris answers the next morning. |
| **9:00 AM ET** Mon–Sat | Story (sticker / recap) | Morning check-in. Sticker stories are `manual`: post between 9:00 AM and noon ET (3–6 PM Berlin). |

Honestly: there is no guaranteed viral time. **Check after 4 weeks:** profile → Insights → Followers → *Most active times* (shows your audience's local time zone mix). Send Claude the screenshot; times are only changed after your approval.

**The first hour after every Reel (decides reach):**
1. 12:30–1:30 PM ET (6:30–7:30 PM Berlin): stay online and **answer every comment within minutes**, ideally with a counter-question
2. ManyChat answers "TOOL" automatically – check that it fired
3. Share the Reel in your own story; send it by DM to 3–5 people who really care about the topic (sends are the strongest signal)
4. The "first-hour checklist" lands as a comment in the approval issue

## How approval works
1. **Mon + Thu 8:47 AM Berlin** the Content Factory (`15_content_factory.md`) builds the next posts and adds them to `automation/plan.json` as `draft`.
2. The autopilot (`automation/approval.py`, workflow `approval.yml`) opens **one approval issue per post** (label `approval`) with preview images, Reel link, caption, `fact_check.md` and the hook pattern used.
3. **Mon + Thu 7:00 PM Berlin** (calendar reminder) you answer in the issue:
   - `go` → status `approved` → the autopilot posts at the planned time
   - `stop` → stays `draft` / pauses an approved post
   - anything else is ignored; only your own comments count
4. At the planned time `automation/post.py` (workflow `post.yml`, plus cron-job.org every 15 min) publishes → status `published` with the permalink.
5. Errors: status `error` with the message in `plan.json`, GitHub sends an email, the watchdog issue comments.

Status values: `draft` → `approved` → `published` · `manual` (Loris posts in the app) · `waiting_<reason>` (blocked, e.g. `waiting_voice_note`) · `error` · `cancelled`.
**Emergency brake:** Actions → *post* → ⋯ → *Disable workflow* (also stops the cron-job.org triggers).
**Dry run:** Actions → *post* → *Run workflow* → field "test" = entry ID → uploads, publishes nothing.

## Launch week (Oct 11–17, 2026)
| Date | Time (ET) | What | Files | How |
|---|---|---|---|---|
| Sun 10/11 | 9:00–9:02 AM | 3 launch stories → then create highlight "Start 👋" | `00_…launch_stories/story_launch_1–3.png` | 🤖 autopilot + ✋ highlight |
| Mon 10/12 | 9:00 AM | Story poll "How many spreadsheets feed your provision?" | `03_…/story_poll.png` | ✋ manual |
| **Mon 10/12** | **12:30 PM** | **Reel "#REF! – 3 days to Oct 15"** | `01_…/reel.mp4`, `cover.png` | 🤖 |
| **Mon 10/12** | **7:30 PM** | **Intro carousel** → **pin it** | `00_…intro/slide_01–07.png` | 🤖 + ✋ pin |
| Tue 10/13 | 12:30 PM | Reel split screen | `02_…/reel.mp4` | 🤖 |
| Tue 10/13 | 7:30 PM | Carousel "5 spreadsheet mistakes" + teaser 7:35 PM | `03_…/slide_*.png` | 🤖 |
| Wed 10/14 | 9:00 AM / 12:30 PM | Question story · Reel "21% typed into 400 cells" | `04_…` | ✋ / 🤖 |
| Thu 10/15 | 9:00 AM / 12:30 PM / 7:30 PM | Poll "Filing today?" · Reel deadline night · Carousel § 163(j) | `05_…`, `06_…` | ✋ / 🤖 / 🤖 |
| Fri 10/16 | 9:00 AM / 12:30 PM | Quiz story · number Reel § 163(j) | `06_…`, `07_…` | ✋ / 🤖 |
| Sat 10/17 | 9:00 AM | Quiz answer | `06_…/story_answer.png` | 🤖 |

Full plan through Oct 25: `03_content_calendar.md`. Week 2 needs **Loris' concept + English voice note** for "My story" (Tue 10/20) – status `waiting_voice_note` until it's there.

Sticker stories: the image is the template. Put the sticker (question, poll, quiz) on the dashed "STICKER HERE" area in the app.

## Music
Instagram music can't be added through the API. Autopilot Reels have royalty-free music baked in (`music/`). If a Reel should use a trending Instagram sound, it gets status `manual` and you post it yourself (Plan B below).

## Plan B: schedule in the Instagram app
**Carousel**
1. ➕ → *Post* → select multiple → tap `slide_01` to `slide_07` **in order** → check 4:5 → *Next*
2. Paste the caption from `caption.txt`
3. *Advanced settings* → **Schedule this post** → date + time (your phone shows Berlin time – convert from ET!) → *Schedule*

**Reel**
1. ➕ → *Reel* → choose `reel.mp4` → *Next*
2. **Add music** if the video is silent: calm lo-fi/electronic, ideally a trending one (↗ arrow in music search)
3. *Edit cover* → *Add from camera roll* → `cover.png`, keep the grid crop centered
4. Paste caption → *More options* → **Schedule** → date + time

Scheduling works up to 75 days ahead. Scheduled content: profile → ☰ → *Scheduled content*. Stories can't be scheduled in the app – use phone reminders.
**Files to your phone:** open the file on GitHub → ⋯ → *Download* → save to *Photos*.

## Checklist before approval (every post)
- [ ] Hook ≤ 1.5 s (Reel) / ≤ 8 words (slide 1), keeps its promise (`08_hooks.md`)
- [ ] Visible transformation + CTA on screen (Reels)
- [ ] Search term in the first caption line, on slide 1 / in the spoken text
- [ ] **Compliance footer** in the caption of every educational post: `Educational content – not tax, legal or accounting advice.`
- [ ] Tax law → `fact_check.md` in the folder: source, as-of date, what Loris double-checks – **read it before "go"**
- [ ] Demo numbers exactly as in `00_us_brief.md`; demo company "Northwind Manufacturing Inc." only
- [ ] Nothing from the employer (names, numbers, logos, browser tabs, bookmarks)
- [ ] No "CPA", "EA", "tax attorney", "former IRS" anywhere
- [ ] **AI label:** realistic AI people in the video → switch on Instagram's "AI info" label (after posting, in the app); no AI-generated on-screen text
- [ ] US formats: `$1,250.50`, `10/15/2026`, `7:30 PM ET`; US spelling
- [ ] CTA keyword is **TOOL** (no other word – ManyChat only knows TOOL)
- [ ] 3–5 hashtags
- [ ] Reel watched once on a phone: text readable, nothing hidden by the Reels UI (safe zone, `09_reel_rules.md`)

## Before launch (once, by Sun 10/11)
- [ ] Profile set up: name, bio, category, link, highlights (`02_bio_highlights.md`, done by Cowork – `17_cowork_prompt.md`)
- [ ] ManyChat flow live and tested (`04_dm_funnel.md`)
- [ ] Booking page live, placeholder link replaced
- [ ] Secrets set and test run green (`SETUP.md`)
- [ ] Calendar "maehrtax Autopilot" shows the launch posts
