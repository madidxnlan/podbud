# CastKit

**Open-source podcast production toolkit for real video podcasters.**

Drop in your transcript + episode topic notes. Get your entire production package in one shot — no more copy-pasting into Claude, no more random YouTube-to-MP3 sites.

---

## The workflow it replaces

| Before CastKit | With CastKit |
|---|---|
| Manually scan transcript for graphic moments | ✅ Auto graphics cue sheet with timestamps |
| Copy transcript → paste into Claude → get show notes | ✅ Show notes generated automatically |
| Manually write YouTube chapter markers | ✅ Chapters from transcript + topic notes |
| Write separate Captivate description | ✅ Captivate-ready short description |
| Go to random site to convert YouTube → MP3 | ✅ Built-in YouTube → MP3 |
| Brainstorm thumbnail text separately | ✅ 4 thumbnail title options (all styles) |
| Write episode title from scratch | ✅ 4 episode titles in `EP ##: Hook with Guest, Company` format |
| Write social posts manually | ✅ LinkedIn, Twitter/X, Instagram ready to post |

---

## Quickstart

### 1. Clone & install

```bash
git clone https://github.com/your-username/castkit.git
cd castkit
pip install -r requirements.txt

# Install ffmpeg (for YouTube→MP3)
# macOS:   brew install ffmpeg
# Ubuntu:  sudo apt install ffmpeg
```

### 2. Add your API key

```bash
cp .env.example .env
# Open .env and add your Anthropic API key
# Get one at https://console.anthropic.com
```

### 3. Run

```bash
python app.py
# Open http://localhost:7860
```

---

## What you get per episode

**Titles**
- 4 episode title options — format: `EP 17: Hook with Guest Name, Company`
- 4 thumbnail title options — one per style: punchy, question, hot take, guest+topic

**Descriptions**
- Full YouTube description (3-4 paragraphs)
- Short Captivate.fm description (under 200 chars)
- YouTube chapter markers

**Graphics Cue Sheet**
A timestamped list of exactly where to insert graphics in your editor, matched against your topic notes. Looks like:

```
CUE 01  [04:32]
  TOPIC:    AI community formation in NYC
  GRAPHIC:  Lower third: Albert Chun, Founder — AI Circle

CUE 02  [11:17]
  TOPIC:    What founders get wrong about AI adoption
  GRAPHIC:  B-roll: office/startup environment or stat callout graphic
```

**Social Posts**
- LinkedIn (professional, 100-150 words)
- Twitter/X (under 280 chars)
- Instagram (conversational + hashtags)

**MP3**
- YouTube URL → download → MP3, ready to upload to Captivate

---

## Input format

**Transcript:** Any `.txt` file with timestamps. Supported formats:
```
[00:00] text here...
(04:32) more text...
00:01:17 more text...
```
Plain text without timestamps also works — you just won't get timestamped graphics cues.

**Topic Notes:** Paste them directly into the app — whatever format you already use.

---

## Tech stack

- [Anthropic Claude](https://anthropic.com) — all content generation
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube audio download
- [ffmpeg](https://ffmpeg.org) — audio processing
- [Gradio](https://gradio.app) — web UI

---

## Contributing

PRs welcome. Roadmap ideas:
- [ ] Direct Captivate.fm API upload
- [ ] Opus Clip link generator output
- [ ] Final Cut Pro XML marker export from cue sheet
- [ ] Batch processing (whole season)
- [ ] Custom show templates (save your defaults)

---

## License

MIT
