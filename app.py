"""
CastKit — Web UI
Run: python app.py → http://localhost:7860
"""

import os
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

:root {
    --bg: #0c0c0c;
    --surface: #141414;
    --surface2: #1e1e1e;
    --border: #2c2c2c;
    --accent: #e8ff47;
    --accent2: #ff6b35;
    --text: #f0f0f0;
    --muted: #777;
    --success: #47ffb2;
    --r: 8px;
}

*, body, .gradio-container {
    background-color: var(--bg) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    color: var(--text) !important;
}

.ck-header {
    padding: 2.5rem 2rem 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: baseline;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.ck-logo {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 4rem;
    letter-spacing: 0.08em;
    color: var(--accent) !important;
    line-height: 1;
    margin: 0;
    text-shadow: 3px 3px 0px var(--accent2);
}

.ck-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-left: 2px solid var(--border);
    padding-left: 1rem;
    line-height: 1.6;
}

.ck-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    padding: 1rem 2rem;
    border-bottom: 1px solid var(--border);
}

.ck-pill {
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.2rem 0.6rem;
}

.ck-pill.active {
    color: var(--accent);
    border-color: var(--accent);
}

.step-label {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.1em !important;
    color: var(--accent2) !important;
    margin: 0 0 0.5rem !important;
}

label, .label-wrap span {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

input[type=text], textarea, .gr-textbox textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
    transition: border-color 0.15s !important;
}

input:focus, textarea:focus {
    border-color: var(--accent) !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(232, 255, 71, 0.1) !important;
}

.tabs > .tab-nav {
    border-bottom: 1px solid var(--border) !important;
    background: transparent !important;
}

.tab-nav button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.05em !important;
    color: var(--muted) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1rem !important;
    text-transform: uppercase !important;
}

.tab-nav button.selected {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}

button.gr-button-primary, .gr-button-primary {
    background: var(--accent) !important;
    border: none !important;
    border-radius: var(--r) !important;
    color: #000 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.75rem 2.5rem !important;
    transition: all 0.15s !important;
    box-shadow: 3px 3px 0 var(--accent2) !important;
}

button.gr-button-primary:hover {
    transform: translate(-1px, -1px) !important;
    box-shadow: 4px 4px 0 var(--accent2) !important;
}

.gr-button {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
}

.output-box {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
}

.highlight-box {
    background: var(--surface2) !important;
    border: 1px solid var(--accent) !important;
    border-radius: var(--r) !important;
    padding: 1rem !important;
    margin-bottom: 1rem !important;
}

