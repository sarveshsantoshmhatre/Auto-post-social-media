from __future__ import annotations

import asyncio

from app.content import generate_content
from app.render import render_video
from app.trends import discover_trends


async def run_once() -> None:
    trends = await discover_trends()
    for trend in trends[:3]:
        content = await generate_content(trend.title, trend.source_url)
        path = render_video(content)
        print(f"prepared: {trend.title} -> {path}")


if __name__ == "__main__":
    asyncio.run(run_once())
