# 12 · Second pillar: interaction (reach + contacts)

Goal: more reach and real contacts with US tax teams, CPA firms and tax creators. It takes **~15 min a day** and uses **official channels only** – no bot that follows, likes or sends mass DMs.
Why: messaging other accounts through the API isn't possible, bots violate Instagram's terms (account restrictions), and unsolicited sales DMs damage the brand with tax pros.

Time zone note: US accounts post during US hours. The radar issue arrives in the Berlin morning – comment on yesterday's US posts then; comments in the Berlin evening (US midday) land while the US is awake and get more replies.

## Who does what

| # | Building block | Runs where | Your time |
|---|---|---|---|
| 1 | **Radar** – fresh posts from the US niche with a comment suggestion | `automation/radar.py`, daily → issue "📡 Radar …" (label `radar`) | 10 min |
| 2 | **DM drafts** – first contact, only after you've commented twice on an account's posts | in the radar issue | 5 min |
| 3 | **Comment keyword → DM** (TOOL) | **ManyChat** (`04_dm_funnel.md`) | 0 |
| 4 | **Comment helper** – new comments under your posts with a suggested reply | `automation/comments.py`, every 15 min → issue "💬 Reply to comments" (label `comments`) | 1–2 min per post |
| 5 | **Ad that opens a DM** (USD 5/day, from week 3) | Ads Manager + **ManyChat** | once 20 min, then 5 min/week |
| 6 | **Collab of the week** – a fitting US account plus a request draft | in the radar issue (Mondays) | 5 min/week |
| 7 | **LinkedIn** (optional, **off by default**) – each carousel as a PDF document plus rewritten text | `automation/linkedin.py` → issue "💼 LinkedIn …" | 2 min per carousel |

Settings: `automation/interaction.json`; remembered contacts: `automation/interaction/contacts.json`.

## Daily routine
1. **Morning (Berlin):** open the radar issue, look at 5–8 posts, **rewrite the suggestion in your own words**, comment, check the box.
2. **Warm accounts:** if there's a DM draft and it feels right → send it by hand, check the box. No reply is fine. Don't follow up.
3. **After your own Reel (first hour, 12:30 PM ET = 6:30 PM Berlin):** GitHub notification "💬 Comments" → reply in the issue with `C12 ok` (post the suggestion) or `C12 <your own text>`. Or reply directly in the app.
4. **Mondays:** look at the collab suggestion, adapt the request, send it.
5. **Carousel nights (7:30 PM ET):** you're asleep – ManyChat handles TOOL; answer the remaining comments from the comment issue the next morning.

**Radar maintenance (Mondays):** the radar suggests quiet or broken accounts for removal (🧹) and people who commented on your posts and have a business/creator account for adding (➕). Only **what you check** is applied – on the next run, in `automation/interaction.json`. New accounts get `"kind": ""` – fill in by hand if needed.

**First hour:** when a carousel/Reel goes live, a checklist comment lands in the approval issue (share to story, answer comments, radar).

**Keywords:** the list in `automation/interaction.json` → comments → ManyChat keywords must match ManyChat. If a scheduled caption asks for a different word (e.g. "DM DEMO"), STATUS.md shows a warning. If the keywords change in ManyChat → update them here too.

Checked boxes count: someone you commented on twice gets a DM draft. Someone who got a DM never gets a second one.

