# LinkedIn 1 · Wissen – wie der Algorithmus bewertet (Stand 03.10.2026, ENTWURF – Loris prüft)

Neu geschrieben von Claude aus allgemeinem Wissen über LinkedIn (Veröffentlichungen von LinkedIn selbst,
Branchenauswertungen 2024–2026). **Keine Zahl hier ist an unserem Profil geprüft.** Sobald die Erstanalyse
(`prompts/01_erstanalyse.md`) und die ersten 4 Wochen Statistik da sind, gewinnen unsere eigenen Zahlen.
Gegenstück auf Instagram: `strategie/11_wissen_instagram.md`.

## Grundsatz: LinkedIn ist kein zweites Instagram
| | Instagram | LinkedIn |
|---|---|---|
| Wer erreicht wird | vor allem Nicht-Follower (Reels) | vor allem **das eigene Netzwerk** und dessen Netzwerk (2. Grad) |
| Stärkstes Signal | Geteilt per DM, Zuschauzeit | **Verweildauer (Dwell Time)** und **Kommentare mit Inhalt** |
| Absender | Marke @maehrsteuern | **die Person Loris** – persönliche Profile erreichen ein Vielfaches einer Unternehmensseite |
| Uhrzeit | abends 19:30 | **morgens vor der Arbeit / Mittagspause** (B2B, Berufstätige) |
| Ton | Du, locker | neutral bis Du, fachlich, eigene Meinung |
| Lebensdauer | 1–2 Tage | 2–3 Tage, Kommentare holen Beiträge oft am Tag 2 wieder hoch |

## Wie ein Beitrag verteilt wird
1. **Qualitätsfilter** direkt nach dem Posten: Spam, Engagement-Köder („Kommentiere JA“), viele Markierungen, reine
   Link-Beiträge werden gebremst.
2. **Testgruppe:** ein kleiner Teil des Netzwerks sieht den Beitrag. Gemessen wird: Wie lange bleiben sie stehen
   (Verweildauer, „mehr anzeigen“ geklickt, Dokument durchgeblättert), wer kommentiert, wer reagiert.
3. **Ausweitung** auf mehr Kontakte und den 2. Grad, wenn die Testgruppe reagiert. Die **ersten 60–90 Minuten**
   entscheiden – deshalb posten, wenn Loris danach eine Stunde antworten kann.
4. **Themen-Abgleich:** Seit 2025 bewertet LinkedIn mit einem großen Sprachmodell, *worüber* ein Beitrag ist, *wer*
   ihn geschrieben hat und *wen* das Thema interessiert. Folge: **Profil (Headline, Info, Erfahrung) und Beiträge
   müssen dasselbe Thema erzählen.** Wer konsequent über Steuern × Code schreibt, wird zu diesem Thema ausgespielt –
   auch an Nicht-Kontakte. Themen-Sprünge (heute KI-News, morgen Urlaubsfoto) verwässern das.

## Signale – Rangfolge
1. **Kommentare mit Substanz** (mehrere Sätze) > kurze Kommentare > Reaktionen. Antworten des Autors auf Kommentare
   verlängern die Diskussion und zählen mit.
2. **Verweildauer:** Dokumente (PDF-Karussell) und gut gegliederte Texte mit „mehr anzeigen“ halten Leute fest.
3. **Speichern und Teilen** (inkl. „Senden“ per Nachricht) – ähnlich wie auf Instagram, aber seltener.
4. **Profilbesuche und Folgen danach** – zeigt LinkedIn, dass der Autor relevant ist.
5. Reaktionen (Like) – schwaches Signal.

## Formate – was zu maehrsteuern passt
| Format | Stärke | Unser Einsatz | Quelle im Repo |
|---|---|---|---|
| **Dokument (PDF-Karussell)** | höchste Verweildauer, wird gespeichert | Praxis- und Wissens-Karussells | `posts/*/linkedin/karussell.pdf` (gibt es schon, `automatik/linkedin.py`) |
| **Text (+ 1 Bild)** | Meinung, Erfahrung, Geschichte – erzeugt Kommentare | „Hinter dem Code“, Thesen, Lehren aus Projekten | neu, aus Sprechtexten und Karussell-Thesen |
| **Video hochformatig** | LinkedIn baut den Video-Feed aus, wenig Konkurrenz in der Steuer-Nische | Demo-Reels, Stimm-Reels, mit Untertiteln | `posts/*/reel*.mp4` |
| Umfrage | viel Reichweite, wenig Wert; wird inzwischen gedrosselt | höchstens 1× im Monat, nur mit echter Fachfrage | – |
| Newsletter (LinkedIn-Artikel) | Abonnenten bekommen eine Benachrichtigung | **später** (ab ca. 500 Followern), z. B. „Steuern × Code – monatlich“ | – |
| Storys | gibt es auf LinkedIn nicht mehr | – | – |

## Text – Regeln
- **Die ersten 2 Zeilen** (ca. 140–200 Zeichen) stehen vor „mehr anzeigen“ – dort kommt der Haken hin: These, Zahl
  oder Fehler. Kein „Ich freue mich, …“.
- Kurze Absätze, 1–3 Sätze, Leerzeilen dazwischen. 800–1.500 Zeichen sind ein guter Bereich.
- **Eigene Erfahrung und Meinung** schlagen allgemeine Tipps (der Themen-Abgleich erkennt austauschbaren Inhalt).
- Ende: **eine echte Fachfrage** an Steuerleute – keine Köderfragen.
- **0–3 Hashtags** – sie bringen kaum noch Reichweite, schaden in Maßen nicht.
- **Keine externen Links im Beitrag** (bremsen sichtbar). Demo-Link gehört in „Im Fokus“ und ins Profil; im Beitrag
  „Demo gefällig? Kurze Nachricht an mich genügt.“ Link im ersten Kommentar nur, wenn es nicht anders geht.
