"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  BookOpen, 
  DollarSign, 
  TrendingUp, 
  Clock, 
  BarChart3, 
  Sparkles, 
  Brain,
  Target,
  Zap,
  Award,
  AlertCircle,
  ChevronRight,
  Star,
  Briefcase,
  GraduationCap,
  Timer,
  CheckCircle2
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface CourseRecommendation {
  id: string;
  title: string;
  platform: string;
  instructor: string;
  thumbnail: string;
  matchScore: number;
  learningStyleFit: {
    visual: number;
    practical: number;
    theoretical: number;
    interactive: number;
  };
  pedagogicalApproach: string;
  pace: 'Fast' | 'Moderate' | 'Relaxed';
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  contentMix: {
    video: number;
    handson: number;
    reading: number;
    quizzes: number;
  };
  technicalBreakdown?: {
    math: number;
    coding: number;
    theory: number;
    systems: number;
  };
  estimatedHours: number;
  personalizedHours: number;
  idealSessionLength: string;
  avgSalary: {
    entry: number;
    mid: number;
    senior: number;
  };
  jobDemand: {
    trend: 'High' | 'Growing' | 'Moderate' | 'Declining';
    openings: number;
    demandMultiplier?: string;
  };
  skillsGained: string[];
  projectOutcomes: string[];
  certificationValue: 'High' | 'Moderate' | 'Low';
  prerequisites: string[];
  completionRate: number;
  studentFriendly: {
    affordability: 'Free' | 'Budget' | 'Premium';
    schedule: 'Self-paced' | 'Deadline-driven';
    supportQuality: number;
  };
  insights: {
    type: 'warning' | 'tip' | 'highlight';
    message: string;
  }[];
}

const sampleCourses: CourseRecommendation[] = [
  {
    id: '1',
    title: 'Machine Learning A-Z: Hands-On Python & R In Data Science',
    platform: 'Udemy',
    instructor: 'Kirill Eremenko',
    thumbnail: '/api/placeholder/400/225',
    matchScore: 94,
    learningStyleFit: {
      visual: 85,
      practical: 95,
      theoretical: 70,
      interactive: 90
    },
    pedagogicalApproach: 'Example-driven, Bottom-up',
    pace: 'Moderate',
    difficulty: 'Beginner',
    contentMix: {
      video: 45,
      handson: 40,
      reading: 10,
      quizzes: 5
    },
    technicalBreakdown: {
      math: 35,
      coding: 45,
      theory: 15,
      systems: 5
    },
    estimatedHours: 44,
    personalizedHours: 38,
    idealSessionLength: '2-3 hour sessions',
    avgSalary: {
      entry: 85000,
      mid: 125000,
      senior: 165000
    },
    jobDemand: {
      trend: 'High',
      openings: 12500,
      demandMultiplier: '5x growth in last 2 years'
    },
    skillsGained: [
      'Supervised & Unsupervised Learning',
      'Neural Networks',
      'Model Evaluation',
      'Feature Engineering',
      'Python/R for ML'
    ],
    projectOutcomes: [
      'Customer Churn Predictor',
      'Recommendation System',
      'Image Classification Model'
    ],
    certificationValue: 'High',
    prerequisites: ['Basic Python', 'High School Math'],
    completionRate: 68,
    studentFriendly: {
      affordability: 'Budget',
      schedule: 'Self-paced',
      supportQuality: 8
    },
    insights: [
      {
        type: 'highlight',
        message: 'Perfect match for your hands-on learning style - 95% practical work'
      },
      {
        type: 'tip',
        message: 'Only 35% math - lighter than most ML courses, great for beginners'
      },
      {
        type: 'warning',
        message: 'Some Python knowledge recommended - take Python basics first if new'
      }
    ]
  },
  {
    id: '2',
    title: 'React - The Complete Guide 2024',
    platform: 'Udemy',
    instructor: 'Maximilian Schwarzmüller',
    thumbnail: '/api/placeholder/400/225',
    matchScore: 92,
    learningStyleFit: {
      visual: 80,
      practical: 90,
      theoretical: 65,
      interactive: 85
    },
    pedagogicalApproach: 'Project-based, Incremental',
    pace: 'Fast',
    difficulty: 'Beginner',
    contentMix: {
      video: 50,
      handson: 45,
      reading: 3,
      quizzes: 2
    },
    estimatedHours: 48,
    personalizedHours: 42,
    idealSessionLength: '1-2 hour sessions',
    avgSalary: {
      entry: 75000,
      mid: 110000,
      senior: 145000
    },
    jobDemand: {
      trend: 'High',
      openings: 18700,
      demandMultiplier: '3x more jobs than Angular in your area'
    },
    skillsGained: [
      'React Hooks & Components',
      'State Management (Redux)',
      'Next.js',
      'Testing & Optimization',
      'Modern JavaScript'
    ],
    projectOutcomes: [
      'Full-Stack E-commerce App',
      'Social Media Dashboard',
      'Real-time Chat Application'
    ],
    certificationValue: 'Moderate',
    prerequisites: ['HTML/CSS', 'JavaScript Basics'],
    completionRate: 72,
    studentFriendly: {
      affordability: 'Budget',
      schedule: 'Self-paced',
      supportQuality: 9
    },
    insights: [
      {
        type: 'highlight',
        message: '3x more React jobs than Angular - highest ROI for frontend development'
      },
      {
        type: 'highlight',
        message: 'Fast-paced fits your learning preference - you finish courses 15% quicker'
      },
      {
        type: 'tip',
        message: '3 portfolio-ready projects - directly hireable after completion'
      }
    ]
  },
  {
    id: '3',
    title: 'Deep Learning Specialization',
    platform: 'Coursera',
    instructor: 'Andrew Ng',
    thumbnail: '/api/placeholder/400/225',
    matchScore: 78,
    learningStyleFit: {
      visual: 70,
      practical: 60,
      theoretical: 90,
      interactive: 55
    },
    pedagogicalApproach: 'Theory-first, Top-down',
    pace: 'Moderate',
    difficulty: 'Advanced',
    contentMix: {
      video: 60,
      handson: 25,
      reading: 10,
      quizzes: 5
    },
    technicalBreakdown: {
      math: 65,
      coding: 20,
      theory: 10,
      systems: 5
    },
    estimatedHours: 120,
    personalizedHours: 145,
    idealSessionLength: '1-1.5 hour sessions',
    avgSalary: {
      entry: 95000,
      mid: 140000,
      senior: 185000
    },
    jobDemand: {
      trend: 'Growing',
      openings: 8200,
      demandMultiplier: '40% growth year-over-year'
    },
    skillsGained: [
      'Neural Network Architecture',
      'CNN & RNN',
      'Transformers',
      'Hyperparameter Tuning',
      'TensorFlow'
    ],
    projectOutcomes: [
      'Image Recognition System',
      'NLP Sentiment Analyzer',
      'Autonomous Car Vision'
    ],
    certificationValue: 'High',
    prerequisites: ['Linear Algebra', 'Calculus', 'Python', 'ML Basics'],
    completionRate: 45,
    studentFriendly: {
      affordability: 'Premium',
      schedule: 'Deadline-driven',
      supportQuality: 7
    },
    insights: [
      {
        type: 'warning',
        message: '65% math content - higher than your typical preference. Consider ML fundamentals first.'
      },
      {
        type: 'warning',
        message: 'Theory-heavy (90%) - may not match your hands-on learning style perfectly'
      },
      {
        type: 'tip',
        message: 'Industry gold standard certification - worth the challenge for career impact'
      }
    ]
  }
];

