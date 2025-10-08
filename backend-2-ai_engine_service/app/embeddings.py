
import tensorflow_hub as hub
import numpy as np
from .config import settings

# Load USE model
_model = None

def get_model():
    global _model
    if _model is None:
        # Multilingual version if you want multi-language support
        _model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    return _model

def embed_texts(texts):
    model = get_model()
    embs = model(texts)
    # Normalize to unit vectors
    embs = embs / np.linalg.norm(embs, axis=1, keepdims=True)
    return np.array(embs, dtype=np.float32)
