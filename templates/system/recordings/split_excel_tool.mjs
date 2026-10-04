/* Split-screen recording for Reel 02: same task, two stopwatches (split.html = spreadsheet top, tool bottom).
   node split_excel_tool.mjs [out.mp4]
   Top (excel_mock.html?compact=1): selection jumps around, errors pile up (#REF!), "can't find" dialog, "Not Responding";
     stopwatch runs as a 720× time-lapse → 2:00:00 at ~10.5 s and keeps going.
   Bottom (demo_tool.html?compact=1): cursor clicks "Fix 4 issues" at ~1.6 s → red → green; stopwatch (5× time-lapse) stops at "✓ 17 s · done" (~5.0 s).
   Length ~13.4 s. Both halves inside the safe zone (px y 256–1488). */
import { start, POSTS } from "./recorder.mjs";

const [out = `${POSTS}/02_2026-10-13_reel_split/clips/rec_split.mp4`] = process.argv.slice(2);
const r = await start({ page: "split.html", time: "2026-10-13T10:02:00" });
const top = r.p.frames().find(f => f.url().includes("excel_mock"));
const bottom = r.p.frames().find(f => f.url().includes("demo_tool"));
const sheet = fn => top.evaluate(fn);
await r.call(() => { split.top(true); });
await r.wait(500);
await sheet(() => mock.select("B3")); await r.wait(400);
await r.moveTo("#bottom", 600, { dx: .8, dy: .3 });
await r.call(() => { split.bottom(true); });
await r.click(await (async () => { const b = await bottom.locator("#btnFix").boundingBox(); return [b.x + b.width / 2, b.y + b.height / 2]; })(), 450);
await sheet(() => mock.select("B5")); await r.wait(400);
await sheet(() => { mock.select("B7"); mock.next(); }); await r.wait(700);          // #REF!
await sheet(() => mock.next()); await r.wait(600);                                  // total #REF!
await sheet(() => mock.select("C7")); await r.wait(600);
await r.wait(400);
await r.call(() => split.done());                                                   // ~5.0 s: tool done, 17 s
await r.moveTo([180, 640], 600);
await sheet(() => mock.dialog(true)); await r.wait(1500);
await sheet(() => mock.dialog(false)); await sheet(() => mock.select("B4")); await r.wait(700);
await sheet(() => mock.select("B5")); await r.wait(500);
await sheet(() => mock.hang(true)); await r.wait(5400);
await r.finish(out);
