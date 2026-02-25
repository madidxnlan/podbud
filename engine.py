"""
CastKit — Core Engine
Workflow: transcript .txt + episode topic notes → full production package
Outputs: graphics cue sheet, show notes, YouTube chapters, Captivate desc,
         social posts, 4 thumbnail titles, 4 episode titles, YouTube→MP3
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


# ─────────────────────────────────────────────
# YOUTUBE → MP3
# ─────────────────────────────────────────────

def download_youtube_audio(url: str, output_dir: str = "./output/downloads") -> str:
    """Download YouTube video as MP3 using yt-dlp. Returns path to MP3."""
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", output_template,
        "--no-playlist",
        "--write-info-json",
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp error: {result.stderr}")

    mp3_files = sorted(Path(output_dir).glob("*.mp3"), key=os.path.getmtime)
    if not mp3_files:
        raise FileNotFoundError("No MP3 found after download.")

    return str(mp3_files[-1])


# ─────────────────────────────────────────────
# PARSE TRANSCRIPT
# ─────────────────────────────────────────────

def parse_transcript(txt_path: str) -> list:
    """
    Parse a .txt transcript file into segments.
    Handles common formats:
      - [00:00] or (00:00) or 00:00:00 timestamps
      - Speaker: text lines
      - Plain paragraphs (no timestamps)
    Returns list of {time_str, time_seconds, text}
    """
    with open(txt_path, "r", encoding="utf-8") as f:
        raw = f.read()

    segments = []

    # Try timestamp-based parsing first
    # Matches: [00:00], (00:00), 00:00, 00:00:00, 0:00:00
    ts_pattern = re.compile(
        r'[\[\(]?(\d{1,2}):(\d{2})(?::(\d{2}))?[\]\)]?\s*(.*?)(?=[\[\(]?\d{1,2}:\d{2}|$)',
        re.DOTALL
    )

    matches = list(ts_pattern.finditer(raw))

    if matches:
        for m in matches:
            h_or_m = int(m.group(1))
            mins = int(m.group(2))
            secs = int(m.group(3)) if m.group(3) else 0
            text = m.group(4).strip()

            # Determine if first group is hours or minutes
            if m.group(3):  # HH:MM:SS
                total_seconds = h_or_m * 3600 + mins * 60 + secs
                time_str = f"{h_or_m:02d}:{mins:02d}:{secs:02d}"
            else:  # MM:SS
                total_seconds = h_or_m * 60 + mins
                time_str = f"{h_or_m:02d}:{mins:02d}"

            if text:
                segments.append({
                    "time_str": time_str,
                    "time_seconds": total_seconds,
                    "text": text
                })
    else:
        # No timestamps — treat whole file as one block
        segments.append({
            "time_str": "00:00",
            "time_seconds": 0,
            "text": raw.strip()
        })

    return segments


def get_full_text(segments: list) -> str:
    """Flatten segments into one readable transcript string."""
    lines = []
    for seg in segments:
        ts = seg.get("time_str", "")
        text = seg.get("text", "").strip()
        if ts:
            lines.append(f"[{ts}] {text}")
        else:
            lines.append(text)
    return "\n".join(lines)


# ─────────────────────────────────────────────
# AI CONTENT GENERATION
# ─────────────────────────────────────────────

def generate_all_content(
    transcript_text: str,
    topic_notes: str,
    show_name: str,
    episode_number: str,
    guest_name: str,
    guest_company: str,
    api_key: Optional[str] = None
) -> dict:
    """
    Single Claude call that generates everything in one shot.
    Returns structured dict with all production assets.
    """
    import anthropic

    client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    ep_label = f"EP {episode_number}" if episode_number else "EP"
    guest_context = f"{guest_name}" + (f" from {guest_company}" if guest_company else "")

    prompt = f"""You are a professional podcast producer for "{show_name}", a tech podcast based in NYC.

EPISODE: {ep_label} featuring {guest_context}

EPISODE TOPIC NOTES (what the hosts planned to cover):
{topic_notes if topic_notes else "No topic notes provided — infer from transcript."}

TRANSCRIPT:
{transcript_text[:14000]}

Generate a complete production package as JSON with these exact keys:

