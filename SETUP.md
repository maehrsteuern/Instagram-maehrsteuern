# Setting up the autopilot for @maehrtax (once, approx. 90 minutes)

Most of the Meta experience comes from the German sister repo `Instagram-maehrsteuern` – the existing developer app and Google service account are reused. Account and profile setup is done by Cowork (`strategy/17_cowork_prompt.md`); this file is the technical checklist.

**Never paste tokens, keys or passwords into a chat.** They go straight into GitHub secrets.

## 1 · Create the repo and push this branch as `main`
1. github.com → **New repository** → owner `maehrsteuern`, name **`maehrtax---instagram`**, public (needed for free GitHub Pages and Actions minutes), no README/license (the branch brings everything).
2. Push the prepared branch as `main`:
   ```bash
   git remote add maehrtax https://github.com/maehrsteuern/maehrtax---instagram.git
   git push maehrtax en-neu:main
   ```
3. Repo → **Settings → General → Default branch** = `main`.
4. **Settings → Actions → General → Workflow permissions** = "Read and write permissions" (the autopilot commits status changes back).

## 2 · Instagram account @maehrtax (professional account)
Done by Cowork, module A in `strategy/17_cowork_prompt.md`: new account @maehrtax, switched to a professional (creator) account, category "Business consultant", name field, bio and highlights from `strategy/02_bio_highlights.md`. The account stays empty until launch (Sun 10/11/2026).

## 3 · Meta: reuse the developer app "maehrsteuern Autopilot"
No new app needed – the existing app gets @maehrtax as a second tester. The app stays in development mode; for your own accounts that's enough, no Meta review needed.

**a) Instagram token for posting and stats (`IG_TOKEN`, `IG_USER_ID`)**
1. https://developers.facebook.com → **My Apps** → `maehrsteuern Autopilot`.
2. **App roles → Roles → Add Instagram testers** → `maehrtax`.
3. In Instagram (logged in as @maehrtax): *Settings → Website permissions → Apps and websites → Tester invites* → accept.
4. App → **Use cases** → Instagram API → **Customize** → **API setup with Instagram login** → **Generate access token** → *Add account* → log in as **@maehrtax** → allow all permissions.
5. You now see two values – **copy both** straight into the secrets (step 4):
   - the **access token** (long text, often starts with `IG…`) → `IG_TOKEN`
   - the **Instagram account ID** (a long number) → `IG_USER_ID`

**b) Facebook page for the radar (`FB_TOKEN`, `FB_IG_USER_ID`)**
The Instagram login API can't read other profiles. For the radar (Business Discovery) the route goes through a Facebook page:
1. Create the Facebook page for @maehrtax (e.g. "Loris | Tax × Code", category Business consultant – Cowork module B), post nothing, and link it to @maehrtax: *page settings → Linked accounts → Instagram*.
2. developers.facebook.com → app `maehrsteuern Autopilot` → if not done yet: *Add use case* → **"Manage everything on your Page"** (or "Instagram API with Facebook login").
3. *Tools → Graph API Explorer* → select the app → *Permissions*: `instagram_basic`, `pages_show_list`, `pages_read_engagement`, `business_management` → **Generate Access Token** → confirm with Facebook (select the @maehrtax page).
4. Query in the Explorer: `me/accounts?fields=name,instagram_business_account` → copy the number at `instagram_business_account.id` of the @maehrtax page → secret **`FB_IG_USER_ID`**.
5. Make the token long-lived: *Tools → Access Token Debugger* → paste the token → **"Extend access token"** → copy the new token → secret **`FB_TOKEN`** (valid 60 days, refreshed automatically via step 6 of the table below).
6. For self-refresh: *App settings → Basic* → **App ID** → secret `FB_APP_ID`, **App secret** → secret `FB_APP_SECRET` (requires `GH_PAT`).

Hashtag search needs the extra feature "Instagram Public Content Access" (app review) – prepared by Chrome module 3 (`strategy/14_chrome_modules.md`), not needed for launch.

## 4 · Secrets
Repo **maehrtax---instagram** → **Settings → Secrets and variables → Actions → New repository secret**:

