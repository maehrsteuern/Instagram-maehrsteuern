import { chromium } from 'playwright';
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p = await b.newPage({viewport:{width:720,height:1280}});
await p.goto('file://'+process.cwd()+'/ende.html'); await p.waitForTimeout(800);
await p.screenshot({path:'ende_9x16.png'}); await b.close();
