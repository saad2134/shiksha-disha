
import numpy as np
from .embeddings import embed_texts
from .catalog import load_catalog
from .indexer import load_index

def semantic_search(profile, top_k=10):
    profile_text = f"{profile.get('headline', '')}. Skills: {', '.join(profile.get('skills', []))}"
    if profile.get('education'):
        profile_text += f" Education: {profile['education']}"
    
    profile_emb = embed_texts([profile_text])[0]
    
    try:
        index, meta = load_index()
        search_k = min(top_k * 2, index.ntotal)
        scores, indices = index.search(profile_emb.reshape(1, -1), search_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:
                course = meta[idx].copy()
                course['_score'] = float(score)
                results.append(course)
        return results
    except Exception as e:
        catalog_df = load_catalog()
        catalog_texts = (catalog_df['title'] + ". " + catalog_df['description'] + " Skills: " + catalog_df['skills']).tolist()
        catalog_embs = embed_texts(catalog_texts)
        
        sims = np.dot(catalog_embs, profile_emb)
        top_idx = sims.argsort()[::-1][:top_k]
        
        results = []
        for idx in top_idx:
            course = catalog_df.iloc[idx].to_dict()
            course['_score'] = float(sims[idx])
            results.append(course)
        return results


def apply_filters(results, profile, filters=None):
    if not filters:
        return results
    
    filtered = []
    for course in results:
        include = True
        
        if 'nsqf_level' in filters:
            if course.get('nsqf_level') != filters['nsqf_level']:
                include = False
        
        if 'region' in filters and filters['region']:
            if course.get('region', '').lower() != filters['region'].lower():
                include = False
        
        if 'language' in filters and filters['language']:
            if course.get('language', '').lower() != filters['language'].lower():
                include = False
        
        if 'max_duration_months' in filters:
            if course.get('duration_months', 0) > filters['max_duration_months']:
                include = False
        
        if 'min_nsqf_level' in filters:
            if course.get('nsqf_level', 0) < filters['min_nsqf_level']:
                include = False
        
        if include:
            filtered.append(course)
    
    return filtered


def compose_scores(results, profile):
    preferred_nsqf = profile.get('preferred_nsqf_level')
    user_skills = set(s.lower() for s in profile.get('skills', []))
    user_region = profile.get('region', '').lower()
    
    for course in results:
        score = course.get('_score', 0)
        
        if preferred_nsqf and course.get('nsqf_level'):
            level_diff = abs(course['nsqf_level'] - preferred_nsqf)
            nsqf_boost = max(0, 0.3 - (level_diff * 0.1))
            score += nsqf_boost
        
        course_skills = set(s.lower() for s in str(course.get('skills', '')).split(','))
        skill_overlap = len(user_skills & course_skills) / max(len(user_skills | course_skills), 1)
        score += skill_overlap * 0.2
        
        if user_region and course.get('region', '').lower() == user_region:
            score += 0.1
        
        course['_final_score'] = min(score, 1.0)
    
    results.sort(key=lambda x: x.get('_final_score', 0), reverse=True)
    return results
