import { authService } from './auth';

const AI_ENGINE_URL = process.env.NEXT_PUBLIC_AI_ENGINE_URL || 'http://localhost:9000';
const AI_COMPANION_URL = process.env.NEXT_PUBLIC_AI_COMPANION_URL || 'http://localhost:9001';
const CORE_API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Course {
    course_id: string;
    title: string;
    provider: string;
    duration_months: number;
    nsqf_level: number;
    match_probability: number;
    skills: string;
}

export interface UserProfile {
    id: number;
    email: string;
    name?: string;
    language?: string;
    education?: string;
    field_of_study?: string;
    skills?: string[];
    interests?: string[];
    learning_goals?: string[];
    target_roles?: string;
    learning_types?: string[];
    video_format?: string;
    learning_style?: string;
    instructor_style?: string;
    course_structure?: string;
    theory_practice_ratio?: string;
    math_intensity?: string;
    learning_environment?: string[];
    internet_situation?: string[];
    collaborative_learning?: string;
    comfortable_subjects?: string[];
    familiar_with?: string[];
    certifications?: string;
    resume_url?: string;
    preferred_nsqf_level?: number;
    region?: string;
    career_goal?: string;
    progress?: number;
    courses_completed?: number;
    skills_gained?: number;
    weeks_remaining?: number;
}

export interface UserStats {
    progress: number;
    courses_completed: number;
    skills_gained: number;
    weeks_remaining: number;
    current_streak: number;
    engagement_score: number;
    dropout_risk: number;
}

export interface OnboardingData {
    fullName?: string;
    contact?: string;
    education?: string;
    fieldOfStudy?: string;
    comfortableSubjects?: string[];
    skills?: string[];
    interests?: string[];
    learningGoals?: string[];
    learningTypes?: string[];
    videoFormat?: string;
    learningStyle?: string;
    instructorStyle?: string;
    courseStructure?: string;
    theoryPracticeRatio?: string;
    mathIntensity?: string;
    learningEnvironment?: string[];
    internetSituation?: string[];
    collaborativeLearning?: string;
    familiarWith?: string[];
    certifications?: string;
    resumeUrl?: string;
    targetRoles?: string;
    preferredLanguage?: string;
    region?: string;
    careerGoal?: string;
}

function getAuthHeaders(): HeadersInit {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('auth_token') || localStorage.getItem('token')}`
    };
}

export const apiService = {
    async getUserProfile(userId: number): Promise<UserProfile | null> {
        try {
            const response = await fetch(`${CORE_API_URL}/users/${userId}`, {
                headers: getAuthHeaders()
            });
            if (!response.ok) throw new Error('Failed to fetch user profile');
            return await response.json();
        } catch (error) {
            console.error('Error fetching user profile:', error);
            return null;
        }
    },

    async saveOnboarding(userId: number, data: OnboardingData): Promise<UserProfile | null> {
        try {
            const response = await fetch(`${CORE_API_URL}/users/${userId}/onboarding`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to save onboarding data');
            return await response.json();
        } catch (error) {
            console.error('Error saving onboarding data:', error);
            return null;
        }
    },

    async getUserStats(userId: number): Promise<UserStats | null> {
        try {
            const response = await fetch(`${CORE_API_URL}/users/${userId}/stats`, {
                headers: getAuthHeaders()
            });
            if (!response.ok) throw new Error('Failed to fetch user stats');
            return await response.json();
        } catch (error) {
            console.error('Error fetching user stats:', error);
            return null;
        }
    },

    async updateUserProfile(userId: number, data: Partial<UserProfile>): Promise<UserProfile | null> {
        try {
            const response = await fetch(`${CORE_API_URL}/users/${userId}`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to update user profile');
            return await response.json();
        } catch (error) {
            console.error('Error updating user profile:', error);
            return null;
        }
    },

    async getRecommendedCourses(profile: any): Promise<Course[]> {
        try {
            const response = await fetch(`${AI_ENGINE_URL}/match/learner`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token') || localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    skills: profile.skills || [],
                    interests: profile.interests || [],
                    career_goal: profile.career_goal || profile.interests?.[0] || '',
                    experience_years: profile.experience_years || 0,
                    preferred_nsqf_level: profile.preferred_nsqf_level || 4,
                    region: profile.region || '',
                    preferred_language: profile.preferred_language || 'en',
                    top_k: 10
                })
            });

            if (!response.ok) throw new Error('Failed to fetch recommendations');

            const data = await response.json();
            return data.map((item: any) => ({
                course_id: item.course_id,
                title: item.title,
                provider: item.provider || 'NSDC',
                duration_months: item.duration_months,
                nsqf_level: item.nsqf_level,
                match_probability: Math.round(item.match_probability * 100),
                skills: item.skills
            }));
        } catch (error) {
            console.error('Error fetching recommendations:', error);
            return [];
        }
    },

    async getDashboardStats(userId?: number) {
        if (userId) {
            const stats = await this.getUserStats(userId);
            if (stats) {
                return {
                    progress: stats.progress,
                    coursesCompleted: stats.courses_completed,
                    skillsGained: stats.skills_gained,
                    weeksRemaining: stats.weeks_remaining,
                    currentStreak: stats.current_streak,
                    engagementScore: stats.engagement_score,
                    dropoutRisk: stats.dropout_risk
                };
            }
        }
        return {
            progress: 0,
            coursesCompleted: 0,
            skillsGained: 0,
            weeksRemaining: 0,
            currentStreak: 0,
            engagementScore: 0,
            dropoutRisk: 0
        };
    },

    async analyzeBehavior(events: any[]) {
        try {
            const response = await fetch(`${AI_ENGINE_URL}/behavior/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ events })
            });
            if (!response.ok) throw new Error('Failed to analyze behavior');
            return await response.json();
        } catch (error) {
            console.error('Error analyzing behavior:', error);
            return null;
        }
    },

    async getBehaviorEngagement(events: any[]) {
        try {
            const response = await fetch(`${AI_ENGINE_URL}/behavior/engagement`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ events })
            });
            if (!response.ok) throw new Error('Failed to predict engagement');
            return await response.json();
        } catch (error) {
            console.error('Error predicting engagement:', error);
            return null;
        }
    },

    async getDropoutRisk(events: any[]) {
        try {
            const response = await fetch(`${AI_ENGINE_URL}/behavior/dropout`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ events })
            });
            if (!response.ok) throw new Error('Failed to predict dropout');
            return await response.json();
        } catch (error) {
            console.error('Error predicting dropout:', error);
            return null;
        }
    },

    async getLearningStyle(events: any[]) {
        try {
            const response = await fetch(`${AI_ENGINE_URL}/learning-style/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ events })
            });
            if (!response.ok) throw new Error('Failed to predict learning style');
            return await response.json();
        } catch (error) {
            console.error('Error predicting learning style:', error);
            return null;
        }
    }
};
