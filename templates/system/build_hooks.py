"""Build the English hook library:  python3 build_hooks.py [h01 h05 …]

Every hook is a ready-made Reel opener (1.8–2.8 s, 1080x1920, 30 fps) with outline text (Outfit Bold): the first line is
visible in frame 1, the second pops in by ~1 s. Ambience only (typing, error beep, clock), music only where the hook already
shows the solution – so a hook fits in front of any Reel (rules: strategy/09_reel_rules.md). For every hook this writes a
cut list to cuts/hooks/<name>.json and renders it with montage.py to ../hooks/<name>.mp4. Overview: ../hooks/README.md.

Hook keys: type (hook pattern), pillar (content pillar from strategy/00_us_brief.md), ai (true = AI-generated footage →
switch on Instagram's AI label and add "Contains AI-generated footage." to the caption), scene (montage.py scene), audio.
Sources: English recordings of the demo tool / spreadsheet mock (re-record with templates/system/recordings/*.mjs)
and the clips in ../hooks/clips/ (ai_* = Runway generations, card_* = halves of the split-screen recording).
"""
import json, subprocess, sys
from pathlib import Path

here = Path(__file__).parent
POSTS = "../../posts/"
SRC = {  # paths relative to templates/system
    "table":       "../hooks/clips/card_top_table.mp4",
    "tool":        "../hooks/clips/card_bottom_tool.mp4",
    "ai_office":   "../hooks/clips/ai_office_evening.mp4",
    "ai_calc":     "../hooks/clips/ai_calculator.mp4",
    "ai_shoulder": "../hooks/clips/ai_over_shoulder.mp4",
    "sheet":       POSTS + "01_2026-10-12_reel_ref_error/clips/rec_spreadsheet.mp4",
    "provision":   POSTS + "01_2026-10-12_reel_ref_error/clips/rec_tool.mp4",
    "rate":        POSTS + "04_2026-10-14_reel_hardcoded_rate/clips/rec_rate.mp4",
    "cleanup":     POSTS + "08_2026-10-19_reel_4000_rows/clips/rec_cleanup.mp4",
    "j163":        POSTS + "11_2026-10-21_reel_163j_demo/clips/rec_163j.mp4",
}
A = "../../music/ambience/"
typing = lambda at, dur=0.45: {"file": A + "typing_error_beep.mp3", "at": at, "start": 0.8, "duration": dur, "volume": 2.6, "fade_out": 0.08}
beep = lambda at: {"file": A + "error_beep.mp3", "at": at, "duration": 0.6, "volume": 0.6}
clock = lambda at, dur: {"file": A + "clock_ticking.mp3", "at": at, "start": 0.3, "duration": dur, "volume": 1.0, "fade_out": 0.2}
lofi = lambda at: {"file": "../../music/06_runway_lofi_ruhig.mp3", "at": at, "volume": 0.35, "fade_in": 0.1}
T = lambda text, y, at=None, color="white", size=110: {k: v for k, v in
     {"text": text, "y": y, "at": at, "color": color, "size": size}.items() if v is not None}

HOOKS = {
 "h01_ref_deadline": dict(type="Error callout", pillar="1 Demo · 2 In practice", ai=False,
   scene=dict(source="sheet", duration=2.0, start=1.0, darken=0.25,
              text=[T("#REF!", 600, None, "red", 210), T("3 days before the deadline.", 760, 0.5, size=95)]),
   audio=[typing(0, 0.2), beep(0.2), clock(0.6, 1.4)]),
 "h02_every_provision": dict(type="Error callout", pillar="2 In practice", ai=False,
   scene=dict(source="table", duration=2.6, start=2.2,
              text=[T("This error is in", 420, None, size=110), T("almost every provision.", 545, 0.6, "yellow", 100)]),
   audio=[typing(0, 0.4), beep(0.2), beep(0.9)]),
 "h03_400_cells": dict(type="Number / pain", pillar="5 Satisfying · 2 In practice", ai=False,
   scene=dict(source="rate", duration=2.4, start=0, darken=0.3,
              text=[T("21% typed", 820, None, size=135), T("into 400 cells.", 965, 0.6, "red", 115)]),
   audio=[typing(0, 1.0)]),
 "h04_17_seconds": dict(type="Number / result", pillar="1 Demo", ai=False,
   scene=dict(source="tool", duration=2.7, start=2.3,
              text=[T("Full provision check:", 420, None, size=105), T("17 seconds.", 1400, 2.55, "green", 150)]),
   audio=[clock(0, 2.4), lofi(2.4)]),
 "h05_interest_limit": dict(type="Reveal", pillar="3 Know-how · 1 Demo", ai=False,
   scene=dict(source="j163", duration=2.4, start=1.4, darken=0.3,
              text=[T("Your interest limit", 820, None, size=100), T("just grew.", 955, 0.6, "green", 135)]),
   audio=[typing(0.2, 0.5), lofi(0.6)]),
 "h06_ready_to_book": dict(type="Question / status", pillar="1 Demo", ai=False,
   scene=dict(source="provision", duration=2.5, start=0.2,
              text=[T("Ready to book?", 830, None, size=120), T("Not yet.", 960, 0.9, "red", 140)]),
   audio=[beep(0.9)]),
 "h07_by_hand": dict(type="Question / pain", pillar="2 In practice · 3 Know-how", ai=True,
   scene=dict(source="ai_calc", duration=2.6, start=0.5, speed=0.9,
              text=[T("Still doing this", 340, None, size=120), T("by hand?", 480, 0.8, "yellow", 130)]),
   audio=[typing(0.1, 0.5), typing(1.3, 0.5)]),
 "h08_friday_night": dict(type="Deadline / pain", pillar="2 In practice · 4 Behind the code", ai=True,
   scene=dict(source="ai_office", duration=2.6, start=0.5, speed=0.9,
              text=[T("Friday, 9:45 PM.", 340, None, size=125), T("Due Monday, 8 AM.", 480, 1.0, "red", 110)]),
   audio=[clock(0, 2.6)]),
 "h09_row_4000": dict(type="Pain / search", pillar="2 In practice (no audit trail, #REF!)", ai=True,
   scene=dict(source="ai_shoulder", duration=2.6, start=0.5, speed=0.9,
              text=[T("There's an error somewhere.", 340, None, size=100), T("Row 1 of 4,000.", 480, 1.0, "yellow", 115)]),
   audio=[clock(0.4, 2.2)]),
 "h10_one_click": dict(type="Before / after", pillar="5 Satisfying", ai=False,
   scene=dict(source="cleanup", duration=2.8, start=0.3,
              text=[T("4,000 messy rows.", 900, None, size=120), T("One click.", 1040, 0.8, "green", 140)]),
   audio=[lofi(0.8)]),
}


def build(name):
    h = HOOKS[name]; src = h["scene"]["source"]
    if not (here / SRC[src]).exists():
        print("–", name, "skipped, source missing:", SRC[src]); return
    cut = {"output": f"../hooks/{name}.mp4", "fps": 30, "crf": 20, "audio": h["audio"],
           "sources": {src: {"video": SRC[src]}}, "scenes": [h["scene"]]}
    file = here / "cuts" / "hooks" / f"{name}.json"
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(cut, ensure_ascii=False, indent=1) + "\n")
    subprocess.run([sys.executable, str(here / "montage.py"), str(file)], check=True)


if __name__ == "__main__":
    pick = sys.argv[1:] or list(HOOKS)
    for n in HOOKS:
        if any(n.startswith(p) for p in pick): build(n)
