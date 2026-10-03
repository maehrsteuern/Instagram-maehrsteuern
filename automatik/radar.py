"""Radar (läuft täglich ca. 07:15 per GitHub Actions): frische Beiträge aus der Nische finden und als
Arbeitsliste für ca. 15 Minuten von Hand in ein GitHub-Issue schreiben.

  1. Kommentieren – 5–8 frische Beiträge beobachteter Konten (und Hashtags, sobald freigeschaltet) mit
     Kommentarvorschlag von Claude. Loris kommentiert von Hand in der App und hakt ab.
  2. DM-Entwürfe – für Konten, unter denen Loris schon mind. 2× kommentiert hat (abgehakt), ein persönlicher
     Erstkontakt. Loris schickt ihn von Hand (oder gar nicht).
  3. Collab – einmal pro Woche (Mo) ein Vorschlag für einen gemeinsamen Beitrag mit einem passenden Konto.

Es wird nie automatisch kommentiert, gefolgt oder geschrieben. Abgehakte Kästchen im Issue vom Vortag werden
beim nächsten Lauf gezählt (automatik/interaktion/kontakte.json) – so weiß der Radar, wer schon „warm“ ist.

Umgebung: FB_TOKEN + FB_IG_USER_ID (Zugang über Facebook-Login, nötig für fremde Profile, EINRICHTUNG.md
Schritt 7), ANTHROPIC_API_KEY (optional, für Vorschläge), GH_TOKEN, GITHUB_REPOSITORY.
  python automatik/radar.py          – normaler Lauf
  python automatik/radar.py --probe  – nur abfragen und Issue-Text ausgeben, nichts speichern
"""
import json, os, re, subprocess, sys, time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ki

WURZEL = Path(__file__).resolve().parent.parent
EINSTELLUNGEN = json.loads((WURZEL / "automatik" / "interaktion.json").read_text())["radar"]
ORDNER = WURZEL / "automatik" / "interaktion"
KONTAKTE, GESEHEN = ORDNER / "kontakte.json", ORDNER / "gesehen.json"
PFLEGE, KOMMENTARE = ORDNER / "pflege.json", ORDNER / "kommentare.json"
EINSTELLUNGS_DATEI = WURZEL / "automatik" / "interaktion.json"
FEHLERHAFT = {}  # Konto → Fehlertext aus der Abfrage (umbenannt, privat, gelöscht …)
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/Instagram-maehrsteuern")
API = "https://graph.facebook.com/v23.0"
LABEL = "radar"
ZONE = ZoneInfo("Europe/Berlin")
JETZT = datetime.now(ZONE)
WOCHENTAG = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
PROBE = "--probe" in sys.argv
FELDER = "id,caption,permalink,timestamp,like_count,comments_count,media_product_type"


# ---------- Hilfen ----------

def gh(*args, eingabe=None):
    return subprocess.run(["gh", *args, "--repo", REPO], input=eingabe, check=True, capture_output=True, text=True).stdout.strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=WURZEL, check=True, capture_output=True, text=True).stdout.strip()


def laden(datei, leer):
    return json.loads(datei.read_text()) if datei.exists() else leer


def api(pfad, **params):
    r = requests.get(f"{API}/{pfad}", params={**params, "access_token": os.environ["FB_TOKEN"]}, timeout=60)
    if not r.ok:
        fehler = r.json().get("error", {}) if r.headers.get("content-type", "").startswith("application/json") else {}
        raise RuntimeError(f"{fehler.get('code', r.status_code)}: {fehler.get('message', r.text[:200])}")
    return r.json()


