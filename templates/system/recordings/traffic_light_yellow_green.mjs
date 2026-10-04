/* Screen recording of the demo tool's provision check: traffic light red → yellow → green (Reels 01, 05, hook library).
   node traffic_light_yellow_green.mjs [out.mp4] [page time, e.g. 2026-10-15T23:49:00]
   Timeline (s): 0–1.1 red state, 3 errors · 1.1–1.8 cursor to "Fix 4 issues" · 1.8 click · 1.8–5.0 fixes run,
   light red → yellow (~3.9) → green (~4.9) · 5.0–9.4 hold "Ready to book." (camera zoom on the status card 5.6–6.3).
   Technique: recorder.mjs (fake clock, one frame per 1/30 s). */
import { start, POSTS } from "./recorder.mjs";

const [out = `${POSTS}/01_2026-10-12_reel_ref_error/clips/rec_tool.mp4`, time = "2026-10-12T16:15:00"] = process.argv.slice(2);
const r = await start({ page: "demo_tool.html", query: "view=provision&state=red", time });
await r.wait(1100);
await r.click("#btnFix", 700);
await r.wait(3300);                       // fix sequence: 37 cells → 1 parameter, link restored, rate rec ties, review confirmed
await r.moveTo([300, 620], 600);          // cursor out of the way
await r.zoom("#statusCard", 1.18, 700);
await r.wait(2400);
await r.zoom(null, 1, 600);
await r.wait(600);
await r.finish(out);
