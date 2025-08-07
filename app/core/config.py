from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str = "sqlite:///./mbti_roster.db"  # Default to SQLite
    secret_key: str = "test_secret_key"  # Safe default for CI or docs
    redis_url: str = "redis://localhost:6379"
    email_from: str = "noreply@mbti-roster.com"

    # 投票限制配置
    daily_vote_limit: int = 20
    daily_no_reason_limit: int = 5
    new_user_24h_limit: int = 3
    daily_registrations_per_ip: int = 3

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        # Override secret_key for CI environment if not provided
        if "secret_key" not in kwargs and os.getenv("CI"):
            kwargs["secret_key"] = "test-secret-key-for-ci-12345"
        super().__init__(**kwargs)


settings = Settings()