{{
  "episode_titles": [
    "EP {episode_number}: [punchy topic hook] with {guest_name}, {guest_company}",
    "EP {episode_number}: [guest name] on [bold statement about episode theme]",
    "EP {episode_number}: [question or hot take hook] ft. {guest_name}",
    "EP {episode_number}: [short 3-5 word hook] — {guest_name}, {guest_company}"
  ],

  "thumbnail_titles": [
    "[SHORT & PUNCHY — 3-5 words max, all caps ok]",
    "[QUESTION FORMAT — under 8 words, conversational]",
    "[BOLD STATEMENT / HOT TAKE — provocative, shareable]",
    "[GUEST NAME + TOPIC — e.g. 'Albert Chun: AI is Changing Everything']"
  ],

  "graphics_cues": [
    {{
      "timestamp": "00:00",
      "topic": "topic from notes being discussed",
      "graphic_suggestion": "specific graphic to insert — e.g. 'Lower third: Albert Chun, Founder AI Circle' or 'B-roll: AI dashboard screenshot' or 'Graphic: stat callout 40% of jobs affected'"
    }}
  ],

  "youtube_chapters": [
    {{"time": "0:00", "label": "Introduction"}},
    {{"time": "X:XX", "label": "chapter label"}},
    "... one chapter every 5-8 minutes, matching topic notes order"
  ],

  "show_notes_full": "Full 3-4 paragraph show notes for YouTube description. Include: what the episode covers, key insights, guest background, why listeners should care. Professional but conversational tone.",

  "captivate_description": "2-3 sentence max description for Captivate.fm audio upload. Under 200 chars ideally.",

  "social_linkedin": "LinkedIn post. Professional tone. 100-150 words. Include key insight from episode, tag guest if known, end with question for engagement.",

  "social_twitter": "Twitter/X post. Under 280 chars. Hook + key insight + link placeholder [link]",

  "social_instagram": "Instagram caption. Conversational. 2-3 short paragraphs. Relevant hashtags at end.",

  "key_quotes": [
    "direct memorable quote from guest or hosts — exact words from transcript"
  ],

  "tags": ["8-10 YouTube/podcast tags for discoverability"]
}}

IMPORTANT RULES:
- Graphics cues should align WITH the topic notes — when a planned topic is first mentioned in the transcript, flag it
- Thumbnail titles must be SHORT enough to read on a thumbnail image (under 8 words)
- Episode titles must follow format: EP {episode_number}: [content] — always include episode number
- Return ONLY valid JSON, no markdown fences, no extra text
"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse failed: {e}", "raw": raw}


# ─────────────────────────────────────────────
# BUILD GRAPHICS CUE SHEET
# ─────────────────────────────────────────────

def format_graphics_cue_sheet(cues: list, episode_number: str, guest_name: str) -> str:
    """Format graphics cues into a clean editor-friendly document."""
    lines = [
        f"GRAPHICS CUE SHEET",
        f"EP {episode_number} — {guest_name}",
        "=" * 50,
        ""
    ]

    for i, cue in enumerate(cues, 1):
        lines.append(f"CUE {i:02d}  [{cue.get('timestamp', '?')}]")
        lines.append(f"  TOPIC:    {cue.get('topic', '')}")
        lines.append(f"  GRAPHIC:  {cue.get('graphic_suggestion', '')}")
        lines.append("")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# BUILD SHOW NOTES MARKDOWN
# ─────────────────────────────────────────────

