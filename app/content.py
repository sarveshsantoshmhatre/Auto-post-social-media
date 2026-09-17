from __future__ import annotations

import json
import re

import httpx

from .config import settings
from .models import ContentPackage


SYSTEM_PROMPT = """You create high-retention, factual short-form social videos. Do not invent facts. Keep claims traceable to the supplied source. Write for a general audience, with a strong first-second hook, clear narrative, short sentences, pattern interrupts, and a concise CTA. Return JSON only."""


async def generate_content(topic: str, source_url: str, source_summary: str = "") -> ContentPackage:
    if not settings.openai_api_key:
        return fallback_content(topic)

    prompt = f"""Topic: {topic}\nSource URL: {source_url}\nSource summary: {source_summary[:5000]}\n\nCreate a 35-55 second vertical video package. JSON keys: hook, script, title, description, hashtags, cta, duration_seconds. The script should contain spoken words only, with natural pauses indicated by sentence boundaries."""
    headers = {"Authorization": f"Bearer {settings.openai_api_key}", "Content-Type": "application/json"}
    payload = {"model": "gpt-4.1-mini", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}], "temperature": 0.8}
    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    raw = data["choices"][0]["message"]["content"]
    raw = re.sub(r"^```(?:json)?|```$", "", raw.strip()).strip()
    obj = json.loads(raw)
    return ContentPackage(topic=topic, hook=obj["hook"], script=obj["script"], title=obj["title"], description=obj["description"], hashtags=obj.get("hashtags", []), cta=obj["cta"], duration_seconds=int(obj.get("duration_seconds", 45)))


def fallback_content(topic: str) -> ContentPackage:
    hook = f"You have probably seen this trending today: {topic}. Here is what actually matters."
    script = f"{hook} We are going to break down the key point in under a minute. First, understand what happened. Then look at why people are talking about it. Finally, separate the useful signal from the noise. Check the linked source for the original reporting before sharing the claim."
    return ContentPackage(topic=topic, hook=hook, script=script, title=topic[:85], description=f"A concise explainer about {topic}.", hashtags=["#shorts", "#reels", "#trending", "#news"], cta="Follow for concise explainers and verify the source before sharing.")
