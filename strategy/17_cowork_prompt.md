# 17 · Cowork prompt – set up @maehrtax

Paste the block below into a **Claude Cowork** session with Claude in Chrome (logged in to Instagram, Facebook, ManyChat, Reclaim and GitHub as Loris). It is written in German because Loris runs it; every text that ends up on the profile is US English.

```text
Moin! Du richtest mit mir das neue englische Instagram-Konto für die USA ein – die Schwester von @maehrsteuern.
Handle: @maehrtax (gesprochen „more tax“ – dasselbe Wortspiel wie „mehr Steuern“). Leitspruch: „Tax × Code“.
Alles, was im Profil steht, ist US-Englisch. Mit mir redest du Deutsch.
Arbeite die Module A–E der Reihe nach ab. Frag mich vor jedem Modul kurz: „Modul X starten?“

══════════ GRUNDREGELN ══════════
- Login, 2-Faktor, Bestätigungscodes, Passwörter: STOPP – das mache ich. Passwörter nie in den Chat.
- Keine Schlüssel/Tokens in den Chat. Wenn ein Token angezeigt wird: STOPP, ich kopiere ihn selbst in GitHub-Secrets.
- Zahlungen, Abos, Testphasen mit Zahlungsdaten, Anträge bei Meta: STOPP vor dem Absenden.
- Nichts posten, niemandem folgen, nichts liken, keine DMs – das neue Konto bleibt bis zum Start (So 11.10.) leer.
- Nichts am deutschen Konto @maehrsteuern ändern.
- Keine Arbeitgeber-Namen oder -Daten, nirgends.
- Am Ende jedes Moduls: kurzer Bericht (Format steht beim Modul).

══════════ MODUL A – Konto anlegen + Profil (ca. 20 Min.) ══════════
1. instagram.com (oder App) → Profil @maehrsteuern → Kontenübersicht / „Konto hinzufügen“ → „Neues Konto erstellen“.
   Frag mich nach der E-Mail-Adresse (Vorschlag: ein Gmail-Alias mit „+maehrtax“, damit alles in mein Postfach geht).
   Benutzername in dieser Reihenfolge versuchen: maehrtax · maehr.tax · maehrtax.ai · taxtimescode
   Nimm den ersten freien und sag mir sofort, welcher es geworden ist.
2. Auf Profi-Konto umstellen: Typ „Creator“ (Ersteller). Kategorie: „Business consultant“/„Unternehmensberater“,
   falls nicht angeboten „Entrepreneur“. Kontaktdaten nicht öffentlich anzeigen.
3. Profil ausfüllen – exakt so:
   Name:   Loris | Tax × Code
   Bio:
   🧠 Tax × Code – tax know-how that computes
   ⚙️ AI + code tools for tax teams that actually run
   🇩🇪 German-trained tax pro · Certified AI Manager
   💬 DM "TOOL" → free demo
   Link: erst nach Modul E eintragen (englischer Buchungslink). Bis dahin leer lassen.
   Profilbild: dasselbe Foto wie bei @maehrsteuern (Konsistenz) – frag mich, falls du es nicht findest.
4. Einstellungen: Konto öffentlich · Sprache Englisch · Region USA, falls wählbar · „Ähnliche Konten vorschlagen“ an.
   Nachrichten-Anfragen von allen erlauben (wichtig für „TOOL“-DMs).
Bericht: Benutzername · Kontotyp/Kategorie · Bio übernommen ja/nein · Profilbild ja/nein.

══════════ MODUL B – Meta-Anbindung für die Automatik (ca. 25 Min.) ══════════
Anleitung im Detail: SETUP.md im Repo maehrtax---instagram (github.com/maehrsteuern/maehrtax---instagram).
1. facebook.com → neue Facebook-Seite „Loris | Tax × Code“ (Kategorie Business consultant), nichts posten.
   Seite mit @maehrtax verknüpfen (Seiten-Einstellungen → Verknüpfte Konten → Instagram).
2. developers.facebook.com/apps → vorhandene App „maehrsteuern Autopilot“ → App-Rollen → Rollen →
   „Instagram-Tester hinzufügen“ → @maehrtax. Dann in Instagram (als @maehrtax) die Tester-Einladung annehmen:
   Einstellungen → Website-Berechtigungen → Apps und Websites → Tester-Einladungen.
3. App → Anwendungsfälle → Instagram-API → API-Einrichtung mit Instagram-Login → „Zugriffstoken generieren“ →
   Konto hinzufügen → @maehrtax → alle Berechtigungen erlauben.
   STOPP: Token und Instagram-Konto-ID werden angezeigt → ich kopiere sie selbst in die GitHub-Secrets
   IG_TOKEN und IG_USER_ID des neuen Repos. Du schreibst sie NICHT in den Chat.
4. Für den Radar (Business Discovery) den Weg aus SETUP.md Schritt „FB_TOKEN“ mit der neuen Facebook-Seite gehen –
   auch hier STOPP, sobald ein Token erscheint.
Bericht: Facebook-Seite angelegt + verknüpft ja/nein · Tester angenommen ja/nein · Token erzeugt (von mir kopiert) ja/nein.

══════════ MODUL C – Radar-Konten USA prüfen und ergänzen (ca. 30 Min.) ══════════
Ziel: 40 aktive US-Konten aus unserer Nische, die der Radar täglich beobachtet (wir kommentieren dort von Hand).
Claude Code hat schon vorrecherchiert: automation/interaction.json im Repo maehrsteuern/maehrtax---instagram
→ radar.accounts (40 Konten, Handle per Web belegt) und radar.candidates_to_verify (17 unsichere Kandidaten).
1. Jedes Konto aus radar.accounts auf instagram.com öffnen und prüfen: existiert, öffentlich, Business/Creator,
   Sitz USA, letzter Beitrag < 30 Tage, wirklich Nische (Steuern/Accounting/Tax-Tech/CPA-Ausbildung).
2. Dasselbe für radar.candidates_to_verify.
3. Lücken auffüllen, bis 40 gute Konten stehen – Mischung ca. 12 CPA-Kanzleien/Tax-Preparer · 12 Creator ·
   8 Software/Tech · 8 Ausbildung. Suche über #taxprofessional #cpa #taxseason #accountingtech #taxtech #asc740
   #salestax #corporatetax #cpaexam. Bevorzugt 1.000–100.000 Follower.
   Nicht: private Konten, Behörden, Werbe-/Gewinnspielkonten, „Tax-Hacks“ Richtung Hinterziehung.
Bericht: Tabelle (Benutzername · Art: cpa_firm | creator | software | education · Follower ca. · letzter Beitrag ·
behalten/raus/neu) – und genau diesen JSON-Block mit der fertigen Liste zum Einfügen in radar.accounts:
[{"name": "beispielkonto", "kind": "creator"}, …]

══════════ MODUL D – ManyChat für @maehrtax (ca. 20 Min.) ══════════
1. app.manychat.com → neues Konto/Seite hinzufügen → Instagram → @maehrtax verbinden. Free-Plan.
   STOPP bei jeder Plan-/Zahlungsfrage – ich entscheide (Trial nur ohne automatische Verlängerung).
2. Automation „Auto-send links from comments, story replies, or DMs“ – Stichwörter: TOOL, Tool, tool, tol, TOOLS, tools.
   Gilt für: Kommentare unter allen Beiträgen + Story-Antworten + DMs.
   Öffentliche Antwort auf Kommentar (rotierend): „Sent you a DM 📩“ · „Check your DMs 👀“ · „On its way – check your inbox ⚙️“
   DM-Text (aus strategy/04_dm_funnel.md, sonst diesen nehmen):
   „Hey! 👋 Here's the free demo: a tax tool that replaces the spreadsheet chaos – with sample data, 2 minutes.
   🎁 Bonus: The Spreadsheet-to-Code Checklist for Tax Teams.
   Want to see it with your own workflow? Book a free 20-min demo + intro call: <LINK AUS MODUL E>
   (Educational only – not tax advice.)“
   Button 1: „Book the demo“ → Link aus Modul E · Button 2: „Get the checklist“ → Link folgt (vorerst weglassen, wenn kein Link).
   Follow-up nach 23 h, falls kein Klick: „Quick one – did the demo make sense? Happy to show it live (20 min, free): <LINK>“
3. Testen: Es gibt noch keine Beiträge – deshalb nur per DM. Ich schicke von meinem Privatkonto „TOOL“ an @maehrtax,
   du prüfst in ManyChat, ob die Antwort rausging.
Bericht: verbunden ja/nein · Stichwörter · Test-DM angekommen ja/nein · Plan/Kosten.

══════════ MODUL E – Englischer Buchungslink (Reclaim, ca. 10 Min.) ══════════
1. app.reclaim.ai → mein Demo-Konto (dasselbe wie für @maehrsteuern – NICHT das Outlook-Konto B) → Scheduling Links →
   neuen Link anlegen: Titel „Demo + Intro Call (20 min)“, Dauer 20 Min., Slug „maehrtax-demo“ (oder ähnlich frei).
   Zeitfenster für US-Kunden: Mo–Fr 15:00–20:00 deutscher Zeit (= 9 AM–2 PM ET), Zeitzone der Buchenden automatisch anzeigen.
   Pflichtfrage: „How did you hear about me?“ (Optionen: Instagram · LinkedIn · Referral · Other).
   Kalender-Titel der Buchung: „Demo + Intro Call – <Name> (US)“. Sprache Englisch.
2. Link in die Bio von @maehrtax eintragen (Modul A, Schritt 3) und in ManyChat (Modul D) einsetzen.
Bericht: Link-URL · Zeitfenster · in Bio + ManyChat eingetragen ja/nein.

══════════ ABSCHLUSS ══════════
Gib mir diesen Text zum Kopieren für Claude Code aus und setz die Berichte ein:
„Moin Claude Code, Cowork-Setup für @maehrtax erledigt:
<BERICHTE A–E>
Bitte: Radar-Konten in automation/interaction.json übernehmen, Buchungslink in Bio-Doku, ManyChat-Text und
DM-Strecke eintragen, STATUS.md neu erzeugen und sagen, was bis zum Start (So 11.10.) noch fehlt.“
```

## After Cowork
- Loris adds the secrets in the new repo (SETUP.md) – never via chat.
- Claude Code: radar accounts → `automation/interaction.json`, booking link → `strategy/02_bio_highlights.md`, `strategy/04_dm_funnel.md`, regenerate STATUS.md.
