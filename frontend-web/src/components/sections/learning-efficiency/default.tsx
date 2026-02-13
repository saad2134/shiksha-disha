'use client';

import { useEffect, useRef, useState } from 'react';
import { cn } from '@/lib/utils';
import { Section } from '@/components/ui/section';
import { Search, Brain, Target, Zap, CheckCircle, Clock, TrendingUp, Sparkles, BookOpen, Award, ChevronDown } from 'lucide-react';

interface ScrollProgressState {
  progress: number;
  stage: 'IDLE' | 'SEARCHING' | 'LEARNING_BEHAVIOR' | 'PERSONALISING' | 'OPTIMISED';
}

const STAGE_LABELS = {
  IDLE: 'Searching for a course...',
  SEARCHING: 'Initial search - Low precision',
  LEARNING_BEHAVIOR: 'System analyzing behavior...',
  PERSONALISING: 'Personalized results appearing',
  OPTIMISED: 'Optimized learning outcome!',
};

const STAGE_MESSAGES = {
  IDLE: 'Start scrolling to see how our AI learns from you',
  SEARCHING: 'Many courses appear with mixed relevance',
  LEARNING_BEHAVIOR: 'AI observes your patterns and preferences',
  PERSONALISING: 'Results refine based on your behavior',
  OPTIMISED: 'Smarter search → Faster learning → Better outcomes',
};

const COURSE_CARDS = [
  { id: 1, title: 'Python Basics', relevance: 0.2 },
  { id: 2, title: 'Web Dev', relevance: 0.3 },
  { id: 3, title: 'Data Science', relevance: 0.4 },
  { id: 4, title: 'Machine Learning', relevance: 0.5 },
  { id: 5, title: 'Cloud Computing', relevance: 0.3 },
  { id: 6, title: 'React JS', relevance: 0.6 },
  { id: 7, title: 'AI Fundamentals', relevance: 0.7 },
  { id: 8, title: 'Your Perfect Match', relevance: 1, highlighted: true },
];

const PERSONALIZED_COURSES = [
  { id: 1, title: 'Advanced React Patterns', match: 98, path: 'Frontend' },
  { id: 2, title: 'TypeScript Mastery', match: 95, path: 'Frontend' },
  { id: 3, title: 'Next.js Full Stack', match: 92, path: 'Frontend' },
];

const LEARNING_PATH = [
  { week: 1, title: 'React Fundamentals', progress: 100 },
  { week: 2, title: 'State Management', progress: 85 },
  { week: 3, title: 'Advanced Patterns', progress: 40, current: true },
  { week: 4, title: 'Testing & Deployment', progress: 0, locked: true },
];

