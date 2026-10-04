"""Autopilot: veröffentlicht fällige, freigegebene Einträge aus plan.json über die Instagram-API.

Aufruf (läuft stündlich per GitHub Actions):
  python automatik/posten.py            – fällige Einträge (nächste 75 Min.) abwarten und posten
  python automatik/posten.py --probe    – nur anzeigen, was passieren würde (kein API-Aufruf, kein Commit)
  python automatik/posten.py --jetzt ID – einen freigegebenen Eintrag sofort posten
  python automatik/posten.py --test ID  – Probelauf: Instagram lädt alles hoch, es wird aber NICHTS veröffentlicht

Umgebung: IG_TOKEN, IG_USER_ID (GitHub-Secrets), GITHUB_REPOSITORY (setzt GitHub automatisch).
Instagram holt die Dateien über öffentliche Links ab; Bilder müssen JPEG sein – das Skript wandelt PNG um,
committet die JPEGs und verlinkt sie über den Commit-Stand (raw.githubusercontent.com/<repo>/<sha>/...).
"""
import json, os, subprocess, sys, time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from PIL import Image

WURZEL = Path(__file__).resolve().parent.parent
PLAN = WURZEL / "automatik" / "plan.json"
ZONE = ZoneInfo("Europe/Berlin")
API = "https://graph.instagram.com/v23.0"
FENSTER = timedelta(minutes=75)      # so weit voraus wird gewartet
NACHHOLEN = timedelta(hours=6)       # verspätete Läufe holen bis zu 6 h nach


def jetzt():
    return datetime.now(ZONE)


def zeit(e):
    return datetime.strptime(e["zeit"], "%Y-%m-%d %H:%M").replace(tzinfo=ZONE)


def git(*args):
    return subprocess.run(["git", *args], cwd=WURZEL, check=True, capture_output=True, text=True).stdout.strip()


def speichern(plan, nachricht):
    """Committen und pushen – mit Wiederholung: geht der Status „veroeffentlicht“ verloren, würde der nächste
    Lauf denselben Beitrag noch einmal posten."""
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    git("add", "-A")
    if git("status", "--porcelain"):
        git("commit", "-m", nachricht)
        for versuch in range(6):
            try:
                git("pull", "--rebase", "-q")
                git("push")
                break
            except subprocess.CalledProcessError as fehler:
                subprocess.run(["git", "rebase", "--abort"], cwd=WURZEL, capture_output=True)
                print(f"Push-Versuch {versuch + 1} fehlgeschlagen: {fehler.stderr.strip()[:200]}")
                time.sleep(5 * (versuch + 1))
        else:
            raise RuntimeError(f"plan.json nicht gepusht ({nachricht}) – Beitrag ist ggf. schon online, Plan prüfen!")
    return git("rev-parse", "HEAD")


def als_jpeg(ordner, namen):
    """PNG → JPEG (Instagram nimmt für Bilder nur JPEG). Gibt die Repo-Pfade der JPEGs zurück."""
    pfade = []
    for n in namen:
        quelle = WURZEL / ordner / n
        ziel = WURZEL / ordner / "_jpg" / (Path(n).stem + ".jpg")
        ziel.parent.mkdir(exist_ok=True)
        if not ziel.exists():
            Image.open(quelle).convert("RGB").save(ziel, "JPEG", quality=92, optimize=True)
        pfade.append(ziel.relative_to(WURZEL).as_posix())
    return pfade


def link(sha, pfad):
    return f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/{sha}/{pfad}"


class Instagram:
    def __init__(self):
        self.token = os.environ["IG_TOKEN"]
        self.user = os.environ["IG_USER_ID"]

    def _anfrage(self, methode, pfad, wiederholen=True, **kwargs):
        """Kurze Aussetzer (Verbindung, Zeitüberschreitung, 5xx) bis zu 3× wiederholen – außer bei media_publish:
        dort kann eine Zeitüberschreitung heißen, dass der Beitrag schon online ist."""
        for versuch in range(3 if wiederholen else 1):
            try:
                r = requests.request(methode, f"{API}/{pfad}", **kwargs)
            except (requests.ConnectionError, requests.Timeout):
                if not wiederholen or versuch == 2:
                    raise
            else:
                if r.ok:
                    return r.json()
                if r.status_code < 500 or not wiederholen or versuch == 2:
                    raise RuntimeError(f"{pfad}: {r.status_code} {r.text}")
            time.sleep(10 * (versuch + 1))

    def _post(self, pfad, wiederholen=True, **daten):
        return self._anfrage("POST", pfad, wiederholen, data={**daten, "access_token": self.token}, timeout=120)

    def _get(self, pfad, **params):
        return self._anfrage("GET", pfad, params={**params, "access_token": self.token}, timeout=60)

    def container(self, **daten):
        cid = self._post(f"{self.user}/media", **daten)["id"]
        for _ in range(60):  # Instagram verarbeitet Videos asynchron
            status = self._get(cid, fields="status_code").get("status_code")
            if status == "FINISHED":
                return cid
            if status in ("ERROR", "EXPIRED"):
                raise RuntimeError(f"Container {cid}: {status}")
            time.sleep(10)
        raise RuntimeError(f"Container {cid}: Zeitüberschreitung")

    def veroeffentlichen(self, cid):
        mid = self._post(f"{self.user}/media_publish", wiederholen=False, creation_id=cid)["id"]
        try:  # ab hier ist der Beitrag online – ein fehlender Link darf ihn nicht als „fehler“ markieren
            return mid, self._get(mid, fields="permalink").get("permalink")
        except Exception as fehler:
            print(f"Hinweis: Link zu {mid} nicht abrufbar ({fehler})")
            return mid, None


