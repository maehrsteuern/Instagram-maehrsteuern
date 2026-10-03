"""Kommentar-Hilfe: neue Kommentare unter eigenen Beiträgen schnell beantworten (erste Stunde = mehr Reichweite).

  python automatik/kommentare.py pruefen            – läuft nach jedem Posten-Takt (alle 15 Min.): neue Kommentare
                                                      holen, Antwortvorschlag von Claude, als Kommentar ins Issue „💬 Kommentare“
  python automatik/kommentare.py antwort "TEXT"      – Loris' Antwort im Issue auswerten:
                                                      „K12 ok“ → Vorschlag posten, „K12 Danke dir, …“ → eigenen Text posten

Kommentare mit ManyChat-Stichwort (z. B. TOOL) bleiben außen vor – die beantwortet ManyChat samt DM.
Hier wird nie eine DM verschickt. Kommentare, auf die Loris schon in der App geantwortet hat, werden erkannt.
Umgebung: IG_TOKEN, IG_USER_ID, ANTHROPIC_API_KEY (optional), GH_TOKEN, GITHUB_REPOSITORY.
"""
import json, os, re, subprocess, sys, time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ki

WURZEL = Path(__file__).resolve().parent.parent
EINSTELLUNGEN = json.loads((WURZEL / "automatik" / "interaktion.json").read_text())["kommentare"]
STAND = WURZEL / "automatik" / "interaktion" / "kommentare.json"
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/Instagram-maehrsteuern")
API = "https://graph.instagram.com/v23.0"
LABEL = "kommentare"
ZONE = ZoneInfo("Europe/Berlin")
JETZT = datetime.now(ZONE)


def gh(*args, eingabe=None):
    return subprocess.run(["gh", *args, "--repo", REPO], input=eingabe, check=True, capture_output=True, text=True).stdout.strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=WURZEL, check=True, capture_output=True, text=True).stdout.strip()


def ig(methode, pfad, **params):
    r = requests.request(methode, f"{API}/{pfad}", params={**params, "access_token": os.environ["IG_TOKEN"]}, timeout=60)
    r.raise_for_status()
    return r.json()


