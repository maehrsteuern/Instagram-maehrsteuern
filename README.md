# maehrtax – Instagram (US)

Content, strategy and autopilot for **@maehrtax** – "Tax × Code: tax know-how that computes." The US English sister account of the German [@maehrsteuern](https://github.com/maehrsteuern/Instagram-maehrsteuern) (separate repo, never cross-posted 1:1).

**Start here:** `strategy/00_us_brief.md` – the source of truth for everything in this repo.

## Autopilot
`automation/plan.json` is the publishing plan (times in **US Eastern, ET**). GitHub Actions posts approved entries at the planned time (`.github/workflows/post.yml`, plus an external cron every 15 min), opens one approval issue per draft (`approval.yml` – answer `go` / `stop`), fetches stats daily (`stats.yml`), refreshes the Instagram/Facebook tokens (`token.yml`), opens a daily radar issue to comment on US posts (`radar.yml`), reports new comments with reply suggestions every 15 min (`comments.yml`), writes a weekly report every Sunday (`weekly_report.yml`) and fetches royalty-free music (`music.yml`). Setup: `SETUP.md`.

New posts come from the **Content Factory** – a Claude routine every Mon + Thu that builds the next posts as drafts (`strategy/15_content_factory.md`). Nothing goes live without Loris' `go`.

## Status page
`STATUS.md` – what goes live next, what needs you, automation health and a log of every change. Regenerated after every push and every automation run (`automation/status.py`, `.github/workflows/status.yml`); notes for it in `automation/status_notes.md`. The same status as a visual page: `STATUS.html` (tiles, 4-week calendar, charts, filterable log; `automation/status_html.py`), published on GitHub Pages: https://maehrsteuern.github.io/maehrtax---instagram/
Never edit STATUS.md / STATUS.html by hand.

**Calendar:** direct sync into the Google calendar "maehrtax Autopilot" (`automation/calendar_sync.py`, every status run): post times, open approvals, manual posts, missing clips/music, reminders – colored by kind; post times "busy" for Reclaim, to-dos "free".

## Structure
| Path | What |
|---|---|
| `strategy/00_us_brief.md` | **Source of truth:** account, bio, positioning, audiences, pillars, US topics, demo numbers, brand, weekly rhythm, launch plan, paths |
| `strategy/01_positioning.md` | Core line, ranked audiences, 5 content pillars, formats, tone, KPIs |
| `strategy/02_bio_highlights.md` | Name field, bio, category, link, highlights incl. FAQ texts, pinned posts |
| `strategy/03_content_calendar.md` | Weekly ET rhythm, launch plan Oct 11–25, idea backlog Nov–Jan, caption template |
| `strategy/04_dm_funnel.md` | ManyChat flow "TOOL" → demo video + booking link + checklist, follow-up, objection replies |
| `strategy/05_publishing.md` | **Schedule with ET times, how approval works, checklist before "go"** |
| `strategy/06_analytics.md` | Evaluation template: KPIs, weekly table, per-post tables, funnel |
| `strategy/07_demo_video.md` | Script for the 60–90 s demo video |
| `strategy/08_demo_reel_formula.md` | Structure for demo Reels (pain → cut → payoff → CTA) |
| `strategy/08_hooks.md` | Hook rules, building blocks, US formulas, variants for the launch posts |
| `strategy/09_reel_rules.md` | Reel rules: hook, voice, AI clips, sound, cuts, safe zone, colors |
| `strategy/10_software_reel_concept.md` | Reel formats for software: split screen, demo recording, face + screen, **satisfying software**; recordings |
| `strategy/11_instagram_knowledge.md` | Algorithm signals, shares/saves, search, series, US seasons, selling without cold outreach |
| `strategy/12_interaction.md` | **Second pillar interaction:** radar, DM drafts, comment helper, click-to-DM ad (USD), collabs, LinkedIn (off), limits |
| `strategy/13_backlog.md` | Automation backlog: carried over, new for the US, deferred, rejected |
| `strategy/14_chrome_modules.md` | Full prompt for Claude in Chrome (modules A, 1–6) + schedule |
| `strategy/15_content_factory.md` | Prompt for the recurring Content Factory routine (Mon + Thu) |
| `strategy/16_us_growth_playbook.md` | Why Reel-first, satisfying principles, funnel numbers, lead magnet, paid boost, collabs, what to stop |
| `strategy/17_cowork_prompt.md` | Cowork prompt to set up the account, Meta, ManyChat, Reclaim |
| `strategy/competition.md` | US competitor check (monthly, Chrome module 6) |
| `strategy/dm_tracking.csv` | Lead tracking (no full names, no companies) |
| `automation/plan.json` | Plan + status (`draft` → `approved` → `published` · `manual` · `waiting_*` · `error` · `cancelled`) |
| `automation/post.py`, `approval.py` | Posting at the planned time · approval issues (`go` / `stop`) |
| `automation/stats.py`, `insights_full.py` | Daily stats, raw data in `automation/stats/` |
| `automation/refresh_ig_token.py`, `refresh_fb_token.py` | Token refresh (expiry dates in `automation/key_expiry.json`) |
| `automation/comments.py` | Comment helper: issue "💬 Reply to comments" with suggestions (`C12 ok`) |
| `automation/radar.py` | Daily radar issue: US posts to comment on, DM drafts, Monday collab + maintenance |
| `automation/linkedin.py` | LinkedIn packages per carousel (off by default) |
| `automation/ai.py` | Shared Claude access for suggestions |
| `automation/calendar_events.py`, `calendar_sync.py` | Events from the plan → Google calendar "maehrtax Autopilot" |
| `automation/watchdog.py` | One issue "🚨 Watchdog" on a red workflow or a key < 14 days |
| `automation/weekly_report.py` | Sunday issue "📊 Week …": followers, views, top posts, radar, funnel; follow-ups `demos 2` / `manychat 14/6` |
| `automation/daily_report.py` | Daily report section in STATUS.md |
| `automation/status.py`, `status_html.py` | STATUS.md + STATUS.html |
| `automation/fetch_music.py` | Royalty-free music into `music/` |
| `automation/apps_script/demo_copy.gs` | Apps Script (runs in Loris' Google account): copies Reclaim demo bookings without names/emails into "maehrtax Autopilot" |
| `automation/interaction.json` | Radar accounts, hashtags, ManyChat keywords, limits |
| `automation/reminders.json`, `status_notes.md` | One-time reminders · notes for STATUS.md |
| `templates/system/` | Image/video templates (below), `jobs/` render jobs, `cuts/` Reel cut lists, `recordings/` screen recordings |
| `templates/hooks/` | Hook library: ready-made Reel openings |
| `posts/<nr>_<date>_<topic>/` | Finished posts: slides or Reel, cover, stories, `caption.txt`, `fact_check.md` |
| `assets/` | Brand images, highlight covers, FAQ stories, end card |
| `music/` | Royalty-free music (CC0 + Runway), `music/ambience/` sound effects |

Issue labels: `approval`, `comments`, `radar`, `weekly`, `watchdog`.

## Template system (`templates/system/`)
- `carousel.html` (1080×1350; types `title`, `content` with text/list/table, `cta`), `story.html` (1080×1920; `info`, `question`, `teaser`), `highlight.html`, `reel_cover.html`, `overlay.html` (Reel text: hook, bar, end), `traffic_light.html` (status light close-up red/yellow/green), `excel_chaos.html` (spreadsheet chaos stills)
- Colors and fonts centrally in `base.css`; `*word*` in text turns green, `\n` breaks the line; headlines that are too long shrink automatically
- Texts live in job files under `jobs/`. Render from the repo root: `node templates/system/render.mjs templates/system/jobs/<job>.json`
- Reels from stills/camera moves: cut list in `cuts/`, then `python3 templates/system/reel.py templates/system/cuts/<cut>.json` (needs `pip install pillow imageio-ffmpeg`); video montages: `montage.py`; hook library: `build_hooks.py`
- `recordings/`: scripted screen recordings of the English demo tool mock `recordings/demo_tool.html` (fictional "Northwind Manufacturing Inc.")
- Output goes to `posts/` or `assets/`

## Brand
- Line: **Tax × Code** – "Tax know-how that computes." German-trained tax pro and Certified AI Manager (IHK, German Chamber of Commerce) who builds AI and code tools for tax teams.
- CTA: **DM "TOOL"** (also as a comment keyword – ManyChat handles both)
- Colors (same visual family as the German account): background `#0B110E` (gradient to `#153A31`), accent green `#53C3A2`, text `#EAF1EC`, muted `#8FA398`
- Fonts: IBM Plex Serif (headlines), IBM Plex Sans (text), IBM Plex Mono (kicker, handle), Outfit Bold (Reel hooks) – embedded via `templates/fonts.css`
- Style: dark, green glow, calm and premium – Reels cut faster than on the German account

## Profile
- Handle **@maehrtax**, name field `Loris | Tax × Code`, category "Business consultant"
- Bio: "🧠 Tax × Code – tax know-how that computes · ⚙️ AI + code tools for tax teams that actually run · 🇩🇪 German-trained tax pro · Certified AI Manager · 💬 DM "TOOL" → free demo"
- Link: English booking page "Demo + Intro Call (20 min)" (`https://app.reclaim.ai/m/maehrsteuern/maehrtax-demo`, live since 10/4)
- Highlights: Start 👋 · Tools ⚙️ · Learn 📚 · FAQ ❓ · Feedback 🙏
- Launch: Sun 10/11/2026

## Rules
- No real numbers, names or logos from the employer – demo data only; never tag the employer as a location or brand.
- Never claim CPA, EA, tax attorney or former IRS. Use "German-trained tax pro" / "Certified AI Manager (IHK, German Chamber of Commerce)".
- Compliance footer on every educational post: `Educational content – not tax, legal or accounting advice.` Every tax-law post gets a `fact_check.md`.
- No individual tax advice in comments or DMs ("Talk to your CPA about your case – happy to show you the tool.").
- Realistic AI people in a video → switch on Instagram's AI label. Never let AI video generation write on-screen text – text is always added as our own overlay.
