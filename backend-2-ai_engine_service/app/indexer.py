import faiss
import numpy as np
import pickle
import os
from .config import settings
from .catalog import load_catalog
from .embeddings import embed_texts, save_embeddings
from typing import Tuple

def build_index(rebuild: bool = False) -> Tuple[faiss.IndexFlatIP, list]:
    df = load_catalog(settings.NSQF_COURSES_PATH)
    texts = (df['title'] + ". " + df['description'] + " Skills: " + df['skills'] + " Keywords: " + df['keywords']).tolist()
    embeds = embed_texts(texts)
    # save embeds and metadata
    os.makedirs(os.path.dirname(settings.EMBEDS_PATH), exist_ok=True)
    np.save(settings.EMBEDS_PATH, embeds)
    meta = df.to_dict(orient='records')
    with open(settings.META_PATH, "wb") as f:
        pickle.dump(meta, f)

    dim = embeds.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine similarity because embeddings are normalized
    index.add(embeds)
    # persist index
    faiss.write_index(index, settings.INDEX_PATH)
    return index, meta

def load_index() -> Tuple[faiss.IndexFlatIP, list]:
    if not os.path.exists(settings.INDEX_PATH):
        return build_index()
    index = faiss.read_index(settings.INDEX_PATH)
    import pickle
    with open(settings.META_PATH, "rb") as f:
        meta = pickle.load(f)
    return index, meta
