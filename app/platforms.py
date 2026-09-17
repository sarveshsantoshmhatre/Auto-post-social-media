from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class PublishResult:
    platform: str
    status: str
    message: str
    remote_id: str | None = None


class PlatformAdapter:
    name = "base"

    async def publish(self, video_path: str, title: str, description: str, hashtags: list[str]) -> PublishResult:
        raise NotImplementedError


class YouTubeAdapter(PlatformAdapter):
    name = "youtube"

    async def publish(self, video_path: str, title: str, description: str, hashtags: list[str]) -> PublishResult:
        return PublishResult(self.name, "not_configured", "YouTube OAuth/API upload adapter is ready for integration; credentials are not configured in the MVP.")


class InstagramAdapter(PlatformAdapter):
    name = "instagram"

    async def publish(self, video_path: str, title: str, description: str, hashtags: list[str]) -> PublishResult:
        return PublishResult(self.name, "not_configured", "Instagram publishing requires a supported Meta business setup and API permissions.")


class FacebookAdapter(PlatformAdapter):
    name = "facebook"

    async def publish(self, video_path: str, title: str, description: str, hashtags: list[str]) -> PublishResult:
        return PublishResult(self.name, "not_configured", "Facebook publishing requires a Page access token and approved API permissions.")


class TikTokAdapter(PlatformAdapter):
    name = "tiktok"

    async def publish(self, video_path: str, title: str, description: str, hashtags: list[str]) -> PublishResult:
        return PublishResult(self.name, "not_configured", "TikTok publishing depends on the account/app permissions available to the project.")


PLATFORMS = {p.name: p() for p in [YouTubeAdapter, InstagramAdapter, FacebookAdapter, TikTokAdapter]}


def available_video(path: str) -> bool:
    return Path(path).exists()
