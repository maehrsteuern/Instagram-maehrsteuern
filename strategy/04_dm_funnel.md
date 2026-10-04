# 4 · DM funnel "TOOL" → demo + intro call (ManyChat)

The US account starts **with ManyChat from day 1** (the German account waited for volume – for the US, the hard conversion funnel is the plan). Every Reel and every client carousel says "Comment or DM TOOL". ManyChat answers within seconds – which also covers the evening posts, when Loris is asleep in Germany.

## The flow at a glance
```
"TOOL" as comment, story reply or DM  (also: Tool / tool / tol / TOOLS)
   │
   ├── comment ──► public auto-reply (rotating): "Sent you a DM 💬" / "Check your DMs ⚙️" / "On its way!"
   │
   ▼
① DM: thanks + "Where do you work?"   [buttons]  In-house tax · CPA firm · Small business · Student
   │
   ├── In-house tax / CPA firm / Small business ──► ② demo video + booking link + checklist (lead magnet)
   │                                                 │
   │                                                 ├── booked ──────────────► ⑤ thanks + how to prepare
   │                                                 └── no click after 23 h ─► ④ one follow-up, then quiet
   │
   └── Student ──► ③ checklist + "Learn 📚" highlight, friendly, no call pressure
```
Why 23 h: Meta allows automated messages only within 24 hours after the person's last message. The follow-up has to go out before that window closes.

## The messages (copy into ManyChat)

**Public comment replies (rotate, so they don't look like spam)**
```
Sent you a DM 💬
Check your DMs ⚙️
On its way – check your inbox!
```

**① Welcome – immediately**
```
Hey, thanks for reaching out! 🙌
Quick question so I send you the right thing – where do you work?
```
Buttons: `In-house tax team` · `CPA firm` · `Small business / freelancer` · `Student / CPA candidate`

**② Demo + booking + checklist (in-house, CPA firm, small business)**
```
Perfect. Here's the 2-min demo (sample data only): [DEMO VIDEO LINK]

Want to see what that looks like for your workflow?
20 minutes, free, no strings attached 👉 https://app.reclaim.ai/m/maehrtax/demo

And here's the free "Spreadsheet-to-Code Checklist for Tax Teams" (PDF): [CHECKLIST LINK]

Heads-up: please don't send client or company data, SSNs or EINs by DM.
```
Variant per button (one line before the demo link):
- In-house: "Provision, rate rec, deferred taxes – that's where I build the most."
- CPA firm: "Recurring calcs before busy season are exactly where this pays off."
- Small business: "I'll show you how the numbers come together – your CPA still makes the calls on your case."

**② Interim version, until the demo video exists**
```
Perfect. I'd love to show you the demo live – with sample data and tailored to your workflow.
20 minutes, free, no strings attached 👉 https://app.reclaim.ai/m/maehrtax/demo

Meanwhile, here's the free "Spreadsheet-to-Code Checklist for Tax Teams" (PDF): [CHECKLIST LINK]

Heads-up: please don't send client or company data, SSNs or EINs by DM.
```

**③ Student / CPA candidate**
```
Awesome – you're in the right place! 🎓
Here's the free checklist (great to understand how real tax teams work): [CHECKLIST LINK]
For learning, check the "Learn 📚" highlight – I collect the worked examples there.
Questions? Just reply here ✌️
```

**④ Follow-up – once, 23 h after ② if the booking link wasn't clicked**
```
Quick nudge in case this got buried: the free 20-min demo is here 👉 https://app.reclaim.ai/m/maehrtax/demo
Not the right time? Totally fine – the checklist is yours either way.
```

**⑤ After booking** (by hand or via ManyChat if the booking can be detected)
```
Awesome, looking forward to it! 🙌 To make the 20 minutes count:
think about which workflow takes your team the longest today. That's all the prep you need.
```

**After the call (1–2 days later, by hand)**
```
Thanks again for the call! Mind if I share your feedback anonymously in my "Feedback" highlight?
```

## Replies for objections (saved replies in ManyChat / Instagram)
Short, friendly, never pushy. Never individual tax advice.

| Shortcut | When | Text |
|---|---|---|
| `price` | "What does it cost?" | Demo and intro call are free. After that you get a quote that fits your scope – often a small, fixed-price tool, no subscription you didn't ask for. |
| `software` | "We already have tax software." | Great – this doesn't replace it. It closes the gaps around it: the side calcs and tie-outs that still live in spreadsheets. |
| `ai` | "AI makes things up – I don't trust it with tax math." | Agreed! That's the point: AI reads and drafts, code does the math. Every number is traceable to its source. |
| `security` | "Our IT/data rules won't allow it." | Fair. The demo uses sample data only, and tools can run inside your own environment. Let's talk through your IT requirements on the call. |
| `cpa` | "Are you a CPA?" | No – I'm a German-trained tax pro (3-year tax administration degree) and Certified AI Manager. I build the tools; your CPA or tax advisor makes the calls on your case. |
| `advice` | someone asks about their own tax case | I can't give advice on individual cases here – please talk to your CPA about that. Happy to show you the tool, though! |
| `busy` | "Busy season, no time." | Totally get it. Book a slot after the deadline – the link stays open: https://app.reclaim.ai/m/maehrtax/demo |
| `later` | "Not now." | No worries! The checklist is yours, and the door stays open. |
| `other` | anything else / no TOOL topic | Thanks! Tell me briefly what it's about – I'll get back to you personally, usually within a day. |

## ManyChat setup (Cowork or Loris, once)
1. ManyChat account for **@maehrtax** (Instagram channel), plan: start free/Essential; Pro only when needed (> 1,000 contacts or API) – ask first, costs money.
2. Automation "TOOL": triggers **comment** (all posts and Reels), **story reply** and **DM** containing `TOOL` / `Tool` / `tool` / `tol` / `TOOLS`.
3. Flow ① → buttons → ② / ③, condition "booking link not clicked" → wait 23 h → ④.
4. Public comment reply: rotate the 3 texts above.
5. Keywords must match `automation/interaction.json` (comments → `manychat_keywords`) – STATUS.md warns if a scheduled caption asks for a different word.
6. Test with an account that has never messaged @maehrtax: comment "TOOL" under a post → public reply + DM within seconds.

## Still missing
- [ ] **Demo video** 1–2 min (script: `07_demo_video.md`), unlisted on YouTube – until then use ② interim version
- [ ] **English booking page** on Reclaim "Demo + Intro Call (20 min)" with required field "How did you find me?" (Instagram Reel · Instagram ad · Instagram DM · LinkedIn · Other) → replace the placeholder link everywhere
- [ ] **Checklist PDF** "The Spreadsheet-to-Code Checklist for Tax Teams" (content outline: `16_us_growth_playbook.md`) → hosted link
- [ ] ManyChat flow live + test (see above)
- [ ] After 2 weeks: TOOL DMs, button split, link clicks, bookings → `06_analytics.md`

## Tracking
Every lead one line in `strategy/dm_tracking.csv`: `date, handle_short, group, keyword, stage, demo_booked (yes/no), source_post`. Only a short handle abbreviation – no full names, companies or emails. After 4 weeks you see which post brought the leads.