| Name | Value | Needed for |
|---|---|---|
| `IG_TOKEN` | Instagram access token of @maehrtax (step 3a) | posting, stats, comments |
| `IG_USER_ID` | Instagram account ID of @maehrtax (step 3a) | posting, stats |
| `GH_PAT` | fine-grained GitHub token: https://github.com/settings/personal-access-tokens → *Generate new token* → repository **maehrtax---instagram** only → permission **Secrets: Read and write** | token self-refresh |
| `FB_TOKEN` | long-lived Facebook token (step 3b) | radar |
| `FB_IG_USER_ID` | `instagram_business_account.id` of @maehrtax (step 3b) | radar |
| `FB_APP_ID` | App ID of "maehrsteuern Autopilot" | FB token refresh |
| `FB_APP_SECRET` | App secret of "maehrsteuern Autopilot" | FB token refresh |
| `ANTHROPIC_API_KEY` | https://console.anthropic.com → *API Keys → Create Key* (set a monthly limit, e.g. $10) – a separate key per repo makes costs visible | comment/radar suggestions |
| `GOOGLE_SA_KEY` | service account JSON (step 7) | calendar sync, weekly report |
| `GOOGLE_CALENDAR_ID` | ID of the calendar "maehrtax Autopilot" (step 7) | calendar sync, weekly report |

Nobody can see these values, not even in a public repo.

## 5 · Test (5 min)
1. Repo → **Actions** → enable workflows if GitHub asks.
2. **Actions → stats → Run workflow.** Green check = the Instagram connection works. This test only reads and posts nothing.
3. **Dry run posting:** Actions → *post* → *Run workflow* → field "test" = an entry ID (e.g. `00-intro`) → uploads, publishes nothing.
4. **Radar:** Actions → *radar* → *Run workflow* → an issue "📡 Radar …" appears (with an empty account list it says so – fine until Cowork module C has added verified US accounts).
5. **Comments:** Actions → *comments* → *Run workflow* → creates the issue "💬 Reply to comments" at the first new comment.
6. **Status:** Actions → *status* → *Run workflow* → `STATUS.md` + `STATUS.html` are committed.
Issue labels (`approval`, `comments`, `radar`, `weekly`, `watchdog`) are created by the scripts on first use.

## 6 · Reliable timer for posting – cron-job.org (10 min, strongly recommended)
GitHub often runs `schedule` triggers late or not at all on small repos (on the German repo, posting stopped for hours on 9/30/2026). An external timer additionally starts the run every 15 minutes. Double starts don't hurt: runs wait for each other, and only entries that are `approved` and due are posted.

**a) A new GitHub token only for this** (don't reuse `GH_PAT` – that one may change secrets; don't reuse the German `cron-posten` token – it's scoped to the other repo)
1. https://github.com/settings/personal-access-tokens → **Generate new token** (fine-grained)
2. Name `cron-post-maehrtax`, expiration **1 year** (set a calendar reminder to renew)
3. Repository access: **Only select repositories → maehrtax---instagram**
4. Permissions → Repository permissions → **Actions: Read and write** (nothing else)
5. *Generate token* → copy it (starts with `github_pat_…`) – **never into a chat**

**b) Timer on cron-job.org** (same account as for the German repo)
1. https://cron-job.org → **Create cronjob**
2. Title `Instagram post maehrtax`, URL:
   `https://api.github.com/repos/maehrsteuern/maehrtax---instagram/actions/workflows/post.yml/dispatches`
3. Execution schedule: **Every 15 minutes**
4. Tab **Advanced**:
   - Request method: **POST**
   - Headers:
     | Key | Value |
     |---|---|
     | `Authorization` | `Bearer github_pat_…` (your token from a) |
     | `Accept` | `application/vnd.github+json` |
     | `X-GitHub-Api-Version` | `2022-11-28` |
     | `User-Agent` | `cron-job-maehrtax` |
   - Request body: `{"ref":"main"}`
5. Save → **Test run**: response **204** = good. Under Actions → *post* a new run "workflow_dispatch" appears.

Errors: 401 = token wrong/expired · 403/404 = permission "Actions: Read and write" or repo selection missing · 422 = body/branch wrong.
The API version `2022-11-28` is supported by GitHub until March 2028 – switch the header to a newer version before then.

## 7 · Google calendar "maehrtax Autopilot"
Direct sync instead of a subscription: every status run writes the plan's events into the Google calendar **"maehrtax Autopilot"** (`automation/calendar_sync.py`, kinds and colors in `automation/calendar_events.py`). Post times are "busy" → Reclaim won't book a demo on them; to-dos (deliver clips, music, manual stories, approvals) are "free".
1. calendar.google.com → *Other calendars → + → Create new calendar* → name **"maehrtax Autopilot"**, time zone of your choice (events carry their own time zone; post times are ET).
2. Reuse the existing service account from the Google Cloud project `maehrsteuern-autopilot` (Calendar API only, no billing). Recommended: create a **second key** for this repo (Google Cloud → Service accounts → `calendar-sync` → Keys → Add key → JSON), so you can revoke one without breaking the other → secret `GOOGLE_SA_KEY`.
3. Calendar settings → **Share with specific people** → the service account's email (`calendar-sync@…`) → **"Make changes to events"**.
4. Calendar settings → **Integrate calendar → Calendar ID** → secret `GOOGLE_CALENDAR_ID`.
- The sync only touches its own events (marker property), fixed event IDs → no duplicates. Scope in code: `calendar.events` only.
- **Revoke access:** Google Cloud → Service accounts → delete the key, or remove the share in the calendar.
- **Demo bookings for the weekly report:** Reclaim writes bookings into your main calendar. A small Apps Script in your own Google account (`automation/apps_script/demo_copy.gs`, new project "maehrtax Demo Copy" on script.google.com, hourly trigger) copies only "Demo + Intro Call" bookings with an external guest into "maehrtax Autopilot" – with booking date and source ("How did you find me?"), without names and emails. Adjust the settings at the top of the script (target calendar, booking title). The service account never sees your main calendar. Switch off: script.google.com → project → delete the trigger.