def format_show_notes(content: dict, episode_number: str, guest_name: str,
                      guest_company: str, show_name: str) -> str:
    """Build a complete .md show notes file."""
    titles = content.get("episode_titles", [])
    primary_title = titles[0] if titles else f"EP {episode_number}"

    lines = [
        f"# {primary_title}",
        f"**Show:** {show_name}",
        f"**Guest:** {guest_name}" + (f", {guest_company}" if guest_company else ""),
        "",
        "---",
        "",
        "## Episode Title Options",
    ]
    for t in titles:
        lines.append(f"- {t}")

    lines += [
        "",
        "## Thumbnail Title Options",
    ]
    for t in content.get("thumbnail_titles", []):
        lines.append(f"- {t}")

    lines += [
        "",
        "---",
        "",
        "## YouTube Description",
        "",
        content.get("show_notes_full", ""),
        "",
        "**Chapters:**",
    ]
    for ch in content.get("youtube_chapters", []):
        lines.append(f"{ch.get('time', '')} {ch.get('label', '')}")

    lines += [
        "",
        "---",
        "",
        "## Captivate.fm Description",
        "",
        content.get("captivate_description", ""),
        "",
        "---",
        "",
        "## Key Quotes",
    ]
    for q in content.get("key_quotes", []):
        lines.append(f'> "{q}"')
        lines.append("")

    lines += [
        "---",
        "",
        "## Social Posts",
        "",
        "### LinkedIn",
        content.get("social_linkedin", ""),
        "",
        "### Twitter / X",
        content.get("social_twitter", ""),
        "",
        "### Instagram",
        content.get("social_instagram", ""),
        "",
        "---",
        "",
        "## Tags",
        ", ".join(content.get("tags", [])),
    ]

    return "\n".join(lines)


# ─────────────────────────────────────────────
# FULL PIPELINE
# ─────────────────────────────────────────────

def run_pipeline(
    transcript_path: Optional[str],
    topic_notes: str,
    show_name: str,
    episode_number: str,
    guest_name: str,
    guest_company: str,
    youtube_url: Optional[str] = None,
    anthropic_key: Optional[str] = None,
    output_dir: str = "./output",
    progress_callback=None
) -> dict:

    os.makedirs(output_dir, exist_ok=True)

    def progress(msg):
        print(f"  → {msg}")
        if progress_callback:
            progress_callback(msg)

    ep_slug = f"ep{episode_number}" if episode_number else "episode"
    mp3_path = None

    # 1. YouTube → MP3 (optional)
    if youtube_url and youtube_url.strip():
        progress("📥 Downloading YouTube audio...")
        try:
            mp3_path = download_youtube_audio(
                youtube_url.strip(),
                os.path.join(output_dir, "downloads")
            )
            progress(f"MP3 saved: {Path(mp3_path).name}")
        except Exception as e:
            progress(f"⚠️  YouTube download failed: {e}")

    # 2. Parse transcript
    if not transcript_path:
        raise ValueError("A transcript .txt file is required.")

    progress("📄 Parsing transcript...")
    segments = parse_transcript(transcript_path)
    full_text = get_full_text(segments)
    progress(f"Parsed {len(segments)} segments, {len(full_text):,} chars")

    # 3. Generate all content
    progress("✨ Generating all production content...")
    content = generate_all_content(
        transcript_text=full_text,
        topic_notes=topic_notes,
        show_name=show_name,
        episode_number=episode_number,
        guest_name=guest_name,
        guest_company=guest_company,
        api_key=anthropic_key
    )

    if "error" in content:
        progress(f"⚠️  Content generation issue: {content['error']}")

    # 4. Save outputs
    progress("💾 Saving files...")

    # Graphics cue sheet
    cues = content.get("graphics_cues", [])
    cue_sheet = format_graphics_cue_sheet(cues, episode_number, guest_name)
    cue_path = os.path.join(output_dir, f"{ep_slug}-graphics-cues.txt")
    with open(cue_path, "w") as f:
        f.write(cue_sheet)

    # Show notes markdown
    notes_md = format_show_notes(content, episode_number, guest_name, guest_company, show_name)
    notes_path = os.path.join(output_dir, f"{ep_slug}-show-notes.md")
    with open(notes_path, "w") as f:
        f.write(notes_md)

    # Raw JSON data
    data_path = os.path.join(output_dir, f"{ep_slug}-data.json")
    with open(data_path, "w") as f:
        json.dump({
            "episode_number": episode_number,
            "guest_name": guest_name,
            "guest_company": guest_company,
            "topic_notes": topic_notes,
            "content": content,
            "mp3_path": mp3_path
        }, f, indent=2)

    progress("✅ Done!")

    return {
        "content": content,
        "mp3_path": mp3_path,
        "files": {
            "graphics_cues": cue_path,
            "show_notes": notes_path,
            "data": data_path,
            "mp3": mp3_path
        }
    }
