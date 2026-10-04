/* Bildschirmaufnahme Ertragsteuer-Programm: GewSt-Hinzurechnung live eintippen (Post 03, Format B).
   node gewst_hinzurechnung.mjs <pfad/zu/steuerberechnung/index.html> <ziel.mp4>
   Technik und Umgebungsvariablen: rekorder.mjs. Breite 600, damit die Rechentabelle ganz ins Bild passt.
   Zahlen wie im Karussell (Folie 5): Zinsen 150.000, Maschinenmiete 100.000, Büromiete 400.000, Lizenzen 80.000
   -> Summe 390.000 ./. Freibetrag 200.000 = 190.000, davon ein Viertel = 47.500. */
import { starte } from "./rekorder.mjs";

const [app, ziel] = process.argv.slice(2);
const POSTEN = [["a", "150000"], ["d", "100000"], ["e", "400000"], ["f", "80000"]];
const { p, warte, hin, weich, oben, beende } = await starte({ app, breite: 600, vorbereiten: async p => {
  // Ausgangslage: Modul Gewerbesteuer, keine Hinzurechnungen erfasst, Eingabekarte oben im Bild
  await p.evaluate(() => { S.gewst.hz = {}; aktiv = "gewst"; renderModul(); });
  const y = await p.locator("#f_gewst_hz_a").evaluate(e => e.closest(".card").getBoundingClientRect().top + scrollY - 190);
  await p.evaluate(y => scrollTo(0, y), y);
  await p.waitForTimeout(300);
}});

await warte(1500);                                             // leere Eingabemaske
for (const [k, betrag] of POSTEN) {
  const feld = p.locator(`#f_gewst_hz_${k}`);
  await (await hin(feld, 22)).click();
  await warte(200);
  await p.keyboard.type(betrag, { delay: 110 });
  await feld.evaluate(e => { e.dispatchEvent(new Event("change", { bubbles: true })); e.blur(); });
  await warte(450);
}
await warte(600);
// runter zur Rechnung: Posten mit Quote, Summe, Freibetrag, ein Viertel
const tabelle = p.locator("details.exp").first();
await weich(await oben(tabelle) - 780, 1600);
await warte(1200);
const herleitung = p.locator("details.exp summary").first();
await (await hin(herleitung, 24)).click();                     // Herleitung: 25 % × 190.000 = 47.500
await warte(3000);
await beende(ziel);
