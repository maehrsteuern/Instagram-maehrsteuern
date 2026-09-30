"""Freigabe per GitHub-Issue: ein Issue je Beitrag, Loris antwortet „go“ oder „stop“.

  python automatik/freigabe.py anfragen          – für jeden Beitrag mit Einträgen im Status „entwurf“ ein Issue öffnen
  python automatik/freigabe.py antwort ISSUE TEXT – Kommentar auswerten („go“ → freigegeben, „stop“ → pause)

Ein Beitrag = alle Einträge mit derselben Nummer vorn in der ID (z. B. 05-karussell, 05-story-teaser).
Umgebung: GH_TOKEN (GitHub-Token mit issues:write), GITHUB_REPOSITORY.
"""
import json, os, re, subprocess, sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
PLAN = WURZEL / "automatik" / "plan.json"
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/Instagram-maehrsteuern")
LABEL = "freigabe"


def gh(*args, eingabe=None):
    return subprocess.run(["gh", *args, "--repo", REPO], input=eingabe, check=True, capture_output=True, text=True).stdout.strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=WURZEL, check=True, capture_output=True, text=True).stdout.strip()


def speichern(plan, nachricht):
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    git("add", str(PLAN))
    if git("status", "--porcelain"):
        git("commit", "-m", nachricht)
        git("pull", "--rebase", "-q")
        git("push")


def gruppen(plan):
    g = {}
    for e in plan["eintraege"]:
        g.setdefault(e["id"].split("-")[0], []).append(e)
    return g


def raw(pfad):
    return f"https://raw.githubusercontent.com/{REPO}/{git('rev-parse', 'HEAD')}/{pfad}"


def vorschau(eintraege):
    zeilen = []
    for e in eintraege:
        art = {"karussell": "Karussell", "reel": "Reel", "story": "Story", "bild": "Bild"}[e["typ"]]
        zeilen.append(f"### {art} · {e['zeit']} Uhr · `{e['id']}`")
        if e["typ"] == "reel":
            hinweis = " ⚠️ noch ohne Musik – wird so nicht automatisch gepostet" if e.get("musik_fehlt") else ""
            zeilen.append(f"▶️ [Reel ansehen]({raw(e['ordner'] + '/' + e['video'])}){hinweis}")
            if e.get("titelbild"):
                zeilen.append(f'<img src="{raw(e["ordner"] + "/" + e["titelbild"])}" width="180">')
        else:
            zeilen.append(" ".join(f'<img src="{raw(e["ordner"] + "/" + b)}" width="180">' for b in e.get("bilder", [])))
        if e.get("text"):
            text = (WURZEL / e["ordner"] / e["text"]).read_text().strip()
            zeilen.append("<details><summary>Bildunterschrift</summary>\n\n```\n" + text + "\n```\n</details>")
        zeilen.append("")
    return "\n".join(zeilen)


def anfragen():
    plan = json.loads(PLAN.read_text())
    try:
        gh("label", "create", LABEL, "--color", "53C3A2", "--description", "Beitrag wartet auf go/stop")
    except subprocess.CalledProcessError:
        pass  # gibt es schon
    neu = 0
    for nr, eintraege in sorted(gruppen(plan).items()):
        offen = [e for e in eintraege if e["status"] == "entwurf" and not e.get("issue")]
        if not offen or any(e["status"].startswith("wartet") for e in eintraege):
            continue
        erster = min(e["zeit"] for e in offen)
        titel = f"Freigabe {nr}: {offen[0]['id'].split('-', 1)[1].replace('-', ' ')} – {erster}"
        text = (f"@{REPO.split('/')[0]} bitte kurz prüfen.\n\n"
                f"**Antworte mit `go`** → geht automatisch zu den Zeiten unten online.\n"
                f"**Antworte mit `stop`** → wird pausiert. Änderungswünsche schreibst du Claude.\n\n"
                + vorschau(offen))
        url = gh("issue", "create", "--title", titel, "--label", LABEL, "--body-file", "-", eingabe=text)
        for e in offen:
            e["issue"] = int(url.rstrip("/").split("/")[-1])
        neu += 1
        print("✓", titel, url)
    if neu:
        speichern(plan, f"Freigabe angefragt ({neu} Beitrag/Beiträge)")
    else:
        print("Keine neuen Entwürfe.")


def antwort(issue, kommentar):
    treffer = re.match(r"\s*(go|stop)\b", kommentar.lower())
    wort = treffer.group(1) if treffer else ""
    if not wort:
        print("Kein go/stop – nichts zu tun.")
        return
    plan = json.loads(PLAN.read_text())
    betroffen = [e for e in plan["eintraege"] if e.get("issue") == issue and e["status"] == "entwurf"]
    if not betroffen:
        gh("issue", "comment", str(issue), "--body", "Nichts mehr offen für diese Freigabe.")
        return
    ziel = "freigegeben" if wort == "go" else "pause"
    for e in betroffen:
        e["status"] = ziel
    speichern(plan, f"Freigabe #{issue}: {wort}")
    zeilen = "\n".join(f"- `{e['id']}` → {e['zeit']} Uhr" + (" (⚠️ Reel noch ohne Musik)" if e.get("musik_fehlt") else "")
                       for e in betroffen)
    antworttext = (f"✅ Eingeplant – der Autopilot postet automatisch:\n{zeilen}" if wort == "go"
                   else f"⏸️ Pausiert:\n{zeilen}\nZum Fortsetzen Claude Bescheid geben.")
    gh("issue", "comment", str(issue), "--body", antworttext)
    gh("issue", "close", str(issue))


if __name__ == "__main__":
    if sys.argv[1] == "anfragen":
        anfragen()
    else:
        antwort(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "")
