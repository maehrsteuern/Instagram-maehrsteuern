/* Record a timeline page (no cursor) for a fixed length: number Reels and the AI-vs-code Reel.
   node timeline.mjs <page.html> <query> <seconds> <out.mp4>
   e.g. node timeline.mjs number_reel.html reel=163j 9.7 ../../../posts/07_2026-10-16_reel_163j_number/clips/rec_number.mp4
   The page starts its timeline in window.play() (called by recorder.mjs right before frame 1). */
import { start } from "./recorder.mjs";

const [page, query, secs, out] = process.argv.slice(2);
const r = await start({ page, query, cursor: false });
await r.wait(+secs * 1000);
await r.finish(out);
