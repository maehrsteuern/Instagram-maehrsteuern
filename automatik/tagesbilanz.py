"""Tagesbilanz: wie viel habe ich heute geschafft? Zählt die Commits aller Repos neben diesem und bewertet den Tag.

Aufruf:  python3 automatik/tagesbilanz.py [--sitzungen N] [--datum JJJJ-MM-TT] [--speichern]
Woche:   python3 automatik/tagesbilanz.py --woche [--datum JJJJ-MM-TT] [--sitzungen-je-tag JJJJ-MM-TT=N,...] [--speichern]
         (7 Tage bis einschließlich --datum; Zusammenfassung pro Repo, Tageswerte in tagesbilanz.md, Woche in wochenbilanz.md)
Repos = alle Git-Ordner neben diesem Repo. Automatische Commits (Lage, Statistik, Radar, Status), Merges,
doppelte Betreffs (Cherry-Picks auf anderen Branches) und Dateien über 5.000 Zeilen (Datenimporte) zählen nicht.
Die Zahl der Claude-Sitzungen kommt über den Skill `tagesbilanz` (Git kennt sie nicht).
"""
import argparse, os, subprocess
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

WURZEL = Path(__file__).resolve().parent.parent
LOG = WURZEL / "automatik" / "tagesbilanz.md"
WOCHE_LOG = WURZEL / "automatik" / "wochenbilanz.md"
AUTOMATIK = ("Lage aktualisiert", "Statistik 20", "Autopilot:", "Freigabe angefragt", "Radar 20",
             "Status updated", "Stats 20", "Tagesbilanz 20", "Wochenbilanz 20", "Approval #", "Freigabe #",
             "Approval requested", "Regenerate STATUS", "Weekly report week", "Wochenbericht KW")
GROSS = 5000  # Datei mit mehr geänderten Zeilen = Datenimport oder erzeugte Datei, zählt nicht
ZEIT = {**os.environ, "TZ": "Europe/Berlin"}  # "heute" = deutscher Kalendertag


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=ZEIT).stdout


def heimat(shas_je_repo):
    """Commits, die in mehreren Repos liegen (fremde Historie auf einem Branch), gehören dem Repo,
    in dem sie auf den meisten Branches liegen. Ergebnis: Repo -> Menge der dort NICHT zu zählenden SHAs."""
    wo = {}
    for repo, shas in shas_je_repo.items():
        for sha in shas:
            wo.setdefault(sha, []).append(repo)
    fremd = {repo: set() for repo in shas_je_repo}
    for sha, liste in wo.items():
        if len(liste) > 1:
            zahl = {r: len(git(r, "for-each-ref", "--contains", sha, "refs/remotes").splitlines()) for r in liste}
            chef = max(liste, key=lambda r: zahl[r])
            for r in liste:
                if r != chef:
                    fremd[r].add(sha)
    return fremd


def alle_shas(repo, von, bis):
    return set(git(repo, "log", "--all", "--no-merges", f"--since={von} 00:00", f"--until={bis} 23:59:59",
                   "--format=%H").split())


def auswerten(repo, tag, gesehen=None, fremd=frozenset()):
    """Commits eines Tages; `gesehen` (Menge von Betreffs) verhindert Doppelzählung über Branches und Tage."""
    gesehen = set() if gesehen is None else gesehen
    aus = git(repo, "log", "--all", "--no-merges", f"--since={tag} 00:00", f"--until={tag} 23:59:59",
              "--format=@%H|%s", "--numstat")
    commits, dateien, zeilen = {}, set(), 0
    for block in aus.split("\n@"):
        kopf, *rest = block.lstrip("@").splitlines() or [""]
        if "|" not in kopf:
            continue
        sha, betreff = kopf.split("|", 1)
        if sha in fremd or betreff in gesehen or betreff.startswith(AUTOMATIK):
            continue
        gesehen.add(betreff)
        commits[sha] = betreff
        for z in rest:
            teile = z.split("\t")
            if len(teile) == 3:
                n = sum(int(x) for x in teile[:2] if x.isdigit())
                if n <= GROSS:
                    dateien.add(teile[2])
                    zeilen += n
    return list(commits.values()), len(dateien), zeilen


