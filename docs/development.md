# Development

## Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-venv ffmpeg
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000.

## Architecture

`/api/trends` discovers current RSS items and scores them with freshness, novelty, and title signals.

`/api/generate` turns a selected trend into a short-form content package. With `OPENAI_API_KEY`, it uses the configured LLM endpoint; without one, it uses a deterministic fallback so the app remains testable.

The renderer produces a vertical 1080x1920 FFmpeg video when FFmpeg is installed. The renderer is intentionally provider-agnostic so B-roll, TTS, subtitles, music, and branded motion templates can be added later.

Platform adapters are isolated in `app/platforms.py`. Actual publishing should use each platform's current official API and OAuth flow, and should be enabled only after the relevant permissions are configured.

## Production flow

Recommended scheduler flow:

`discover -> deduplicate -> source verification -> script -> quality checks -> render -> caption/hashtag variants -> approval -> platform queue -> publish -> analytics`

Keep API credentials in deployment secrets, never in Git.