def pruefen(e):
    """Gibt einen Grund zurück, warum der Eintrag (noch) nicht gepostet werden darf – oder None."""
    if e["typ"] == "reel":
        if not (WURZEL / e["ordner"] / e["video"]).exists():
            return "Video fehlt"
        if e.get("musik_fehlt"):
            return "Reel ist noch stumm (musik_fehlt) – erst Musik einbauen oder Feld entfernen"
    for n in e.get("bilder", []):
        if not (WURZEL / e["ordner"] / n).exists():
            return f"Bild fehlt: {n}"
    return None


def posten(ig, e, sha, veroeffentlichen=True):
    text = (WURZEL / e["ordner"] / e["text"]).read_text().strip() if e.get("text") else ""
    if e["typ"] == "karussell":
        kinder = [ig.container(image_url=link(sha, p), is_carousel_item="true") for p in e["_jpg"]]
        cid = ig.container(media_type="CAROUSEL", children=",".join(kinder), caption=text)
    elif e["typ"] == "bild":
        cid = ig.container(image_url=link(sha, e["_jpg"][0]), caption=text)
    elif e["typ"] == "story":
        cid = ig.container(media_type="STORIES", image_url=link(sha, e["_jpg"][0]))
    elif e["typ"] == "reel":
        daten = dict(media_type="REELS", video_url=link(sha, f"{e['ordner']}/{e['video']}"), caption=text, share_to_feed="true")
        if e.get("_jpg"):
            daten["cover_url"] = link(sha, e["_jpg"][0])
        cid = ig.container(**daten)
    else:
        raise ValueError(f"Unbekannter Typ {e['typ']}")
    if not veroeffentlichen:
        return cid, None
    return ig.veroeffentlichen(cid)


def probelauf(eid):
    """Container anlegen und von Instagram verarbeiten lassen, aber nicht veröffentlichen.
    Nicht veröffentlichte Container verfallen nach 24 Stunden von selbst."""
    plan = json.loads(PLAN.read_text())
    e = next(x for x in plan["eintraege"] if x["id"] == eid)
    grund = pruefen(e)
    if grund and not grund.startswith("Reel ist noch stumm"):
        sys.exit(f"✗ {eid}: {grund}")
    bilder = e.get("bilder") or ([e["titelbild"]] if e.get("titelbild") else [])
    e["_jpg"] = als_jpeg(e["ordner"], bilder)
    sha = speichern(plan_ohne_intern(plan), f"Autopilot: Dateien fuer Probelauf {eid} vorbereitet")
    cid, _ = posten(Instagram(), e, sha, veroeffentlichen=False)
    print(f"✓ Probelauf {eid}: Instagram hat alles angenommen (Container {cid}). Nichts veröffentlicht.")