const CourseRecommendationPage: React.FC = () => {
  const [selectedCourse, setSelectedCourse] = useState<string | null>(null);

  return (
    <div className="p-6 space-y-6">
      <div className="bg-card  rounded-2xl p-8  border">
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="w-8 h-8" />
          <h1 className="text-3xl font-bold">Your Personalized Learning Path</h1>
        </div>
        <p className="text-lg ">
          Curated based on your visual-practical learning style • Project-focused approach • Career goals in Tech
        </p>
      </div>

      <div className="bg-card rounded-xl border p-6">
        <div className="flex items-center gap-2 mb-4">
          <Brain className="w-6 h-6 text-violet-500" />
          <h2 className="text-xl font-semibold">Your Learning Profile</h2>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-3 bg-violet-50 dark:bg-violet-950/30 rounded-lg">
            <div className="text-2xl font-bold text-violet-600">Visual</div>
            <div className="text-sm text-muted-foreground">Primary Style</div>
          </div>
          <div className="text-center p-3 bg-violet-50 dark:bg-violet-950/30 rounded-lg">
            <div className="text-2xl font-bold text-violet-600">Hands-On</div>
            <div className="text-sm text-muted-foreground">Learning Mode</div>
          </div>
          <div className="text-center p-3 bg-violet-50 dark:bg-violet-950/30 rounded-lg">
            <div className="text-2xl font-bold text-violet-600">Fast</div>
            <div className="text-sm text-muted-foreground">Pace Preference</div>
          </div>
          <div className="text-center p-3 bg-violet-50 dark:bg-violet-950/30 rounded-lg">
            <div className="text-2xl font-bold text-violet-600">2-3hrs</div>
            <div className="text-sm text-muted-foreground">Session Length</div>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        {sampleCourses.map((course) => (
          <CourseCard 
            key={course.id} 
            course={course} 
            isExpanded={selectedCourse === course.id}
            onToggle={() => setSelectedCourse(selectedCourse === course.id ? null : course.id)}
          />
        ))}
      </div>
    </div>
  );
};

