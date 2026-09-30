/* Bildschirmaufnahme Ertragsteuer-Programm: Abschlussreife Gelb -> Gruen.
   node ampel_gelb_gruen.mjs <pfad/zu/steuerberechnung/index.html> <ziel.mp4>
   Braucht Playwright (Chromium) und ffmpeg (imageio-ffmpeg). Reel-Datensatz: index.html?demo=reel.
   Ablauf: Dashboard "Punkte offen" -> Stammdaten -> Ersteller -> Hebesatz 400 -> Dashboard "vollstaendig". */
import { createRequire } from "module";
import fs from "fs";
import path from "path";
import { execFileSync } from "child_process";
const require = createRequire(process.env.PW_PFAD || import.meta.url);
const { chromium } = require("playwright");

const [app, ziel] = process.argv.slice(2);
const tmp = fs.mkdtempSync("/tmp/aufnahme-");
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2, colorScheme: "dark" });
await p.addInitScript(() => { localStorage.setItem("ertragsteuern.theme", "dark"); localStorage.setItem("ertragsteuern.lang", "de"); });
await p.goto("file://" + path.resolve(app) + "?demo=reel");
await p.waitForTimeout(1500);
await p.locator("#btn-ein-demo").click().catch(() => {});
// Ausgangslage: Hebesatz und Ersteller fehlen -> Abschlussreife gelb
await p.evaluate(() => { S.param.hebesatz = 0; S.meta.ersteller = ""; aktiv = "dash"; renderModul(); scrollTo(0, 0); });
// sichtbarer Mauszeiger mit Klick-Welle (headless zeigt keinen)
await p.evaluate(() => {
  const c = document.createElement("div");
  c.id = "rec-cursor";
  c.innerHTML = `<svg width="26" height="26" viewBox="0 0 24 24"><path d="M4 2l15 11-6.5 1.2L16 21l-3 1.4-3.4-6.6L4 20z" fill="#fff" stroke="#000" stroke-width="1.4" stroke-linejoin="round"/></svg>`;
  Object.assign(c.style, { position: "fixed", left: "270px", top: "620px", zIndex: 2147483647, pointerEvents: "none", transition: "none", filter: "drop-shadow(0 2px 3px rgba(0,0,0,.5))" });
  document.body.appendChild(c);
  addEventListener("mousemove", e => { c.style.left = e.clientX - 3 + "px"; c.style.top = e.clientY - 2 + "px"; }, true);
  addEventListener("mousedown", e => {
    const r = document.createElement("div");
    Object.assign(r.style, { position: "fixed", left: e.clientX - 18 + "px", top: e.clientY - 18 + "px", width: "36px", height: "36px", borderRadius: "50%",
      border: "3px solid #53C3A2", zIndex: 2147483646, pointerEvents: "none", transition: "transform .45s ease-out, opacity .45s ease-out" });
    document.body.appendChild(r);
    requestAnimationFrame(() => { r.style.transform = "scale(1.8)"; r.style.opacity = "0"; });
    setTimeout(() => r.remove(), 600);
  }, true);
});
await p.mouse.move(270, 620);
await p.waitForTimeout(300);

// Aufnahme über CDP-Screencast: Bilder in Gerätepixeln (1080x1920), mit Zeitstempel
const cdp = await p.context().newCDPSession(p);
const bilder = [];
cdp.on("Page.screencastFrame", async f => {
  const datei = path.join(tmp, `f${String(bilder.length).padStart(5, "0")}.jpg`);
  fs.writeFileSync(datei, Buffer.from(f.data, "base64"));
  bilder.push({ datei, t: f.metadata.timestamp });
  await cdp.send("Page.screencastFrameAck", { sessionId: f.sessionId }).catch(() => {});
});
await cdp.send("Page.startScreencast", { format: "jpeg", quality: 92, maxWidth: 1080, maxHeight: 1920, everyNthFrame: 1 });

const warte = ms => p.waitForTimeout(ms);
const hin = async (loc, steps = 28) => {  // Mauszeiger ruhig zum Element fahren
  await loc.scrollIntoViewIfNeeded();
  const k = await loc.boundingBox();
  await p.mouse.move(k.x + Math.min(k.width * 0.35, 90), k.y + k.height / 2, { steps });
  return loc;
};
const weich = async y => { await p.evaluate(y => scrollTo({ top: y, behavior: "smooth" }), y); await warte(900); };

await warte(1800);                                             // Dashboard: Punkte offen, GewSt 0 €
await weich(0);
const chipStamm = p.locator(".rail li", { hasText: "Stammdaten" }).first();
await chipStamm.evaluate(e => e.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" }));
await warte(700);
await (await hin(chipStamm)).click();
await warte(900);
const ersteller = p.locator("#f_meta_ersteller");
await (await hin(ersteller)).click();
await warte(250);
await p.keyboard.type("M. Muster", { delay: 95 });
await warte(400);
const hebe = p.locator("#f_param_hebesatz");
const y = await hebe.evaluate(e => e.getBoundingClientRect().top + scrollY - 380);
await weich(y);
await (await hin(hebe)).click({ clickCount: 3 });
await warte(300);
await p.keyboard.type("400", { delay: 230 });
await hebe.evaluate(e => e.dispatchEvent(new Event("change", { bubbles: true })));
await p.mouse.move(470, 300, { steps: 18 }); await p.mouse.down(); await p.mouse.up();   // daneben klicken statt Tab (sonst markiert das nächste Feld)
await warte(1400);                                             // Fußleiste: laufende Steuer springt
await weich(0);
const chipDash = p.locator(".rail li", { hasText: "Dashboard" }).first();
await chipDash.evaluate(e => e.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" }));
await warte(700);
await (await hin(chipDash)).click();
await warte(2600);                                             // Dashboard: vollständig, 14,9 %
const ende = Date.now() / 1000;   // letztes Bild bis hierher halten (bei Stillstand kommen keine Bilder)
await cdp.send("Page.stopScreencast");
await b.close();

// Bilder mit ihren echten Standzeiten zu 30 fps zusammensetzen
const liste = bilder.map((f, i) => `file '${f.datei}'\nduration ${((bilder[i + 1] ? bilder[i + 1].t : Math.max(ende, f.t + 0.1)) - f.t).toFixed(4)}`).join("\n")
  + `\nfile '${bilder[bilder.length - 1].datei}'\n`;
fs.writeFileSync(path.join(tmp, "liste.txt"), liste);
const ffmpeg = process.env.FFMPEG || "ffmpeg";
execFileSync(ffmpeg, ["-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", path.join(tmp, "liste.txt"),
  "-vf", "fps=30,scale=1080:1920,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "medium", ziel]);
console.log("✓", ziel, bilder.length, "Bilder");