export default function LearningEfficiency() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [state, setState] = useState<ScrollProgressState>({
    progress: 0,
    stage: 'IDLE',
  });

  useEffect(() => {
    const handleScroll = () => {
      if (!containerRef.current) return;
      
      const rect = containerRef.current.getBoundingClientRect();
      const windowHeight = window.innerHeight;
      const sectionTop = rect.top;
      const sectionHeight = rect.height;
      
      const scrolled = windowHeight - sectionTop;
      const totalScroll = windowHeight + sectionHeight;
      const progress = Math.max(0, Math.min(1, scrolled / totalScroll));
      
      let stage: ScrollProgressState['stage'];
      if (progress < 0.1) {
        stage = 'IDLE';
      } else if (progress < 0.3) {
        stage = 'SEARCHING';
      } else if (progress < 0.55) {
        stage = 'LEARNING_BEHAVIOR';
      } else if (progress < 0.8) {
        stage = 'PERSONALISING';
      } else {
        stage = 'OPTIMISED';
      }
      
      setState({ progress, stage });
    };
    
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const getRelevanceScore = () => {
    switch (state.stage) {
      case 'IDLE': return 0;
      case 'SEARCHING': return Math.round(20 + state.progress * 80);
      case 'LEARNING_BEHAVIOR': return Math.round(35 + (state.progress - 0.3) * 200);
      case 'PERSONALISING': return Math.round(60 + (state.progress - 0.55) * 160);
      case 'OPTIMISED': return Math.round(92 + (state.progress - 0.8) * 32);
    }
  };

  const getTimeToFind = () => {
    switch (state.stage) {
      case 'IDLE': return '--';
      case 'SEARCHING': return Math.round(45 - state.progress * 20) + 's';
      case 'LEARNING_BEHAVIOR': return Math.round(25 - (state.progress - 0.3) * 60) + 's';
      case 'PERSONALISING': return Math.round(12 - (state.progress - 0.55) * 30) + 's';
      case 'OPTIMISED': return Math.round(3 + (0.8 - state.progress) * 12) + 's';
    }
  };

  const getEfficiency = () => {
    return Math.round(getRelevanceScore() * 0.85);
  };

  const getTimeSaved = () => {
    switch (state.stage) {
      case 'IDLE': return 0;
      case 'SEARCHING': return Math.round(state.progress * 20);
      case 'LEARNING_BEHAVIOR': return Math.round(20 + (state.progress - 0.3) * 80);
      case 'PERSONALISING': return Math.round(40 + (state.progress - 0.55) * 120);
      case 'OPTIMISED': return Math.round(70 + (state.progress - 0.8) * 80);
    }
  };

  const getIntelligenceLevel = () => {
    switch (state.stage) {
      case 'IDLE': return 0;
      case 'SEARCHING': return 10;
      case 'LEARNING_BEHAVIOR': return Math.round(10 + (state.progress - 0.3) * 120);
      case 'PERSONALISING': return Math.round(40 + (state.progress - 0.55) * 100);
      case 'OPTIMISED': return Math.round(90 + (state.progress - 0.8) * 40);
    }
  };

  const showInitialSearch = state.stage !== 'IDLE';
  const showAnalysis = state.stage === 'LEARNING_BEHAVIOR' || state.stage === 'PERSONALISING' || state.stage === 'OPTIMISED';
  const showPersonalized = state.stage === 'PERSONALISING' || state.stage === 'OPTIMISED';
  const showOptimized = state.stage === 'OPTIMISED';

  return (
    <Section className="relative bg-background">
      <div 
        ref={containerRef}
        className="sticky top-0 min-h-screen overflow-hidden"
      >
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background/99 to-background" />
        
        <div className="relative z-10 h-full flex flex-col py-8 px-4 md:px-6">
          <div className="flex-1 flex items-center justify-center">
            <div className="w-full max-w-5xl grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className={cn(
                    "px-3 py-1.5 rounded-full text-sm font-medium transition-all duration-500",
                    state.stage === 'IDLE' && "bg-muted text-muted-foreground",
                    state.stage === 'SEARCHING' && "bg-amber-500/20 text-amber-600 dark:text-amber-400",
                    state.stage === 'LEARNING_BEHAVIOR' && "bg-blue-500/20 text-blue-600 dark:text-blue-400",
                    state.stage === 'PERSONALISING' && "bg-purple-500/20 text-purple-600 dark:text-purple-400",
                    state.stage === 'OPTIMISED' && "bg-green-500/20 text-green-600 dark:text-green-400"
                  )}>
                    {state.stage === 'IDLE' && <Search className="w-4 h-4 inline-block mr-2" />}
                    {state.stage === 'SEARCHING' && <Search className="w-4 h-4 inline-block mr-2" />}
                    {state.stage === 'LEARNING_BEHAVIOR' && <Brain className="w-4 h-4 inline-block mr-2" />}
                    {state.stage === 'PERSONALISING' && <Target className="w-4 h-4 inline-block mr-2" />}
                    {state.stage === 'OPTIMISED' && <Zap className="w-4 h-4 inline-block mr-2" />}
                    {STAGE_LABELS[state.stage]}
                  </div>
                </div>
                
                <div className={cn(
                  "p-4 rounded-xl bg-card border transition-all duration-500",
                  showOptimized ? "border-green-500/30 shadow-lg shadow-green-500/10" : "border-border"
                )}>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-9 bg-muted rounded-lg flex items-center px-3 gap-2">
                        <Search className="w-4 h-4 text-muted-foreground" />
                        <span className="text-muted-foreground text-sm">Search courses...</span>
                        <span className="ml-auto animate-pulse">|</span>
                      </div>
                    </div>
                    
                    <p className="text-sm text-muted-foreground font-medium">{STAGE_MESSAGES[state.stage]}</p>
                    
                    {showInitialSearch && (
                      <div className={cn(
                        "grid grid-cols-2 gap-2 transition-all duration-500",
                        showPersonalized ? "opacity-0 hidden" : "opacity-100"
                      )}>
                        {COURSE_CARDS.slice(0, showAnalysis ? 8 : 6).map((course) => (
                          <div 
                            key={course.id}
                            className={cn(
                              "p-2 rounded-lg text-xs border transition-all duration-500",
                              course.relevance > 0.6 ? "bg-green-500/10 border-green-500/30" :
                              course.relevance > 0.4 ? "bg-amber-500/10 border-amber-500/30" :
                              "bg-red-500/10 border-red-500/30"
                            )}
                            style={{
                              opacity: showAnalysis ? Math.min(1, course.relevance + 0.3) : 0.7,
                            }}
                          >
                            <span className="font-medium">{course.title}</span>
                          </div>
                        ))}
                      </div>
                    )}
                    
                    {showPersonalized && (
                      <div className="space-y-2">
                        {PERSONALIZED_COURSES.map((course, i) => (
                          <div 
                            key={course.id}
                            className={cn(
                              "p-2.5 rounded-lg border bg-gradient-to-r transition-all duration-500",
                              course.match > 90 ? "from-green-500/20 to-transparent border-green-500/40" :
                              "from-purple-500/20 to-transparent border-purple-500/40"
                            )}
                          >
                            <div className="flex items-center justify-between">
                              <div>
                                <p className="font-medium text-sm">{course.title}</p>
                                <p className="text-xs text-muted-foreground">{course.path}</p>
                              </div>
                              <span className="text-lg font-bold text-green-500">{course.match}%</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                    
                    {showOptimized && (
                      <div className="space-y-2 pt-1">
                        <p className="text-sm font-medium flex items-center gap-2">
                          <BookOpen className="w-4 h-4 text-green-500" />
                          Your Learning Path
                        </p>
                        {LEARNING_PATH.map((item, i) => (
                          <div 
                            key={i}
                            className={cn(
                              "flex items-center gap-2 p-2 rounded-lg transition-all duration-500",
                              item.locked ? "opacity-40" : "opacity-100"
                            )}
                          >
                            <div className={cn(
                              "w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0",
                              item.progress === 100 ? "bg-green-500 text-white" :
                              item.current ? "bg-primary text-primary-foreground" :
                              "bg-muted text-muted-foreground"
                            )}>
                              {item.progress === 100 ? <CheckCircle className="w-3 h-3" /> : item.week}
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-xs font-medium truncate">{item.title}</p>
                              <div className="h-1 bg-muted rounded-full overflow-hidden mt-0.5">
                                <div 
                                  className="h-full bg-primary rounded-full transition-all duration-300"
                                  style={{ width: `${item.progress}%` }}
                                />
                              </div>
                            </div>
                            {item.current && (
                              <Sparkles className="w-3 h-3 text-primary animate-pulse shrink-0" />
                            )}
                          </div>
                        ))}
                        
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {['React Pro', 'Fast Learner'].map((badge) => (
                            <div 
                              key={badge}
                              className="flex items-center gap-1 px-2 py-0.5 bg-amber-500/20 text-amber-600 dark:text-amber-400 rounded-full text-xs"
                            >
                              <Award className="w-3 h-3" />
                              {badge}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="p-4 rounded-xl bg-card border border-border">
                  <h3 className="font-semibold text-sm mb-3 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-primary" />
                    Live Metrics
                  </h3>
                  
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-3 rounded-lg bg-muted/50">
                      <div className="flex items-center gap-1.5 mb-1">
                        <Target className="w-3 h-3 text-primary" />
                        <span className="text-xs text-muted-foreground">Relevance</span>
                      </div>
                      <div className="text-xl font-bold text-primary">{getRelevanceScore()}%</div>
                      <div className="h-1 bg-muted rounded-full overflow-hidden mt-1.5">
                        <div 
                          className="h-full bg-primary rounded-full transition-all duration-300"
                          style={{ width: `${getRelevanceScore()}%` }}
                        />
                      </div>
                    </div>
                    
                    <div className="p-3 rounded-lg bg-muted/50">
                      <div className="flex items-center gap-1.5 mb-1">
                        <Clock className="w-3 h-3 text-amber-500" />
                        <span className="text-xs text-muted-foreground">Time</span>
                      </div>
                      <div className="text-xl font-bold">{getTimeToFind()}</div>
                      <p className="text-[10px] text-muted-foreground">vs 45s avg</p>
                    </div>
                    
                    <div className="p-3 rounded-lg bg-muted/50">
                      <div className="flex items-center gap-1.5 mb-1">
                        <Zap className="w-3 h-3 text-green-500" />
                        <span className="text-xs text-muted-foreground">Saved</span>
                      </div>
                      <div className="text-xl font-bold text-green-500">+{getTimeSaved()}s</div>
                    </div>
                    
                    <div className="p-3 rounded-lg bg-muted/50">
                      <div className="flex items-center gap-1.5 mb-1">
                        <Brain className="w-3 h-3 text-purple-500" />
                        <span className="text-xs text-muted-foreground">AI Level</span>
                      </div>
                      <div className="text-xl font-bold text-purple-500">{getIntelligenceLevel()}%</div>
                    </div>
                  </div>
                </div>
                
                <div className="p-4 rounded-xl bg-card border border-border">
                  <h3 className="font-semibold text-sm mb-3 flex items-center gap-2">
                    <Zap className="w-4 h-4 text-green-500" />
                    Efficiency
                  </h3>
                  
                  <div className="relative h-20 flex items-center justify-center">
                    <svg className="w-40 h-20 -rotate-90" viewBox="0 0 100 50">
                      <path
                        d="M 10 45 A 40 40 0 0 1 90 45"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="8"
                        strokeLinecap="round"
                        className="text-muted"
                      />
                      <path
                        d="M 10 45 A 40 40 0 0 1 90 45"
                        fill="none"
                        stroke="url(#efficiencyGradient)"
                        strokeWidth="8"
                        strokeLinecap="round"
                        strokeDasharray={`${getEfficiency() * 1.26} 126`}
                        className="transition-all duration-300"
                      />
                      <defs>
                        <linearGradient id="efficiencyGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                          <stop offset="0%" stopColor="var(--primary)" />
                          <stop offset="100%" stopColor="var(--chart-5)" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-2xl font-bold">{getEfficiency()}%</span>
                    </div>
                  </div>
                </div>
                
                {showOptimized && (
                  <div className={cn(
                    "p-3 rounded-lg border text-center transition-all duration-500",
                    "bg-green-500/20 border-green-500/40"
                  )}>
                    <p className="text-sm font-semibold text-green-500 flex items-center justify-center gap-2">
                      <CheckCircle className="w-4 h-4" />
                      {STAGE_MESSAGES.OPTIMISED}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
          
          <div className="flex justify-center mt-4">
            <div className="flex flex-col items-center gap-1 animate-bounce">
              <span className="text-xs text-muted-foreground">Scroll to explore</span>
              <ChevronDown className="w-4 h-4 text-muted-foreground" />
            </div>
          </div>
        </div>
        
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-muted">
          <div 
            className="h-full bg-primary transition-all duration-150"
            style={{ width: `${state.progress * 100}%` }}
          />
        </div>
      </div>
    </Section>
  );
}
