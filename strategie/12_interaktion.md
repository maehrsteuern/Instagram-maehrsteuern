# 12 · Zweite Säule: Interaktion (Reichweite + Kontakte)

Ziel: mehr Reichweite und echte Kontakte zu Kanzleien und Steuerabteilungen. Dafür brauchst du **ca. 15 Min. am Tag** und nutzt **nur offizielle Wege** – kein Bot, der folgt, liked oder Massen-DMs schreibt.
Warum: Fremde Konten über die Schnittstelle anschreiben geht nicht. Bots verstoßen gegen die Instagram-Regeln (Sperre droht), und ungefragte Werbe-DMs sind nach § 7 UWG heikel.

## Wer macht was

| # | Baustein | Läuft wo | Deine Zeit |
|---|---|---|---|
| 1 | **Radar** – frische Beiträge aus der Nische, mit Kommentarvorschlag | `automatik/radar.py`, täglich ca. 07:00 → Issue „📡 Radar …“ | 10 Min. |
| 2 | **DM-Entwürfe** – Erstkontakt, erst nachdem du 2× unter den Beiträgen eines Kontos kommentiert hast | im Radar-Issue | 5 Min. |
| 3 | **Kommentar-Stichwort → DM** (TOOL) | **ManyChat** | 0 |
| 4 | **Kommentar-Hilfe** – neue Kommentare unter deinen Beiträgen mit Antwortvorschlag | `automatik/kommentare.py`, alle 15 Min. → Issue „💬 Kommentare beantworten“ | 1–2 Min. pro Beitrag |
| 5 | **Anzeige, die eine DM öffnet** (1 €/Tag) | Werbeanzeigenmanager + **ManyChat** | einmal 20 Min. |
| 6 | **Collab der Woche** – passendes Konto plus Anfrage-Entwurf | im Radar-Issue (montags) | 5 Min./Woche |
| 7 | **LinkedIn** – jedes Karussell als PDF-Dokument plus umgeschriebener Text | `automatik/linkedin.py` → Issue „💼 LinkedIn …“ | 2 Min. pro Karussell |

Einstellungen: `automatik/interaktion.json`, gemerkte Kontakte: `automatik/interaktion/kontakte.json`.

## So arbeitest du damit (Tagesablauf)
1. **Morgens:** Radar-Issue öffnen, 5–8 Beiträge ansehen, Vorschlag **in eigene Worte bringen**, kommentieren, abhaken.
2. **Warme Konten:** Steht ein DM-Entwurf da, und es fühlt sich passend an → von Hand schicken, abhaken. Kommt keine Antwort, ist das okay. Nicht nachhaken.
3. **Nach eigenem Post (erste Stunde):** GitHub-Benachrichtigung „💬 Kommentare“ → im Issue `K12 ok` (Vorschlag posten) oder `K12 eigener Text`. Oder direkt in der App antworten.
4. **Montags:** Collab-Vorschlag ansehen, Anfrage anpassen und schicken.
5. **Am LinkedIn-Tag:** PDF und Text aus dem Issue hochladen, Issue schließen.

Abgehakte Kästchen zählen: Wer 2× kommentiert wurde, bekommt einen DM-Entwurf. Wer eine DM bekommen hat, bekommt keinen zweiten.

## Konten für den Radar (Pflege: einmalig 20 Min., danach ab und zu)
In `automatik/interaktion.json` → `radar.konten` 20–40 Business- oder Creator-Konten eintragen, z. B.:
```json
"konten": [
  {"name": "kanzleiname", "art": "kanzlei"},
  {"name": "steuer_creator", "art": "creator"}
]
```
Gute Kandidaten: Kanzleien mit aktivem Instagram, Steuer-/Buchhaltungs-Creator mit 1.000–50.000 Followern, DATEV- und Excel-Konten, Steuerberaterexamen-Seiten, Fachschulen. **Nicht:** private Konten (liefert die Schnittstelle nicht), Konten deines Arbeitgebers.
Finden: Instagram-Suche nach „Steuerberater“, „Steuerkanzlei“, „Jahresabschluss“; wer unter deinen Beiträgen kommentiert; „Ähnliche Konten“ auf passenden Profilen. Schick mir die Namen, ich trage sie ein.