## 8 · GitHub Pages
Repo → **Settings → Pages → Build and deployment → Source: "GitHub Actions"**. The status workflow publishes `STATUS.html` to https://maehrsteuern.github.io/maehrtax---instagram/ after the next run.

## 9 · ManyChat for @maehrtax
1. app.manychat.com → new account / channel **Instagram** → connect **@maehrtax** (allow access to messages: Instagram → *Settings → Messages and story replies → Message controls → Connected tools → Allow access to messages* = on).
2. Build the automation "TOOL" exactly as in `strategy/04_dm_funnel.md` (comment + story reply + DM triggers, buttons by group, demo video + booking link + checklist, follow-up after 23 h, rotating public replies).
3. Keywords must match `automation/interaction.json` → `comments.manychat_keywords`.
4. Test from an account that has never messaged @maehrtax: comment "TOOL" → public reply + DM within seconds.
Plan: start on the free/entry plan; upgrades cost money → decide first (Pro is needed from ~1,000 contacts or for the API).
**The scripts in this repo never send DMs** – only ManyChat does.

## 10 · English booking page on Reclaim
1. Reclaim → **Scheduling links → New** → title **"Demo + Intro Call (20 min)"**, 20 minutes, video call link automatic.
2. Language/texts in English; show times in the **invitee's time zone**. Availability: US-friendly hours from Germany, e.g. 6:00–9:00 PM Berlin = 12:00–3:00 PM ET (adjust to your day job).
3. Required question **"How did you find me?"** with options: `Instagram Reel` · `Instagram ad` · `Instagram DM` · `LinkedIn` · `Other` (the demo copy script reads it for the weekly report).
4. Description ends with: "Demo with sample data only – please don't bring client data. Educational content – not tax, legal or accounting advice."
5. ✅ Done 10/4: link is `https://app.reclaim.ai/m/maehrsteuern/maehrtax-demo`, replaced everywhere: Instagram bio link, ManyChat messages, `strategy/02_bio_highlights.md`, `strategy/04_dm_funnel.md`, `strategy/14_chrome_modules.md`, `strategy/12_interaction.md`.

## How it runs afterwards
| When | What happens | Who |
|---|---|---|
| **Mon + Thu 8:47 AM Berlin** | Content Factory builds the next posts and adds them as drafts (`strategy/15_content_factory.md`) | Claude |
| right after | GitHub opens one **approval issue** per post with preview (images, Reel link, caption, fact check) | autopilot |
| **Mon + Thu 7:00 PM Berlin** | Calendar reminder → answer **`go`** or **`stop`** in the issue | Loris |
| Reels Mon–Fri 12:30 PM ET, carousels Tue/Thu 7:30 PM ET, stories 9:00 AM ET | posts and stories go live automatically (sticker stories: by hand) | autopilot / Loris |
| **daily** | stats fetched, daily report in `STATUS.md` | autopilot |
| **daily** | radar issue: US posts to comment on, DM drafts, Mondays collab + maintenance | autopilot + Loris (15 min) |
| every 15 min | new comments with reply suggestions in "💬 Reply to comments" – `C12 ok` posts the reply | autopilot + Loris |
| **Sundays** | weekly report issue "📊 Week …" – add demos and ManyChat numbers as a comment (`demos 2`, `manychat 14/6`) | autopilot + Loris (2 min) |
| **monthly** | Instagram and Facebook tokens are refreshed (needs `GH_PAT`) | autopilot |

**Approvals:** https://github.com/maehrsteuern/maehrtax---instagram/issues?q=is%3Aopen+label%3Aapproval
Only your own comments count. `go` = schedule, `stop` = pause, everything else is ignored.
**Emergency brake:** Actions → *post* → ⋯ → *Disable workflow* (also stops the cron-job.org triggers).
**Errors:** shown in `automation/plan.json` at the entry (`"status": "error"`), GitHub emails you, the watchdog issue comments.
**Dry run:** Actions → *post* → *Run workflow* → field "test" = entry ID → uploads, publishes nothing.
