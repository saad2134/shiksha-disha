
import numpy as np
from .embeddings_tf import embed_texts
from .catalog import load_catalog

# Preload catalog embeddings
catalog_df = load_catalog()
catalog_texts = (catalog_df['title'] + ". " + catalog_df['description'] + " Skills: " + catalog_df['skills']).tolist()
catalog_embs = embed_texts(catalog_texts)

def match_profile_tf(profile, top_k=5):
    # Encode profile
    profile_text = f"{profile.get('headline','')}. Skills: {';'.join(profile.get('skills',[]))}"
    profile_emb = embed_texts([profile_text])[0]
    
    # Compute cosine similarity
    sims = np.dot(catalog_embs, profile_emb)
    top_idx = sims.argsort()[::-1][:top_k]
    
    results = []
    for idx in top_idx:
        course = catalog_df.iloc[idx].to_dict()
        course['_score'] = float(sims[idx])
        results.append(course)
    return results
