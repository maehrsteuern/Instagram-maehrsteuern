/* Screen recording of the demo tool's cleanup view: 4,000 messy rows → one click → clean (Reel 08, satisfying loop).
   node cleanup_4000_rows.mjs [out.mp4]
   Timeline (s): 0–0.5 messy · 0.5–1.1 cursor to "Clean 4,000 rows" · 1.1 click · 1.1–4.4 cleaning front races down, glides back ·
   4.4–7.3 hold clean · 7.3 cursor back to its start point · 7.6–8.1 wipe back to messy (loop) · 8.2 end = first frame again. */
import { start, POSTS } from "./recorder.mjs";

const [out = `${POSTS}/08_2026-10-19_reel_4000_rows/clips/rec_cleanup.mp4`] = process.argv.slice(2);
const r = await start({ page: "demo_tool.html", query: "view=cleanup&state=messy", time: "2026-10-19T11:40:00" });
const home = await r.p.evaluate(() => [window.__rec.x, window.__rec.y]);
await r.wait(500);
await r.click("#btnClean", 600);
await r.wait(3300);
await r.wait(2900);
await r.moveTo(home, 450);
await r.call(() => { demo.mess(450); });   // braces: don't await the page promise (page time only moves inside wait())
await r.wait(500);
await r.finish(out);
