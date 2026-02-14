import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os
from collections import defaultdict
from datetime import datetime


class AdaptiveRecommender:
    def __init__(self):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.state_encoder = StandardScaler()
        self.action_model = None
        self.reward_model = None
        self.scaler = StandardScaler()
        
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        self.epsilon_decay = 0.99
        self.min_epsilon = 0.01
        
        self.state_history = defaultdict(list)
        self.reward_history = defaultdict(list)
        
        self.models_dir = 'models'
        os.makedirs(self.models_dir, exist_ok=True)
        
        self.action_space = [
            'recommend_same_difficulty',
            'recommend_harder',
            'recommend_easier',
            'recommend_different_topic',
            'recommend_interactive',
            'recommend_video',
            'recommend_reading',
            'recommend_quiz'
        ]
        
        self.feature_weights = {
            'engagement': 0.3,
            'completion': 0.25,
            'performance': 0.25,
            'satisfaction': 0.2
        }
    
    def _get_state_key(self, learner_state):
        engagement_bucket = int(learner_state.get('engagement_score', 50) / 20)
        performance_bucket = int(learner_state.get('performance_score', 50) / 20)
        completion_bucket = int(learner_state.get('completion_rate', 50) / 20)
        streak_bucket = int(min(learner_state.get('streak_days', 0), 5) / 2)
        
        return f"s_{engagement_bucket}_{performance_bucket}_{completion_bucket}_{streak_bucket}"
    
    def _get_action_index(self, action):
        return self.action_space.index(action) if action in self.action_space else 0
    
    def _select_action(self, state_key, explore=True):
        if explore and np.random.random() < self.epsilon:
            return np.random.choice(self.action_space)
        
        q_values = [self.q_table[state_key][action] for action in self.action_space]
        max_q = max(q_values)
        
        if max_q == 0:
            return np.random.choice(self.action_space)
        
        best_actions = [a for a, q in zip(self.action_space, q_values) if q == max_q]
        return np.random.choice(best_actions)
    
    def _calculate_reward(self, feedback):
        reward = 0.0
        
        if 'engagement_delta' in feedback:
            reward += self.feature_weights['engagement'] * feedback['engagement_delta']
        
        if 'completion' in feedback:
            reward += self.feature_weights['completion'] * (1 if feedback['completion'] else -0.5)
        
        if 'performance_delta' in feedback:
            reward += self.feature_weights['performance'] * feedback['performance_delta']
        
        if 'satisfaction' in feedback:
            reward += self.feature_weights['satisfaction'] * (feedback['satisfaction'] - 0.5) * 2
        
        if 'skip' in feedback and feedback['skip']:
            reward -= 0.3
        
        if 'negative_feedback' in feedback and feedback['negative_feedback']:
            reward -= 0.5
        
        return np.clip(reward, -1, 1)
    
    def _update_q_value(self, state_key, action, reward, next_state_key):
        current_q = self.q_table[state_key][action]
        
        next_q_values = [self.q_table[next_state_key][a] for a in self.action_space]
        max_next_q = max(next_q_values) if next_q_values else 0
        
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state_key][action] = new_q
    
    def get_recommendation(self, learner_state, available_courses):
        state_key = self._get_state_key(learner_state)
        action = self._select_action(state_key)
        
        recommended = []
        
        if action == 'recommend_harder':
            recommended = [c for c in available_courses if c.get('nsqf_level', 0) > learner_state.get('current_level', 1)]
        elif action == 'recommend_easier':
            recommended = [c for c in available_courses if c.get('nsqf_level', 0) < learner_state.get('current_level', 1)]
        elif action == 'recommend_same_difficulty':
            recommended = [c for c in available_courses if c.get('nsqf_level', 0) == learner_state.get('current_level', 1)]
        elif action == 'recommend_different_topic':
            recommended = available_courses[:5]
        elif action == 'recommend_interactive':
            recommended = [c for c in available_courses if 'interactive' in c.get('keywords', '').lower()]
        elif action == 'recommend_video':
            recommended = [c for c in available_courses if 'video' in c.get('keywords', '').lower()]
        elif action == 'recommend_reading':
            recommended = [c for c in available_courses if 'reading' in c.get('keywords', '').lower()]
        elif action == 'recommend_quiz':
            recommended = [c for c in available_courses if 'quiz' in c.get('keywords', '').lower()]
        
        if not recommended:
            recommended = available_courses[:5]
        
        return {
            'action_taken': action,
            'state': state_key,
            'recommended_courses': recommended[:5],
            'exploration': self.epsilon > self.min_epsilon
        }
    
    def update(self, learner_state, action, feedback):
        state_key = self._get_state_key(learner_state)
        
        reward = self._calculate_reward(feedback)
        
        new_engagement = learner_state.get('engagement_score', 50)
        new_performance = learner_state.get('performance_score', 50)
        new_completion = learner_state.get('completion_rate', 50)
        
        new_state = {
            'engagement_score': new_engagement,
            'performance_score': new_performance,
            'completion_rate': new_completion,
            'current_level': learner_state.get('current_level', 1),
            'streak_days': learner_state.get('streak_days', 0)
        }
        next_state_key = self._get_state_key(new_state)
        
        self._update_q_value(state_key, action, reward, next_state_key)
        
        self.state_history[state_key].append({
            'action': action,
            'reward': reward,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        self.reward_history[state_key].append(reward)
        
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        
        return {'reward': reward, 'epsilon': self.epsilon}
    
    def get_state_value(self, learner_state):
        state_key = self._get_state_key(learner_state)
        q_values = [self.q_table[state_key][action] for action in self.action_space]
        
        return {
            'state_key': state_key,
            'q_values': dict(zip(self.action_space, [round(q, 3) for q in q_values])),
            'best_action': self.action_space[np.argmax(q_values)] if any(q_values) else 'explore',
            'epsilon': self.epsilon
        }
    
    def get_policy(self):
        policy = {}
        for state_key in self.q_table:
            q_values = [self.q_table[state_key][action] for action in self.action_space]
            best_idx = np.argmax(q_values)
            policy[state_key] = {
                'action': self.action_space[best_idx],
                'q_value': q_values[best_idx]
            }
        return policy
    
    def get_stats(self):
        total_updates = sum(len(v) for v in self.state_history.values())
        avg_reward = np.mean([np.mean(v) for v in self.reward_history.values()]) if self.reward_history else 0
        
        return {
            'states_visited': len(self.q_table),
            'total_updates': total_updates,
            'average_reward': round(avg_reward, 3),
            'epsilon': round(self.epsilon, 3),
            'q_table_size': sum(len(v) for v in self.q_table.values())
        }
    
    def save(self, path=None):
        path = path or os.path.join(self.models_dir, 'adaptive_recommender.joblib')
        joblib.dump({
            'q_table': dict(self.q_table),
            'epsilon': self.epsilon,
            'alpha': self.alpha,
            'gamma': self.gamma,
            'feature_weights': self.feature_weights
        }, path)
    
    def load(self, path=None):
        path = path or os.path.join(self.models_dir, 'adaptive_recommender.joblib')
        if os.path.exists(path):
            data = joblib.load(path)
            self.q_table = defaultdict(lambda: defaultdict(float), data['q_table'])
            self.epsilon = data.get('epsilon', 0.1)
            self.alpha = data.get('alpha', 0.1)
            self.gamma = data.get('gamma', 0.9)
            self.feature_weights = data.get('feature_weights', self.feature_weights)
        return self


recommender = AdaptiveRecommender()
try:
    recommender.load()
except:
    pass