def punkte_und_ampel(commits, sitzungen, zeilen):
    # Hausnummer: Commit 3 Punkte, Sitzung 2, je 100 geänderte Zeilen 1 (max. 10)
    punkte = commits * 3 + sitzungen * 2 + min(zeilen // 100, 10)
    return punkte, ampel(punkte)


def ampel(punkte):
    return "🟢 viel geschafft" if punkte >= 60 else "🟡 okay" if punkte >= 25 else "🔴 wenig"


def tag_speichern(datum, c, s, d, z, p, a):
    if not LOG.exists():
        LOG.write_text("# Tagesbilanz\n\nPunkte: Commit 3, Sitzung 2, je 100 Zeilen 1 (max. 10). "
                       "🟢 ab 60, 🟡 ab 25.\n\n| Tag | Commits | Sitzungen | Dateien | Zeilen | Punkte | Einstufung |\n"
                       "|---|---|---|---|---|---|---|\n")
    kopf, zeilen = [], []
    for z_ in LOG.read_text().splitlines():
        (zeilen if z_.startswith("| 20") else kopf).append(z_)
    zeilen = [z_ for z_ in zeilen if not z_.startswith(f"| {datum} ")] + [f"| {datum} | {c} | {s} | {d} | {z} | {p} | {a} |"]
    LOG.write_text("\n".join(kopf + sorted(zeilen)) + "\n")


def tag(repos, datum, sitzungen, speichern):
    fremd = heimat({r: alle_shas(r, datum, datum) for r in repos})
    summe_c = summe_d = summe_z = 0
    print(f"# Tagesbilanz {datum}\n")
    for repo in repos:
        commits, dateien, zeilen = auswerten(repo, datum, fremd=fremd[repo])
        if not commits:
            continue
        summe_c, summe_d, summe_z = summe_c + len(commits), summe_d + dateien, summe_z + zeilen
        print(f"## {repo.name} – {len(commits)} Commits, {dateien} Dateien, {zeilen} Zeilen")
        for betreff in commits:
            print(f"- {betreff}")
        print()
    punkte, a = punkte_und_ampel(summe_c, sitzungen, summe_z)
    print(f"**{punkte} Punkte – {a}** ({summe_c} Commits, {sitzungen} Sitzungen, "
          f"{summe_d} Dateien, {summe_z} Zeilen)")
    if speichern:
        tag_speichern(datum, summe_c, sitzungen, summe_d, summe_z, punkte, a)


def woche(repos, ende, sitzungen_je_tag, speichern):
    tage = [(ende - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    pro_repo = {}  # Repo -> [Commits, Zeilen, Betreffs]
    gesehen = {repo.name: set() for repo in repos}
    fremd = heimat({r: alle_shas(r, tage[0], tage[-1]) for r in repos})
    print(f"# Wochenbilanz {tage[0]} bis {tage[-1]}\n")
    print("| Tag | Commits | Sitzungen | Zeilen | Punkte | Einstufung |\n|---|---|---|---|---|---|")
    summe = [0, 0, 0, 0, 0]  # Commits, Sitzungen, Dateien, Zeilen, Punkte
    for t_ in tage:
        c = d = z = 0
        for repo in repos:
            commits, dateien, zeilen = auswerten(repo, t_, gesehen[repo.name], fremd[repo])
            c, d, z = c + len(commits), d + dateien, z + zeilen
            r = pro_repo.setdefault(repo.name, [0, 0, []])
            r[0], r[1] = r[0] + len(commits), r[1] + zeilen
            r[2] += commits
        s = sitzungen_je_tag.get(t_, 0)
        p, a = punkte_und_ampel(c, s, z)
        wt = "Mo Di Mi Do Fr Sa So".split()[date.fromisoformat(t_).weekday()]
        print(f"| {wt} {t_} | {c} | {s} | {z} | {p} | {a} |")
        for i, w in enumerate((c, s, d, z, p)):
            summe[i] += w
        if speichern:
            tag_speichern(t_, c, s, d, z, p, a)
    schnitt = summe[4] // 7
    print(f"| **Woche** | **{summe[0]}** | **{summe[1]}** | **{summe[3]}** | **{summe[4]}** | Ø {schnitt}/Tag {ampel(schnitt)} |\n")
    for name, (c, z, betreffs) in sorted(pro_repo.items(), key=lambda x: -x[1][0]):
        if not c:
            continue
        print(f"## {name} – {c} Commits, {z} Zeilen")
        for betreff in betreffs:
            print(f"- {betreff}")
        print()
    if speichern:
        if not WOCHE_LOG.exists():
            WOCHE_LOG.write_text("# Wochenbilanz\n\nSumme der Tagespunkte (siehe tagesbilanz.md); Ampel nach Tagesschnitt "
                                 "(🟢 ab 60, 🟡 ab 25).\n\n| Woche | Commits | Sitzungen | Zeilen | Punkte | Ø/Tag | Einstufung |\n"
                                 "|---|---|---|---|---|---|---|\n")
        schluessel = f"| {tage[0]} – {tage[-1]} "
        alt = [z_ for z_ in WOCHE_LOG.read_text().splitlines() if not z_.startswith(schluessel)]
        neu = f"{schluessel}| {summe[0]} | {summe[1]} | {summe[3]} | {summe[4]} | {schnitt} | {ampel(schnitt)} |"
        WOCHE_LOG.write_text("\n".join(alt + [neu]) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sitzungen", type=int, default=0)
    ap.add_argument("--sitzungen-je-tag", default="", help="für --woche: JJJJ-MM-TT=N,JJJJ-MM-TT=N,...")
    ap.add_argument("--datum", default=datetime.now(ZoneInfo("Europe/Berlin")).date().isoformat())
    ap.add_argument("--woche", action="store_true", help="die 7 Tage bis einschließlich --datum")
    ap.add_argument("--speichern", action="store_true")
    a = ap.parse_args()

    repos = sorted(p.parent for p in WURZEL.parent.glob("*/.git"))
    for repo in repos:
        git(repo, "fetch", "--all", "-q")
    if a.woche:
        je_tag = dict((k, int(v)) for k, v in (x.split("=") for x in a.sitzungen_je_tag.split(",") if x))
        woche(repos, date.fromisoformat(a.datum), je_tag, a.speichern)
    else:
        tag(repos, a.datum, a.sitzungen, a.speichern)


if __name__ == "__main__":
    main()
