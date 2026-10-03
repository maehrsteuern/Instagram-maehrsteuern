/**
 * maehrsteuern – Demo-Kopie (Google Apps Script, läuft in Loris' eigenem Google-Konto)
 *
 * Kopiert NUR Reclaim-Buchungen „Demo + Erstgespräch“ aus dem Hauptkalender in den Kalender
 * „maehrsteuern Autopilot“, damit der Wochenbericht (automatik/wochenbericht.py) sie zählen kann –
 * ohne dass das Dienstkonto den Hauptkalender sehen muss.
 *
 * Kopiert werden: Zeitpunkt, Buchungsdatum, Herkunft („Woher kennst du mich?“). KEINE Namen, KEINE E-Mail-Adressen.
 * Testbuchungen ohne fremden Gast werden ausgelassen. Abgesagte Buchungen → Kopie wird gelöscht.
 * Andere Termine im Autopilot-Kalender werden nie angefasst (nur Kopien mit Tag „maehrsteuernDemo“).
 *
 * Einrichtung: script.google.com → Neues Projekt → diesen Code einfügen → Funktion „einrichten“ einmal ausführen
 * (legt einen stündlichen Auslöser an) → Zugriff erlauben.
 */
const ZIEL_NAME = 'maehrsteuern Autopilot';
const SUCHE = 'Demo + Erstgespräch';
const TAG = 'maehrsteuernDemo';

function einrichten() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'kopieren')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('kopieren').timeBased().everyHours(1).create();
  kopieren();
}

function kopieren() {
  const ziel = CalendarApp.getCalendarsByName(ZIEL_NAME)[0];
  if (!ziel) throw new Error('Kalender „' + ZIEL_NAME + '“ nicht gefunden');
  const quelle = CalendarApp.getDefaultCalendar();
  const ich = Session.getEffectiveUser().getEmail().toLowerCase();
  const von = new Date(Date.now() - 14 * 864e5), bis = new Date(Date.now() + 90 * 864e5);

  const vorhanden = {};
  ziel.getEvents(von, bis).forEach(e => { const id = e.getTag(TAG); if (id) vorhanden[id] = e; });

  const gesehen = {};
  quelle.getEvents(von, bis, { search: SUCHE }).forEach(e => {
    const text = (e.getTitle() + '\n' + (e.getDescription() || ''));
    if (text.indexOf(SUCHE) < 0) return;
    const gaeste = e.getGuestList().map(g => g.getEmail().toLowerCase()).filter(m => m && m !== ich);
    if (!gaeste.length) return;                                  // Testbuchung
    const id = Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_1, e.getId())).slice(0, 16);
    gesehen[id] = true;
    const klartext = (e.getDescription() || '').replace(/<[^>]+>/g, '\n');
    const m = klartext.match(/Woher kennst du mich\??\s*[:\-–]?\s*\n*\s*([^\n]+)/i);
    const herkunft = m ? m[1].trim().slice(0, 40) : 'unbekannt';
    const gebucht = Utilities.formatDate(e.getDateCreated(), 'Europe/Berlin', 'yyyy-MM-dd');
    const beschreibung = 'maehrsteuern-demo\nGebucht: ' + gebucht + '\nHerkunft: ' + herkunft +
                         '\n(Kopie aus dem Hauptkalender, automatisch – nicht bearbeiten)';
    const alt = vorhanden[id];
    if (alt) {
      if (alt.getStartTime().getTime() !== e.getStartTime().getTime() || alt.getDescription() !== beschreibung) {
        alt.setTime(e.getStartTime(), e.getEndTime());
        alt.setDescription(beschreibung);
      }
    } else {
      const neu = ziel.createEvent('📅 Demo gebucht (' + herkunft + ')', e.getStartTime(), e.getEndTime(),
                                   { description: beschreibung });
      neu.setTag(TAG, id);
      neu.removeAllReminders();
    }
  });
  Object.keys(vorhanden).forEach(id => { if (!gesehen[id]) vorhanden[id].deleteEvent(); });  // abgesagt
}
