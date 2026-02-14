import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os
from .catalog import load_catalog
from .embeddings import embed_texts


class LearnerCourseMatcher:
    def __init__(self):
        self.match_model = None
        self.completion_model = None
        self.performance_model = None
        self.engagement_model = None
        
        self.scaler = StandardScaler()
        self.skill_encoder = LabelEncoder()
        self.region_encoder = LabelEncoder()
        self.is_trained = False
        
        self.models_dir = 'models'
        os.makedirs(self.models_dir, exist_ok=True)
    
    def _profile_to_features(self, profile, course=None):
        features = {}
        
        features['experience_years'] = profile.get('experience_years', 0)
        features['preferred_nsqf_level'] = profile.get('preferred_nsqf_level', 0) or 0
        
        user_skills = profile.get('skills', [])
        features['num_skills'] = len(user_skills)
        
        if course:
            course_skills = [s.strip().lower() for s in str(course.get('skills', '')).split(';')]
            user_skills_lower = [s.lower() for s in user_skills]
            
            skill_match = len(set(user_skills_lower) & set(course_skills))
            features['skill_match_count'] = skill_match
            features['skill_match_ratio'] = skill_match / max(len(set(user_skills_lower + course_skills)), 1)
            
            features['course_nsqf_level'] = course.get('nsqf_level', 0)
            features['nsqf_level_diff'] = abs(features['preferred_nsqf_level'] - features['course_nsqf_level'])
            
            features['course_duration'] = course.get('duration_months', 0)
            
            course_region = course.get('region', '').lower()
            user_region = profile.get('region', '').lower()
            features['region_match'] = 1 if course_region == user_region else 0
            
            course_lang = course.get('language', '').lower()
            user_lang = profile.get('preferred_language', '').lower()
            features['language_match'] = 1 if course_lang == user_lang else 0
        
        return features
    
    def _features_to_vector(self, features_list):
        feature_names = [
            'experience_years', 'preferred_nsqf_level', 'num_skills',
            'skill_match_count', 'skill_match_ratio', 'course_nsqf_level',
            'nsqf_level_diff', 'course_duration', 'region_match', 'language_match'
        ]
        
        vectors = []
        for f in features_list:
            vector = [f.get(name, 0) for name in feature_names]
            vectors.append(vector)
        
        return np.array(vectors)
    
    def _generate_training_data(self):
        df = load_catalog()
        
        np.random.seed(42)
        n_samples = 1000
        
        profiles = []
        courses = []
        match_labels = []
        completion_labels = []
        performance_labels = []
        engagement_labels = []
        
        sample_courses = df.sample(min(50, len(df)), random_state=42).to_dict('records')
        
        for _ in range(n_samples):
            course = np.random.choice(sample_courses)
            
            profile = {
                'experience_years': np.random.uniform(0, 15),
                'preferred_nsqf_level': np.random.choice([3, 4, 5, 6, 7, 8]),
                'skills': np.random.choice([
                    [], ['basic'], ['tools'], ['safety'],
                    ['wiring', 'tools'], ['cooking'], ['marketing'],
                    ['testing', 'qa'], ['design'], ['plumbing']
                ]),
                'region': np.random.choice(['delhi', 'mumbai', 'bangalore', 'kolkata', 'chennai', 'pune', '']),
                'preferred_language': np.random.choice(['en', 'hi', ''])
            }
            
            features = self._profile_to_features(profile, course)
            
            skill_match_ratio = features['skill_match_ratio']
            nsqf_diff = features['nsqf_level_diff']
            
            match_prob = 0.3 + (skill_match_ratio * 0.4) + (0.1 if nsqf_diff <= 1 else 0)
            match_prob = min(1, max(0, match_prob + np.random.normal(0, 0.15)))
            match_label = 1 if match_prob > 0.5 else 0
            
            completion_prob = 0.5 + (features['experience_years'] * 0.02) - (nsqf_diff * 0.1)
            completion_prob = min(1, max(0, completion_prob + np.random.normal(0, 0.1)))
            completion_label = 1 if completion_prob > 0.5 else 0
            
            performance_prob = 0.6 + (features['experience_years'] * 0.03) + (skill_match_ratio * 0.2)
            performance_prob = min(1, max(0, performance_prob + np.random.normal(0, 0.1)))
            performance_label = 1 if performance_prob > 0.6 else 0
            
            engagement_prob = 0.5 + (features['region_match'] * 0.2) + (features['language_match'] * 0.15)
            engagement_prob = min(1, max(0, engagement_prob + np.random.normal(0, 0.1)))
            engagement_label = 1 if engagement_prob > 0.5 else 0
            
            profiles.append(profile)
            courses.append(course)
            match_labels.append(match_label)
            completion_labels.append(completion_label)
            performance_labels.append(performance_label)
            engagement_labels.append(engagement_label)
        
        all_features = []
        for profile, course in zip(profiles, courses):
            f = self._profile_to_features(profile, course)
            all_features.append(f)
        
        X = self._features_to_vector(all_features)
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, match_labels, completion_labels, performance_labels, engagement_labels
    
    def train(self):
        X, match_labels, completion_labels, performance_labels, engagement_labels = self._generate_training_data()
        
        self.match_model = LogisticRegression(random_state=42, max_iter=1000)
        self.match_model.fit(X, match_labels)
        
        self.completion_model = LogisticRegression(random_state=42, max_iter=1000)
        self.completion_model.fit(X, completion_labels)
        
        self.performance_model = LogisticRegression(random_state=42, max_iter=1000)
        self.performance_model.fit(X, performance_labels)
        
        self.engagement_model = LogisticRegression(random_state=42, max_iter=1000)
        self.engagement_model.fit(X, engagement_labels)
        
        self.is_trained = True
        return self
    
    def predict_match(self, profile, course):
        if not self.is_trained:
            self.train()
        
        features = self._profile_to_features(profile, course)
        X = self._features_to_vector([features])
        X_scaled = self.scaler.transform(X)
        
        prob = self.match_model.predict_proba(X_scaled)[0]
        
        return {
            'match_probability': round(float(prob[1]), 3),
            'will_match': bool(prob[1] > 0.5)
        }
    
    def predict_completion(self, profile, course):
        if not self.is_trained:
            self.train()
        
        features = self._profile_to_features(profile, course)
        X = self._features_to_vector([features])
        X_scaled = self.scaler.transform(X)
        
        prob = self.completion_model.predict_proba(X_scaled)[0]
        
        return {
            'completion_probability': round(float(prob[1]), 3),
            'likely_to_complete': bool(prob[1] > 0.5)
        }
    
    def predict_performance(self, profile, course):
        if not self.is_trained:
            self.train()
        
        features = self._profile_to_features(profile, course)
        X = self._features_to_vector([features])
        X_scaled = self.scaler.transform(X)
        
        prob = self.performance_model.predict_proba(X_scaled)[0]
        
        return {
            'performance_probability': round(float(prob[1]), 3),
            'likely_to_perform_well': bool(prob[1] > 0.6)
        }
    
    def predict_engagement(self, profile, course):
        if not self.is_trained:
            self.train()
        
        features = self._profile_to_features(profile, course)
        X = self._features_to_vector([features])
        X_scaled = self.scaler.transform(X)
        
        prob = self.engagement_model.predict_proba(X_scaled)[0]
        
        return {
            'engagement_probability': round(float(prob[1]), 3),
            'likely_to_engage': bool(prob[1] > 0.5)
        }
    
    def match_courses(self, profile, courses, top_k=10):
        if not self.is_trained:
            self.train()
        
        results = []
        
        for course in courses:
            match_pred = self.predict_match(profile, course)
            completion_pred = self.predict_completion(profile, course)
            performance_pred = self.predict_performance(profile, course)
            engagement_pred = self.predict_engagement(profile, course)
            
            combined_score = (
                match_pred['match_probability'] * 0.35 +
                completion_pred['completion_probability'] * 0.25 +
                performance_pred['performance_probability'] * 0.25 +
                engagement_pred['engagement_probability'] * 0.15
            )
            
            results.append({
                'course_id': course.get('course_id'),
                'title': course.get('title'),
                'description': course.get('description'),
                'nsqf_level': course.get('nsqf_level'),
                'skills': course.get('skills'),
                'duration_months': course.get('duration_months'),
                'language': course.get('language'),
                'region': course.get('region'),
                'match_probability': match_pred['match_probability'],
                'completion_probability': completion_pred['completion_probability'],
                'performance_probability': performance_pred['performance_probability'],
                'engagement_probability': engagement_pred['engagement_probability'],
                'combined_score': round(combined_score, 3),
                'predictions': {
                    'match': match_pred,
                    'completion': completion_pred,
                    'performance': performance_pred,
                    'engagement': engagement_pred
                }
            })
        
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        return results[:top_k]
    
    def save(self, path=None):
        path = path or os.path.join(self.models_dir, 'learner_course_matcher.joblib')
        joblib.dump({
            'match_model': self.match_model,
            'completion_model': self.completion_model,
            'performance_model': self.performance_model,
            'engagement_model': self.engagement_model,
            'scaler': self.scaler,
            'is_trained': self.is_trained
        }, path)
    
    def load(self, path=None):
        path = path or os.path.join(self.models_dir, 'learner_course_matcher.joblib')
        if os.path.exists(path):
            data = joblib.load(path)
            self.match_model = data['match_model']
            self.completion_model = data['completion_model']
            self.performance_model = data['performance_model']
            self.engagement_model = data['engagement_model']
            self.scaler = data['scaler']
            self.is_trained = data['is_trained']
        return self


matcher = LearnerCourseMatcher()
try:
    matcher.load()
except:
    pass
