/* Still 1080×1920 PNG of a recording page, e.g. the default app background assets/app_9x16.png:
   node screenshot.mjs "demo_tool.html?view=provision&auto=1" ../../../assets/app_9x16.png 4500
   Arguments: page with query · output PNG · wait in ms before the shot (lets auto-play animations finish, real time). */
import { createRequire } from "module";
import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";
let chromium;
try { ({ chromium } = await import("playwright")); }
catch { ({ chromium } = createRequire(execSync("npm root -g").toString().trim() + "/")("playwright")); }
const here = path.dirname(fileURLToPath(import.meta.url));
const [page, out, ms = "800"] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2, colorScheme: "dark" });
await p.clock.install({ time: new Date("2026-10-12T16:15:00") });   // fixed clock text in the app ("4:15 PM")
await p.goto("file://" + path.join(here, page));
await p.evaluate(() => document.fonts.ready);
await p.clock.runFor(+ms);
await p.screenshot({ path: path.resolve(out) });
await b.close();
console.log("✓", out);
