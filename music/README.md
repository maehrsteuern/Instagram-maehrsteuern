# Music for automatic Reels

Instagram music can't be added through the API. So that Reels can still go live automatically, a royalty-free track is baked into the video.

**Filled automatically** by the workflow "music" (`.github/workflows/music.yml`, `automation/fetch_music.py` – public-domain tracks, see `SOURCES.md`). You can add or replace your own tracks at any time:

**Upload a track yourself** (GitHub → this folder → *Add file → Upload files*):
- Source: https://pixabay.com/music/ (free, no attribution, allowed for social media) – check the license of every track
- Style: instrumental, electronic / tech / lo-fi, **beat from second 0**, 15–60 s
- Names: `07_tech.mp3`, `08_lofi.mp3`, … (no spaces), and add a line to `SOURCES.md`

The Content Factory rotates through the tracks. Rules: ambience in the hook, music only from the solution on, music quiet under a voice (`strategy/09_reel_rules.md`).

**Sound effects** are in `ambience/`: `typing_error_beep.mp3` (typing only), `error_beep.mp3`, `clock_ticking.mp3`.

If you want an Instagram trending sound for a Reel anyway, the Reel gets status `manual` in the plan and you post it yourself (`strategy/05_publishing.md`, Plan B).