def main():
    if "--test" in sys.argv:
        return probelauf(sys.argv[sys.argv.index("--test") + 1])
    probe = "--probe" in sys.argv
    sofort = sys.argv[sys.argv.index("--jetzt") + 1] if "--jetzt" in sys.argv else None
    plan = json.loads(PLAN.read_text())
    n = jetzt()
    faellig = [e for e in plan["eintraege"] if e["status"] == "freigegeben" and
               (e["id"] == sofort if sofort else n - NACHHOLEN <= zeit(e) <= n + FENSTER)]
    if not faellig:
        print("Nichts fällig.", n.strftime("%d.%m. %H:%M"))
        return
    ig = None if probe else Instagram()
    fehlgeschlagen = []
    for e in sorted(faellig, key=zeit):
        # immer den Eintrag aus dem aktuellen Plan nehmen (der Plan wird nach dem Warten neu gelesen)
        e = next((x for x in plan["eintraege"] if x["id"] == e["id"]), None)
        if not e or e["status"] != "freigegeben":
            continue
        grund = pruefen(e)
        if grund:
            print(f"✗ {e['id']}: {grund}")
            continue
        bilder = e.get("bilder") or ([e["titelbild"]] if e.get("titelbild") else [])
        if probe:
            print(f"• {e['id']} ({e['typ']}) um {e['zeit']}: {len(bilder)} Bild(er)", e.get("video", ""))
            continue
        e["_jpg"] = als_jpeg(e["ordner"], bilder)
        sha = speichern(plan_ohne_intern(plan), f"Autopilot: Dateien fuer {e['id']} vorbereitet")
        warten = (zeit(e) - jetzt()).total_seconds()
        if warten > 0 and not sofort:
            print(f"… warte {int(warten // 60)} Min. bis {e['zeit']} für {e['id']}")
            time.sleep(warten)
        # Direkt vor dem Posten IMMER den neuesten Plan holen – nicht nur nach dem Warten: Ein Lauf startet mit dem
        # Stand vom Start-Zeitpunkt; hat ein früherer Lauf den Beitrag inzwischen gepostet, steht das nur auf GitHub
        # (04.10.: Reel doppelt online). Auch „stop“, eine neue Zeit oder „entfaellt“ während des Wartens greifen so.
        try:
            git("pull", "--rebase", "-q")
            plan = json.loads(PLAN.read_text())
        except subprocess.CalledProcessError as fehler:
            subprocess.run(["git", "rebase", "--abort"], cwd=WURZEL, capture_output=True)
            print(f"✗ {e['id']}: Plan nicht neu geladen ({fehler.stderr.strip()[:200]}) – nicht gepostet, nächster Lauf versucht es erneut")
            continue
        aktuell = next((x for x in plan["eintraege"] if x["id"] == e["id"]), None)
        if not aktuell or aktuell["status"] != "freigegeben" or aktuell["zeit"] != e["zeit"]:
            print(f"↷ {e['id']}: Plan hat sich geändert (schon gepostet, gestoppt oder verschoben) – übersprungen")
            continue
        aktuell["_jpg"], e = e["_jpg"], aktuell
        try:
            mid, permalink = posten(ig, e, sha)
            e.update(status="veroeffentlicht", media_id=mid, link=permalink, veroeffentlicht_am=jetzt().strftime("%Y-%m-%d %H:%M"))
            print(f"✓ {e['id']} online: {permalink}")
            erste_stunde(e)
        except Exception as fehler:  # Fehler im Plan vermerken, damit er im Repo sichtbar ist
            # Verbindungsfehler enthalten die URL samt access_token – nie ins öffentliche Repo schreiben
            meldung = str(fehler).replace(ig.token, "***")
            e.update(status="fehler", fehler=meldung[:500])
            fehlgeschlagen.append(e["id"])
            print(f"✗ {e['id']}: {meldung}")
        e.pop("_jpg", None)
        speichern(plan, f"Autopilot: {e['id']} {e['status']}")
    if fehlgeschlagen:
        sys.exit(1)


def erste_stunde(e):
    """Nach einem Feed-Beitrag: Checkliste als Kommentar ins bestehende Freigabe-Issue (kein neues Issue).
    Fehler hier stoppen das Posten nie."""
    if e["typ"] not in ("karussell", "reel", "bild") or not e.get("issue") or not os.environ.get("GH_TOKEN"):
        return
    repo = os.environ["GITHUB_REPOSITORY"]
    suche = f"https://github.com/{repo}/issues?q=is%3Aopen+label%3A"
    zeilen = [f"Moin, `{e['id']}` ist online 🚀 [Beitrag ansehen]({e.get('link')})", "",
              "Die erste Stunde zählt doppelt – wie Fristverlängerung, nur ohne Antrag:", "",
              "- [ ] In die Story teilen (Papierflieger → „Zu deiner Story hinzufügen“), mit Sticker oder kurzer Frage",
              f"- [ ] Kommentare zügig beantworten → [💬 Kommentare]({suche}kommentare) (`K12 ok` reicht)",
              f"- [ ] 2–3 Beiträge aus dem [📡 Radar]({suche}radar) kommentieren – bringt Gegenbesuch"]
    if e["typ"] == "karussell":
        zeilen.append(f"- [ ] LinkedIn-Paket steht bereit → [💼 LinkedIn]({suche}linkedin)")
    try:
        subprocess.run(["gh", "issue", "comment", str(e["issue"]), "--repo", repo, "--body", "\n".join(zeilen)],
                       check=True, capture_output=True, text=True, timeout=60)
    except Exception as fehler:
        print(f"Hinweis: Erste-Stunde-Checkliste nicht gepostet ({fehler})")


def plan_ohne_intern(plan):
    return {**plan, "eintraege": [{k: v for k, v in e.items() if not k.startswith("_")} for e in plan["eintraege"]]}


if __name__ == "__main__":
    main()
