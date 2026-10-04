/* Deterministic screen recorder for the Tax × Code demo pages (demo_tool.html, excel_mock.html, split.html, …).
   Playwright (Chromium) with a fake page clock: every video frame = advance page time by 1/30 s + one screenshot.
   No dropped frames, no timing jitter, independent of machine load. All animations in the recorded pages are
   JavaScript-driven (performance.now / requestAnimationFrame), so the fake clock moves them frame by frame.
   A visible cursor with click ripple is drawn into the page (headless Chromium shows none).

   Usage in a recording script:
     import { start } from "./recorder.mjs";
     const r = await start({ page: "demo_tool.html", query: "view=163j" });
     await r.wait(800); await r.click("#basis-ebitda"); await r.wait(2500);
     await r.finish(out);   // scripts default to posts/<reel>/clips/…, see POSTS below

   Options of start():
     page     HTML file relative to this folder (or absolute)      query   URL query without "?"
     width    CSS width of the window (540 = phone layout, 2× pixel density → 1080 px)
     format   output size [w, h]; default [1080, 1920]                fps     default 30
     time     wall-clock time the page sees (ISO string, local time)  cursor  false = no cursor
     prepare  async (page) => {} – sets the initial state before the first frame
     crf      x264 quality of the output (default 18)
   Environment: CHROMIUM (browser binary), FFMPEG (ffmpeg binary, default "ffmpeg").

   Rebuild every Reel (run in this folder, then `cd .. && python3 montage.py cuts/<cut>.json`):
     01 ref_error        node spreadsheet_errors.mjs deadline · node traffic_light_yellow_green.mjs   → cuts/r01_ref_error.json
     02 split            node split_excel_tool.mjs                                                   → cuts/r02_split.json
     04 hardcoded_rate   node rate_one_parameter.mjs                                                 → cuts/r04_hardcoded_rate.json
     05 deadline_night   node spreadsheet_errors.mjs night ·
                         node traffic_light_yellow_green.mjs <posts/05_…/clips/rec_tool.mp4> 2026-10-15T23:48:20 → cuts/r05_deadline_night.json
     07 / 14 numbers     node timeline.mjs number_reel.html reel=163j|174a 9.7 <posts/…/clips/rec_number.mp4>
     08 4000_rows        node cleanup_4000_rows.mjs                                                  → cuts/r08_4000_rows.json
     11 163j_demo        node interest_limit_163j.mjs                                                → cuts/r11_163j_demo.json
     12 ai_vs_code       node timeline.mjs ai_vs_code.html "" 14.6 <posts/12_…/clips/rec_ai_vs_code.mp4>
     App still           node screenshot.mjs "demo_tool.html?view=provision&auto=1" ../../../assets/app_9x16.png 5000
   Covers: node render.mjs jobs/r_covers.json (backgrounds = posts/<reel>/clips/cover_bg.jpg, a frame of the recording).
*/
import { createRequire } from "module";
import { execSync, spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

let chromium;
try { ({ chromium } = await import("playwright")); }
catch { ({ chromium } = createRequire(execSync("npm root -g").toString().trim() + "/")("playwright")); }

const here = path.dirname(fileURLToPath(import.meta.url));
export const POSTS = path.resolve(here, "../../../posts");   // default output root of the recording scripts
const CHROME = process.env.CHROMIUM || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const ease = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

export async function start({ page, query = "", width = 540, format = [1080, 1920], fps = 30,
                              time = "2026-10-12T16:12:00", cursor = true, prepare, crf = 18 }) {
  const [outW, outH] = format;
  const height = Math.round(width * outH / outW);
  const browser = await chromium.launch({ executablePath: CHROME });
  const context = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: outW / width, colorScheme: "dark" });
  const p = await context.newPage();
  await p.clock.install({ time: new Date(time) });
  const file = path.isAbsolute(page) ? page : path.join(here, page);
  await p.goto("file://" + file + (query ? "?" + query : ""));
  await p.evaluate(() => document.fonts.ready);
  await p.clock.pauseAt(new Date(+new Date(time) + 2000));   // from here on, time only moves frame by frame
  await p.clock.runFor(100);
  if (prepare) await prepare(p);

  // cursor + click ripple, drawn inside #stage (so a camera zoom scales it like in a real screen recording)
  await p.evaluate(([x, y, show]) => {
    const stage = document.getElementById("stage") || document.body;
    const c = document.createElement("div");
    c.id = "rec-cursor";
    c.innerHTML = `<svg width="26" height="26" viewBox="0 0 24 24"><path d="M4 2l15 11-6.5 1.2L16 21l-3 1.4-3.4-6.6L4 20z" fill="#fff" stroke="#000" stroke-width="1.4" stroke-linejoin="round"/></svg>`;
    Object.assign(c.style, { position: "absolute", left: "0", top: "0", zIndex: 2147483647, pointerEvents: "none",
      filter: "drop-shadow(0 2px 3px rgba(0,0,0,.5))", display: show ? "block" : "none" });
    stage.appendChild(c);
    const rec = window.__rec = { x, y, stage, cursor: c };
    rec.place = (x, y) => { rec.x = x; rec.y = y; c.style.transform = `translate(${x - 3}px,${y - 2}px)`; };
    rec.ripple = (x, y) => {
      const r = document.createElement("div");
      Object.assign(r.style, { position: "absolute", left: x - 18 + "px", top: y - 18 + "px", width: "36px", height: "36px",
        borderRadius: "50%", border: "3px solid #53C3A2", zIndex: 2147483646, pointerEvents: "none" });
      stage.appendChild(r);
      const t0 = performance.now();
      const step = () => {
        const k = Math.min((performance.now() - t0) / 450, 1);
        r.style.transform = `scale(${1 + 0.8 * k})`; r.style.opacity = String(1 - k);
        if (k < 1) requestAnimationFrame(step); else r.remove();
      };
      requestAnimationFrame(step);
    };
    rec.place(x, y);
  }, [width / 2, height * 0.62, cursor]);

  await p.evaluate(() => window.play && window.play());   // pages with a timeline start it now (t = 0 in frame 1)

  // ---- video output: JPEG frames → ffmpeg (H.264)
  // written to a temp file first, moved to the target in finish()
  const tmpOut = path.join("/tmp", `rec-${process.pid}-${Date.now()}.mp4`);
  const enc = spawn(process.env.FFMPEG || "ffmpeg", ["-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", String(fps),
    "-c:v", "mjpeg", "-i", "-", "-vf", `scale=${outW}:${outH}:flags=lanczos,format=yuv420p`, "-c:v", "libx264",
    "-preset", "medium", "-crf", String(crf), "-r", String(fps), "-movflags", "+faststart", tmpOut], { stdio: ["pipe", "inherit", "inherit"] });
  const done = new Promise(res => enc.on("close", res));

  let frames = 0, clockMs = 0;
  async function frame() {
    const target = Math.round((frames + 1) * 1000 / fps);
    await p.clock.runFor(target - clockMs); clockMs = target;
    const buf = await p.screenshot({ type: "jpeg", quality: 93 });
    if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once("drain", r));
    frames++;
  }
  const nFrames = ms => Math.max(1, Math.round(ms / 1000 * fps));
  const wait = async ms => { for (let i = 0, n = nFrames(ms); i < n; i++) await frame(); };

  // where is an element? → centre in viewport coordinates
  async function point(target, dx = 0.5, dy = 0.5) {
    if (Array.isArray(target)) return target;
    const loc = typeof target === "string" ? p.locator(target).first() : target;
    const b = await loc.boundingBox();
    if (!b) throw new Error("not visible: " + target);
    return [b.x + b.width * dx, b.y + b.height * dy];
  }
  // viewport → stage coordinates (undo the camera zoom)
  const toStage = ([x, y]) => p.evaluate(([x, y]) => {
    const r = window.__rec.stage.getBoundingClientRect(), s = r.width / window.__rec.stage.offsetWidth || 1;
    return [(x - r.left) / s, (y - r.top) / s];
  }, [x, y]);

  async function moveTo(target, ms = 650, opts = {}) {
    const [vx, vy] = await point(target, opts.dx, opts.dy);
    const [tx, ty] = await toStage([vx, vy]);
    const [sx, sy] = await p.evaluate(() => [window.__rec.x, window.__rec.y]);
    const n = nFrames(ms);
    for (let i = 1; i <= n; i++) {
      const k = ease(i / n), arc = Math.sin(Math.PI * i / n) * Math.min(40, Math.hypot(tx - sx, ty - sy) * 0.12);
      await p.evaluate(([x, y]) => window.__rec.place(x, y), [sx + (tx - sx) * k, sy + (ty - sy) * k - arc]);
      await frame();
    }
    await p.mouse.move(vx, vy);
    return [vx, vy];
  }
  async function click(target, ms = 650, opts = {}) {
    const [vx, vy] = await moveTo(target, ms, opts);
    await p.evaluate(() => window.__rec.ripple(window.__rec.x, window.__rec.y));
    await p.mouse.down(); await frame(); await p.mouse.up(); await frame();
  }
  async function type(text, msPerChar = 110) {
    for (const ch of text) { await p.keyboard.type(ch); await wait(msPerChar); }
  }
  const press = async (key, ms = 120) => { await p.keyboard.press(key); await wait(ms); };
  // run code in the page (e.g. trigger a demo step). Never return a pending promise from fn: page time only moves
  // inside wait()/moveTo(), so awaiting an animation here would hang – wrap async calls in braces: () => { demo.fix(); }
  const call = (fn, arg) => p.evaluate(fn, arg);
  const cursorShow = on => p.evaluate(on => { window.__rec.cursor.style.display = on ? "block" : "none"; }, on);

  // smooth camera zoom on #stage: zoom(target, 1.35, 700) – zoom(null, 1, 700) back to full view
  async function zoom(target, scale = 1.3, ms = 700) {
    const from = await p.evaluate(() => { const m = (window.__rec.stage.style.transform || "").match(/translate\(([-\d.]+)px, *([-\d.]+)px\) scale\(([-\d.]+)\)/);
      return m ? [+m[1], +m[2], +m[3]] : [0, 0, 1]; });
    let to = [0, 0, 1];
    if (target && scale !== 1) {
      const [vx, vy] = await point(target);
      const [cx, cy] = await toStage([vx, vy]);
      const tx = Math.min(0, Math.max(width - width * scale, width / 2 - cx * scale));
      const ty = Math.min(0, Math.max(height - height * scale, height / 2 - cy * scale));
      to = [tx, ty, scale];
    }
    const n = nFrames(ms);
    for (let i = 1; i <= n; i++) {
      const k = ease(i / n), v = from.map((a, j) => a + (to[j] - a) * k);
      await p.evaluate(v => { const s = window.__rec.stage.style; s.transformOrigin = "0 0"; s.transform = `translate(${v[0]}px, ${v[1]}px) scale(${v[2]})`; }, v);
      await frame();
    }
  }

  async function finish(target) {
    enc.stdin.end();
    await done;
    await browser.close();
    const out = path.resolve(target);   // relative to the current directory (scripts pass absolute paths)
    execSync(`mkdir -p "${path.dirname(out)}" && mv "${tmpOut}" "${out}"`);
    console.log("✓", path.relative(process.cwd(), out), `${frames} frames, ${(frames / fps).toFixed(2)} s`);
  }
  return { p, frame, wait, moveTo, click, type, press, call, zoom, cursorShow, finish, point };
}
