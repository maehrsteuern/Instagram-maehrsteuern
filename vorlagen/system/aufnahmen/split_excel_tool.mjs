/* Split-Screen-Aufnahme für Post 02 (Format A): gleiche Aufgabe, zwei Stoppuhren.
   node split_excel_tool.mjs <pfad/zu/steuerberechnung/index.html> <ziel_oben.mp4> <ziel_unten.mp4>
   Oben: Tabellen-Attrappe (excel_attrappe.html) – Hebesatz 400 -> 450, externe Verknüpfung -> #BEZUG!, Uhr läuft weiter.
   Unten: Ertragsteuer-Programm (Reel-Datensatz) – Hebesatz 400 -> 450, Fußleiste rechnet neu, Uhr stoppt.
   Ziel "-" überspringt eine Hälfte (z. B. nur unten neu aufnehmen).
   Die Delta-Plakette (+87.500) braucht den Fix aus Branch claude/delta-beim-tippen.
   Beide Hälften 1080x640 (Platz für die Safe-Zone: oben y 210–850, unten 860–1500) mit gleichem Zeitplan (Klick ins Feld bei ca. 1,6 s); Zusammensetzen im Schnitt. */
import { starte } from "./rekorder.mjs";
import path from "path";
import { fileURLToPath } from "url";

const [app, zielOben, zielUnten] = process.argv.slice(2);
const hier = path.dirname(fileURLToPath(import.meta.url));
const HALB = { breite: 600, format: [1080, 640] };
const ENDE = 11500;   // Länge beider Aufnahmen in ms

// ---- oben: Tabelle
if (zielOben !== "-") {
  const { p, warte, hin, beende, uhr } = await starte({ ...HALB, seite: path.join(hier, "excel_attrappe.html") });
  const t0 = Date.now();
  await uhr.zeige();
  await warte(1000);
  const hebe = p.locator("#hebe");
  await hin(hebe, 20);
  await uhr.start();
  await hebe.click();
  await warte(250);
  await p.keyboard.type("450", { delay: 200 });
  await p.keyboard.press("Enter");                               // -> #BEZUG! in GewSt, laufender Steuer, Rückstellung
  await warte(1300);
  await (await hin(p.locator("#gewst"), 22)).click();          // Formel zeigt auf eine Datei, die es dort nicht mehr gibt
  await warte(1500);
  await (await hin(p.locator("#reiter-daten"), 24)).click();
  await warte(500);
  await (await hin(p.locator("#m-verkn"), 14)).click();
  await warte(900);
  await (await hin(p.locator("#btn-akt"), 20)).click();          // Werte aktualisieren -> Fehler: Quelle nicht gefunden
  await warte(Math.max(0, ENDE - (Date.now() - t0)));
  await beende(zielOben);
}

// ---- unten: Programm
if (zielUnten !== "-") {
  const { p, warte, hin, beende, uhr } = await starte({ ...HALB, app, vorbereiten: async p => {
    // Vergleichswert der Fußleiste auf den Ausgangsstand setzen, damit das Delta nur die Hebesatz-Änderung zeigt
    await p.evaluate(() => { aktiv = "stamm"; renderModul(); deltaZeigen(berechne(S)); document.querySelectorAll(".kpi-delta").forEach(x => x.remove()); });
    await p.waitForTimeout(300);
    const y = await p.locator("#f_param_hebesatz").evaluate(e => e.getBoundingClientRect().top + scrollY - 150);
    await p.evaluate(y => scrollTo(0, y), y);
    await p.waitForTimeout(300);
  }});
  const t0 = Date.now();
  await uhr.zeige();
  await warte(1000);
  const hebe = p.locator("#f_param_hebesatz");
  await hin(hebe, 20);
  await uhr.start();
  await hebe.click({ clickCount: 3 });
  await warte(250);
  await p.keyboard.type("450", { delay: 200 });
  await hebe.evaluate(e => { e.dispatchEvent(new Event("change", { bubbles: true })); e.blur(); });
  await warte(700);
  await uhr.stopp("fertig");                                     // Fußleiste: laufende Steuer, Plakette +87.500
  await p.mouse.move(300, 250, { steps: 20 });
  await warte(Math.max(0, ENDE - (Date.now() - t0)));
  await beende(zielUnten);
}
