// Renders the lead magnet:  node assets/lead_magnet/render_pdf.mjs
// → spreadsheet_to_code_checklist.pdf (US Letter, 2 pages) + checklist_preview.png (page 1, used by the story_cta)
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';
import { execSync } from 'child_process';

let chromium;
try { ({ chromium } = await import('playwright')); }
catch { ({ chromium } = createRequire(execSync('npm root -g').toString().trim()+'/')('playwright')); }

const here = dirname(fileURLToPath(import.meta.url));
const src = 'file://' + resolve(here, 'spreadsheet_to_code_checklist.html');
const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport:{ width:816, height:1056 }, deviceScaleFactor:2 });
await page.goto(src);
await page.evaluate(async () => { await document.fonts.ready; });
await page.pdf({ path: resolve(here, 'spreadsheet_to_code_checklist.pdf'), preferCSSPageSize:true, printBackground:true });
await page.screenshot({ path: resolve(here, 'checklist_preview.png'), clip:{ x:0, y:0, width:816, height:1056 } });
// overflow check: every page's content must end above its footer
const bad = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p,i) => {
  const foot = p.querySelector('.foot').getBoundingClientRect().top;
  const last = [...p.children].filter(c => !c.classList.contains('foot')).pop().getBoundingClientRect().bottom;
  return last > foot - 8 ? `page ${i+1}: content ends at ${Math.round(last)}, footer at ${Math.round(foot)}` : null; }).filter(Boolean));
console.log(bad.length ? '⚠ ' + bad.join('; ') : '✓ no overflow');
await browser.close();
console.log('✓ spreadsheet_to_code_checklist.pdf, checklist_preview.png');