def zeitpunkt(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z").astimezone(ZONE)


def kurz(text, n=220):
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " …"


def vor(t):
    h = (JETZT - t).total_seconds() / 3600
    return f"vor {int(h)} h" if h < 48 else f"vor {int(h // 24)} Tagen"


# ---------- abgehakte Kästchen vom letzten Mal zählen ----------

def abgehakt_zaehlen(kontakte):
    """Offene Radar-Issues lesen, abgehakte Kästchen in kontakte.json übernehmen.
    Gibt (Issue-Nummern, abgehakte 🧹 entfernen, abgehakte ➕ aufnehmen) zurück."""
    try:
        offen = json.loads(gh("issue", "list", "--label", LABEL, "--state", "open", "--json", "number,body,comments"))
    except subprocess.CalledProcessError:
        return [], [], []
    entfernen, aufnehmen = [], []
    inhaber = REPO.split("/")[0]
    for issue in offen:
        # Pflege-Vorschläge stehen im Issue-Text (montags) oder in Loris' eigenen Kommentaren (z. B. Konten-Suche
        # per Chrome) – Häkchen in fremden Kommentaren zählen nicht
        texte = [issue["body"]] + [c["body"] for c in issue.get("comments", [])
                                   if c.get("author", {}).get("login") == inhaber]
        for text in texte:
            entfernen += re.findall(r"^- \[[xX]\] 🧹[^@\n]*@([\w.]+)", text, re.M)
            aufnehmen += re.findall(r"^- \[[xX]\] ➕[^@\n]*@([\w.]+)", text, re.M)
        for art, nutzer in re.findall(r"^- \[[xX]\] (💬|✉️|🤝)[^@\n]*@([\w.]+)", issue["body"], re.M):
            k = kontakte.setdefault(nutzer, {"kommentare": 0})
            if art == "💬":
                k["kommentare"] = k.get("kommentare", 0) + 1
                k["letzter_kommentar"] = JETZT.strftime("%Y-%m-%d")
            elif art == "✉️":
                k["dm"] = JETZT.strftime("%Y-%m-%d")
            else:
                k["collab"] = JETZT.strftime("%Y-%m-%d")
    return [i["number"] for i in offen], entfernen, aufnehmen


# ---------- Radar-Pflege: nur was Loris abgehakt hat, wird geändert ----------

def konten_uebernehmen(entfernen, aufnehmen):
    """Abgehakte Pflege-Vorschläge in interaktion.json übernehmen (das Häkchen ist die Entscheidung)."""
    alles = json.loads(EINSTELLUNGS_DATEI.read_text())
    konten = [k for k in alles["radar"]["konten"] if (k["name"] if isinstance(k, dict) else k) not in entfernen]
    vorhanden = {k["name"] if isinstance(k, dict) else k for k in konten}
    konten += [{"name": n, "art": ""} for n in dict.fromkeys(aufnehmen) if n not in vorhanden]
    alles["radar"]["konten"] = konten
    text = json.dumps(alles, ensure_ascii=False, indent=2)
    # ein Konto pro Zeile, wie von Hand gepflegt
    text = re.sub(r'\{\n\s+"name": ("[^"]*"),\n\s+"art": ("[^"]*")\n\s+\}', r'{"name": \1, "art": \2}', text)
    # kurze Listen (Hashtags, Schlagwörter, Zahlen) in eine Zeile
    text = re.sub(r'\[\n\s+((?:(?:"[^"\n]*"|-?\d+),\n\s+)*(?:"[^"\n]*"|-?\d+))\n\s+\]',
                  lambda m: "[" + re.sub(r",\n\s+", ", ", m.group(1)) + "]", text)
    EINSTELLUNGS_DATEI.write_text(text + "\n")
    EINSTELLUNGEN["konten"] = konten
    print(f"✓ Radar-Pflege übernommen: −{len(entfernen)} / +{len(aufnehmen)}")


def pflege_vorschlaege(profile):
    """Einmal pro Woche (collab_tag): ruhige oder kaputte Konten zum Entfernen, Kommentierende mit
    Business-/Creator-Konto zum Aufnehmen. Ein Vorschlag kommt höchstens alle 60 Tage wieder."""
    if WOCHENTAG[JETZT.weekday()] != EINSTELLUNGEN["collab_tag"]:
        return [], []
    pflege = laden(PFLEGE, {"vorgeschlagen": {}})
    frisch = (JETZT - timedelta(days=60)).strftime("%Y-%m-%d")
    neu_genug = lambda n: pflege["vorgeschlagen"].get(n, "") < frisch
    grenze = JETZT - timedelta(days=30)
    weg = [(n, f"nicht abrufbar ({kurz(f, 80)})") for n, f in FEHLERHAFT.items()]
    for p in profile:
        medien = p.get("media", {}).get("data", [])
        if not medien:
            weg.append((p["username"], "noch nie gepostet"))
        elif zeitpunkt(medien[0]["timestamp"]) < grenze:
            weg.append((p["username"], f"letzter Beitrag {vor(zeitpunkt(medien[0]['timestamp']))}"))
    weg = [(n, g) for n, g in weg if neu_genug(n)]
    vorhanden = {k["name"] if isinstance(k, dict) else k for k in EINSTELLUNGEN["konten"]}
    kommentierende = sorted({v.get("von") for v in laden(KOMMENTARE, {}).get("kommentare", {}).values()
                             if v.get("von") and v["datum"] >= grenze.strftime("%Y-%m-%d")} - vorhanden)
    dazu = []
    for name in [n for n in kommentierende if neu_genug(n)][:10]:
        try:  # klappt nur bei Business-/Creator-Konten – genau die, die der Radar lesen kann
            d = api(os.environ["FB_IG_USER_ID"], fields=f"business_discovery.username({name}){{followers_count,media_count}}")
        except RuntimeError:
            continue
        b = d["business_discovery"]
        if b.get("media_count"):
            dazu.append((name, f"hat bei dir kommentiert · {b.get('followers_count')} Follower · {b['media_count']} Beiträge"))
    for n, _ in weg + dazu:
        pflege["vorgeschlagen"][n] = JETZT.strftime("%Y-%m-%d")
    if not PROBE:
        PFLEGE.write_text(json.dumps(pflege, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    return weg, dazu


# ---------- Daten holen ----------

def konten_abfragen(fehler):
    profile = []
    for eintrag in EINSTELLUNGEN["konten"]:
        name = eintrag["name"] if isinstance(eintrag, dict) else eintrag
        try:
            d = api(os.environ["FB_IG_USER_ID"],
                    fields=f"business_discovery.username({name}){{username,name,followers_count,media_count,"
                           f"media.limit(6){{{FELDER}}}}}")["business_discovery"]
        except RuntimeError as e:
            fehler.append(f"@{name}: {e}")
            FEHLERHAFT[name] = str(e)
            continue
        d["art"] = eintrag.get("art", "") if isinstance(eintrag, dict) else ""
        profile.append(d)
    return profile


def hashtags_abfragen(fehler):
    """Braucht die Meta-Freigabe „Instagram Public Content Access“. Ohne sie: ein Hinweis, sonst nichts."""
    beitraege, ids = [], laden(ORDNER / "hashtag_ids.json", {})
    for tag in EINSTELLUNGEN["hashtags"]:
        try:
            if tag not in ids:
                ids[tag] = api("ig_hashtag_search", user_id=os.environ["FB_IG_USER_ID"], q=tag)["data"][0]["id"]
            for m in api(f"{ids[tag]}/recent_media", user_id=os.environ["FB_IG_USER_ID"], fields=FELDER, limit=30)["data"]:
                m["hashtag"] = tag
                beitraege.append(m)
        except (RuntimeError, IndexError, KeyError) as e:
            fehler.append(f"Hashtags noch nicht verfügbar ({e}) – Freischaltung siehe strategie/12_interaktion.md")
            break
    if ids and not PROBE:
        (ORDNER / "hashtag_ids.json").write_text(json.dumps(ids, indent=1) + "\n")
    return beitraege


# ---------- auswählen ----------

def punkte(m, kontakt):
    alter = (JETZT - zeitpunkt(m["timestamp"])).total_seconds() / 3600
    text = (m.get("caption") or "").lower()
    treffer = [w for w in EINSTELLUNGEN["schlagwoerter"] if w in text]
    p = 10 * max(0.0, 1 - alter / EINSTELLUNGEN["max_alter_stunden"])  # frisch = früh dabei = sichtbar
    p += 4 * len(treffer)
    p += min(10, (m.get("comments_count") or 0) * 0.5 + (m.get("like_count") or 0) * 0.05)
    p += 6 if kontakt and kontakt.get("kommentare") and not kontakt.get("dm") else 0  # Beziehung weiter aufbauen
    return p, treffer


def auswaehlen(profile, hashtag_beitraege, kontakte, gesehen):
    kandidaten = []
    for p in profile:
        for m in p.get("media", {}).get("data", []):
            m["konto"], m["art"], m["follower"] = p["username"], p.get("art", ""), p.get("followers_count")
            kandidaten.append(m)
    kandidaten += hashtag_beitraege
    grenze = JETZT - timedelta(hours=EINSTELLUNGEN["max_alter_stunden"])
    wertung = []
    for m in kandidaten:
        if m["id"] in gesehen or zeitpunkt(m["timestamp"]) < grenze:
            continue
        p, treffer = punkte(m, kontakte.get(m.get("konto", "")))
        wertung.append((p, treffer, m))
    wertung.sort(key=lambda x: -x[0])
    auswahl, je_konto = [], {}
    for p, treffer, m in wertung:  # höchstens 2 Beiträge pro Konto, damit die Liste breit bleibt
        schluessel = m.get("konto") or m["id"]
        if je_konto.get(schluessel, 0) >= 2:
            continue
        je_konto[schluessel] = je_konto.get(schluessel, 0) + 1
        m["treffer"] = treffer
        auswahl.append(m)
        if len(auswahl) >= EINSTELLUNGEN["max_beitraege"]:
            break
    return auswahl


def dm_kandidaten(profile, kontakte):
    aus = []
    for p in profile:
        k = kontakte.get(p["username"], {})
        if k.get("kommentare", 0) >= EINSTELLUNGEN["kommentare_vor_dm"] and not k.get("dm"):
            letzte = (p.get("media", {}).get("data") or [{}])[0]
            aus.append({"konto": p["username"], "name": p.get("name"), "art": p.get("art"),
                        "follower": p.get("followers_count"), "kommentare_von_loris": k["kommentare"],
                        "letzter_beitrag": kurz(letzte.get("caption"), 500), "link": letzte.get("permalink")})
    return aus[:EINSTELLUNGEN["max_dm_entwuerfe"]]


def collab_kandidat(profile, kontakte):
    if WOCHENTAG[JETZT.weekday()] != EINSTELLUNGEN["collab_tag"]:
        return None
    unten, oben = EINSTELLUNGEN["collab_follower"]
    passend = []
    for p in profile:
        k, follower = kontakte.get(p["username"], {}), p.get("followers_count") or 0
        if k.get("collab") or not unten <= follower <= oben:
            continue
        medien = p.get("media", {}).get("data", [])
        if not medien:
            continue
        rate = sum((m.get("like_count") or 0) + 3 * (m.get("comments_count") or 0) for m in medien) / len(medien) / follower
        passend.append((rate + 0.02 * k.get("kommentare", 0), p))
    if not passend:
        return None
    p = max(passend, key=lambda x: x[0])[1]
    return {"konto": p["username"], "name": p.get("name"), "art": p.get("art"), "follower": p.get("followers_count"),
            "letzte_beitraege": [kurz(m.get("caption"), 300) for m in p.get("media", {}).get("data", [])[:4]]}


# ---------- Vorschläge ----------

SCHEMA = {
    "type": "object",
    "properties": {
        "kommentare": {"type": "array", "items": {"type": "object", "properties": {
            "nr": {"type": "integer"}, "text": {"type": "string"}}, "required": ["nr", "text"], "additionalProperties": False}},
        "dms": {"type": "array", "items": {"type": "object", "properties": {
            "konto": {"type": "string"}, "text": {"type": "string"}}, "required": ["konto", "text"], "additionalProperties": False}},
        "collab": {"type": "object", "properties": {
            "idee": {"type": "string"}, "text": {"type": "string"}}, "required": ["idee", "text"], "additionalProperties": False},
    },
    "required": ["kommentare", "dms", "collab"],
    "additionalProperties": False,
}

AUFGABE = """Schreib Vorschläge, die Loris von Hand in der Instagram-App verwendet.

kommentare: zu JEDEM Beitrag (nr) ein Kommentar, 1–2 Sätze, max. 220 Zeichen. Er soll für die Person und ihre
Follower einen echten Mehrwert haben: eine fachliche Ergänzung, ein Praxisbeispiel aus Steuerabteilung/Kanzlei
oder eine ehrliche Rückfrage. Gern mit Bezug zu Excel/Automatisierung, wenn es natürlich passt. Ist der Beitrag
fachlich zu dünn oder nicht deutsch, schreib als text genau „überspringen“.

dms: für jedes Konto in dm_kandidaten eine erste Direktnachricht (3–5 Sätze). Loris hat schon mehrmals unter
deren Beiträgen kommentiert. Anknüpfen am letzten Beitrag, ein konkretes Kompliment, eine echte Frage oder ein
kleiner Mehrwert (z. B. „ich hab mir dazu mal einen Rechner gebaut, falls du ihn sehen willst“). Kein Verkauf,
kein Termin, kein Link. Es muss sich lesen wie von einem Kollegen.

collab: falls collab_kandidat gesetzt ist: idee = ein konkreter gemeinsamer Beitrag (1–2 Sätze, z. B.
Collab-Karussell „Steuerberater vs. Code“, Gast-Folie, gemeinsames Q&A in der Story), text = die Anfrage-DM
(4–6 Sätze, locker, mit klarem Vorschlag und warum es für beide Follower spannend ist). Sonst beide leer."""


def vorschlaege(auswahl, dms, collab):
    daten = {"beitraege": [{"nr": i + 1, "konto": m.get("konto") or f"#{m.get('hashtag')}", "art": m.get("art", ""),
                            "text": kurz(m.get("caption"), 900)} for i, m in enumerate(auswahl)],
             "dm_kandidaten": dms, "collab_kandidat": collab}
    if not auswahl and not dms and not collab:
        return None
    return ki.json_antwort(AUFGABE, daten, SCHEMA)


# ---------- Issue ----------

def issue_text(auswahl, dms, collab, ki_text, fehler, kontakte, pflege=([], [])):
    kom = {k["nr"]: k["text"] for k in (ki_text or {}).get("kommentare", [])}
    dm_text = {d["konto"]: d["text"] for d in (ki_text or {}).get("dms", [])}
    teile = [f"@{REPO.split('/')[0]} – dein Radar für heute, ca. 15 Min. Alles **von Hand in der App**, "
             "danach hier abhaken. Abgehakte Kästchen merkt sich der Radar (wer warm ist, bekommt später einen DM-Entwurf).", ""]
    teile += ["## 💬 Kommentieren (ca. 10 Min.)",
              "Erst den Beitrag ansehen, Vorschlag anpassen (eigene Worte wirken besser), dann kommentieren.", ""]
    if not auswahl:
        teile.append("_Heute nichts Frisches – Konten in `automatik/interaktion.json` ergänzen._")
    for i, m in enumerate(auswahl, 1):
        vorschlag = kom.get(i, "")
        if vorschlag.strip().lower().startswith("überspringen"):
            continue
        wer = f"@{m['konto']}" if m.get("konto") else f"#{m['hashtag']}"
        warm = kontakte.get(m.get("konto", ""), {}).get("kommentare", 0)
        info = " · ".join(x for x in [
            vor(zeitpunkt(m["timestamp"])),
            f"❤️ {m['like_count']}" if m.get("like_count") is not None else "",
            f"💬 {m.get('comments_count', 0)}",
            f"🔥 schon {warm}× kommentiert" if warm else "",
            ("Stichwort: " + ", ".join(m["treffer"])) if m.get("treffer") else ""] if x)
        teile += [f"- [ ] 💬 kommentiert · {wer} · [Beitrag öffnen]({m['permalink']}) · {info}",
                  f"  > {kurz(m.get('caption'), 160)}"]
        if vorschlag:
            teile += ["", f"  ✍️ {vorschlag}"]
        teile.append("")
    if dms:
        teile += ["## ✉️ DM-Entwürfe (ca. 5 Min.)",
                  "Nur schicken, wenn es sich natürlich anfühlt. Max. eine DM pro Konto, kein Nachhaken, wenn keine Antwort kommt.", ""]
        for d in dms:
            teile += [f"- [ ] ✉️ DM geschickt · @{d['konto']} · schon {d['kommentare_von_loris']}× kommentiert"
                      + (f" · [letzter Beitrag]({d['link']})" if d.get("link") else ""),
                      "", f"  ✍️ {dm_text.get(d['konto'], '_(kein Vorschlag – eigene Worte)_')}", ""]
    c = (ki_text or {}).get("collab", {})
    if collab:
        teile += ["## 🤝 Collab der Woche", "",
                  f"- [ ] 🤝 angefragt · @{collab['konto']} · {collab.get('follower')} Follower", "",
                  f"  💡 {c.get('idee') or 'Idee: gemeinsames Karussell oder Story-Q&A'}", ""]
        if c.get("text"):
            teile += [f"  ✍️ {c['text']}", ""]
    weg, dazu = pflege
    if weg or dazu:
        teile += ["## 🧹 Radar-Pflege (wöchentlich)",
                  "Nur was du abhakst, wird beim nächsten Lauf in `automatik/interaktion.json` übernommen. "
                  "Nicht abgehakt = bleibt, wie es ist (der Vorschlag kommt frühestens in 60 Tagen wieder).", ""]
        teile += [f"- [ ] 🧹 entfernen · @{n} · {g}" for n, g in weg]
        teile += [f"- [ ] ➕ aufnehmen · @{n} · {g}" for n, g in dazu]
        teile.append("")
    if fehler:
        teile += ["<details><summary>⚠️ Hinweise</summary>", "", *[f"- {f}" for f in fehler], "", "</details>"]
    teile += ["", "_Regeln: max. ~10 Kommentare und ~5 DMs am Tag, nie kopierte Massennachrichten – sonst drosselt Instagram das Konto._"]
    return "\n".join(teile)


def speichern(nachricht):
    git("add", str(ORDNER), str(EINSTELLUNGS_DATEI))
    if not git("status", "--porcelain", "--", str(ORDNER), str(EINSTELLUNGS_DATEI)):
        return
    git("commit", "-m", nachricht)
    for versuch in range(5):
        try:
            git("pull", "--rebase", "-q")
            git("push")
            return
        except subprocess.CalledProcessError:
            time.sleep(5 * (versuch + 1))
    raise RuntimeError("Radar-Daten konnten nicht gespeichert werden (push 5× fehlgeschlagen)")


def main():
    if not os.environ.get("FB_TOKEN") or not os.environ.get("FB_IG_USER_ID"):
        print("Radar: FB_TOKEN / FB_IG_USER_ID fehlen – Einrichtung siehe EINRICHTUNG.md Schritt 7. Nichts zu tun.")
        return
    ORDNER.mkdir(parents=True, exist_ok=True)
    kontakte, gesehen = laden(KONTAKTE, {}), laden(GESEHEN, {})
    alte_issues, entfernen, aufnehmen = ([], [], []) if PROBE else abgehakt_zaehlen(kontakte)
    if entfernen or aufnehmen:
        konten_uebernehmen(entfernen, aufnehmen)
    fehler = []
    profile = konten_abfragen(fehler)
    pflege = pflege_vorschlaege(profile)
    auswahl = auswaehlen(profile, hashtags_abfragen(fehler), kontakte, gesehen)
    dms, collab = dm_kandidaten(profile, kontakte), collab_kandidat(profile, kontakte)
    text = issue_text(auswahl, dms, collab, vorschlaege(auswahl, dms, collab), fehler, kontakte, pflege)
    titel = (f"📡 Radar {WOCHENTAG[JETZT.weekday()]} {JETZT:%d.%m.} – {len(auswahl)} Beiträge"
             + (f", {len(dms)} DM-Entwürfe" if dms else "") + (", Collab" if collab else "") + (", Pflege" if any(pflege) else ""))
    if PROBE:
        print(titel, "\n", text)
        return
    try:
        gh("label", "create", LABEL, "--color", "8FA398", "--description", "Tägliche Interaktions-Liste")
    except subprocess.CalledProcessError:
        pass
    print("✓", titel, gh("issue", "create", "--title", titel, "--label", LABEL, "--body-file", "-", eingabe=text))
    for nr in alte_issues:
        gh("issue", "close", str(nr))  # ohne Kommentar – spart eine Benachrichtigung am Tag
    # gesehene Beiträge 30 Tage merken, damit nichts doppelt kommt
    gesehen.update({m["id"]: JETZT.strftime("%Y-%m-%d") for m in auswahl})
    grenze = (JETZT - timedelta(days=30)).strftime("%Y-%m-%d")
    gesehen = {k: v for k, v in gesehen.items() if v >= grenze}
    GESEHEN.write_text(json.dumps(gesehen, indent=1, sort_keys=True) + "\n")
    KONTAKTE.write_text(json.dumps(kontakte, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    speichern(f"Radar {JETZT:%Y-%m-%d}: {len(auswahl)} Beiträge, {len(dms)} DM-Entwürfe"
              + (f", Konten −{len(entfernen)}/+{len(aufnehmen)} (abgehakt)" if entfernen or aufnehmen else ""))


if __name__ == "__main__":
    main()
