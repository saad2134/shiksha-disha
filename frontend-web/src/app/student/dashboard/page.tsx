"use client";

import * as React from "react";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import {
    LogOut,
    BookOpen,
    Target,
    TrendingUp,
    Clock,
    MapPin,
    Star,
    ChevronRight,
    Users,
    Award,
    Briefcase,
    Calendar
} from "lucide-react";
import { siteConfig } from "@/config/site";

export default function Dashboard() {
    const router = useRouter();
    const [userData, setUserData] = React.useState({
        name: "Saad Mohammed",
        education: "Bachelor's Degree",
        careerGoal: "Software Development",
        skillLevel: "Beginner",
        progress: 25,
        learningPace: "1-2 hours/day"
    });

    const handleLogout = () => {
        router.push("/");
    };

    const recommendedCourses = [
        {
            id: 1,
            title: "Web Development Fundamentals",
            provider: "NSQF Level 4",
            duration: "6 weeks",
            level: "Beginner",
            match: 95,
            type: "course"
        },
        {
            id: 2,
            title: "Python Programming Basics",
            provider: "Skill India",
            duration: "4 weeks",
            level: "Beginner",
            match: 88,
            type: "course"
        },
        {
            id: 3,
            title: "IT Support Internship",
            provider: "Tech Solutions Ltd.",
            duration: "3 months",
            level: "Intermediate",
            match: 76,
            type: "internship"
        }
    ];

    const milestones = [
        { id: 1, title: "Profile Setup", status: "completed", description: "Basic information collected" },
        { id: 2, title: "Web Dev Fundamentals", status: "current", description: "Next recommended step" },
        { id: 3, title: "Python Certification", status: "upcoming", description: "Build programming skills" },
        { id: 4, title: "Internship", status: "upcoming", description: "Gain practical experience" },
        { id: 5, title: "Job Ready", status: "upcoming", description: "Start applying for roles" }
    ];

    const skillAreas = [
        { name: "Programming", level: 30, target: 80 },
        { name: "Web Development", level: 20, target: 85 },
        { name: "Problem Solving", level: 60, target: 90 },
        { name: "Communication", level: 70, target: 85 }
    ];

    useEffect(() => {
        document.title = `Dashboard ✦ ${siteConfig.name}`;
    }, []);

    return (
        <div className="min-h-screen bg-background p-18">
            {/* Header */}
            <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-foreground">Career GPS</h1>
                        <p className="text-muted-foreground">Your personalized learning journey</p>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="text-right">
                            <p className="font-medium text-foreground">Welcome back, {userData.name}!</p>
                            <p className="text-sm text-muted-foreground">{userData.careerGoal} Path</p>
                        </div>
                        <Button variant="outline" onClick={handleLogout} className="flex items-center gap-2">
                            <LogOut size={16} />
                            Logout
                        </Button>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                    {/* Main Content - 2/3 width */}
                    <div className="lg:col-span-2 space-y-6">
                        {/* Welcome Card */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.1 }}
                        >
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <TrendingUp className="text-primary" size={20} />
                                        Journey Progress
                                    </CardTitle>
                                    <CardDescription>
                                        Your overall progress towards becoming job-ready in {userData.careerGoal}
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-4">
                                        <div className="flex justify-between items-center">
                                            <span className="text-sm font-medium">Overall Completion</span>
                                            <span className="text-sm font-medium">{userData.progress}%</span>
                                        </div>
                                        <Progress value={userData.progress} className="h-3" />
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                                            <div className="text-center p-4 border rounded-lg">
                                                <div className="text-2xl font-bold text-primary">2</div>
                                                <div className="text-sm text-muted-foreground">Courses Completed</div>
                                            </div>
                                            <div className="text-center p-4 border rounded-lg">
                                                <div className="text-2xl font-bold text-primary">5</div>
                                                <div className="text-sm text-muted-foreground">Skills Gained</div>
                                            </div>
                                            <div className="text-center p-4 border rounded-lg">
                                                <div className="text-2xl font-bold text-primary">12</div>
                                                <div className="text-sm text-muted-foreground">Weeks Remaining</div>
                                            </div>
                                            <div className="text-center p-4 border rounded-lg">
                                                <div className="text-2xl font-bold text-primary">85%</div>
                                                <div className="text-sm text-muted-foreground">Path Match</div>
                                            </div>
                                        </div>

                                        {/* Add the View Full Path button here */}
                                        <div className="mt-6">
                                            <Button
                                                onClick={() => router.push('/student/career_map')}
                                                className="w-full flex items-center gap-2"
                                            >
                                                <MapPin size={16} />
                                                View Full Career Path
                                            </Button>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>

                        {/* Progress Overview */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.1 }}
                        >
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <TrendingUp className="text-primary" size={20} />
                                        Journey Progress
                                    </CardTitle>
                                    <CardDescription>
                                        Your overall progress towards becoming job-ready in {userData.careerGoal}
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-4">
                                        <div className="flex justify-between items-center">
                                            <span className="text-sm font-medium">Overall Completion</span>
                                            <span className="text-sm font-medium">{userData.progress}%</span>
                                        </div>
                                        <Progress value={userData.progress} className="h-3" />
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                                            <div className="text-center p-4 border rounded-lg">
                                                <div className="text-2xl font-bold text-primary">2</div>
                                                <div className="text-sm text-muted-foreground">Courses Completed</div>
                                            </div>
                                            <div className="text-center p-4 border rounded-lg">
                                                <div className="text-2xl font-bold text-primary">5</div>
                                                <div className="text-sm text-muted-foreground">Skills Gained</div>
                                            </div>
                                            <div className="text-center p-4 border rounded-lg">
                                                <div className="text-2xl font-bold text-primary">12</div>
                                                <div className="text-sm text-muted-foreground">Weeks Remaining</div>
                                            </div>
                                            <div className="text-center p-4 border rounded-lg">
                                                <div className="text-2xl font-bold text-primary">85%</div>
                                                <div className="text-sm text-muted-foreground">Path Match</div>
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>

                        {/* Recommended Next Steps */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.2 }}
                        >
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Star className="text-primary" size={20} />
                                        Recommended Next Steps
                                    </CardTitle>
                                    <CardDescription>
                                        AI-suggested learning opportunities based on your profile and goals
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-4">
                                        {recommendedCourses.map((course, index) => (
                                            <motion.div
                                                key={course.id}
                                                initial={{ opacity: 0, x: -20 }}
                                                animate={{ opacity: 1, x: 0 }}
                                                transition={{ duration: 0.5, delay: 0.1 * index }}
                                            >
                                                <Card className="hover:shadow-md transition-shadow cursor-pointer">
                                                    <CardContent className="p-4">
                                                        <div className="flex items-start justify-between">
                                                            <div className="flex-1">
                                                                <div className="flex items-center gap-3 mb-2">
                                                                    <h3 className="font-semibold text-foreground">{course.title}</h3>
                                                                    <Badge variant={course.type === "internship" ? "default" : "secondary"}>
                                                                        {course.type}
                                                                    </Badge>
                                                                </div>
                                                                <p className="text-sm text-muted-foreground mb-2">{course.provider}</p>
                                                                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                                                    <div className="flex items-center gap-1">
                                                                        <Clock size={14} />
                                                                        <span>{course.duration}</span>
                                                                    </div>
                                                                    <div className="flex items-center gap-1">
                                                                        <Award size={14} />
                                                                        <span>{course.level}</span>
                                                                    </div>
                                                                    <div className="flex items-center gap-1">
                                                                        <TrendingUp size={14} />
                                                                        <span>{course.match}% Match</span>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <Button size="sm" className="flex items-center gap-1">
                                                                Enroll
                                                                <ChevronRight size={16} />
                                                            </Button>
                                                        </div>
                                                    </CardContent>
                                                </Card>
                                            </motion.div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>
                    </div>

                    {/* Sidebar - 1/3 width */}
                    <div className="space-y-6">
                        {/* Career Journey Map */}
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5, delay: 0.3 }}
                        >
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <MapPin className="text-primary" size={20} />
                                        Career Journey Map
                                    </CardTitle>
                                    <CardDescription>
                                        Your path from beginner to job-ready professional
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-4">
                                        {milestones.map((milestone, index) => (
                                            <div key={milestone.id} className="flex items-start gap-3">
                                                <div className={`flex flex-col items-center ${milestone.status === "completed" ? "text-primary" :
                                                    milestone.status === "current" ? "text-green-500" : "text-muted-foreground"
                                                    }`}>
                                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 ${milestone.status === "completed" ? "bg-primary border-primary text-primary-foreground" :
                                                        milestone.status === "current" ? "bg-green-500 border-green-500 text-white" :
                                                            "bg-muted border-muted text-muted-foreground"
                                                        }`}>
                                                        {milestone.status === "completed" ? "✓" : index + 1}
                                                    </div>
                                                    {index < milestones.length - 1 && (
                                                        <div className={`w-0.5 h-8 ${milestone.status === "completed" ? "bg-primary" : "bg-muted"
                                                            }`} />
                                                    )}
                                                </div>
                                                <div className="flex-1 pb-4">
                                                    <h3 className={`font-medium ${milestone.status === "current" ? "text-green-600" : "text-foreground"
                                                        }`}>
                                                        {milestone.title}
                                                    </h3>
                                                    <p className="text-sm text-muted-foreground">{milestone.description}</p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>

                        {/* Skill Progress */}
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5, delay: 0.4 }}
                        >
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Award className="text-primary" size={20} />
                                        Skill Development
                                    </CardTitle>
                                    <CardDescription>
                                        Track your progress in key areas
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-4">
                                        {skillAreas.map((skill, index) => (
                                            <div key={skill.name} className="space-y-2">
                                                <div className="flex justify-between text-sm">
                                                    <span className="font-medium">{skill.name}</span>
                                                    <span className="text-muted-foreground">{skill.level}% / {skill.target}%</span>
                                                </div>
                                                <div className="space-y-1">
                                                    <Progress value={skill.level} className="h-2" />
                                                    <Progress value={skill.target} className="h-1 bg-muted" />
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>

                        {/* Quick Stats */}
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5, delay: 0.5 }}
                        >
                            <Card>
                                <CardHeader>
                                    <CardTitle className="text-lg">Market Insights</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-3">
                                    <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                                        <div>
                                            <p className="font-medium text-green-800">High Demand</p>
                                            <p className="text-sm text-green-600">Web Developers</p>
                                        </div>
                                        <TrendingUp className="text-green-600" size={20} />
                                    </div>
                                    <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                                        <div>
                                            <p className="font-medium text-blue-800">Growing Field</p>
                                            <p className="text-sm text-blue-600">AI & ML Jobs</p>
                                        </div>
                                        <Users className="text-blue-600" size={20} />
                                    </div>
                                    <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                                        <div>
                                            <p className="font-medium text-orange-800">New Opportunity</p>
                                            <p className="text-sm text-orange-600">Cloud Computing</p>
                                        </div>
                                        <Briefcase className="text-orange-600" size={20} />
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