def zeitpunkt(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z").astimezone(ZONE)


def laden():
    if STAND.exists():
        return json.loads(STAND.read_text())
    return {"naechste_nr": 1, "kommentare": {}, "erster_lauf": True}


def speichern(stand, nachricht):
    grenze = (JETZT - timedelta(days=30)).strftime("%Y-%m-%d")
    stand["kommentare"] = {k: v for k, v in stand["kommentare"].items() if v["datum"] >= grenze}
    stand.pop("erster_lauf", None)
    STAND.parent.mkdir(parents=True, exist_ok=True)
    STAND.write_text(json.dumps(stand, ensure_ascii=False, indent=1) + "\n")
    git("add", str(STAND))
    if not git("status", "--porcelain", "--", str(STAND)):
        return
    git("commit", "-m", nachricht)
    for versuch in range(5):
        try:
            git("pull", "--rebase", "-q")
            git("push")
            return
        except subprocess.CalledProcessError:
            subprocess.run(["git", "rebase", "--abort"], cwd=WURZEL, capture_output=True)  # sonst scheitern alle Versuche gleich
            time.sleep(5 * (versuch + 1))
    raise RuntimeError("kommentare.json konnte nicht gespeichert werden (push 5× fehlgeschlagen)")


def sammel_issue():
    """Ein offenes Issue für alle Kommentare – GitHub schickt bei jedem neuen Eintrag eine Benachrichtigung."""
    nummern = gh("issue", "list", "--label", LABEL, "--state", "open", "--json", "number", "--jq", ".[].number").split()
    if nummern:
        return nummern[0]
    try:
        gh("label", "create", LABEL, "--color", "53C3A2", "--description", "Neue Kommentare mit Antwortvorschlag")
    except subprocess.CalledProcessError:
        pass
    text = (f"@{REPO.split('/')[0]} Hier landen neue Kommentare unter deinen Beiträgen – mit Antwortvorschlag.\n\n"
            "**Antworten:** hier kommentieren mit\n"
            "- `K12 ok` → der Vorschlag wird als Antwort gepostet\n"
            "- `K12 Danke dir, genau so …` → dein eigener Text wird gepostet\n"
            "- mehrere Zeilen gehen auch (eine pro Kommentar)\n\n"
            "Oder direkt in der App antworten – das wird beim nächsten Lauf erkannt.\n"
            "Kommentare mit ManyChat-Stichwort (TOOL) beantwortet ManyChat, die tauchen hier nicht auf.")
    url = gh("issue", "create", "--title", "💬 Kommentare beantworten", "--label", LABEL, "--body-file", "-", eingabe=text)
    return url.rstrip("/").split("/")[-1]


def ist_manychat(text):
    return any(re.search(rf"\b{re.escape(w)}\b", text or "", re.I) for w in EINSTELLUNGEN["manychat_stichwoerter"])


SCHEMA = {"type": "object", "properties": {"antworten": {"type": "array", "items": {"type": "object", "properties": {
    "nr": {"type": "integer"}, "text": {"type": "string"}}, "required": ["nr", "text"], "additionalProperties": False}}},
    "required": ["antworten"], "additionalProperties": False}

AUFGABE = """Schreib zu jedem Kommentar (nr) unter Loris' eigenen Beiträgen eine Antwort, die er öffentlich postet.
1–2 Sätze, max. 200 Zeichen, persönlich (Person darf mit Namen/@ angesprochen werden, wenn es passt).
Ziel: Gespräch am Laufen halten – bei Fragen kurz und richtig antworten, sonst eine Gegenfrage stellen.
Bei reinen Emojis oder „👍“: kurze herzliche Antwort. Bei Fachfragen, die eine Beratung im Einzelfall wären:
freundlich auf allgemeine Info beschränken. Spam oder Beleidigung: text = „ignorieren“."""


def pruefen():
    stand = laden()
    ich = ig("GET", os.environ["IG_USER_ID"], fields="username")["username"]
    medien = ig("GET", f"{os.environ['IG_USER_ID']}/media", fields="id,caption,permalink",
                limit=EINSTELLUNGEN["beitraege_pruefen"]).get("data", [])
    neu, erledigt = [], 0
    grenze = JETZT - timedelta(hours=48 if stand.get("erster_lauf") else 24 * 7)
    for m in medien:
        for c in ig("GET", f"{m['id']}/comments", fields="id,text,timestamp,username,replies{username}", limit=50).get("data", []):
            if c.get("username") == ich or ist_manychat(c.get("text")):
                continue
            beantwortet = any(r.get("username") == ich for r in c.get("replies", {}).get("data", []))
            bekannt = stand["kommentare"].get(c["id"])
            if bekannt:
                if beantwortet and bekannt["status"] == "offen":
                    bekannt["status"] = "beantwortet"
                    erledigt += 1
                continue
            if beantwortet or zeitpunkt(c["timestamp"]) < grenze:
                continue
            neu.append({"c": c, "m": m})
    if not neu:
        print(f"Keine neuen Kommentare ({erledigt} in der App beantwortet).")
        if erledigt:
            speichern(stand, f"Kommentare: {erledigt} in der App beantwortet")
        return
    for n in neu:
        n["nr"] = stand["naechste_nr"]
        stand["naechste_nr"] += 1
    vorschlaege = ki.json_antwort(AUFGABE, [{"nr": n["nr"], "von": n["c"].get("username"), "kommentar": n["c"].get("text"),
                                             "beitrag": (n["m"].get("caption") or "")[:600]} for n in neu], SCHEMA) or {}
    vorschlag = {a["nr"]: a["text"] for a in vorschlaege.get("antworten", [])}
    zeilen = []
    for n in neu:
        v = vorschlag.get(n["nr"], "")
        stand["kommentare"][n["c"]["id"]] = {"nr": n["nr"], "vorschlag": v, "status": "offen",
                                            "datum": JETZT.strftime("%Y-%m-%d"), "von": n["c"].get("username")}
        anfang = " ".join((n["m"].get("caption") or "Beitrag").split()[:6])
        zeilen += [f"**K{n['nr']}** · @{n['c'].get('username')} unter [{anfang} …]({n['m']['permalink']}):",
                   f"> {' '.join((n['c'].get('text') or '').split())}", ""]
        zeilen += [f"✍️ {v}", ""] if v and v.strip().lower() != "ignorieren" else (["_(eher ignorieren)_", ""] if v else [])
    zeilen.append("Antwort hier mit `K<Nr> ok` oder `K<Nr> eigener Text`.")
    gh("issue", "comment", sammel_issue(), "--body", "\n".join(zeilen))
    speichern(stand, f"Kommentare: {len(neu)} neu")
    print(f"✓ {len(neu)} neue Kommentare gemeldet")


def antwort(text):
    stand = laden()
    nach_nr = {v["nr"]: (cid, v) for cid, v in stand["kommentare"].items()}
    ergebnis = []
    for nr, inhalt in re.findall(r"^\s*K(\d+)\s+(.+?)\s*$", text, re.M | re.I):
        cid, v = nach_nr.get(int(nr), (None, None))
        if not cid:
            ergebnis.append(f"❓ K{nr}: nicht gefunden (älter als 30 Tage?)")
            continue
        antworttext = v["vorschlag"] if inhalt.strip().lower() == "ok" else inhalt.strip()
        if not antworttext or antworttext.lower() == "ignorieren":
            ergebnis.append(f"❓ K{nr}: kein Vorschlag da – bitte eigenen Text schreiben")
            continue
        try:
            ig("POST", f"{cid}/replies", message=antworttext)
        except requests.HTTPError as e:
            ergebnis.append(f"🔴 K{nr}: Instagram hat abgelehnt ({e.response.status_code})")
            continue
        v["status"] = "beantwortet"
        ergebnis.append(f"✅ K{nr} an @{v.get('von')}: {antworttext}")
    if not ergebnis:
        print("Keine K-Nummer im Kommentar – nichts zu tun.")
        return
    nummer = gh("issue", "list", "--label", LABEL, "--state", "open", "--json", "number", "--jq", ".[0].number")
    if nummer:
        gh("issue", "comment", nummer, "--body", "\n".join(ergebnis))
    speichern(stand, f"Kommentare: {sum(z.startswith('✅') for z in ergebnis)} beantwortet")


if __name__ == "__main__":
    if sys.argv[1] == "pruefen":
        pruefen()
    else:
        antwort(sys.argv[2] if len(sys.argv) > 2 else "")
