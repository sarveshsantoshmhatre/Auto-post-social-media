from __future__ import annotations

from datetime import datetime, timezone
import math
import re

import feedparser
import httpx

from .models import Trend

DEFAULT_FEEDS = {
    "Google News": "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
}


def _freshness(published: str | None) -> float:
    if not published:
        return 0.45
    try:
        parsed = feedparser._parse_date(published)
        if not parsed:
            return 0.45
        age_hours = max(0.0, (datetime.now(timezone.utc) - datetime(*parsed[:6], tzinfo=timezone.utc)).total_seconds() / 3600)
        return math.exp(-age_hours / 30)
    except Exception:
        return 0.45


def _keywords(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9+#.-]{2,}", text)}


async def fetch_feed(name: str, url: str) -> list[Trend]:
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        response = await client.get(url, headers={"User-Agent": "AutoPostAI/1.0"})
        response.raise_for_status()
    parsed = feedparser.parse(response.text)
    trends: list[Trend] = []
    for entry in parsed.entries[:25]:
        title = entry.get("title", "Untitled").strip()
        summary = entry.get("summary", "")
        link = entry.get("link", "")
        freshness = _freshness(entry.get("published") or entry.get("updated"))
        words = _keywords(f"{title} {summary}")
        novelty = min(1.0, len(words) / 20.0)
        score = 100 * (0.50 * freshness + 0.30 * novelty + 0.20 * min(1.0, len(title) / 90))
        trends.append(Trend(topic=title, title=title, source_url=link, source=name, score=round(score, 2), freshness=round(freshness, 3), relevance=round(novelty, 3), engagement_potential=round(min(1.0, len(title) / 90), 3)))
    return trends


async def discover_trends() -> list[Trend]:
    all_trends: list[Trend] = []
    for name, url in DEFAULT_FEEDS.items():
        try:
            all_trends.extend(await fetch_feed(name, url))
        except Exception:
            continue
    deduped: dict[str, Trend] = {}
    for item in all_trends:
        key = re.sub(r"\W+", " ", item.title.lower()).strip()
        if key not in deduped or item.score > deduped[key].score:
            deduped[key] = item
    return sorted(deduped.values(), key=lambda x: x.score, reverse=True)[:30]
