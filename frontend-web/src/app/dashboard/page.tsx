"use client";

import * as React from "react";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";
import { 
  LogOut, 
  BookOpen, 
  Target, 
  TrendingUp, 
  Clock, 
  MapPin, 
  Star, 
  ChevronRight,
  Award
} from "lucide-react";
import { siteConfig } from "@/config/site";

export default function DashboardPage() {
  const router = useRouter();
  
  const userData = {
    name: "User",
    careerGoal: "Software Development",
    progress: 0,
  };

  const handleLogout = () => {
    router.push("/auth");
  };

  useEffect(() => {
    document.title = `Dashboard ✦ ${siteConfig.name}`;
  }, []);

  const recommendedCourses = [
    {
      id: 1,
      title: "Web Development Fundamentals",
      provider: "NSQF Level 4",
      duration: "6 weeks",
      level: "Beginner",
      match: 95,
    },
    {
      id: 2,
      title: "Python Programming Basics",
      provider: "Skill India",
      duration: "4 weeks",
      level: "Beginner",
      match: 88,
    },
  ];

  return (
    <div className="min-h-screen bg-background pt-24 sm:pt-28 px-4 sm:px-6 lg:px-8 pb-12">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6 sm:mb-8">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground">Career GPS</h1>
            <p className="text-sm sm:text-base text-muted-foreground">Your personalized learning journey</p>
          </div>
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4">
            <div className="text-left sm:text-right">
              <p className="font-medium text-foreground">Welcome!</p>
              <p className="text-sm text-muted-foreground">Complete your profile to get started</p>
            </div>
            <Button variant="outline" onClick={handleLogout} className="flex items-center justify-center gap-2 shrink-0">
              <LogOut size={16} />
              Logout
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="text-primary" size={20} />
                    Get Started
                  </CardTitle>
                  <CardDescription>
                    Complete your profile to receive personalized recommendations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8">
                    <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                      <BookOpen className="text-primary" size={32} />
                    </div>
                    <h3 className="text-lg font-semibold mb-2">Complete Your Profile</h3>
                    <p className="text-muted-foreground mb-4">
                      Answer a few questions to get personalized learning recommendations
                    </p>
                    <Button onClick={() => router.push("/onboarding")}>
                      Start Profile Setup
                      <ChevronRight size={16} className="ml-2" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Star className="text-primary" size={20} />
                    Recommended For You
                  </CardTitle>
                  <CardDescription>
                    Popular learning paths based on current trends
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recommendedCourses.map((course, index) => (
                      <div
                        key={course.id}
                        className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors"
                      >
                        <div>
                          <h4 className="font-semibold">{course.title}</h4>
                          <p className="text-sm text-muted-foreground">{course.provider}</p>
                          <div className="flex items-center gap-3 mt-1 text-sm text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <Clock size={14} />
                              {course.duration}
                            </span>
                            <Badge variant="secondary">{course.level}</Badge>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-lg font-bold text-primary">{course.match}%</div>
                          <div className="text-xs text-muted-foreground">Match</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>

          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Your Progress</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-4">
                    <div className="text-4xl font-bold text-primary mb-2">0%</div>
                    <p className="text-sm text-muted-foreground">Complete your profile to track progress</p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Market Insights</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-950/30 rounded-lg">
                    <div>
                      <p className="font-medium text-green-800 dark:text-green-300">High Demand</p>
                      <p className="text-sm text-green-600 dark:text-green-400">Web Developers</p>
                    </div>
                    <TrendingUp className="text-green-600" size={20} />
                  </div>
                  <div className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-950/30 rounded-lg">
                    <div>
                      <p className="font-medium text-blue-800 dark:text-blue-300">Growing Field</p>
                      <p className="text-sm text-blue-600 dark:text-blue-400">AI & ML Jobs</p>
                    </div>
                    <Award className="text-blue-600" size={20} />
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
