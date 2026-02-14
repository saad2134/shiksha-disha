import pandas as pd
from typing import Optional
from .config import settings

REQUIRED_COLUMNS = [
    "course_id", "title", "description", "nsqf_level",
    "skills", "keywords", "duration_months", "language", "region"
]

def load_catalog(path: Optional[str] = None) -> pd.DataFrame:
    path = path or settings.NSQF_COURSES_PATH
    df = pd.read_csv(path)
    for c in REQUIRED_COLUMNS:
        if c not in df.columns:
            df[c] = ""
    df['course_id'] = df['course_id'].astype(str)
    df['skills'] = df['skills'].fillna("").astype(str)
    df['keywords'] = df['keywords'].fillna("").astype(str)
    df['description'] = df['description'].fillna("").astype(str)
    df['title'] = df['title'].fillna("").astype(str)
    return df