select {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

.gr-file {
    background: var(--surface) !important;
    border: 1px dashed var(--border) !important;
    border-radius: var(--r) !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

.ck-footer {
    text-align: center;
    padding: 2rem;
    color: var(--muted);
    font-size: 0.7rem;
    letter-spacing: 0.06em;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
}
"""


def run_pipeline_ui(
    transcript_file,
    topic_notes,
    show_name,
    episode_number,
    guest_name,
    guest_company,
    youtube_url,
    anthropic_key,
    progress=gr.Progress()
):
    from engine import run_pipeline

    if not transcript_file:
        return ("❌ Please upload your transcript .txt file.", "", "", "", "", "", "", "", None, None, None)

    transcript_path = transcript_file if isinstance(transcript_file, str) else transcript_file.name

    ant_key = (anthropic_key or "").strip() or os.getenv("ANTHROPIC_API_KEY")
    if not ant_key:
        return ("❌ No Anthropic API key found. Add it in Settings or your .env file.", "", "", "", "", "", "", "", None, None, None)

    log_lines = []
    def log(msg): log_lines.append(msg)

    try:
        result = run_pipeline(
            transcript_path=transcript_path,
            topic_notes=topic_notes or "",
            show_name=show_name or "My Podcast",
            episode_number=episode_number or "",
            guest_name=guest_name or "",
            guest_company=guest_company or "",
            youtube_url=youtube_url or None,
            anthropic_key=ant_key,
            output_dir="./output",
            progress_callback=log
        )
    except Exception as e:
        return (f"❌ Error: {e}", "", "", "", "", "", "", "", None, None, None)

    content = result.get("content", {})
    files = result.get("files", {})

    # Episode titles
    ep_titles = "\n".join(f"{i+1}. {t}" for i, t in enumerate(content.get("episode_titles", [])))

    # Thumbnail titles
    thumb_titles = "\n".join(f"{i+1}. {t}" for i, t in enumerate(content.get("thumbnail_titles", [])))

    # YouTube chapters
    chapters = "\n".join(
        f"{ch.get('time','')} {ch.get('label','')}"
        for ch in content.get("youtube_chapters", [])
    )

    # Graphics cues (preview)
    cues_preview = ""
    for cue in content.get("graphics_cues", [])[:15]:
        cues_preview += f"[{cue.get('timestamp','?')}] {cue.get('graphic_suggestion','')}\n"

    status = "✅ Done!\n" + "\n".join(f"  {l}" for l in log_lines)

    return (
        status,
        ep_titles,
        thumb_titles,
        content.get("captivate_description", ""),
        content.get("show_notes_full", ""),
        chapters,
        cues_preview,
        content.get("social_linkedin", "") + "\n\n---\n\n" + content.get("social_twitter", "") + "\n\n---\n\n" + content.get("social_instagram", ""),
        files.get("graphics_cues"),
        files.get("show_notes"),
        files.get("mp3"),
    )


def build_ui():
    with gr.Blocks(title="CastKit") as app:

        gr.HTML("""
        <div class="ck-header">
            <h1 class="ck-logo">CastKit</h1>
            <div class="ck-sub">
                Podcast production toolkit<br>
                by + for real video podcasters
            </div>
        </div>
        <div class="ck-pills">
            <span class="ck-pill active">Transcript → Graphics Cues</span>
            <span class="ck-pill active">Auto Show Notes</span>
            <span class="ck-pill active">YouTube Chapters</span>
            <span class="ck-pill active">Captivate Description</span>
            <span class="ck-pill active">Thumbnail Titles</span>
            <span class="ck-pill active">Episode Titles</span>
            <span class="ck-pill active">Social Posts</span>
            <span class="ck-pill active">YouTube → MP3</span>
        </div>
        """)

        with gr.Tabs():

            # ── STEP 1: INPUT ──────────────────────────────────
            with gr.Tab("01 / Input"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML('<p class="step-label">Transcript</p>')
                        transcript_file = gr.File(
                            label="Upload .txt transcript",
                            file_types=[".txt"],
                            type="filepath"
                        )
                        gr.HTML('<p class="step-label" style="margin-top:1.5rem">Episode Topic Notes</p>')
                        topic_notes = gr.Textbox(
                            label="Paste your topic notes (what you planned to cover)",
                            placeholder="- Intro: who is Albert, background at AI Circle\n- Topic 1: how AI communities form in NYC\n- Topic 2: what founders get wrong about AI adoption\n- Topic 3: the future of AI meetups\n- Outro: where to find Albert",
                            lines=8
                        )

                    with gr.Column(scale=1):
                        gr.HTML('<p class="step-label">Episode Info</p>')
                        show_name = gr.Textbox(label="Show Name", value="AI in NYC", placeholder="AI in NYC")
                        episode_number = gr.Textbox(label="Episode Number", placeholder="17")
                        guest_name = gr.Textbox(label="Guest Name", placeholder="Albert Chun")
                        guest_company = gr.Textbox(label="Guest Company", placeholder="AI Circle")

                        gr.HTML('<p class="step-label" style="margin-top:1.5rem">YouTube → MP3</p>')
                        youtube_url = gr.Textbox(
                            label="YouTube URL (optional — skip if you have the file)",
                            placeholder="https://youtube.com/watch?v=...",
                            info="Converts to MP3 for Captivate upload"
                        )

                with gr.Accordion("🔑 API Key", open=False):
                    anthropic_key = gr.Textbox(
                        label="Anthropic API Key (or set ANTHROPIC_API_KEY in .env)",
                        type="password",
                        placeholder="sk-ant-..."
                    )

                run_btn = gr.Button("▶  Run CastKit", variant="primary", size="lg")

            # ── STEP 2: TITLES ─────────────────────────────────
            with gr.Tab("02 / Titles"):
                status_log = gr.Textbox(label="Status", lines=4, interactive=False)
                with gr.Row():
                    with gr.Column():
                        gr.HTML('<p class="step-label">Episode Titles — pick one</p>')
                        episode_titles = gr.Textbox(
                            label="Format: EP ##: [hook] with [guest], [company]",
                            lines=6,
                            interactive=True,
                            
                        )
                    with gr.Column():
                        gr.HTML('<p class="step-label">Thumbnail Titles — pick one</p>')
                        thumbnail_titles = gr.Textbox(
                            label="Short enough to read on a thumbnail",
                            lines=6,
                            interactive=True,
                            
                        )

            # ── STEP 3: DESCRIPTIONS ───────────────────────────
            with gr.Tab("03 / Descriptions"):
                gr.HTML('<p class="step-label">Captivate.fm Description</p>')
                captivate_desc = gr.Textbox(
                    label="Paste this into Captivate when uploading your MP3",
                    lines=3,
                    interactive=True,
                    
                )
                gr.HTML('<p class="step-label" style="margin-top:1.5rem">YouTube Description + Chapters</p>')
                with gr.Row():
                    with gr.Column(scale=2):
                        show_notes = gr.Textbox(
                            label="Full show notes for YouTube description",
                            lines=12,
                            interactive=True,
                            
                        )
                    with gr.Column(scale=1):
                        chapters_out = gr.Textbox(
                            label="YouTube Chapters — paste at bottom of description",
                            lines=12,
                            interactive=True,
                            
                        )

            # ── STEP 4: GRAPHICS CUES ─────────────────────────
            with gr.Tab("04 / Graphics Cues"):
                gr.HTML("""
                <p style="font-size:0.8rem;color:#777;margin-bottom:1rem">
                Timestamps matched against your topic notes — tells you exactly where to drop graphics in Final Cut.
                Download the full cue sheet below.
                </p>
                """)
                graphics_cues = gr.Textbox(
                    label="Graphics cue preview",
                    lines=20,
                    interactive=False,
                    
                )

            # ── STEP 5: SOCIAL ────────────────────────────────
            with gr.Tab("05 / Social"):
                social_out = gr.Textbox(
                    label="LinkedIn · Twitter/X · Instagram",
                    lines=20,
                    interactive=True,
                    
                )

            # ── DOWNLOADS ─────────────────────────────────────
            with gr.Tab("↓ Downloads"):
                gr.HTML("""
                <p style="font-size:0.8rem;color:#777;margin-bottom:1.5rem">
                All files also saved to <code style="color:#e8ff47">./output/</code>
                </p>
                """)
                with gr.Row():
                    dl_cues = gr.File(label="📋 Graphics Cue Sheet (.txt)")
                    dl_notes = gr.File(label="📄 Full Show Notes (.md)")
                    dl_mp3 = gr.File(label="🎵 MP3 for Captivate")

        gr.HTML("""
        <div class="ck-footer">
            CastKit &nbsp;·&nbsp; open-source podcast production toolkit
            &nbsp;·&nbsp; transcript + notes in → full production package out
        </div>
        """)

        run_btn.click(
            fn=run_pipeline_ui,
            inputs=[
                transcript_file, topic_notes, show_name, episode_number,
                guest_name, guest_company, youtube_url, anthropic_key
            ],
            outputs=[
                status_log, episode_titles, thumbnail_titles,
                captivate_desc, show_notes, chapters_out,
                graphics_cues, social_out,
                dl_cues, dl_notes, dl_mp3
            ]
        )

    return app


if __name__ == "__main__":
    app = build_ui()
    app.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
