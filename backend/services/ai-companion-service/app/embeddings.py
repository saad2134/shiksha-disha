
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import settings

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model

def embed_texts(texts: list) -> np.ndarray:
    model = get_model()
    embs = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    embs = embs / np.linalg.norm(embs, axis=1, keepdims=True)
    return np.array(embs, dtype=np.float32)

def embed_query(text: str) -> np.ndarray:
    return embed_texts([text])[0]
