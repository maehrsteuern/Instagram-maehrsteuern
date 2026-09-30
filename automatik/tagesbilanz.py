"""Tagesbilanz: wie viel habe ich heute geschafft? Zählt die Commits aller Repos neben diesem und bewertet den Tag.

Aufruf:  python3 automatik/tagesbilanz.py [--sitzungen N] [--datum JJJJ-MM-TT] [--speichern]
Repos = alle Git-Ordner neben diesem Repo. Automatische Commits (Lage, Statistik) und Merges zählen nicht.
Die Zahl der Claude-Sitzungen kommt über den Skill `tagesbilanz` (Git kennt sie nicht).
"""
import argparse, os, subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

WURZEL = Path(__file__).resolve().parent.parent
LOG = WURZEL / "automatik" / "tagesbilanz.md"
AUTOMATIK = ("Lage aktualisiert", "Statistik 20", "Autopilot:", "Freigabe angefragt")
ZEIT = {**os.environ, "TZ": "Europe/Berlin"}  # "heute" = deutscher Kalendertag


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=ZEIT).stdout


def auswerten(repo, tag):
    git(repo, "fetch", "--all", "-q")
    aus = git(repo, "log", "--all", "--no-merges", f"--since={tag} 00:00", f"--until={tag} 23:59:59",
              "--format=@%H|%s", "--numstat")
    commits, dateien, zeilen = {}, set(), 0
    for block in aus.split("\n@"):
        kopf, *rest = block.lstrip("@").splitlines() or [""]
        if "|" not in kopf:
            continue
        sha, betreff = kopf.split("|", 1)
        if sha in commits or betreff.startswith(AUTOMATIK):
            continue
        commits[sha] = betreff
        for z in rest:
            teile = z.split("\t")
            if len(teile) == 3:
                dateien.add(teile[2])
                zeilen += sum(int(x) for x in teile[:2] if x.isdigit())
    return list(commits.values()), len(dateien), zeilen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sitzungen", type=int, default=0)
    ap.add_argument("--datum", default=datetime.now(ZoneInfo("Europe/Berlin")).date().isoformat())
    ap.add_argument("--speichern", action="store_true")
    a = ap.parse_args()

    repos = sorted(p.parent for p in WURZEL.parent.glob("*/.git"))
    summe_c = summe_d = summe_z = 0
    print(f"# Tagesbilanz {a.datum}\n")
    for repo in repos:
        commits, dateien, zeilen = auswerten(repo, a.datum)
        if not commits:
            continue
        summe_c, summe_d, summe_z = summe_c + len(commits), summe_d + dateien, summe_z + zeilen
        print(f"## {repo.name} – {len(commits)} Commits, {dateien} Dateien, {zeilen} Zeilen")
        for betreff in commits:
            print(f"- {betreff}")
        print()

    # Hausnummer: Commit 3 Punkte, Sitzung 2, je 100 geänderte Zeilen 1 (max. 10)
    punkte = summe_c * 3 + a.sitzungen * 2 + min(summe_z // 100, 10)
    ampel = "🟢 viel geschafft" if punkte >= 60 else "🟡 okay" if punkte >= 25 else "🔴 wenig"
    zeile = (f"| {a.datum} | {summe_c} | {a.sitzungen} | {summe_d} | {summe_z} | {punkte} | {ampel} |")
    print(f"**{punkte} Punkte – {ampel}** ({summe_c} Commits, {a.sitzungen} Sitzungen, "
          f"{summe_d} Dateien, {summe_z} Zeilen)")

    if a.speichern:
        if not LOG.exists():
            LOG.write_text("# Tagesbilanz\n\nPunkte: Commit 3, Sitzung 2, je 100 Zeilen 1 (max. 10). "
                           "🟢 ab 60, 🟡 ab 25.\n\n| Tag | Commits | Sitzungen | Dateien | Zeilen | Punkte | Einstufung |\n"
                           "|---|---|---|---|---|---|---|\n")
        alt = [z for z in LOG.read_text().splitlines() if not z.startswith(f"| {a.datum} ")]
        LOG.write_text("\n".join(alt + [zeile]) + "\n")


if __name__ == "__main__":
    main()
