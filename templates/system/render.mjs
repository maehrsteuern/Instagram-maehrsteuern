// Render images from templates:  node render.mjs jobs/c01_excel_mistakes.json [...]
// A job file: { "output": "../../posts/<folder>", "images": [ { "template": "carousel", "file": "slide_01.png", ...data } ] }
// Template data keys are English (type, title, sub, text, box, pillar, …) – see the comment at the top of each template.
import { readFileSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';
import { execSync } from 'child_process';

// Find Playwright locally or globally (npm -g)
let chromium;
try { ({ chromium } = await import('playwright')); }
catch { ({ chromium } = createRequire(execSync('npm root -g').toString().trim()+'/')('playwright')); }

const here = dirname(fileURLToPath(import.meta.url));
const SIZE = { carousel:[1080,1350], story:[1080,1920], reel_cover:[1080,1920], highlight:[1080,1920], overlay:[1080,1920], excel_chaos:[1404,2496], traffic_light:[1080,1920] };

const jobs = process.argv.slice(2);
if (!jobs.length) { console.log('Usage: node render.mjs jobs/<file>.json [...]'); process.exit(1); }

const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const job of jobs) {
  const cfg = JSON.parse(readFileSync(resolve(job),'utf8'));
  const target = resolve(here, cfg.output); mkdirSync(target, { recursive:true });
  const of = cfg.images.filter(b => b.template==='carousel').length;
  let page_no = 0;
  for (const b of cfg.images) {
    const [width,height] = SIZE[b.template];
    if (b.template==='carousel') b.page ??= ++page_no, b.of ??= of;
    const page = await browser.newPage({ viewport:{ width, height } });
    await page.addInitScript(d => { window.DATA = d; }, b);
    await page.goto('file://'+resolve(here, b.template+'.html'));
    await page.evaluate(async () => { await document.fonts.ready; window.fitAll?.(); }); await page.waitForTimeout(300);
    await page.screenshot({ path: resolve(target, b.file), omitBackground: !!b.transparent });
    await page.close(); console.log('✓', cfg.output+'/'+b.file);
  }
}
await browser.close();
