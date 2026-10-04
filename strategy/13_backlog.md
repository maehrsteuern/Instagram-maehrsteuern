# 13 · Automation backlog

As of 10/4/2026. Evaluation and approval by Loris, implementation by Claude. The autopilot was built and hardened on the German sister repo (`Instagram-maehrsteuern`) and carried over to this repo with English names.

## ✅ Carried over from the sister repo (implemented there, renamed here)
**Core**
- **Publishing plan + autopilot** – `automation/plan.json` (English schema, times in ET), `automation/post.py` (`post.yml`, plus cron-job.org every 15 min)
- **Approval issues** – one issue per draft with preview, `go` / `stop` (`automation/approval.py`, `approval.yml`, label `approval`)
- **Stats** – daily (`automation/stats.py`, `automation/insights_full.py`, `stats.yml`), raw data in `automation/stats/`
- **Token refresh** – Instagram (`refresh_ig_token.py`) and Facebook (`refresh_fb_token.py`), monthly via `token.yml`, expiry dates in `automation/key_expiry.json`
- **Status page** – `STATUS.md` + `STATUS.html` (`automation/status.py`, `status_html.py`, `status.yml`), published on GitHub Pages; notes in `automation/status_notes.md`
- **Daily report** in STATUS.md (`automation/daily_report.py`)

**Sprint 1 (sister repo, 10/3)**
- **Watchdog** – one open issue "🚨 Watchdog", comments only on a red workflow or a key < 14 days (`automation/watchdog.py`, runs in the status run, label `watchdog`)
- **Keyword sync** – `automation/interaction.json` is the single source; captions that ask for another keyword show up in STATUS.md under "Needs you"
- **Radar maintenance** – Mondays in the radar issue: 🧹 remove / ➕ add, only checked items are applied
- **First-hour checklist** – after every feed post as a comment in the approval issue
- Actions on Node 24, runner pinned to `ubuntu-24.04`

**Sprint 2 (sister repo, 10/3)**
- **Weekly report + demo source** – Sundays one issue "📊 Week …" (`automation/weekly_report.py`, label `weekly`); demos/ManyChat/source by hand as a comment, plus counted from `strategy/dm_tracking.csv` (column `demo_booked` = `yes`). Automatic: Reclaim books into the main calendar → Apps Script `automation/apps_script/demo_copy.gs` (Loris' Google account) copies only demo bookings, without names/emails, into "maehrtax Autopilot", source from the required booking field "How did you find me?". Rejected: service account reads the main calendar (too broad). Not used: UTM (Reclaim doesn't store it reliably), ManyChat API (Pro only), Reclaim webhooks (Business only).
- **Calendar direct sync** – Google calendar "maehrtax Autopilot" via service account (only this calendar, scope `calendar.events`), every status run, idempotent, post times "busy" for Reclaim, to-dos "free", colors per kind (`automation/calendar_sync.py`, `calendar_events.py`)

**Robustness (sister repo, 10/3)**
- **No double post:** status push with retry; after waiting the plan is re-read (`stop`, new time, `cancelled` still apply); short API hiccups (connection, 5xx) retried 3× – `media_publish` never; a missing permalink after publishing no longer marks the post as `error`
- **No key in repo/log:** IG_TOKEN is stripped from error messages in `plan.json`; the new key is masked and passed via stdin to `gh secret set`; expiry date only updated after a successful replace
- **No lost replies:** `go` / `C12 ok` / follow-ups run in their own concurrency group per comment
- **Push retry** with `rebase --abort` in all scripts
- **Reserve timer:** the status run triggers the token refresh if < 30 days are left; stats retry after 30 min
- **post.yml:** inputs only as environment variables (no command injection)
- **Radar:** backoff on Meta throttling (HTTP 429, codes 4/17/32/613/8000x; 30/90/270 s, respects `Retry-After`), abort instead of hammering; only permanent errors lead to 🧹 suggestions; 1 s pause per account
- **Weekly report:** demo copies read without full-text search and with paging; follow-ups only at line start / after a comma
- **One-time reminders:** `automation/reminders.json` → "Needs you" in STATUS.md + event in the autopilot calendar (kind `reminder`, "free")

Open (small, carried over): `insights_full.py` re-fetches the full history daily; `status.py` reads the whole git log; merge the push loops into one module.

## 🆕 New for the US (proposed – Loris decides)
| # | Item | What | Effort |
|---|---|---|---|
| U1 | **ET everywhere** | Verify every script uses `America/New_York` for plan times, calendar events and reports; Berlin time only in Loris' reminders | small – check during renaming |
| U2 | **Compliance check in approval** | `approval.py` warns in the issue if an educational caption lacks the footer `Educational content – not tax, legal or accounting advice.`, if a tax-law post has no `fact_check.md`, or if text contains "CPA", "EA", "former IRS" as a self-description | small |
| U3 | **Boost candidate** | Weekly report computes (saves + shares) / reach per Reel and names the best Reel of the last 14 days as the ad candidate (from week 3) | small |
| U4 | **Lead magnet + ad in the weekly report** | Extra lines: checklist sent (ManyChat, by hand), ad spend + cost per conversation (by hand, e.g. `ad 35/14` = $ spent / conversations) | small |
| U5 | **Content Factory routine** | Recurring Claude routine Mon + Thu (`15_content_factory.md`) | prompt done |
| U6 | **Sticker-story reminders** | Calendar reminders for `manual` 9:00 AM ET stories at 3:00 PM Berlin | probably already covered by calendar sync – verify |
| U7 | **DST gap warning** | STATUS.md note while Berlin = ET + 5 h (Oct 25–31, Mar 14–27) | tiny |
| U8 | **US holiday awareness** | Content Factory skips/lightens Thanksgiving week and Dec 24 – Jan 1 (list in `15_content_factory.md`) | prompt only |
| U9 | **Caption checks** | US number/date format lint (`$1,250.50`, `10/15/2026`), hashtag count 3–5 | small |

## ⏸️ Deferred until ~15 posts
Before that there's not enough data to conclude anything.
- **Feedback loop to the Content Factory** – 48 h after each post rate saves/shares per reach, result in `strategy/what_works.md`, the factory reads it
- **Topic list from comments and radar** – weekly collect questions and frequent terms (Claude, approx. $0.50/month) → `strategy/topics.md`
- **Best times monthly** – recommendation from followers' active times, never switched automatically
- **Collab follow-up** – 7 days after a checked request without a reply, a hint in the radar issue

## ❌ Rejected
- **LinkedIn via API** – document posts need the restricted Community Management API; 2 minutes by hand are cheaper (and LinkedIn is off by default for the US)
- **Cross-posting from @maehrsteuern** – German content is never posted 1:1 (brief)

## Principles
- Never automatically post (except approved plan entries), comment, follow, like or send DMs. DMs only via ManyChat.
- Keep notifications low, bundle them (one issue per purpose, status in the issue body instead of new comments).
- Costs, upgrades, new access: ask first.
