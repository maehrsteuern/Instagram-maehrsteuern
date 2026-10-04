"""LinkedIn package (runs daily with the radar): prepare every approved carousel for LinkedIn as well.

OFF by default – only runs when automation/interaction.json has "linkedin": {"enabled": true}.

For every carousel from today on without a package, posts/<folder>/linkedin/ gets:
  carousel.pdf – the slides as a PDF (LinkedIn shows PDFs as a swipeable document, the strongest format there)
  text.md      – post text, rewritten for LinkedIn by Claude (more context, question at the end)
plus an issue "💼 LinkedIn …" with links and a suggested day (1 business day after Instagram, 8:00 AM ET).
Uploading is done by hand (2 min): LinkedIn → Start a post → Add a document. Doing it via API would need
the Community Management API (requires approval), so this stays manual on purpose.

Environment: ANTHROPIC_API_KEY (optional), GH_TOKEN, GITHUB_REPOSITORY.
"""
import json, os, subprocess, sys, time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "automation" / "plan.json"
SETTINGS = ROOT / "automation" / "interaction.json"
REPO = os.environ.get("GITHUB_REPOSITORY", "maehrsteuern/maehrtax---instagram")
LABEL = "linkedin"
TODAY = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
WEEKDAY = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

SCHEMA = {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"], "additionalProperties": False}
TASK = """Rewrite this Instagram caption as a LinkedIn post that goes with a PDF carousel. US English.
- First line: a hook that works without "see more" (max. 120 characters).
- Then 4–8 short paragraphs with a bit more professional context than on Instagram, line breaks between paragraphs.
- Professional, direct tone ("you" is fine), no emojis except at most one arrow.
- End: a real question to tax professionals (comments are the strongest signal on LinkedIn).
- Replace "DM TOOL" with: "Want a demo? Just send me a message."
- Keep the compliance line: "Educational content – not tax, legal or accounting advice."
- Max. 3 hashtags at the very end (e.g. #Tax #Excel #Automation).
In this case mentions of Loris' tools are allowed – they are in the original."""


def enabled():
    try:
        return bool(json.loads(SETTINGS.read_text()).get("linkedin", {}).get("enabled"))
    except (OSError, ValueError):
        return False


def gh(*args, stdin=None):
    return subprocess.run(["gh", *args, "--repo", REPO], input=stdin, check=True, capture_output=True, text=True).stdout.strip()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def linkedin_day(time_str):
    t = datetime.strptime(time_str[:10], "%Y-%m-%d") + timedelta(days=1)
    while t.weekday() >= 5:
        t += timedelta(days=1)
    return f"{WEEKDAY[t.weekday()]} {t.month}/{t.day} at 8:00 AM ET"


def pdf(folder, images, target):
    from PIL import Image
    pages = []
    for b in images:
        jpg = folder / "_jpg" / (Path(b).stem + ".jpg")  # usually exists already (smaller)
        pages.append(Image.open(jpg if jpg.exists() else folder / b).convert("RGB"))
    pages[0].save(target, save_all=True, append_images=pages[1:], resolution=150, quality=88)


def main():
    if not enabled():
        print("LinkedIn: disabled (interaction.json → \"linkedin\": {\"enabled\": false}) – nothing to do.")
        return
    import ai
    plan = json.loads(PLAN.read_text())
    new = []
    for e in plan["entries"]:
        if e["type"] != "carousel" or e["status"] not in ("approved", "published") or e["time"][:10] < TODAY:
            continue
        folder = ROOT / e["folder"]
        package = folder / "linkedin"
        if (package / "carousel.pdf").exists() or not all((folder / b).exists() for b in e.get("images", [])):
            continue
        package.mkdir(exist_ok=True)
        pdf(folder, e["images"], package / "carousel.pdf")
        original = (folder / e["caption"]).read_text().strip() if e.get("caption") and (folder / e["caption"]).exists() else ""
        rewritten = (ai.json_answer(TASK, {"instagram": original}, SCHEMA) or {}).get("text")
        (package / "text.md").write_text((rewritten or "⚠️ Created without AI – please adapt for LinkedIn:\n\n" + original) + "\n")
        new.append(e)
        print("✓ LinkedIn package", e["id"])
    if not new:
        print("No new LinkedIn packages.")
        return
    git("add", "posts")
    git("commit", "-m", f"LinkedIn packages: {', '.join(e['id'] for e in new)}")
    for attempt in range(5):
        try:
            git("pull", "--rebase", "-q")
            git("push")
            break
        except subprocess.CalledProcessError:
            subprocess.run(["git", "rebase", "--abort"], cwd=ROOT, capture_output=True)  # otherwise every retry fails the same way
            time.sleep(5 * (attempt + 1))
    else:  # without the push the issue links point nowhere and tomorrow a second package would be built
        raise RuntimeError("LinkedIn packages could not be saved (push failed 5×)")
    try:
        gh("label", "create", LABEL, "--color", "0A66C2", "--description", "Post the carousel on LinkedIn too")
    except subprocess.CalledProcessError:
        pass
    for e in new:
        base = f"https://github.com/{REPO}/blob/main/{e['folder']}/linkedin"
        body = (f"@{REPO.split('/')[0]} Carousel `{e['id']}` (Instagram {e['time']} ET) is ready for LinkedIn.\n\n"
                f"**Post:** {linkedin_day(e['time'])} – LinkedIn → *Start a post* → *Add a document* → "
                f"upload the PDF, title = first line, paste the text.\n\n"
                f"- 📄 [carousel.pdf]({base}/carousel.pdf) (on GitHub → *Download raw file*)\n"
                f"- ✍️ [text.md]({base}/text.md)\n\n"
                "Reply to every comment in the first hour. Then close this issue.")
        gh("issue", "create", "--title", f"💼 LinkedIn: {e['id'].split('-', 1)[1].replace('-', ' ')} – {linkedin_day(e['time'])}",
           "--label", LABEL, "--body-file", "-", stdin=body)


if __name__ == "__main__":
    main()
