# Auto-post Social Media

AI-powered content automation platform that discovers trending topics, generates short-form videos, adapts them for multiple social platforms, and schedules publishing.

## Planned pipeline

1. Discover and score trends from configurable sources.
2. Fact-check and summarize source material.
3. Generate a short-form script, hook, captions, title, description, hashtags, and CTA.
4. Build a vertical 9:16 video with voiceover, subtitles, visuals, and branding.
5. Run safety, copyright, and quality checks.
6. Queue platform-specific versions.
7. Publish through official platform APIs when credentials and permissions are configured.
8. Record publishing status and analytics for later optimization.

## Initial architecture

- Python backend
- FastAPI API
- SQLite for local development
- Background worker for scheduled jobs
- FFmpeg for rendering
- Provider adapters for trend sources, LLMs, TTS, and social platforms
- Environment variables for all secrets

## Important

The application should require explicit user approval by default before publishing generated content. Automatic publishing can be enabled per platform after credentials and review settings are configured.

## Development

Copy `.env.example` to `.env`, install dependencies, then run the FastAPI server using the instructions in `docs/development.md`.
