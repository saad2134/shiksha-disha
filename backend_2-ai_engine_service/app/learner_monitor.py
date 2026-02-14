import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import joblib
import os
from datetime import datetime, timedelta
from collections import deque


class LearnerMonitor:
    def __init__(self):
        self.anomaly_model = None
        self.struggle_model = None
        self.boredom_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
        self.models_dir = 'models'
        os.makedirs(self.models_dir, exist_ok=True)
        
        self.session_windows = {}
        self.alert_thresholds = {
            'inactive_hours': 2.0,
            'struggle_score': 0.7,
            'boredom_score': 0.6,
            'fast_completion_hours': 0.5
        }
    
    def _extract_session_features(self, events):
        if not events or len(events) == 0:
            return None
        
        df = pd.DataFrame(events)
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
        
        features = {}
        
        features['total_events'] = len(events)
        
        event_types = df['event_type'].value_counts() if 'event_type' in df.columns else pd.Series()
        features['page_views'] = event_types.get('page_view', 0)
        features['clicks'] = event_types.get('click', 0)
        features['scrolls'] = event_types.get('scroll', 0)
        features['video_plays'] = event_types.get('video_play', 0)
        features['video_pauses'] = event_types.get('video_pause', 0)
        features['video_completes'] = event_types.get('video_complete', 0)
        features['tab_switches'] = event_types.get('tab_switch', 0)
        features['quiz_attempts'] = event_types.get('quiz_attempt', 0)
        features['quiz_fails'] = event_types.get('quiz_fail', 0)
        features['quiz_success'] = event_types.get('quiz_success', 0)
        features['timeouts'] = event_types.get('timeout', 0)
        features['searches'] = event_types.get('search', 0)
        features['repeats'] = event_types.get('content_repeat', 0)
        
        if 'timestamp' in df.columns and len(df) > 1:
            session_start = df['timestamp'].min()
            session_end = df['timestamp'].max()
            session_duration = (session_end - session_start).total_seconds() / 3600
            features['session_duration_hours'] = session_duration
            
            time_diffs = df['timestamp'].diff().dt.total_seconds().dropna()
            features['avg_time_between_events'] = time_diffs.mean() if len(time_diffs) > 0 else 0
            features['max_gap_hours'] = time_diffs.max() / 3600 if len(time_diffs) > 0 else 0
            
            inactive_periods = time_diffs[time_diffs > 300]
            features['long_inactive_periods'] = len(inactive_periods)
            features['total_inactive_seconds'] = inactive_periods.sum() if len(inactive_periods) > 0 else 0
        else:
            features['session_duration_hours'] = 0
            features['avg_time_between_events'] = 0
            features['max_gap_hours'] = 0
            features['long_inactive_periods'] = 0
            features['total_inactive_seconds'] = 0
        
        features['events_per_minute'] = features['total_events'] / max(features['session_duration_hours'] * 60, 1)
        
        engagement_positive = features['clicks'] + features['video_plays'] + features['quiz_success']
        engagement_negative = features['tab_switches'] + features['timeouts'] + features['quiz_fails']
        features['engagement_ratio'] = engagement_positive / max(engagement_positive + engagement_negative, 1)
        
        features['scroll_depth_avg'] = df['scroll_depth'].mean() if 'scroll_depth' in df.columns else 0
        features['video_watch_ratio'] = features['video_plays'] / max(features['video_completes'], 1)
        
        features['content_diversity'] = df['content_id'].nunique() if 'content_id' in df.columns else 1
        
        if 'content_type' in df.columns:
            content_types = df['content_type'].value_counts()
            features['content_type_mode'] = content_types.idxmax() if len(content_types) > 0 else 'unknown'
        else:
            features['content_type_mode'] = 'unknown'
        
        return features
    
    def _features_to_vector(self, features):
        return np.array([
            features.get('total_events', 0),
            features.get('session_duration_hours', 0),
            features.get('max_gap_hours', 0),
            features.get('long_inactive_periods', 0),
            features.get('events_per_minute', 0),
            features.get('engagement_ratio', 0.5),
            features.get('tab_switches', 0),
            features.get('quiz_fails', 0),
            features.get('video_pauses', 0),
            features.get('repeats', 0),
            features.get('content_diversity', 1),
            features.get('scroll_depth_avg', 0)
        ])
    
    def _generate_training_data(self):
        np.random.seed(42)
        n_samples = 500
        
        data = {
            'total_events': np.random.randint(5, 150, n_samples),
            'session_duration_hours': np.random.exponential(1, n_samples),
            'max_gap_hours': np.random.exponential(0.5, n_samples),
            'long_inactive_periods': np.random.randint(0, 10, n_samples),
            'events_per_minute': np.random.uniform(0.1, 3, n_samples),
            'engagement_ratio': np.random.uniform(0.2, 1, n_samples),
            'tab_switches': np.random.randint(0, 15, n_samples),
            'quiz_fails': np.random.randint(0, 8, n_samples),
            'video_pauses': np.random.randint(0, 10, n_samples),
            'repeats': np.random.randint(0, 5, n_samples),
            'content_diversity': np.random.randint(1, 15, n_samples),
            'scroll_depth_avg': np.random.uniform(0.1, 1, n_samples),
            'struggle_label': np.zeros(n_samples),
            'boredom_label': np.zeros(n_samples),
            'inactive_label': np.zeros(n_samples),
            'fast_completion_label': np.zeros(n_samples)
        }
        
        for i in range(n_samples):
            if data['tab_switches'][i] > 8 or data['quiz_fails'][i] > 4:
                data['struggle_label'][i] = 1
            
            if data['events_per_minute'][i] < 0.3 and data['session_duration_hours'][i] > 1:
                data['boredom_label'][i] = 1
            
            if data['max_gap_hours'][i] > 2:
                data['inactive_label'][i] = 1
            
            if data['session_duration_hours'][i] < 0.5 and data['total_events'][i] > 20:
                data['fast_completion_label'][i] = 1
        
        return pd.DataFrame(data)
    
    def train(self):
        df = self._generate_training_data()
        
        feature_cols = [
            'total_events', 'session_duration_hours', 'max_gap_hours',
            'long_inactive_periods', 'events_per_minute', 'engagement_ratio',
            'tab_switches', 'quiz_fails', 'video_pauses', 'repeats',
            'content_diversity', 'scroll_depth_avg'
        ]
        
        X = df[feature_cols].values
        X_scaled = self.scaler.fit_transform(X)
        
        self.anomaly_model = IsolationForest(
            n_estimators=100,
            contamination=0.15,
            random_state=42
        )
        self.anomaly_model.fit(X_scaled)
        
        self.struggle_model = LinearRegression()
        self.struggle_model.fit(X_scaled, df['struggle_label'])
        
        self.boredom_model = LinearRegression()
        self.boredom_model.fit(X_scaled, df['boredom_label'])
        
        self.is_trained = True
        return self
    
    def detect_anomaly(self, events):
        if not self.is_trained:
            self.train()
        
        features = self._extract_session_features(events)
        if features is None:
            return {'is_anomaly': False, 'anomaly_score': 0, 'alert_type': 'none'}
        
        X = self._features_to_vector(features).reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        
        is_anomaly = self.anomaly_model.predict(X_scaled)[0] == -1
        anomaly_score = abs(self.anomaly_model.score_samples(X_scaled)[0])
        
        return {
            'is_anomaly': bool(is_anomaly),
            'anomaly_score': round(float(anomaly_score), 3)
        }
    
    def detect_boredom(self, events):
        features = self._extract_session_features(events)
        if features is None:
            return {'boredom_probability': 0, 'is_bored': False, 'signals': []}
        
        X = self._features_to_vector(features).reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        
        boredom_prob = self.boredom_model.predict(X_scaled)[0]
        boredom_prob = max(0, min(1, boredom_prob))
        
        signals = []
        if features.get('events_per_minute', 1) < 0.3:
            signals.append('low_interaction_rate')
        if features.get('max_gap_hours', 0) > 1:
            signals.append('long_gaps')
        if features.get('scroll_depth_avg', 1) < 0.3:
            signals.append('low_scroll_depth')
        if features.get('content_diversity', 1) == 1 and features.get('total_events', 0) > 10:
            signals.append('no_content_exploration')
        
        return {
            'boredom_probability': round(float(boredom_prob), 3),
            'is_bored': bool(boredom_prob > self.alert_thresholds['boredom_score']),
            'signals': signals
        }
    
    def detect_inactivity(self, events):
        features = self._extract_session_features(events)
        if features is None:
            return {'inactive_hours': 0, 'is_inactive': False, 'signals': []}
        
        signals = []
        inactive_hours = features.get('max_gap_hours', 0)
        
        if features.get('long_inactive_periods', 0) > 2:
            signals.append('multiple_long_gaps')
        if inactive_hours > self.alert_thresholds['inactive_hours']:
            signals.append('extended_inactivity')
        
        return {
            'inactive_hours': round(inactive_hours, 2),
            'is_inactive': inactive_hours > self.alert_thresholds['inactive_hours'],
            'long_inactive_periods': features.get('long_inactive_periods', 0),
            'signals': signals
        }
    
    def detect_struggle(self, events):
        features = self._extract_session_features(events)
        if features is None:
            return {'struggle_probability': 0, 'is_struggling': False, 'signals': []}
        
        X = self._features_to_vector(features).reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        
        struggle_prob = self.struggle_model.predict(X_scaled)[0]
        struggle_prob = max(0, min(1, struggle_prob))
        
        signals = []
        if features.get('tab_switches', 0) > 5:
            signals.append('excessive_tab_switching')
        if features.get('quiz_fails', 0) > 3:
            signals.append('multiple_quiz_failures')
        if features.get('video_pauses', 0) > 5:
            signals.append('excessive_video_pausing')
        if features.get('repeats', 0) > 2:
            signals.append('content_repetition')
        if features.get('events_per_minute', 1) > 2 and features.get('quiz_fails', 0) > 2:
            signals.append('rushed_with_failures')
        
        return {
            'struggle_probability': round(float(struggle_prob), 3),
            'is_struggling': bool(struggle_prob > self.alert_thresholds['struggle_score']),
            'signals': signals
        }
    
    def detect_fast_completion(self, events):
        features = self._extract_session_features(events)
        if features is None:
            return {'is_suspicious': False, 'completion_speed_hours': 0, 'signals': []}
        
        session_hours = features.get('session_duration_hours', 0)
        total_events = features.get('total_events', 0)
        
        signals = []
        is_suspicious = False
        
        if session_hours < self.alert_thresholds['fast_completion_hours'] and total_events > 15:
            signals.append('completion_too_fast')
            is_suspicious = True
        
        if session_hours < 0.1 and total_events > 30:
            signals.append('impossibly_fast')
            is_suspicious = True
        
        if features.get('scroll_depth_avg', 0) < 0.2 and total_events > 10:
            signals.append('no_meaningful_interaction')
            is_suspicious = True
        
        engagement_ratio = features.get('engagement_ratio', 1)
        if engagement_ratio < 0.3 and total_events > 20:
            signals.append('low_engagement_high_events')
            is_suspicious = True
        
        return {
            'is_suspicious': is_suspicious,
            'completion_speed_hours': round(session_hours, 2),
            'total_events': total_events,
            'signals': signals
        }
    
    def analyze_session(self, events, user_id=None):
        if user_id:
            self.session_windows[user_id] = events
        
        anomaly = self.detect_anomaly(events)
        boredom = self.detect_boredom(events)
        inactivity = self.detect_inactivity(events)
        struggle = self.detect_struggle(events)
        fast_completion = self.detect_fast_completion(events)
        
        alerts = []
        
        if anomaly['is_anomaly']:
            alerts.append({
                'type': 'anomaly',
                'severity': 'high',
                'message': 'Unusual learning pattern detected'
            })
        
        if boredom['is_bored']:
            alerts.append({
                'type': 'boredom',
                'severity': 'medium',
                'message': 'User appears bored or disengaged'
            })
        
        if inactivity['is_inactive']:
            alerts.append({
                'type': 'inactivity',
                'severity': 'high',
                'message': f"User inactive for {inactivity['inactive_hours']} hours"
            })
        
        if struggle['is_struggling']:
            alerts.append({
                'type': 'struggle',
                'severity': 'high',
                'message': 'User is struggling with content'
            })
        
        if fast_completion['is_suspicious']:
            alerts.append({
                'type': 'fast_completion',
                'severity': 'high',
                'message': 'Suspiciously fast completion detected'
            })
        
        overall_status = 'normal'
        if len(alerts) >= 3:
            overall_status = 'critical'
        elif len(alerts) == 2:
            overall_status = 'warning'
        elif len(alerts) == 1:
            overall_status = 'attention'
        
        return {
            'overall_status': overall_status,
            'alerts': alerts,
            'analysis': {
                'anomaly': anomaly,
                'boredom': boredom,
                'inactivity': inactivity,
                'struggle': struggle,
                'fast_completion': fast_completion
            }
        }
    
    def get_recommendations(self, events):
        analysis = self.analyze_session(events)
        recommendations = []
        
        for alert in analysis['alerts']:
            if alert['type'] == 'boredom':
                recommendations.append({
                    'action': 'suggest_interactive_content',
                    'reason': 'User shows boredom signals',
                    'content_type': 'quiz'
                })
            elif alert['type'] == 'struggle':
                recommendations.append({
                    'action': 'provide_hint_or_help',
                    'reason': 'User is struggling with material',
                    'content_type': 'tutorial'
                })
            elif alert['type'] == 'inactivity':
                recommendations.append({
                    'action': 'send_reminder',
                    'reason': 'User has been inactive',
                    'content_type': 'notification'
                })
            elif alert['type'] == 'fast_completion':
                recommendations.append({
                    'action': 'verify_learning',
                    'reason': 'Suspicious completion pattern',
                    'content_type': 'assessment'
                })
        
        if not recommendations:
            recommendations.append({
                'action': 'continue',
                'reason': 'Normal learning pattern',
                'content_type': 'current'
            })
        
        return recommendations
    
    def save(self, path=None):
        path = path or os.path.join(self.models_dir, 'learner_monitor.joblib')
        joblib.dump({
            'anomaly_model': self.anomaly_model,
            'struggle_model': self.struggle_model,
            'boredom_model': self.boredom_model,
            'scaler': self.scaler,
            'is_trained': self.is_trained,
            'alert_thresholds': self.alert_thresholds
        }, path)
    
    def load(self, path=None):
        path = path or os.path.join(self.models_dir, 'learner_monitor.joblib')
        if os.path.exists(path):
            data = joblib.load(path)
            self.anomaly_model = data['anomaly_model']
            self.struggle_model = data['struggle_model']
            self.boredom_model = data['boredom_model']
            self.scaler = data['scaler']
            self.is_trained = data['is_trained']
            self.alert_thresholds = data.get('alert_thresholds', self.alert_thresholds)
        return self


monitor = LearnerMonitor()
try:
    monitor.load()
except:
    pass
