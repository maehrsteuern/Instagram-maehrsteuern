/* Bildschirmaufnahme Ertragsteuer-Programm: Abschlussreife Gelb -> Gruen.
   node ampel_gelb_gruen.mjs <pfad/zu/steuerberechnung/index.html> <ziel.mp4>
   Technik und Umgebungsvariablen: rekorder.mjs. Reel-Datensatz: index.html?demo=reel.
   Ablauf: Dashboard "Punkte offen" -> Stammdaten -> Ersteller -> Hebesatz 400 -> Dashboard "vollstaendig". */
import { starte } from "./rekorder.mjs";

const [app, ziel] = process.argv.slice(2);
const { p, warte, hin, weich, oben, beende } = await starte({ app, breite: 540, vorbereiten: p =>
  // Ausgangslage: Hebesatz und Ersteller fehlen -> Abschlussreife gelb
  p.evaluate(() => { S.param.hebesatz = 0; S.meta.ersteller = ""; aktiv = "dash"; renderModul(); scrollTo(0, 0); }) });

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
await weich(await oben(hebe) - 380);
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
await beende(ziel);
