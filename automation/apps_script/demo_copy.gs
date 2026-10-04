/**
 * maehrtax – demo copy (Google Apps Script, runs in Loris' own Google account)
 *
 * Copies ONLY Reclaim bookings "Demo + Intro Call" from the main calendar into the calendar
 * "maehrtax Autopilot", so the weekly report (automation/weekly_report.py) can count them –
 * without the service account having to see the main calendar.
 *
 * Copied: time, booking date, source ("How did you hear about me?"). NO names, NO email addresses.
 * Test bookings without an outside guest are skipped. Cancelled bookings → the copy is deleted.
 * Other events in the autopilot calendar are never touched (only copies with the tag "maehrtaxDemo").
 * Independent of the German script "maehrsteuern Demo-Kopie" (different booking title, tag, calendar and marker).
 *
 * Setup: script.google.com → New project → paste this code → run the function "setup" once
 * (creates an hourly trigger) → allow access.
 */
const TARGET_NAME = 'maehrtax Autopilot';
const SEARCH = 'Demo + Intro Call';
const TAG = 'maehrtaxDemo';
const MARKER = 'maehrtax-demo';
const TIME_ZONE = 'America/New_York';
const QUESTION = 'How did you hear about me';
// answers in the required Reclaim field "How did you hear about me?" (dropdown) – recognized first
const OPTIONS = ['Instagram', 'LinkedIn', 'Referral', 'Google', 'Other'];

/** Read the source from the Reclaim description (HTML): first the fixed options after the question, otherwise the line after it. */
function readSource(html) {
  const text = (html || '').replace(/<br\s*\/?>/gi, '\n').replace(/<[^>]+>/g, '\n')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>');
  const pos = text.search(new RegExp(QUESTION, 'i'));
  if (pos < 0) return 'unknown';
  const after = text.slice(pos + QUESTION.length, pos + 300);
  const hits = OPTIONS.map(o => ({ o, i: after.search(new RegExp('\\b' + o + '\\b', 'i')) }))
    .filter(t => t.i >= 0).sort((x, y) => x.i - y.i);
  if (hits.length && hits[0].i < 120) return hits[0].o;  // first option right after the question
  const m = after.match(/^\??\s*[:\-–]?\s*([^\n]+)/) || after.match(/\n\s*([^\n]+)/);
  return m && m[1].trim() ? m[1].trim().slice(0, 40) : 'unknown';
}

function setup() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'copyBookings')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('copyBookings').timeBased().everyHours(1).create();
  copyBookings();
}

function copyBookings() {
  const target = CalendarApp.getCalendarsByName(TARGET_NAME)[0];
  if (!target) throw new Error('Calendar "' + TARGET_NAME + '" not found');
  const source = CalendarApp.getDefaultCalendar();
  const me = Session.getEffectiveUser().getEmail().toLowerCase();
  const from = new Date(Date.now() - 14 * 864e5), to = new Date(Date.now() + 90 * 864e5);

  const existing = {};
  target.getEvents(from, to).forEach(e => { const id = e.getTag(TAG); if (id) existing[id] = e; });

  const seen = {};
  source.getEvents(from, to, { search: SEARCH }).forEach(e => {
    const text = (e.getTitle() + '\n' + (e.getDescription() || ''));
    if (text.indexOf(SEARCH) < 0) return;
    const guests = e.getGuestList().map(g => g.getEmail().toLowerCase()).filter(m => m && m !== me);
    if (!guests.length) return;                                  // test booking
    const id = Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_1, e.getId())).slice(0, 16);
    seen[id] = true;
    const origin = readSource(e.getDescription());
    const booked = Utilities.formatDate(e.getDateCreated(), TIME_ZONE, 'yyyy-MM-dd');
    const description = MARKER + '\nBooked: ' + booked + '\nSource: ' + origin +
                        '\n(Copy from the main calendar, automatic – do not edit)';
    const old = existing[id];
    if (old) {
      if (old.getStartTime().getTime() !== e.getStartTime().getTime() || old.getDescription() !== description) {
        old.setTime(e.getStartTime(), e.getEndTime());
        old.setDescription(description);
      }
    } else {
      const created = target.createEvent('📅 Demo booked (' + origin + ')', e.getStartTime(), e.getEndTime(),
                                         { description: description });
      created.setTag(TAG, id);
      created.removeAllReminders();
    }
  });
  Object.keys(existing).forEach(id => { if (!seen[id]) existing[id].deleteEvent(); });  // cancelled
}
