import { authService } from './auth';

const AI_ENGINE_URL = process.env.NEXT_PUBLIC_AI_ENGINE_URL || 'http://localhost:9000';
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

export const apiService = {
    async getRecommendedCourses(profile: any): Promise<Course[]> {
        try {
            const response = await fetch(`${AI_ENGINE_URL}/match/learner`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({
                    skills: profile.skills || [],
                    experience_years: profile.experience_years || 0,
                    preferred_nsqf_level: profile.preferred_nsqf_level || 4,
                    region: profile.region || '',
                    preferred_language: profile.preferred_language || 'en',
                    top_k: 5
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

    async getDashboardStats() {
        // Placeholder for actual stats endpoint if available
        return {
            progress: 25,
            coursesCompleted: 2,
            skillsGained: 5,
            weeksRemaining: 12
        };
    }
};
