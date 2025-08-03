from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    redis_url: str = "redis://localhost:6379"
    email_from: str = "noreply@mbti-roster.com"
    
    # 投票限制配置
    daily_vote_limit: int = 20
    daily_no_reason_limit: int = 5
    new_user_24h_limit: int = 3
    daily_registrations_per_ip: int = 3
    
    class Config:
        env_file = ".env"

settings = Settings() 