import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os


class LearningStyleClassifier:
    LEARNING_STYLES = ['visual', 'auditory', 'reading_writing', 'kinesthetic']
    
    def __init__(self):
        self.model = None
        self.feature_encoder = LabelEncoder()
        self.is_trained = False
        
        self.models_dir = 'models'
        os.makedirs(self.models_dir, exist_ok=True)
    
    def _extract_features(self, events):
        if not events or len(events) == 0:
            return None
        
        df = pd.DataFrame(events)
        
        features = {}
        
        content_type_counts = df['content_type'].value_counts() if 'content_type' in df.columns else pd.Series()
        features['video_watches'] = content_type_counts.get('video', 0)
        features['audio_listens'] = content_type_counts.get('audio', 0)
        features['reading_views'] = content_type_counts.get('text', 0) + content_type_counts.get('reading', 0)
        features['interactive_plays'] = content_type_counts.get('interactive', 0) + content_type_counts.get('simulation', 0)
        
        event_types = df['event_type'].value_counts() if 'event_type' in df.columns else pd.Series()
        features['plays'] = event_types.get('video_play', 0) + event_types.get('audio_play', 0)
        features['listens'] = event_types.get('audio_listen', 0)
        features['reads'] = event_types.get('page_view', 0) + event_types.get('scroll', 0)
        features['clicks'] = event_types.get('click', 0)
        features['interactions'] = event_types.get('interaction', 0)
        
        if 'timestamp' in df.columns and len(df) > 1:
            df = df.sort_values('timestamp')
            time_diffs = df['timestamp'].diff().dt.total_seconds().dropna()
            
            features['avg_time_per_event'] = time_diffs.mean() if len(time_diffs) > 0 else 0
            features['session_duration'] = (df['timestamp'].max() - df['timestamp'].min()).total_seconds()
        else:
            features['avg_time_per_event'] = 0
            features['session_duration'] = 0
        
        features['total_events'] = len(events)
        
        features['video_completion_rate'] = 0
        features['quiz_attempts'] = event_types.get('quiz_attempt', 0)
        features['practice_attempts'] = event_types.get('practice_attempt', 0)
        
        features['note_taking'] = event_types.get('note_create', 0)
        features['bookmarking'] = event_types.get('bookmark', 0)
        features['sharing'] = event_types.get('share', 0)
        
        return features
    
    def _features_to_vector(self, features):
        if features is None:
            return None
        
        return np.array([
            features.get('video_watches', 0),
            features.get('audio_listens', 0),
            features.get('reading_views', 0),
            features.get('interactive_plays', 0),
            features.get('plays', 0),
            features.get('listens', 0),
            features.get('reads', 0),
            features.get('clicks', 0),
            features.get('interactions', 0),
            features.get('avg_time_per_event', 0),
            features.get('session_duration', 0),
            features.get('quiz_attempts', 0),
            features.get('practice_attempts', 0),
            features.get('note_taking', 0),
            features.get('bookmarking', 0)
        ])
    
    def _generate_training_data(self):
        np.random.seed(42)
        n_samples = 600
        
        data = []
        
        for _ in range(n_samples // 4):
            features = {
                'video_watches': np.random.randint(20, 50),
                'audio_listens': np.random.randint(0, 10),
                'reading_views': np.random.randint(0, 15),
                'interactive_plays': np.random.randint(0, 10),
                'plays': np.random.randint(15, 40),
                'listens': np.random.randint(0, 5),
                'reads': np.random.randint(0, 10),
                'clicks': np.random.randint(5, 20),
                'interactions': np.random.randint(0, 10),
                'avg_time_per_event': np.random.uniform(5, 30),
                'session_duration': np.random.uniform(600, 3600),
                'quiz_attempts': np.random.randint(0, 10),
                'practice_attempts': np.random.randint(0, 5),
                'note_taking': np.random.randint(0, 3),
                'bookmarking': np.random.randint(0, 3),
                'learning_style': 'visual'
            }
            data.append(features)
        
        for _ in range(n_samples // 4):
            features = {
                'video_watches': np.random.randint(5, 20),
                'audio_listens': np.random.randint(20, 50),
                'reading_views': np.random.randint(5, 15),
                'interactive_plays': np.random.randint(0, 10),
                'plays': np.random.randint(5, 15),
                'listens': np.random.randint(20, 45),
                'reads': np.random.randint(5, 15),
                'clicks': np.random.randint(3, 15),
                'interactions': np.random.randint(0, 8),
                'avg_time_per_event': np.random.uniform(10, 40),
                'session_duration': np.random.uniform(800, 4000),
                'quiz_attempts': np.random.randint(5, 15),
                'practice_attempts': np.random.randint(0, 5),
                'note_taking': np.random.randint(0, 5),
                'bookmarking': np.random.randint(0, 3),
                'learning_style': 'auditory'
            }
            data.append(features)
        
        for _ in range(n_samples // 4):
            features = {
                'video_watches': np.random.randint(5, 20),
                'audio_listens': np.random.randint(0, 10),
                'reading_views': np.random.randint(25, 50),
                'interactive_plays': np.random.randint(0, 8),
                'plays': np.random.randint(3, 12),
                'listens': np.random.randint(0, 5),
                'reads': np.random.randint(20, 45),
                'clicks': np.random.randint(10, 25),
                'interactions': np.random.randint(0, 5),
                'avg_time_per_event': np.random.uniform(20, 60),
                'session_duration': np.random.uniform(1500, 5000),
                'quiz_attempts': np.random.randint(10, 20),
                'practice_attempts': np.random.randint(5, 12),
                'note_taking': np.random.randint(10, 25),
                'bookmarking': np.random.randint(8, 20),
                'learning_style': 'reading_writing'
            }
            data.append(features)
        
        for _ in range(n_samples // 4):
            features = {
                'video_watches': np.random.randint(10, 25),
                'audio_listens': np.random.randint(5, 15),
                'reading_views': np.random.randint(5, 15),
                'interactive_plays': np.random.randint(20, 45),
                'plays': np.random.randint(8, 18),
                'listens': np.random.randint(3, 10),
                'reads': np.random.randint(3, 12),
                'clicks': np.random.randint(15, 30),
                'interactions': np.random.randint(20, 40),
                'avg_time_per_event': np.random.uniform(3, 15),
                'session_duration': np.random.uniform(400, 2000),
                'quiz_attempts': np.random.randint(8, 18),
                'practice_attempts': np.random.randint(15, 30),
                'note_taking': np.random.randint(0, 5),
                'bookmarking': np.random.randint(0, 5),
                'learning_style': 'kinesthetic'
            }
            data.append(features)
        
        return pd.DataFrame(data)
    
    def train(self):
        df = self._generate_training_data()
        
        feature_cols = [
            'video_watches', 'audio_listens', 'reading_views', 'interactive_plays',
            'plays', 'listens', 'reads', 'clicks', 'interactions',
            'avg_time_per_event', 'session_duration', 'quiz_attempts', 'practice_attempts',
            'note_taking', 'bookmarking'
        ]
        
        X = df[feature_cols].values
        y = df['learning_style'].values
        
        self.model = DecisionTreeClassifier(
            max_depth=10,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42
        )
        self.model.fit(X, y)
        
        self.is_trained = True
        return self
    
    def predict(self, events):
        if not self.is_trained:
            self.train()
        
        features = self._extract_features(events)
        if features is None:
            return {
                'learning_style': 'visual',
                'confidence': 0.25,
                'probabilities': {style: 0.25 for style in self.LEARNING_STYLES},
                'signals': []
            }
        
        X = self._features_to_vector(features).reshape(1, -1)
        
        style = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        prob_dict = dict(zip(self.model.classes_, probabilities))
        
        signals = []
        if features.get('video_watches', 0) > features.get('reading_views', 0) * 1.5:
            signals.append('prefers_video_content')
        if features.get('audio_listens', 0) > features.get('video_watches', 0):
            signals.append('prefers_audio_content')
        if features.get('note_taking', 0) > 10:
            signals.append('takes_notes')
        if features.get('interactive_plays', 0) > features.get('reading_views', 0):
            signals.append('prefers_hands_on')
        if features.get('avg_time_per_event', 0) > 40:
            signals.append('slow_paced_learner')
        if features.get('interactions', 0) > features.get('reads', 0):
            signals.append('interactive_learner')
        
        return {
            'learning_style': style,
            'confidence': round(float(max(probabilities)), 3),
            'probabilities': {k: round(v, 3) for k, v in prob_dict.items()},
            'signals': signals,
            'feature_counts': {
                'videos': features.get('video_watches', 0),
                'audio': features.get('audio_listens', 0),
                'reading': features.get('reading_views', 0),
                'interactive': features.get('interactive_plays', 0)
            }
        }
    
    def get_style_recommendations(self, learning_style):
        recommendations = {
            'visual': {
                'preferred_content': ['video', 'infographic', 'diagram', 'slides'],
                'study_tips': [
                    'Use visual aids and charts',
                    'Watch video tutorials',
                    'Create mind maps',
                    'Use color-coded notes'
                ],
                'avoid': ['long audio recordings', 'text-heavy materials']
            },
            'auditory': {
                'preferred_content': ['audio', 'podcast', 'lecture', 'discussion'],
                'study_tips': [
                    'Listen to audiobooks and podcasts',
                    'Participate in discussions',
                    'Use text-to-speech',
                    'Record and replay lectures'
                ],
                'avoid': ['silent reading', 'isolated study']
            },
            'reading_writing': {
                'preferred_content': ['text', 'article', 'book', 'documentation'],
                'study_tips': [
                    'Take detailed notes',
                    'Write summaries',
                    'Create flashcards',
                    'Read instructions thoroughly'
                ],
                'avoid': ['video-only content', 'hands-on without reading']
            },
            'kinesthetic': {
                'preferred_content': ['interactive', 'simulation', 'lab', 'practice'],
                'study_tips': [
                    'Hands-on practice exercises',
                    'Role-playing and simulations',
                    'Take frequent breaks',
                    'Learn by doing'
                ],
                'avoid': ['passive listening', 'long reading sessions']
            }
        }
        
        return recommendations.get(learning_style, {
            'preferred_content': ['mixed'],
            'study_tips': ['Use varied learning methods'],
            'avoid': []
        })
    
    def get_feature_importance(self):
        if not self.is_trained:
            self.train()
        
        feature_names = [
            'video_watches', 'audio_listens', 'reading_views', 'interactive_plays',
            'plays', 'listens', 'reads', 'clicks', 'interactions',
            'avg_time_per_event', 'session_duration', 'quiz_attempts', 'practice_attempts',
            'note_taking', 'bookmarking'
        ]
        
        importance = self.model.feature_importances_
        importance_dict = dict(zip(feature_names, importance))
        
        sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        
        return [{'feature': k, 'importance': round(v, 4)} for k, v in sorted_importance]
    
    def save(self, path=None):
        path = path or os.path.join(self.models_dir, 'learning_style_classifier.joblib')
        joblib.dump({
            'model': self.model,
            'is_trained': self.is_trained
        }, path)
    
    def load(self, path=None):
        path = path or os.path.join(self.models_dir, 'learning_style_classifier.joblib')
        if os.path.exists(path):
            data = joblib.load(path)
            self.model = data['model']
            self.is_trained = data['is_trained']
        return self


classifier = LearningStyleClassifier()
try:
    classifier.load()
except:
    pass