## Hashtags
Die Hashtag-Suche braucht bei Meta die Freigabe **„Instagram Public Content Access“** (App-Prüfung mit Unternehmensnachweis). Bis dahin meldet der Radar „Hashtags noch nicht verfügbar“ und arbeitet nur mit der Kontenliste – das reicht für den Anfang. Höchstens 30 verschiedene Hashtags in 7 Tagen.

## 5 · Anzeige, die eine DM öffnet (Click-to-DM, ca. 30 €/Monat)
Das ist der einzige erlaubte Weg, Fremde automatisch ins DM-Gespräch zu holen: Sie tippen selbst auf „Nachricht senden“. Danach übernimmt ManyChat.
1. **ManyChat:** *Automation → New → Trigger „Instagram Ads JSON“* (oder „Ad“) → Fluss = DM-Strecke ① aus `04_dm_strecke.md` → JSON kopieren.
2. **Werbeanzeigenmanager** (business.facebook.com/adsmanager) → *Erstellen* → Ziel **Interaktion** → Interaktionsort **Nachrichten-Apps → Instagram**.
3. **Budget:** 1 € pro Tag, Laufzeit 30 Tage. **Ort:** Deutschland. **Alter:** 25–55. **Interessen:** Steuerberatung, DATEV, Buchhaltung, Microsoft Excel, Wirtschaftsprüfung. Platzierung: nur Instagram (Feed, Reels).
4. **Anzeige:** vorhandenen Beitrag nutzen – am besten das Reel mit den meisten Speicherungen (z. B. Ampel, Split-Screen). Nachrichtenvorlage: *Benutzerdefiniert* → ManyChat-JSON einfügen.
5. **Nach 7 Tagen prüfen:** Kosten pro Gespräch unter 1,50 € = gut. Darüber: anderes Reel oder enger zielen (nur „Steuerberater“).

Text-Vorschlag für die Anzeige:
> Excel-Liste mit #BEZUG! zwei Tage vor der Frist? Ich zeig dir, wie das Steuer-Tool das in Sekunden löst – mit Beispieldaten. Schreib mir „TOOL“.

## 6 · Collab-Formate (für die Anfrage)
- **Collab-Beitrag** (beide Profile als Autor): „Steuerberater vs. Code“ – sie erklären die Regel, du zeigst die Berechnung.
- **Gast-Folie:** Ein Tipp von ihnen in deinem Karussell, mit Markierung.
- **Story-Q&A:** Ihr beantwortet gemeinsam Fragen, jeder teilt beim anderen.
- **Live (später):** 20 Minuten „Jahresabschluss-Fehler, die wir ständig sehen“.
Regel: Erst 2–3× ehrlich kommentieren, dann anfragen. Kleine Konten (1.000–10.000 Follower) sagen viel öfter ja.

## Grenzen (damit Instagram nicht drosselt)
- Höchstens ca. **10 Kommentare** und **5 neue DMs am Tag**, verteilt, nie dieselbe Nachricht kopiert.
- Kein Folgen/Entfolgen-Spiel, keine Kommentar-Gruppen, keine gekauften Follower.
- In DMs keine echten Mandanten- oder Firmendaten annehmen (siehe `04_dm_strecke.md`).
- Nichts über den Arbeitgeber, auch nicht in Kommentaren.

## Kosten
| Posten | pro Monat |
|---|---|
| Claude-Vorschläge (Radar, Kommentare, LinkedIn) | ca. 2–5 € |
| Anzeige Click-to-DM | ca. 30 € (1 €/Tag) |
| ManyChat Pro (ab ca. 1.000 Kontakten nötig) | ca. 15 € |
| Meta-Schnittstellen, GitHub Actions | 0 € |
