import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    NSQF_COURSES_PATH: str = os.getenv("NSQF_COURSES_PATH", "./data/nsqf_courses.csv")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    INDEX_PATH: str = os.getenv("INDEX_PATH", "./models/faiss.index")
    EMBEDS_PATH: str = os.getenv("EMBEDS_PATH", "./models/course_embeds.npy")
    META_PATH: str = os.getenv("META_PATH", "./models/course_meta.pkl")
    TOP_K: int = 10
    class Config:
        env_file = ".env"

settings = Settings()