const CourseCard: React.FC<{
  course: CourseRecommendation;
  isExpanded: boolean;
  onToggle: () => void;
}> = ({ course, isExpanded, onToggle }) => {
  return (
    <div className=" bg-gradient-to-br from-violet-600 to-indigo-600 rounded-2xl shadow-xl overflow-hidden">
      <div className="bg-gradient-to-r from-yellow-400 to-yellow-500 px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Star className="w-5 h-5 text-yellow-900 fill-yellow-900" />
          <span className="font-bold text-yellow-900 text-lg">{course.matchScore}% Match Score</span>
          <span className="text-yellow-800 text-sm">- Perfect for your learning style!</span>
        </div>
        <div className="flex items-center gap-2 bg-yellow-300 px-3 py-1 rounded-full">
          <TrendingUp className="w-4 h-4 text-yellow-900" />
          <span className="text-sm font-semibold text-yellow-900">{course.jobDemand.trend} Demand</span>
        </div>
      </div>

      <div className="p-6 text-white">
        <div className="flex gap-6 mb-6">
          <div className="flex-shrink-0">
            <img 
              src={course.thumbnail} 
              alt={course.title}
              className="w-48 h-28 object-cover rounded-lg shadow-md"
            />
          </div>
          <div className="flex-1">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="text-2xl font-bold mb-1">{course.title}</h3>
                <div className="flex items-center gap-3 text-violet-100">
                  <span className="flex items-center gap-1">
                    <GraduationCap className="w-4 h-4" />
                    {course.instructor}
                  </span>
                  <span>•</span>
                  <span>{course.platform}</span>
                  <span>•</span>
                  <span className="flex items-center gap-1">
                    <Award className="w-4 h-4" />
                    {course.difficulty}
                  </span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 mt-4">
              <div className="bg-white/10 backdrop-blur rounded-lg p-3">
                <div className="flex items-center gap-2 mb-1">
                  <DollarSign className="w-5 h-5 text-green-300" />
                  <span className="text-sm text-violet-100">Avg Salary</span>
                </div>
                <div className="text-2xl font-bold">${(course.avgSalary.entry / 1000).toFixed(0)}k-${(course.avgSalary.senior / 1000).toFixed(0)}k</div>
                <div className="text-xs text-violet-200">Entry to Senior</div>
              </div>

              <div className="bg-white/10 backdrop-blur rounded-lg p-3">
                <div className="flex items-center gap-2 mb-1">
                  <Briefcase className="w-5 h-5 text-blue-300" />
                  <span className="text-sm text-violet-100">Job Openings</span>
                </div>
                <div className="text-2xl font-bold">{(course.jobDemand.openings / 1000).toFixed(1)}k+</div>
                <div className="text-xs text-violet-200">{course.jobDemand.demandMultiplier}</div>
              </div>

              <div className="bg-white/10 backdrop-blur rounded-lg p-3">
                <div className="flex items-center gap-2 mb-1">
                  <Timer className="w-5 h-5 text-yellow-300" />
                  <span className="text-sm text-violet-100">Time to Complete</span>
                </div>
                <div className="text-2xl font-bold">{course.personalizedHours}hrs</div>
                <div className="text-xs text-violet-200">Based on your pace</div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white/10 backdrop-blur rounded-lg p-4 mb-4">
          <div className="flex items-center gap-2 mb-3">
            <Target className="w-5 h-5" />
            <span className="font-semibold">Learning Style Compatibility</span>
          </div>
          <div className="grid grid-cols-4 gap-3">
            {Object.entries(course.learningStyleFit).map(([style, score]) => (
              <div key={style}>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm capitalize text-violet-100">{style}</span>
                  <span className="text-sm font-bold">{score}%</span>
                </div>
                <div className="w-full bg-white/20 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${
                      score >= 80 ? 'bg-green-400' : score >= 60 ? 'bg-yellow-400' : 'bg-red-400'
                    }`}
                    style={{ width: `${score}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-white/10 backdrop-blur rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              <BarChart3 className="w-5 h-5" />
              <span className="font-semibold">Content Breakdown</span>
            </div>
            <div className="space-y-2">
              {Object.entries(course.contentMix).map(([type, percentage]) => (
                <div key={type} className="flex items-center justify-between">
                  <span className="text-sm capitalize text-violet-100">{type}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-24 bg-white/20 rounded-full h-2">
                      <div 
                        className="bg-violet-300 h-2 rounded-full"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                    <span className="text-sm font-semibold w-10 text-right">{percentage}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {course.technicalBreakdown && (
            <div className="bg-white/10 backdrop-blur rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <Brain className="w-5 h-5" />
                <span className="font-semibold">Technical Requirements</span>
              </div>
              <div className="space-y-2">
                {Object.entries(course.technicalBreakdown).map(([type, percentage]) => (
                  <div key={type} className="flex items-center justify-between">
                    <span className="text-sm capitalize text-violet-100">
                      {type}
                      {type === 'math' && percentage > 50 && ' ⚠️'}
                    </span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 bg-white/20 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            type === 'math' && percentage > 50 ? 'bg-orange-400' : 'bg-indigo-300'
                          }`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                      <span className="text-sm font-semibold w-10 text-right">{percentage}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="space-y-2 mb-4">
          {course.insights.map((insight, index) => (
            <div 
              key={index}
              className={`flex items-start gap-2 p-3 rounded-lg ${
                insight.type === 'warning' 
                  ? 'bg-orange-500/20 border border-orange-400/30' 
                  : insight.type === 'highlight'
                  ? 'bg-green-500/20 border border-green-400/30'
                  : 'bg-blue-500/20 border border-blue-400/30'
              }`}
            >
              {insight.type === 'warning' ? (
                <AlertCircle className="w-5 h-5 text-orange-300 flex-shrink-0 mt-0.5" />
              ) : insight.type === 'highlight' ? (
                <CheckCircle2 className="w-5 h-5 text-green-300 flex-shrink-0 mt-0.5" />
              ) : (
                <Zap className="w-5 h-5 text-blue-300 flex-shrink-0 mt-0.5" />
              )}
              <span className="text-sm">{insight.message}</span>
            </div>
          ))}
        </div>

        {isExpanded && (
          <div className="space-y-4 pt-4 border-t border-white/20">
            <div>
              <h4 className="font-semibold mb-2 flex items-center gap-2">
                <Sparkles className="w-4 h-4" />
                Skills You'll Gain
              </h4>
              <div className="flex flex-wrap gap-2">
                {course.skillsGained.map((skill, index) => (
                  <span 
                    key={index}
                    className="bg-white/20 px-3 py-1 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-semibold mb-2 flex items-center gap-2">
                <BookOpen className="w-4 h-4" />
                Portfolio Projects
              </h4>
              <ul className="space-y-1">
                {course.projectOutcomes.map((project, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm">
                    <CheckCircle2 className="w-4 h-4 text-green-300 flex-shrink-0 mt-0.5" />
                    {project}
                  </li>
                ))}
              </ul>
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div className="bg-white/10 rounded-lg p-3">
                <div className="text-sm text-violet-200 mb-1">Cost</div>
                <div className="font-semibold">{course.studentFriendly.affordability}</div>
              </div>
              <div className="bg-white/10 rounded-lg p-3">
                <div className="text-sm text-violet-200 mb-1">Schedule</div>
                <div className="font-semibold">{course.studentFriendly.schedule}</div>
              </div>
              <div className="bg-white/10 rounded-lg p-3">
                <div className="text-sm text-violet-200 mb-1">Support</div>
                <div className="font-semibold">{course.studentFriendly.supportQuality}/10</div>
              </div>
            </div>

            {course.prerequisites.length > 0 && (
              <div>
                <h4 className="font-semibold mb-2 flex items-center gap-2">
                  <AlertCircle className="w-4 h-4" />
                  Prerequisites
                </h4>
                <div className="flex flex-wrap gap-2">
                  {course.prerequisites.map((prereq, index) => (
                    <span 
                      key={index}
                      className="bg-orange-500/20 border border-orange-400/30 px-3 py-1 rounded-full text-sm"
                    >
                      {prereq}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="bg-white/10 rounded-lg p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-violet-200">Student Completion Rate</span>
                <span className="font-bold">{course.completionRate}%</span>
              </div>
              <div className="w-full bg-white/20 rounded-full h-2">
                <div 
                  className="bg-green-400 h-2 rounded-full"
                  style={{ width: `${course.completionRate}%` }}
                />
              </div>
            </div>
          </div>
        )}

        <div className="flex gap-3 mt-6">
          <button className="flex-1 bg-white text-violet-600 py-3 px-6 rounded-lg font-semibold hover:bg-violet-50 transition-colors flex items-center justify-center gap-2">
            <BookOpen className="w-5 h-5" />
            Start Learning
          </button>
          <button 
            onClick={onToggle}
            className="bg-white/20 backdrop-blur text-white py-3 px-6 rounded-lg font-semibold hover:bg-white/30 transition-colors flex items-center gap-2"
          >
            {isExpanded ? 'Show Less' : 'View Details'}
            <ChevronRight className={`w-5 h-5 transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default CourseRecommendationPage;
