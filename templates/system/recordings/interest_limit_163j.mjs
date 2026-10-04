/* Screen recording of the demo tool's § 163(j) view: ATI basis EBIT → EBITDA (Reel 11, hook library).
   node interest_limit_163j.mjs [out.mp4]
   Numbers (strategy/00_us_brief.md): EBITDA $14.0M · D&A $4.0M · EBIT $10.0M · interest $4.0M.
   Limit 30% × $10.0M = $3.0M ($1.0M disallowed) → 30% × $14.0M = $4.2M (all $4.0M deductible) → +$1,000,000 × 21% = $210,000.
   Timeline (s): 0–1.1 EBIT state · 1.1–1.8 cursor to the toggle · 1.8 click · 1.8–3.1 numbers + bar move ·
   3.1–4.9 banner "+$1,000,000 deductible" / "$210,000" ticks in · 5.1–5.8 zoom on the banner · hold · 8.4–9.0 zoom out · 9.6 end. */
import { start, POSTS } from "./recorder.mjs";

const [out = `${POSTS}/11_2026-10-21_reel_163j_demo/clips/rec_163j.mp4`] = process.argv.slice(2);
const r = await start({ page: "demo_tool.html", query: "view=163j&state=ebit", time: "2026-10-21T11:05:00" });
await r.wait(1100);
await r.click("#basis-ebitda", 700);
await r.wait(3000);
await r.moveTo([250, 470], 500);
await r.zoom("#jBanner", 1.28, 700);
await r.wait(2300);
await r.zoom(null, 1, 600);
await r.wait(600);
await r.finish(out);
