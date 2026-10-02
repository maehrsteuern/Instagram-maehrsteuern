"""LinkedIn-Paket (läuft täglich mit dem Radar): jedes freigegebene Karussell auch für LinkedIn vorbereiten.

Für jedes Karussell ab heute ohne Paket entsteht in posts/<ordner>/linkedin/:
  karussell.pdf – die Folien als PDF (LinkedIn zeigt PDFs als blätterbares Dokument, das stärkste Format dort)
  text.md       – Beitragstext, von Claude für LinkedIn umgeschrieben (Sie/Du neutral, mehr Kontext, Frage am Ende)
und ein Issue „💼 LinkedIn …“ mit Link und Vorschlag für den Tag (1 Tag nach Instagram, morgens, nie am Wochenende).
Hochladen von Hand (2 Min.): LinkedIn → Beitrag → Dokument hinzufügen. Per Schnittstelle geht das nur mit
der freigabepflichtigen Community-Management-API, deshalb bewusst von Hand.

Umgebung: ANTHROPIC_API_KEY (optional), GH_TOKEN, GITHUB_REPOSITORY.
"""
import json, os, subprocess, sys, time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ki

WURZEL = Path(__file__).resolve().parent.parent
PLAN = WURZEL / "automatik" / "plan.json"
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/Instagram-maehrsteuern")
LABEL = "linkedin"
HEUTE = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%d")
WOCHENTAG = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

SCHEMA = {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"], "additionalProperties": False}
AUFGABE = """Schreib diese Instagram-Bildunterschrift zu einem LinkedIn-Beitrag um, der zu einem PDF-Karussell gehört.
- Erste Zeile: Haken, der ohne „mehr anzeigen“ funktioniert (max. 120 Zeichen).
- Danach 4–8 kurze Absätze mit etwas mehr Fachkontext als auf Instagram, Zeilenumbrüche zwischen den Absätzen.
- Anrede neutral (ohne du/Sie, z. B. „Wer … kennt das:“), professioneller Ton, keine Emojis außer max. einem Pfeil.
- Ende: eine echte Frage an Steuerleute (Kommentare sind auf LinkedIn das stärkste Signal).
- „Schreib TOOL per DM“ ersetzen durch: „Demo gefällig? Kurze Nachricht an mich genügt.“
- Max. 3 Hashtags ganz am Ende (z. B. #Steuern #Excel #Automatisierung).
In diesem Fall dürfen Hinweise auf Loris' Tools vorkommen, sie stehen ja im Original."""


def gh(*args, eingabe=None):
    return subprocess.run(["gh", *args, "--repo", REPO], input=eingabe, check=True, capture_output=True, text=True).stdout.strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=WURZEL, check=True, capture_output=True, text=True).stdout.strip()


def tag_fuer_linkedin(zeit):
    t = datetime.strptime(zeit[:10], "%Y-%m-%d") + timedelta(days=1)
    while t.weekday() >= 5:
        t += timedelta(days=1)
    return f"{WOCHENTAG[t.weekday()]} {t:%d.%m.} um 08:00"


def pdf(ordner, bilder, ziel):
    seiten = []
    for b in bilder:
        jpg = ordner / "_jpg" / (Path(b).stem + ".jpg")  # gibt es meist schon (kleiner)
        seiten.append(Image.open(jpg if jpg.exists() else ordner / b).convert("RGB"))
    seiten[0].save(ziel, save_all=True, append_images=seiten[1:], resolution=150, quality=88)


def main():
    plan = json.loads(PLAN.read_text())
    neu = []
    for e in plan["eintraege"]:
        if e["typ"] != "karussell" or e["status"] not in ("freigegeben", "veroeffentlicht") or e["zeit"][:10] < HEUTE:
            continue
        ordner = WURZEL / e["ordner"]
        paket = ordner / "linkedin"
        if (paket / "karussell.pdf").exists():
            continue
        paket.mkdir(exist_ok=True)
        pdf(ordner, e["bilder"], paket / "karussell.pdf")
        original = (ordner / e["text"]).read_text().strip() if e.get("text") else ""
        umgeschrieben = (ki.json_antwort(AUFGABE, {"instagram": original}, SCHEMA) or {}).get("text")
        (paket / "text.md").write_text((umgeschrieben or "⚠️ Ohne KI erzeugt – bitte für LinkedIn anpassen:\n\n" + original) + "\n")
        neu.append(e)
        print("✓ LinkedIn-Paket", e["id"])
    if not neu:
        print("Keine neuen LinkedIn-Pakete.")
        return
    git("add", "posts")
    git("commit", "-m", f"LinkedIn-Pakete: {', '.join(e['id'] for e in neu)}")
    for versuch in range(5):
        try:
            git("pull", "--rebase", "-q")
            git("push")
            break
        except subprocess.CalledProcessError:
            time.sleep(5 * (versuch + 1))
    try:
        gh("label", "create", LABEL, "--color", "0A66C2", "--description", "Karussell auch auf LinkedIn posten")
    except subprocess.CalledProcessError:
        pass
    for e in neu:
        basis = f"https://github.com/{REPO}/blob/claude/instagram/{e['ordner']}/linkedin"
        text = (f"@{REPO.split('/')[0]} Karussell `{e['id']}` (Instagram {e['zeit']}) ist fertig für LinkedIn.\n\n"
                f"**Posten:** {tag_fuer_linkedin(e['zeit'])} – LinkedIn → *Beitrag beginnen* → *Dokument hinzufügen* → "
                f"PDF hochladen, Titel = erste Zeile, Text einfügen.\n\n"
                f"- 📄 [karussell.pdf]({basis}/karussell.pdf) (auf GitHub → *Download raw file*)\n"
                f"- ✍️ [text.md]({basis}/text.md)\n\n"
                "In der ersten Stunde auf jeden Kommentar antworten. Danach dieses Issue schließen.")
        gh("issue", "create", "--title", f"💼 LinkedIn: {e['id'].split('-', 1)[1].replace('-', ' ')} – {tag_fuer_linkedin(e['zeit'])}",
           "--label", LABEL, "--body-file", "-", eingabe=text)


if __name__ == "__main__":
    main()
