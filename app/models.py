from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Trend:
    topic: str
    title: str
    source_url: str
    source: str
    score: float = 0.0
    freshness: float = 0.0
    relevance: float = 0.0
    engagement_potential: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ContentPackage:
    topic: str
    hook: str
    script: str
    title: str
    description: str
    hashtags: list[str]
    cta: str
    duration_seconds: int = 45


@dataclass
class PublishJob:
    content_id: str
    platform: str
    status: str = "pending_approval"
    scheduled_for: datetime | None = None
    remote_id: str | None = None