## Accounts for the radar (to be filled by Cowork – `17_cowork_prompt.md`)
In `automation/interaction.json` → `radar.accounts` add 20–40 **verified US** business or creator accounts, e.g.:
```json
"accounts": [
  {"name": "examplecpafirm", "kind": "cpa_firm"},
  {"name": "example_tax_creator", "kind": "creator"}
]
```
Kinds: `cpa_firm` · `creator` · `tax_team` · `software` · `education`.
`radar.candidates_to_verify` is a to-do list for Cowork/Loris (handle exists, US, active, business/creator account) – the radar never reads it. Only verified accounts move to `radar.accounts`.
Categories to research (no names yet – **to research**):
- US CPA firms with an active Instagram (small and mid-size firms, posting at least every 2 weeks)
- Tax & accounting creators with 1,000–50,000 followers (CPA life, busy season humor, tax tips)
- Excel / spreadsheet / automation creators with a finance audience
- Accounting & tax software accounts (to see what they post – not to sell to them)
- CPA exam prep and accounting student communities, university accounting clubs
**Not:** private accounts (the API doesn't return them), government accounts (IRS, state agencies), the employer's accounts, German accounts.
How to find them: Instagram search for "CPA", "tax accountant", "busy season", "tax provision"; people who comment on your posts; "Suggested accounts" on fitting profiles. Send Claude the names, Claude adds them.

## Hashtags
Hashtag search needs Meta's approval for **"Instagram Public Content Access"** (app review with business verification). Until then the radar reports "hashtags not available yet" and works with the account list only – enough for the start. Max. 30 different hashtags in 7 days.
The hashtags to watch once approved are in `radar.hashtags` (e.g. `#taxprofessional`, `#cpa`, `#taxseason`, `#asc740`) – check their volume first (to research).

## 5 · Ad that opens a DM (click-to-DM, USD 5/day ≈ $150/month, from week 3)
This is the only allowed way to bring strangers into a DM automatically: they tap "Send message" themselves. Then ManyChat takes over.
1. **Pick the Reel:** the best Reel of weeks 1–2 by **(saves + shares) / reach** (`06_analytics.md`). Loris confirms.
2. **ManyChat:** check whether the plan offers an Instagram ads trigger ("Instagram Ads JSON" / "Ad"). If yes: flow = DM funnel ① from `04_dm_funnel.md` → copy the JSON. If no: use a prefilled message "TOOL" in the ad – the existing TOOL automation fires.
3. **Ads Manager** (business.facebook.com/adsmanager) → *Create* → objective **Engagement** → conversion location **Messaging apps → Instagram**.
4. **Budget:** USD 5 per day, 30 days. **Location:** United States only. **Age:** 25–55. **Interests:** accounting, tax, Certified Public Accountant, corporate finance (plus e.g. Microsoft Excel if available). Placement: Instagram only (feed, Reels).
5. **Ad:** use the existing Reel from step 1. Message template: greeting "Hey! Reply TOOL and I'll send you the demo + the free checklist 👇", prefilled reply "TOOL" (or the ManyChat JSON).
6. **Loris pays and submits himself.** Claude/Chrome only prepare up to the summary (`14_chrome_modules.md`, module 2).
7. **Check after 7 days:** cost per started conversation ≤ $3 = good (starting assumption, recalibrate). Above that: another Reel or narrower targeting (only "CPA" / "tax").

Ad text suggestion:
> #REF! three days before the deadline? I'll show you how a small tool fixes that in seconds – with sample data. Reply "TOOL" for the free demo + checklist.
> Educational content – not tax, legal or accounting advice.

## 6 · Collabs with US creators (for the request)
- **Collab post** (both profiles as authors): "CPA vs. code" – they explain the rule, you show the calculation.
- **Guest slide:** one tip from them in your carousel, tagged.
- **Story Q&A:** you answer questions together, each shares on the other's profile.
- **Satisfying duet:** they show their messiest (demo) workbook, you show it cleaned up – split screen.
- **Live (later):** 20 minutes "Year-end provision mistakes we see all the time".
Rule: comment honestly 2–3 times first, then ask. Small accounts (1,000–10,000 followers) say yes much more often. Never pay for collabs without asking Loris.

Request draft (adapt every time):
> Hey [name], I've been enjoying your posts on [topic] – especially [specific post]. I build small tax tools (German-trained tax pro, now building for US tax teams). Would you be up for a collab: you explain [rule], I show the calculation live in 15 seconds? Happy to do the editing.

## 7 · LinkedIn (optional, off by default)
For the US launch, LinkedIn is **off** – focus is Instagram. If Loris switches it on later (`automation/interaction.json`), each carousel becomes a PDF document plus a rewritten text in an issue "💼 LinkedIn …"; Loris uploads by hand (2 min). Posting via API is rejected (needs the restricted Community Management API).

## Limits (so Instagram doesn't throttle)
- Max. ~**10 comments** and **5 new DMs per day**, spread out, never the same message copied.
- No follow/unfollow games, no engagement pods, no bought followers.
- In DMs never accept real client or company data, SSNs or EINs (`04_dm_funnel.md`).
- No individual tax advice in comments or DMs: "Talk to your CPA about your case – happy to show you the tool."
- Nothing about the employer, not even in comments.

## Costs
| Item | per month |
|---|---|
| Claude suggestions (radar, comments, optional LinkedIn) | approx. $2–6 |
| Click-to-DM ad (from week 3) | approx. $150 (USD 5/day) |
| ManyChat Pro (needed from ~1,000 contacts) | check current pricing – ask first |
| Meta APIs, GitHub Actions | $0 |
