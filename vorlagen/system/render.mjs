// Bilder aus Vorlagen erzeugen:  node render.mjs jobs/w02_karussell.json
// Eine Job-Datei: { "ausgabe": "../../assets/<ordner>", "bilder": [ { "vorlage": "karussell", "datei": "01.png", ...Daten } ] }
import { readFileSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';
import { execSync } from 'child_process';

// Playwright lokal oder global (npm -g) finden
let chromium;
try { ({ chromium } = await import('playwright')); }
catch { ({ chromium } = createRequire(execSync('npm root -g').toString().trim()+'/')('playwright')); }

const hier = dirname(fileURLToPath(import.meta.url));
const GROESSE = { karussell:[1080,1350], story:[1080,1920], reel_titel:[1080,1920], highlight:[1080,1920], einblendung:[1080,1920], excel_chaos:[1404,2496], ampel:[1080,1920], linkedin_banner:[1584,396] };

const jobs = process.argv.slice(2);
if (!jobs.length) { console.log('Aufruf: node render.mjs jobs/<datei>.json [...]'); process.exit(1); }

const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const job of jobs) {
  const cfg = JSON.parse(readFileSync(resolve(job),'utf8'));
  const ziel = resolve(hier, cfg.ausgabe); mkdirSync(ziel, { recursive:true });
  const von = cfg.bilder.filter(b => b.vorlage==='karussell').length;
  let seite = 0;
  for (const b of cfg.bilder) {
    const [width,height] = GROESSE[b.vorlage];
    if (b.vorlage==='karussell') b.seite ??= ++seite, b.von ??= von;
    const page = await browser.newPage({ viewport:{ width, height } });
    await page.addInitScript(d => { window.DATA = d; }, b);
    await page.goto('file://'+resolve(hier, b.vorlage+'.html'));
    await page.evaluate(async () => { await document.fonts.ready; window.fitAll?.(); }); await page.waitForTimeout(300);
    await page.screenshot({ path: resolve(ziel, b.datei), omitBackground: !!b.transparent });
    await page.close(); console.log('✓', cfg.ausgabe+'/'+b.datei);
  }
}
await browser.close();
