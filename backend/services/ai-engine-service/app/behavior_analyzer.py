import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from datetime import datetime, timedelta

class BehaviorAnalyzer:
    def __init__(self):
        self.engagement_model = None
        self.dropout_model = None
        self.content_type_encoder = LabelEncoder()
        self.difficulty_encoder = LabelEncoder()
        self.is_trained = False
        
    def _extract_features(self, events_df):
        if events_df.empty:
            return None
            
        features = {}
        
        features['total_events'] = len(events_df)
        features['unique_content'] = events_df['content_id'].nunique() if 'content_id' in events_df.columns else 0
        
        event_types = events_df['event_type'].value_counts() if 'event_type' in events_df.columns else pd.Series()
        features['page_views'] = event_types.get('page_view', 0)
        features['clicks'] = event_types.get('click', 0)
        features['scrolls'] = event_types.get('scroll', 0)
        features['pauses'] = event_types.get('pause', 0)
        features['resumes'] = event_types.get('resume', 0)
        features['completes'] = event_types.get('complete', 0)
        features['tab_switches'] = event_types.get('tab_switch', 0)
        features['video_watches'] = event_types.get('video_play', 0)
        features['quiz_attempts'] = event_types.get('quiz_answer', 0)
        
        if 'timestamp' in events_df.columns:
            if len(events_df) > 1:
                time_diffs = events_df['timestamp'].diff().dt.total_seconds().dropna()
                features['avg_time_between_events'] = time_diffs.mean() if len(time_diffs) > 0 else 0
                features['session_duration'] = (events_df['timestamp'].max() - events_df['timestamp'].min()).total_seconds()
            else:
                features['avg_time_between_events'] = 0
                features['session_duration'] = 0
        else:
            features['avg_time_between_events'] = 0
            features['session_duration'] = 0
        
        features['interaction_density'] = features['total_events'] / max(features['session_duration'], 1) * 60
        
        engagement_signals = features['completes'] + features['video_watches'] * 0.5
        friction_signals = features['tab_switches'] + features['pauses'] * 0.3
        features['raw_engagement_score'] = (engagement_signals * 10) / max(features['total_events'], 1)
        features['friction_score'] = friction_signals / max(features['total_events'], 1)
        
        if 'content_type' in events_df.columns:
            dominant = events_df['content_type'].mode()
            features['dominant_content_type'] = dominant.iloc[0] if len(dominant) > 0 else 'video'
        else:
            features['dominant_content_type'] = 'video'
            
        return features
    
    def _features_to_vector(self, features):
        if features is None:
            return None
            
        content_type = self.content_type_encoder.transform([features['dominant_content_type']])[0] if features['dominant_content_type'] in self.content_type_encoder.classes_ else 0
        
        return np.array([
            features['total_events'],
            features['unique_content'],
            features['page_views'],
            features['clicks'],
            features['scrolls'],
            features['pauses'],
            features['resumes'],
            features['completes'],
            features['tab_switches'],
            features['video_watches'],
            features['quiz_attempts'],
            features['avg_time_between_events'],
            features['session_duration'],
            features['interaction_density'],
            features['raw_engagement_score'],
            features['friction_score'],
            content_type
        ])
    
    def train(self, training_data_path=None):
        np.random.seed(42)
        
        n_samples = 500
        data = {
            'total_events': np.random.randint(5, 200, n_samples),
            'unique_content': np.random.randint(1, 20, n_samples),
            'page_views': np.random.randint(1, 50, n_samples),
            'clicks': np.random.randint(0, 30, n_samples),
            'scrolls': np.random.randint(0, 50, n_samples),
            'pauses': np.random.randint(0, 15, n_samples),
            'resumes': np.random.randint(0, 10, n_samples),
            'completes': np.random.randint(0, 10, n_samples),
            'tab_switches': np.random.randint(0, 20, n_samples),
            'video_watches': np.random.randint(0, 20, n_samples),
            'quiz_attempts': np.random.randint(0, 10, n_samples),
            'avg_time_between_events': np.random.exponential(30, n_samples),
            'session_duration': np.random.exponential(300, n_samples),
            'interaction_density': np.random.uniform(0.1, 5, n_samples),
            'dominant_content_type': np.random.choice(['video', 'quiz', 'text', 'interactive'], n_samples),
        }
        
        df = pd.DataFrame(data)
        
        engagement_scores = []
        dropout_probs = []
        for _, row in df.iterrows():
            raw_eng = (row['completes'] * 10 + row['video_watches'] * 5 + row['quiz_attempts'] * 7) / max(row['total_events'], 1) * 100
            raw_eng = min(100, max(0, raw_eng + np.random.normal(0, 10)))
            engagement_scores.append(int(raw_eng))
            
            dropout = 0.3
            dropout += row['tab_switches'] * 0.03
            dropout += row['pauses'] * 0.02
            dropout -= row['completes'] * 0.05
            dropout -= row['quiz_attempts'] * 0.03
            dropout = min(1, max(0, dropout + np.random.normal(0, 0.1)))
            dropout_probs.append(dropout)
        
        df['engagement_score'] = engagement_scores
        df['dropout_probability'] = dropout_probs
        
        self.content_type_encoder.fit(['video', 'quiz', 'text', 'interactive', 'simulation'])
        
        X = []
        for _, row in df.iterrows():
            features = row.to_dict()
            features['dominant_content_type'] = row['dominant_content_type']
            X.append(self._features_to_vector(features))
        X = np.array(X)
        
        y_engagement = df['engagement_score'].values
        y_dropout = (df['dropout_probability'] > 0.5).astype(int).values
        
        self.engagement_model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
        self.engagement_model.fit(X, y_engagement)
        
        self.dropout_model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
        self.dropout_model.fit(X, y_dropout)
        
        self.is_trained = True
        return self
    
    def predict_engagement(self, events_df):
        if not self.is_trained:
            self.train()
        
        features = self._extract_features(events_df)
        if features is None:
            return {'engagement_score': 50, 'confidence': 0}
        
        X = self._features_to_vector(features).reshape(1, -1)
        score = self.engagement_model.predict(X)[0]
        score = max(0, min(100, score))
        
        return {
            'engagement_score': round(float(score), 2),
            'confidence': 0.85,
            'signals': {
                'total_events': features['total_events'],
                'completes': features['completes'],
                'friction': features['friction_score']
            }
        }
    
    def predict_dropout(self, events_df):
        if not self.is_trained:
            self.train()
        
        features = self._extract_features(events_df)
        if features is None:
            return {'dropout_probability': 0.5, 'risk_level': 'medium'}
        
        X = self._features_to_vector(features).reshape(1, -1)
        prob = self.dropout_model.predict_proba(X)[0]
        
        dropout_prob = prob[1] if len(prob) > 1 else prob[0]
        
        risk_level = 'low'
        if dropout_prob > 0.7:
            risk_level = 'high'
        elif dropout_prob > 0.4:
            risk_level = 'medium'
        
        return {
            'dropout_probability': round(float(dropout_prob), 3),
            'risk_level': risk_level,
            'signals': {
                'tab_switches': features['tab_switches'],
                'pauses': features['pauses'],
                'completes': features['completes']
            }
        }
    
    def get_recommendation(self, events_df):
        engagement = self.predict_engagement(events_df)
        dropout = self.predict_dropout(events_df)
        
        recommendation = {
            'action': 'continue',
            'content_type': 'video',
            'reason': 'Normal engagement patterns detected'
        }
        
        if engagement['engagement_score'] < 30:
            recommendation['action'] = 'boost'
            recommendation['content_type'] = 'quiz'
            recommendation['reason'] = 'Low engagement - switching to interactive content'
        elif dropout['dropout_probability'] > 0.6:
            recommendation['action'] = 'intervene'
            recommendation['content_type'] = 'interactive'
            recommendation['reason'] = 'High dropout risk - offering engaging content'
        elif engagement['engagement_score'] > 70:
            recommendation['action'] = 'advance'
            recommendation['content_type'] = 'video'
            recommendation['reason'] = 'High engagement - can proceed with next content'
        
        return {
            **recommendation,
            'engagement': engagement,
            'dropout': dropout
        }
    
    def save(self, path='models/behavior_model.joblib'):
        joblib.dump({
            'engagement_model': self.engagement_model,
            'dropout_model': self.dropout_model,
            'content_type_encoder': self.content_type_encoder,
            'is_trained': self.is_trained
        }, path)
    
    def load(self, path='models/behavior_model.joblib'):
        if os.path.exists(path):
            data = joblib.load(path)
            self.engagement_model = data['engagement_model']
            self.dropout_model = data['dropout_model']
            self.content_type_encoder = data['content_type_encoder']
            self.is_trained = data['is_trained']
        return self


analyzer = BehaviorAnalyzer()
try:
    analyzer.load()
except:
    pass
