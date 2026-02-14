from typing import List, Dict, Any, Optional
from .embeddings import embed_texts
import numpy as np

CONTENT_DATABASE = [
    {"title": "Introduction to Python Programming", "type": "course", "skills": ["python", "programming", "coding"], "level": "beginner", "duration": "8 weeks"},
    {"title": "Advanced Machine Learning", "type": "course", "skills": ["machine learning", "ai", "data science"], "level": "advanced", "duration": "12 weeks"},
    {"title": "Cloud Computing Fundamentals", "type": "course", "skills": ["cloud", "aws", "azure"], "level": "intermediate", "duration": "6 weeks"},
    {"title": "Data Structures and Algorithms", "type": "course", "skills": ["algorithms", "data structures", "programming"], "level": "intermediate", "duration": "10 weeks"},
    {"title": "Web Development Bootcamp", "type": "course", "skills": ["html", "css", "javascript", "web development"], "level": "beginner", "duration": "16 weeks"},
    {"title": "Cybersecurity Essentials", "type": "course", "skills": ["cybersecurity", "networking", "security"], "level": "intermediate", "duration": "8 weeks"},
    {"title": "Data Science with Python", "type": "course", "skills": ["data science", "python", "analytics"], "level": "intermediate", "duration": "10 weeks"},
    {"title": "DevOps Engineering", "type": "course", "skills": ["devops", "kubernetes", "docker"], "level": "advanced", "duration": "12 weeks"},
    {"title": "Artificial Intelligence Foundations", "type": "course", "skills": ["ai", "machine learning", "neural networks"], "level": "intermediate", "duration": "10 weeks"},
    {"title": "Digital Marketing Masterclass", "type": "course", "skills": ["digital marketing", "seo", "social media"], "level": "beginner", "duration": "6 weeks"},
    {"title": "Project Management Professional", "type": "course", "skills": ["project management", "agile", "scrum"], "level": "intermediate", "duration": "8 weeks"},
    {"title": "UI/UX Design Fundamentals", "type": "course", "skills": ["ui design", "ux design", "figma"], "level": "beginner", "duration": "6 weeks"},
    {"title": "Financial Modeling & Analysis", "type": "course", "skills": ["finance", "excel", "modeling"], "level": "intermediate", "duration": "8 weeks"},
    {"title": "Blockchain Development", "type": "course", "skills": ["blockchain", "solidity", "ethereum"], "level": "advanced", "duration": "10 weeks"},
    {"title": "Product Management Basics", "type": "course", "skills": ["product management", "agile", "analytics"], "level": "beginner", "duration": "4 weeks"},
    {"title": "Natural Language Processing", "type": "course", "skills": ["nlp", "ai", "machine learning"], "level": "advanced", "duration": "8 weeks"},
    {"title": "Cloud Architecture Design", "type": "course", "skills": ["cloud architecture", "aws", "gcp"], "level": "advanced", "duration": "10 weeks"},
    {"title": "Excel for Data Analysis", "type": "workshop", "skills": ["excel", "data analysis", "analytics"], "level": "beginner", "duration": "2 weeks"},
    {"title": "Git & GitHub Essentials", "type": "workshop", "skills": ["git", "github", "version control"], "level": "beginner", "duration": "1 week"},
    {"title": "SQL for Data Science", "type": "workshop", "skills": ["sql", "database", "data science"], "level": "intermediate", "duration": "3 weeks"},
]

class ContentRecommender:
    def __init__(self):
        self.content = CONTENT_DATABASE
        self._build_index()
    
    def _build_index(self):
        texts = [self._get_text(c) for c in self.content]
        self.embeddings = embed_texts(texts)
    
    def _get_text(self, item: dict) -> str:
        return f"{item['title']}. Skills: {', '.join(item['skills'])}. Level: {item['level']}"
    
    def recommend(self, skills: List[str] = [], interests: List[str] = [], current_course: str = None, limit: int = 5) -> List[Dict[str, Any]]:
        if not skills and not interests:
            return self._get_general_recommendations(limit)
        
        query_skills = skills + interests
        query_text = f"Learning {', '.join(query_skills)}"
        query_emb = embed_texts([query_text])[0]
        
        scores = np.dot(self.embeddings, query_emb)
        
        if current_course:
            current_idx = None
            for i, c in enumerate(self.content):
                if current_course.lower() in c["title"].lower():
                    current_idx = i
                    break
            if current_idx is not None:
                scores[current_idx] = -1
        
        top_indices = scores.argsort()[::-1][:limit * 2]
        
        results = []
        for idx in top_indices:
            if len(results) >= limit:
                break
            item = self.content[idx].copy()
            item["relevance_score"] = float(scores[idx])
            results.append(item)
        
        return results
    
    def _get_general_recommendations(self, limit: int) -> List[Dict[str, Any]]:
        popular = ["Python Programming", "Machine Learning", "Cloud Computing", "Data Science", "Web Development"]
        results = []
        
        for title in popular[:limit]:
            for item in self.content:
                if title.lower() in item["title"].lower():
                    item_copy = item.copy()
                    item_copy["relevance_score"] = 0.9
                    results.append(item_copy)
                    break
        
        return results[:limit]
    
    def recommend_by_type(self, content_type: str, level: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        filtered = [c for c in self.content if c["type"] == content_type]
        
        if level:
            filtered = [c for c in filtered if c["level"] == level]
        
        return filtered[:limit]
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        query_emb = embed_texts([query])[0]
        scores = np.dot(self.embeddings, query_emb)
        
        top_indices = scores.argsort()[::-1][:limit]
        
        results = []
        for idx in top_indices:
            item = self.content[idx].copy()
            item["relevance_score"] = float(scores[idx])
            results.append(item)
        
        return results


recommender = ContentRecommender()
