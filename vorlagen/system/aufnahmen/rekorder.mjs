/* Gemeinsame Aufnahmetechnik für Klickstrecken im Ertragsteuer-Programm.
   Playwright (Chromium) + CDP-Screencast in Gerätepixeln, sichtbarer Mauszeiger mit Klick-Welle,
   Zusammensetzen zu 1080x1920 bei 30 fps über ffmpeg (imageio-ffmpeg).
   Umgebung: PW_PFAD (node_modules mit playwright), CHROMIUM, FFMPEG. */
import { createRequire } from "module";
import fs from "fs";
import path from "path";
import { execFileSync } from "child_process";
const require = createRequire(process.env.PW_PFAD || import.meta.url);
const { chromium } = require("playwright");

/* breite: CSS-Breite des Fensters; 540 = Handy-Ansicht, 600 = breite Tabellen passen noch.
   format: Ausgabegröße, [1080, 1920] ganzes Reel oder [1080, 960] eine Hälfte im Split-Screen.
   seite: statt des Programms eine andere Seite aufnehmen (z. B. excel_attrappe.html).
   vorbereiten(p): setzt die Ausgangslage, bevor die Aufnahme startet. */
export async function starte({ app, seite, breite = 540, format = [1080, 1920], vorbereiten }) {
  const [ausB, ausH] = format;
  const hoehe = Math.round(breite * ausH / ausB);
  const tmp = fs.mkdtempSync("/tmp/aufnahme-");
  const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  const p = await b.newPage({ viewport: { width: breite, height: hoehe }, deviceScaleFactor: ausB / breite, colorScheme: "dark" });
  await p.addInitScript(() => { localStorage.setItem("ertragsteuern.theme", "dark"); localStorage.setItem("ertragsteuern.lang", "de"); });
  if (seite) await p.goto("file://" + path.resolve(seite));
  else {
    await p.goto("file://" + path.resolve(app) + "?demo=reel");
    await p.waitForTimeout(1500);
    await p.locator("#btn-ein-demo").click().catch(() => {});
  }
  if (vorbereiten) await vorbereiten(p);
  // sichtbarer Mauszeiger mit Klick-Welle (headless zeigt keinen)
  await p.evaluate(([x, y]) => {
    const c = document.createElement("div");
    c.id = "rec-cursor";
    c.innerHTML = `<svg width="26" height="26" viewBox="0 0 24 24"><path d="M4 2l15 11-6.5 1.2L16 21l-3 1.4-3.4-6.6L4 20z" fill="#fff" stroke="#000" stroke-width="1.4" stroke-linejoin="round"/></svg>`;
    Object.assign(c.style, { position: "fixed", left: x + "px", top: y + "px", zIndex: 2147483647, pointerEvents: "none", transition: "none", filter: "drop-shadow(0 2px 3px rgba(0,0,0,.5))" });
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
  }, [breite / 2, hoehe * 0.65]);
  await p.mouse.move(breite / 2, hoehe * 0.65);
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
  await cdp.send("Page.startScreencast", { format: "jpeg", quality: 92, maxWidth: ausB, maxHeight: ausH, everyNthFrame: 1 });

  const warte = ms => p.waitForTimeout(ms);
  const hin = async (loc, steps = 28) => {  // Mauszeiger ruhig zum Element fahren
    await loc.scrollIntoViewIfNeeded();
    const k = await loc.boundingBox();
    await p.mouse.move(k.x + Math.min(k.width * 0.35, 90), k.y + k.height / 2, { steps });
    return loc;
  };
  const weich = async (y, ms = 900) => { await p.evaluate(y => scrollTo({ top: y, behavior: "smooth" }), y); await warte(ms); };
  const oben = loc => loc.evaluate(e => e.getBoundingClientRect().top + scrollY);   // Seitenposition eines Elements

  async function beende(ziel) {
    const ende = Date.now() / 1000;   // letztes Bild bis hierher halten (bei Stillstand kommen keine Bilder)
    await cdp.send("Page.stopScreencast");
    await b.close();
    // Bilder mit ihren echten Standzeiten zu 30 fps zusammensetzen
    const liste = bilder.map((f, i) => `file '${f.datei}'\nduration ${((bilder[i + 1] ? bilder[i + 1].t : Math.max(ende, f.t + 0.1)) - f.t).toFixed(4)}`).join("\n")
      + `\nfile '${bilder[bilder.length - 1].datei}'\n`;
    fs.writeFileSync(path.join(tmp, "liste.txt"), liste);
    execFileSync(process.env.FFMPEG || "ffmpeg", ["-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", path.join(tmp, "liste.txt"),
      "-vf", `fps=30,scale=${ausB}:${ausH},format=yuv420p`, "-c:v", "libx264", "-crf", "16", "-preset", "medium", ziel]);
    fs.rmSync(tmp, { recursive: true, force: true });
    console.log("✓", ziel, bilder.length, "Bilder");
  }
  // Stoppuhr oben rechts im Bild: uhr.start(), uhr.stopp("fertig") – läuft in Echtzeit mit der Aufnahme
  const uhr = {
    zeige: () => p.evaluate(() => {
      const u = document.createElement("div"); u.id = "rec-uhr";
      Object.assign(u.style, { position: "fixed", right: "14px", top: "12px", zIndex: 2147483645, pointerEvents: "none",
        font: "700 22px/1 ui-monospace, 'DejaVu Sans Mono', monospace", color: "#fff", background: "rgba(20,20,20,.82)",
        padding: "8px 12px", borderRadius: "10px", border: "2px solid rgba(255,255,255,.25)" });
      u.textContent = "⏱ 0,0 s"; document.body.appendChild(u);
    }),
    start: () => p.evaluate(() => {
      const u = document.getElementById("rec-uhr"), t0 = performance.now();
      window._uhr = setInterval(() => { u.textContent = "⏱ " + ((performance.now() - t0) / 1000).toFixed(1).replace(".", ",") + " s"; }, 50);
    }),
    stopp: text => p.evaluate(text => {
      clearInterval(window._uhr);
      const u = document.getElementById("rec-uhr");
      u.textContent = "✓ " + u.textContent.slice(2) + (text ? " · " + text : "");
      Object.assign(u.style, { background: "#53C3A2", color: "#06201a", borderColor: "#53C3A2" });
    }, text),
  };
  return { p, warte, hin, weich, oben, beende, uhr };
}