- Personen nur markieren, wenn sie wirklich beteiligt sind (sonst wertet LinkedIn es als Köder).
- In der ersten Stunde nicht groß nachbearbeiten.

## Takt und Uhrzeit (Vorschlag, nach 4 Wochen an eigenen Zahlen prüfen)
- **3 Beiträge pro Woche**, nie mehr als 1 pro 24 h (Beiträge nehmen sich sonst gegenseitig Reichweite).
- **Di, Mi, Do zwischen 07:45 und 08:30**, kein Wochenende.
- Die Instagram-Inhalte kommen **mit 1 Tag Abstand** (Karussell Di 19:30 auf Instagram → Mi 08:00 als Dokument auf
  LinkedIn) – so laufen keine zwei ersten Stunden gleichzeitig.

| Tag | LinkedIn | Herkunft |
|---|---|---|
| Di 08:00 | Text: These oder Erfahrung („Hinter dem Code“, Lehre aus der Woche) | neu geschrieben |
| Mi 08:00 | Dokument: Karussell vom Di | Instagram-Karussell |
| Do 08:00 | Video: Begleit- oder Demo-Reel, **oder** Dokument zum Karussell vom Do | Instagram-Reel / -Karussell |

## Interaktion – der eigentliche Hebel bei kleinem Netzwerk
- **Kommentieren bei anderen** bringt am Anfang mehr als eigene Beiträge: 15–20 Min. am Tag, 5–10 durchdachte
  Kommentare (2–4 Sätze, eigener Fachpunkt) bei Steuerberatern, Steuerabteilungs-Leitern, DATEV-/Excel-Leuten,
  Tax-Tech-Accounts. Am besten direkt nach deren Beitrag.
- **Vernetzen** gezielt mit der Zielgruppe (Steuerabteilung, Kanzlei, Examens-Kollegen 2025), mit kurzer persönlicher
  Notiz, max. 15–20 Anfragen am Tag. Offene Anfragen, die nach 3 Wochen nicht angenommen sind, zurückziehen.
- **Auf jeden Kommentar** am eigenen Beitrag innerhalb der ersten Stunde antworten – mit einer Rückfrage.
- **Keine Cold-DMs mit Verkauf.** Gleicher Grundsatz wie auf Instagram: Leute melden sich von selbst.

## Profil – was der Algorithmus und Besucher lesen
- **Headline** (220 Zeichen): Wem hilfst du wobei + Beleg. Sie steht unter jedem Kommentar – wichtigste Werbefläche.
- **Info** (2.600 Zeichen, die ersten ~3 Zeilen sind sichtbar): Problem der Zielgruppe → was du baust → Beleg →
  Aufruf („Demo: Nachricht an mich“). Suchbegriffe einbauen (Steuerrückstellung, Tax Technology, Excel, KI).
- **Im Fokus:** Demo-Link (Reclaim), bestes Dokument, Neuvorstellung.
- **Titelbild** 1584 × 396 im maehrsteuern-Stil („Steuern × Code – Steuerwissen, das rechnet.“).
- **Folgen statt Vernetzen** als Hauptknopf einstellen, eigene Profil-URL, Profil öffentlich sichtbar.
- **Arbeitgeber:** Die aktuelle Anstellung steht als Erfahrung im Profil, aber **kein Beitrag, kein Bild, keine Zahl
  aus dem Job**. maehrsteuern als eigener Eintrag (selbstständig/nebenberuflich). Ob und wie das mit dem Arbeitgeber
  abgestimmt ist, klärt Loris selbst.

## Was wir messen (alle 4 Wochen, LinkedIn-Statistik)
| Kennzahl | Wofür | Startziel nach 8 Wochen |
|---|---|---|
| Impressionen je Beitrag (Median) | Reichweite | Wert der Erstanalyse × 3 |
| Kommentare je Beitrag | Diskussion | ≥ 5 |
| Profilbesuche / Woche | Interesse an Loris | Wert der Erstanalyse × 2 |
| Follower aus der Zielgruppe (Jobtitel Steuer/Finanzen) | Richtige Leute | + 150 |
| Demo-Anfragen „LinkedIn“ (Reclaim „Woher kennst du mich?“) | Kunden | ≥ 3 |

## Bewusst nicht übernommen
- **Automatisches Posten, Kommentieren, Vernetzen, Nachrichten** (Bots, Erweiterungen, auch Claude in Chrome) –
  LinkedIn verbietet das in den Nutzungsbedingungen und sperrt Konten. Claude in Chrome **liest und bereitet vor**,
  Loris klickt „Posten“ und „Senden“.
- Engagement-Gruppen („Pods“), gekaufte Follower, Kommentar-Köder.
- Unternehmensseite als Hauptkanal (später als Spiegel möglich).
- Feste „beste Uhrzeiten“ aus Listen über die eigenen Zahlen stellen.

## Offene Entscheidungen (Loris)
- [ ] Ton: Du oder neutral? (Vorschlag: neutral im Text, Du in Kommentaren, wenn der andere duzt)
- [ ] maehrsteuern als eigener Erfahrungs-Eintrag oder nur in der Headline?
- [ ] Startdatum erster Beitrag (Vorschlag: nach Profil-Überarbeitung, frühestens Di 13.10.)
