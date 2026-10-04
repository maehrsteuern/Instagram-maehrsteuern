# Reel 09 · "From the German tax office to building tax tools" – script draft

**Status: waiting for Loris' concept + his English voice note.** No video is built yet (plan status `waiting_concept`).
Pillar 4 · Behind the code · goal: likeability + follows · CTA: **Follow** (soft "DM TOOL" on the end card).
Length 20–30 s · 1080×1920 · Loris' own voice carries the Reel, music only very quiet underneath (≈ −30 dB under the voice).

## Hook options (on-screen text, first frame, ≤ 1.5 s)
1. **"I was trained by the German tax office."** – second line at 1.0 s: *"Now I build tax tools."*
2. **"The most rule-obsessed tax system on earth trained me."** – second line: *"Here's what I do with that."*
3. **"3 years of German tax school. 0 spreadsheets I trust."** – second line: *"So I write code."*

Recommendation: option 1 (clear, personal, true – matches the bio line "German-trained tax pro").

## Voice-note script (≈ 75 words, ~25 s at a calm pace)
> I was trained by the German tax office – three years, every rule, every form.
> The most rule-obsessed tax system on earth.
> Then I watched tax teams lose whole nights to spreadsheets: a moved file, a hard-coded 21 percent, #REF!.
> So I became a Certified AI Manager and started building small tax tools that actually run – and show where every number comes from.
> I'm Loris. Tax times code. Follow along – I'll show you everything I build.

Record on the phone, quiet room, phone ~30 cm away, relaxed tone. One take is fine – small imperfections are good on Instagram.
Subtitles = the spoken words, word for word (we time them from the recording).

## Shot list (≈ 26 s)
| Time | Picture | On-screen text (subtitle style, Outfit Bold, safe zone y 250–1500, right 150 px free) |
|---|---|---|
| 0.0–2.5 s | `assets/brand/card_1_current_9x16.png` (real photo, slow push-in) | **I was trained by the German tax office.** |
| 2.5–5.5 s | Same photo, cut to closer crop (or a phone selfie clip if Loris films one) | 3 years. Every rule. Every form. |
| 5.5–10 s | Spreadsheet chaos: `templates/system/recordings/excel_mock.html` (#REF!, "Not Responding") – recording `posts/01_…/clips/rec_spreadsheet.mp4` | Then I watched tax teams lose nights to spreadsheets. |
| 10–15 s | Demo tool: red → green (`posts/01_…/clips/rec_tool.mp4`) | So I build small tax tools that actually run. |
| 15–20 s | Demo tool § 163(j) banner zoom (`posts/11_…/clips/rec_163j.mp4`) | …and show where every number comes from. |
| 20–24 s | `assets/brand/loris_current_cutout.png` on the brand gradient + handle | I'm Loris. **Tax × Code.** |
| 24–26 s | End card `assets/end_9x16.png` | Follow along → @maehrtax |

## Brand images – what fits
- ✅ `card_1_current_9x16.png`, `loris_current_cutout.png` – real photos of Loris: use these for a personal story.
- ⚠️ `card_2_ai_portrait_9x16.png`, `loris_ai_portrait_instagram.jpg`, `card_3_ai_avatar_2025_9x16.png`, `loris_ai_avatar_2025.jpg` – AI-generated
  (realistic portrait / robot avatar). Only if the story is "from AI avatar to real person"; then add "Contains AI-generated imagery." to the caption
  and switch on Instagram's AI label. Recommendation: leave them out – a real face builds more trust.

## Music
Very quiet under the voice: `music/06_runway_lofi_ruhig.mp3` (own Runway generation, see music sources file), volume ≈ 0.12, from the cut to the tool (10 s).
No music under the hook – voice only.

## To build once the voice note is there
1. Put the voice note into `posts/09_2026-10-20_reel_my_story/clips/voice.m4a`.
2. Transcribe with timestamps (faster-whisper "small"), proof-read the words by hand.
3. Cut list `templates/system/cuts/r09_my_story.json` (montage.py: one `audio` track for the voice at volume 1.0, subtitles as `text` entries with `at`/`until`).
4. Cover via `templates/system/jobs/r_covers.json` (pillar "Behind the code", title e.g. "German tax office\n→ *tax tools*").
