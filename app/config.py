from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AutoPost AI"
    database_url: str = "sqlite+aiosqlite:///./autopost.db"
    app_base_url: str = "http://localhost:8000"
    openai_api_key: str | None = None
    gnews_api_key: str | None = None
    newsapi_api_key: str | None = None
    elevenlabs_api_key: str | None = None
    auto_publish_enabled: bool = False
    require_approval: bool = True
    default_timezone: str = "Asia/Kolkata"
    youtube_client_id: str | None = None
    youtube_client_secret: str | None = None
    youtube_refresh_token: str | None = None
    instagram_access_token: str | None = None
    instagram_business_account_id: str | None = None
    facebook_page_access_token: str | None = None
    facebook_page_id: str | None = None
    tiktok_access_token: str | None = None
    tiktok_open_id: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
