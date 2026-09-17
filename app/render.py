from __future__ import annotations

from pathlib import Path
import subprocess

from .models import ContentPackage


def render_video(content: ContentPackage, output_dir: str = "outputs") -> str:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    slug = "".join(c.lower() if c.isalnum() else "-" for c in content.topic)[:55].strip("-") or "video"
    output = out / f"{slug}.mp4"
    script_file = out / f"{slug}.txt"
    script_file.write_text(content.script, encoding="utf-8")

    # MVP placeholder: render a branded text card when FFmpeg is available.
    # Production media providers can replace this with B-roll, TTS, captions,
    # transitions, and platform-specific templates without changing the API.
    vf = "drawtext=text='" + content.title.replace("'", "\\'")[:90] + "':fontcolor=white:fontsize=52:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.55:boxborderw=24"
    cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:r=30", "-t", str(content.duration_seconds), "-vf", vf, "-an", str(output)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return str(output)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return str(script_file)
