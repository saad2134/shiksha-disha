import numpy as np
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime

SKILL_TRENDS_DATA = {
    "technology": {
        "emerging": [
            {"skill": "Generative AI", "growth_rate": 0.85, "urgency": "high"},
            {"skill": "LLM Fine-tuning", "growth_rate": 0.78, "urgency": "high"},
            {"skill": "MLOps", "growth_rate": 0.72, "urgency": "medium"},
            {"skill": "Edge AI", "growth_rate": 0.68, "urgency": "medium"},
            {"skill": "Kubernetes", "growth_rate": 0.65, "urgency": "medium"},
        ],
        "declining": [
            {"skill": "Legacy Java", "decline_rate": 0.35, "urgency": "low"},
            {"skill": "Flash Development", "decline_rate": 0.45, "urgency": "high"},
            {"skill": "Perl", "decline_rate": 0.30, "urgency": "medium"},
        ]
    },
    "healthcare": {
        "emerging": [
            {"skill": "Telemedicine", "growth_rate": 0.75, "urgency": "high"},
            {"skill": "Health AI", "growth_rate": 0.80, "urgency": "high"},
            {"skill": "Medical Data Analytics", "growth_rate": 0.70, "urgency": "medium"},
            {"skill": "Healthcare Robotics", "growth_rate": 0.60, "urgency": "medium"},
        ],
        "declining": [
            {"skill": "Manual Record Keeping", "decline_rate": 0.50, "urgency": "high"},
            {"skill": "Paper-based Billing", "decline_rate": 0.55, "urgency": "high"},
        ]
    },
    "finance": {
        "emerging": [
            {"skill": "FinTech", "growth_rate": 0.82, "urgency": "high"},
            {"skill": "Blockchain Development", "growth_rate": 0.65, "urgency": "medium"},
            {"skill": "Risk Analytics", "growth_rate": 0.70, "urgency": "medium"},
            {"skill": "RegTech", "growth_rate": 0.68, "urgency": "medium"},
        ],
        "declining": [
            {"skill": "Manual Auditing", "decline_rate": 0.40, "urgency": "medium"},
            {"skill": "Basic Accounting", "decline_rate": 0.35, "urgency": "low"},
        ]
    },
    "marketing": {
        "emerging": [
            {"skill": "AI Content Creation", "growth_rate": 0.88, "urgency": "high"},
            {"skill": "Marketing Analytics", "growth_rate": 0.75, "urgency": "high"},
            {"skill": "Social Media AI", "growth_rate": 0.72, "urgency": "medium"},
            {"skill": "Voice Search SEO", "growth_rate": 0.65, "urgency": "medium"},
        ],
        "declining": [
            {"skill": "Traditional Advertising", "decline_rate": 0.45, "urgency": "medium"},
            {"skill": "Print Marketing", "decline_rate": 0.40, "urgency": "medium"},
        ]
    },
    "general": {
        "emerging": [
            {"skill": "Cloud Computing", "growth_rate": 0.75, "urgency": "high"},
            {"skill": "Data Science", "growth_rate": 0.80, "urgency": "high"},
            {"skill": "Cybersecurity", "growth_rate": 0.78, "urgency": "high"},
            {"skill": "Project Management (Agile)", "growth_rate": 0.65, "urgency": "medium"},
            {"skill": "Communication (Digital)", "growth_rate": 0.60, "urgency": "medium"},
        ],
        "declining": [
            {"skill": "Basic Data Entry", "decline_rate": 0.55, "urgency": "high"},
            {"skill": "Routine Documentation", "decline_rate": 0.40, "urgency": "medium"},
            {"skill": "Basic Spreadsheet Only", "decline_rate": 0.35, "urgency": "low"},
        ]
    }
}

class SkillForecaster:
    def __init__(self):
        self.industry_keywords = {
            "technology": ["software", "it", "tech", "developer", "programming", "coding", "ai", "ml", "data"],
            "healthcare": ["health", "medical", "hospital", "nurse", "doctor", "pharma", "biotech"],
            "finance": ["finance", "banking", "accounting", "investment", "fintech", "audit"],
            "marketing": ["marketing", "digital", "seo", "content", "social media", "advertising", "brand"],
        }
    
    def _detect_industry(self, skills: List[str], industry: str = None) -> str:
        if industry:
            industry_lower = industry.lower()
            for key in self.industry_keywords:
                if key in industry_lower:
                    return key
        
        skills_text = " ".join(skills).lower()
        for key, keywords in self.industry_keywords.items():
            if any(kw in skills_text for kw in keywords):
                return key
        return "general"
    
    def forecast(self, current_skills: List[str], industry: str = None, years_ahead: int = 3) -> Dict[str, Any]:
        detected_industry = self._detect_industry(current_skills, industry)
        trends = SKILL_TRENDS_DATA.get(detected_industry, SKILL_TRENDS_DATA["general"])
        
        current_skills_set = set(s.lower() for s in current_skills)
        
        emerging = []
        for skill_data in trends["emerging"]:
            skill_lower = skill_data["skill"].lower()
            if skill_lower not in current_skills_set:
                projected_growth = min(1.0, skill_data["growth_rate"] * (years_ahead / 3))
                emerging.append({
                    "skill": skill_data["skill"],
                    "growth_rate": skill_data["growth_rate"],
                    "projected_demand": round(projected_growth * 100, 1),
                    "urgency": skill_data["urgency"],
                    "time_to_learn": self._estimate_learning_time(skill_data["skill"])
                })
        
        declining = trends["declining"]
        
        recommended_focus = [e["skill"] for e in emerging[:5]]
        
        confidence = 0.75 if detected_industry != "general" else 0.60
        
        return {
            "detected_industry": detected_industry,
            "years_forecast": years_ahead,
            "emerging_skills": sorted(emerging, key=lambda x: x["projected_demand"], reverse=True)[:10],
            "declining_skills": declining,
            "recommended_focus": recommended_focus,
            "confidence": confidence,
            "advice": self._generate_advice(detected_industry, years_ahead)
        }
    
    def _estimate_learning_time(self, skill: str) -> str:
        quick_learn = ["seo", "agile", "analytics", "cloud"]
        medium_learn = ["python", "kubernetes", "blockchain", "ai"]
        
        skill_lower = skill.lower()
        if any(q in skill_lower for q in quick_learn):
            return "2-4 weeks"
        elif any(m in skill_lower for m in medium_learn):
            return "2-3 months"
        else:
            return "3-6 months"
    
    def _generate_advice(self, industry: str, years: int) -> str:
        advice_map = {
            "technology": f"In the next {years} years, focus on AI/ML skills while maintaining strong cloud and cybersecurity foundations. The demand for AI engineers will continue to grow significantly.",
            "healthcare": f"Healthcare is rapidly digitizing. Prioritize telemedicine and health data analytics skills. AI in healthcare is expected to see massive growth.",
            "finance": f"FinTech is transforming the industry. Focus on data analytics, blockchain basics, and regulatory technology knowledge.",
            "marketing": f"AI-powered marketing is the future. Focus on analytics, content creation tools, and understanding digital customer journey.",
            "general": f"Regardless of your field, digital literacy, data analysis, and AI tool proficiency will be essential across all industries."
        }
        return advice_map.get(industry, advice_map["general"])


forecaster = SkillForecaster()
