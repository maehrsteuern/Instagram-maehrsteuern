/* Screen recording of the spreadsheet mock (excel_mock.html), full screen (Reels 01 and 05, hook library).
   node spreadsheet_errors.mjs <deadline|night> [out.mp4]
   deadline (Reel 01): pill counts down to the Oct 15 deadline (60× speed); errors pile up at
     1.2 #REF! · 2.2 #REF! · 2.6 #REF! · 3.0 #REF! · 3.4 #VALUE! · 3.8 #NAME? · 4.2 #REF! · 4.8 dialog "can't find" · end 6.6 s
   night (Reel 05): pill "Thu, Oct 15 · 11:48 PM" (20× → 11:50 PM at the end); errors at 0.6 … 3.0 · 3.4 dialog · 4.4 "(Not Responding)" · end 6.4 s */
import { start, POSTS } from "./recorder.mjs";

const [mode = "deadline", out] = process.argv.slice(2);
const night = mode === "night";
const target = out || `${POSTS}/${night ? "05_2026-10-15_reel_deadline_night" : "01_2026-10-12_reel_ref_error"}/clips/rec_spreadsheet.mp4`;
const r = await start({ page: "excel_mock.html", query: `clock=${night ? "night" : "deadline"}&speed=${night ? 20 : 60}`, time: night ? "2026-10-15T23:48:00" : "2026-10-12T23:47:00" });
const err = () => r.call(() => mock.next());
if (night) {
  await r.moveTo("#B7", 550);
  await err(); await r.wait(500); await err(); await r.wait(400); await err(); await r.wait(400);
  await r.click("#B14", 400); await err(); await r.wait(350); await err(); await r.wait(350); await err(); await r.wait(350); await err();
  await r.wait(300);
  await r.call(() => mock.dialog(true)); await r.wait(1000);
  await r.call(() => { mock.hang(true); mock.status("Calculating (4 threads): 37%"); });
  await r.moveTo([300, 520], 900); await r.wait(1000);
} else {
  await r.wait(400);
  await r.moveTo("#B7", 700);
  await err(); await r.wait(1000);       // 1.2 s: the first #REF!
  for (let i = 0; i < 6; i++) { await err(); await r.wait(400); }
  await r.wait(200);
  await r.call(() => mock.dialog(true));  // 4.8 s
  await r.moveTo(".dlg button.d", 700);
  await r.wait(1100);
}
await r.finish(target);
