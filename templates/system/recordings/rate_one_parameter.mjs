/* Screen recording of the demo tool's rate view: 400 cells with a hard-coded 21% → one parameter (Reel 04, satisfying).
   node rate_one_parameter.mjs [out.mp4]
   Timeline (s): 0–1.5 400 red cells · 1.5–2.2 cursor to "Link all" · 2.2 click · 2.2–4.4 green wave from top-left ·
   4.6–5.3 zoom on the parameter panel ("0 / 400") · hold · 7.6–8.2 zoom out · 8.6 end. */
import { start, POSTS } from "./recorder.mjs";

const [out = `${POSTS}/04_2026-10-14_reel_hardcoded_rate/clips/rec_rate.mp4`] = process.argv.slice(2);
const r = await start({ page: "demo_tool.html", query: "view=rate&state=hard", time: "2026-10-14T11:20:00" });
await r.wait(1500);
await r.click("#btnLink", 700);
await r.wait(2300);
await r.moveTo([250, 700], 400);
await r.zoom(".param", 1.25, 700);
await r.wait(2200);
await r.zoom(null, 1, 600);
await r.wait(400);
await r.finish(out);
