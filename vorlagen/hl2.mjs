import { chromium } from 'playwright';
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p = await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/highlight2.html'); await p.waitForTimeout(800);
await p.screenshot({path:'maehrsteuern_Highlight_Feedback.png'}); await b.close();
