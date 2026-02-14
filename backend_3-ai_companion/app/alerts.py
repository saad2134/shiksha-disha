from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random

INDUSTRY_ALERTS = [
    {
        "id": "alert_001",
        "title": "AI/ML Skills Demand Surge",
        "description": "Job postings requiring AI/ML skills have increased by 75% year-over-year. Major tech companies are actively hiring for AI roles.",
        "industry": "technology",
        "severity": "high",
        "impact": "positive",
        "date": (datetime.now() - timedelta(days=5)).isoformat(),
        "action": "Consider upskilling in AI/ML to boost career prospects."
    },
    {
        "id": "alert_002",
        "title": "Cloud Certifications Premium",
        "description": "Professionals with AWS/Azure certifications are commanding 20-30% higher salaries compared to non-certified peers.",
        "industry": "technology",
        "severity": "medium",
        "impact": "positive",
        "date": (datetime.now() - timedelta(days=10)).isoformat(),
        "action": "Invest in cloud certification to increase earning potential."
    },
    {
        "id": "alert_003",
        "title": "Remote Work becoming Hybrid",
        "description": "Major companies shifting from fully remote to hybrid models. In-office presence becoming mandatory 2-3 days per week.",
        "industry": "general",
        "severity": "medium",
        "impact": "neutral",
        "date": (datetime.now() - timedelta(days=3)).isoformat(),
        "action": "Prepare for hybrid work arrangements when job hunting."
    },
    {
        "id": "alert_004",
        "title": "Healthcare Digital Transformation",
        "description": "Hospitals and healthcare providers rapidly adopting digital health solutions. High demand for health informatics professionals.",
        "industry": "healthcare",
        "severity": "high",
        "impact": "positive",
        "date": (datetime.now() - timedelta(days=7)).isoformat(),
        "action": "Explore digital health courses and certifications."
    },
    {
        "id": "alert_005",
        "title": "FinTech Disruption Alert",
        "description": "Traditional banking facing disruption from FinTech startups. Digital banking skills in high demand.",
        "industry": "finance",
        "severity": "high",
        "impact": "positive",
        "date": (datetime.now() - timedelta(days=14)).isoformat(),
        "action": "Learn about digital banking, payment systems, and blockchain."
    },
    {
        "id": "alert_006",
        "title": "Green Jobs Growth",
        "description": "Sustainability and green technology sectors seeing 40% job growth. New roles in ESG and renewable energy.",
        "industry": "general",
        "severity": "medium",
        "impact": "positive",
        "date": (datetime.now() - timedelta(days=21)).isoformat(),
        "action": "Consider green skills for future-proofing your career."
    },
    {
        "id": "alert_007",
        "title": "Automation Impact on Admin Roles",
        "description": "Administrative and entry-level clerical roles seeing reduced hiring due to automation. Focus on strategic skills.",
        "industry": "general",
        "severity": "high",
        "impact": "negative",
        "date": (datetime.now() - timedelta(days=2)).isoformat(),
        "action": "Upskill to move beyond routine administrative tasks."
    },
    {
        "id": "alert_008",
        "title": "Data Science Market Saturation",
        "description": "Entry-level data science positions becoming competitive. Mid-senior roles still in high demand.",
        "industry": "technology",
        "severity": "medium",
        "impact": "neutral",
        "date": (datetime.now() - timedelta(days=8)).isoformat(),
        "action": "Specialize in niche areas like MLOps or domain-specific analytics."
    },
    {
        "id": "alert_009",
        "title": "Cybersecurity Talent Shortage",
        "description": "Critical shortage of cybersecurity professionals. 3.5 million unfilled cybersecurity jobs globally.",
        "industry": "technology",
        "severity": "high",
        "impact": "positive",
        "date": (datetime.now() - timedelta(days=1)).isoformat(),
        "action": "Cybersecurity offers excellent job security and high salaries."
    },
    {
        "id": "alert_010",
        "title": "AI Content Tools Adoption",
        "description": "Marketing teams rapidly adopting AI content creation tools. Human-AI collaboration becoming essential skill.",
        "industry": "marketing",
        "severity": "medium",
        "impact": "positive",
        "date": (datetime.now() - timedelta(days=4)).isoformat(),
        "action": "Learn to work with AI content tools to stay relevant."
    }
]

class AlertManager:
    def __init__(self):
        self.alerts = INDUSTRY_ALERTS
    
    def get_alerts(self, industry: Optional[str] = None, region: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        filtered = self.alerts
        
        if industry:
            filtered = [a for a in filtered if industry.lower() in a["industry"].lower() or a["industry"] == "general"]
        
        sorted_alerts = sorted(filtered, key=lambda x: x["date"], reverse=True)
        return sorted_alerts[:limit]
    
    def get_alert_by_id(self, alert_id: str) -> Optional[Dict[str, Any]]:
        for alert in self.alerts:
            if alert["id"] == alert_id:
                return alert
        return None
    
    def get_alerts_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        return [a for a in self.alerts if a["severity"] == severity.lower()]
    
    def get_high_priority_alerts(self) -> List[Dict[str, Any]]:
        return [a for a in self.alerts if a["severity"] == "high"]


alert_manager = AlertManager()
