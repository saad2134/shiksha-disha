import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    SKILL_TRENDS_PATH: str = os.getenv("SKILL_TRENDS_PATH", "./data/skill_trends.csv")
    ALERTS_PATH: str = os.getenv("ALERTS_PATH", "./data/industry_alerts.csv")
    CONVERSATION_HISTORY_LIMIT: int = 50
    MAX_TOKENS: int = 500
    TEMPERATURE: float = 0.7
    
    class Config:
        env_file = ".env"

settings = Settings()
