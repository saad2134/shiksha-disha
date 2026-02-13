"use client";

import * as React from "react";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import {
    User,
    Mail,
    Phone,
    MapPin,
    Calendar,
    Award,
    BookOpen,
    Target,
    Clock,
    Star,
    Edit,
    Settings,
    Shield,
    Bell,
    Palette,
    Users,
    Briefcase,
    GraduationCap,
    TrendingUp,
    CheckCircle,
    XCircle,
    ExternalLink
} from "lucide-react";
import { siteConfig } from "@/config/site";

const userProfile = {
    name: "Saad Mohammed",
    email: "saad.mohammed@example.com",
    phone: "+91 98765 43210",
    location: "Mumbai, Maharashtra",
    joinedDate: "January 2025",
    avatar: "SM",
    level: 8,
    points: 2450,
    rank: 42,
    streak: 12,
    
    education: {
        qualification: "Bachelor's Degree",
        field: "Computer Science",
        institution: "Mumbai University"
    },
    
    careerGoal: "Software Development",
    targetRoles: "Full Stack Developer, Backend Engineer",
    
    skills: [
        { name: "JavaScript", level: 75, certified: true },
        { name: "React", level: 65, certified: true },
        { name: "Python", level: 60, certified: false },
        { name: "Node.js", level: 55, certified: false },
        { name: "SQL", level: 50, certified: false },
    ],
    
    interests: ["Web Development", "Data Science", "AI/ML", "Cloud Computing"],
    
    learningPreferences: {
        type: "Hands-on projects",
        style: "Self-paced",
        timeCommitment: "1-2 hours/day",
    },
    
    completedCourses: 5,
    inProgressCourses: 3,
    totalHoursLearned: 48,
    certificatesEarned: 4,
    
    achievements: [
        { id: 1, title: "Fast Learner", description: "Completed 5 courses in first month", icon: "🚀", date: "Feb 2025" },
        { id: 2, title: "Code Warrior", description: "Solved 100 coding challenges", icon: "⚔️", date: "Jan 2025" },
        { id: 3, title: "Streak Master", description: "Maintained 7-day learning streak", icon: "🔥", date: "Jan 2025" },
    ],
    
    activityLog: [
        { id: 1, action: "Completed module", target: "React Fundamentals", date: "Today, 2:30 PM", type: "course" },
        { id: 2, action: "Earned badge", target: "Fast Learner", date: "Yesterday", type: "achievement" },
        { id: 3, action: "Started course", target: "Python for Data Science", date: "Feb 10, 2025", type: "course" },
        { id: 4, action: "Completed quiz", target: "JavaScript Basics", date: "Feb 8, 2025", type: "quiz" },
    ]
};

type TabType = "activity" | "achievements" | "preferences";

export default function Profile() {
    const router = useRouter();
    const [activeTab, setActiveTab] = React.useState<TabType>("activity");
    
    useEffect(() => {
        document.title = `Profile ✦ ${siteConfig.name}`;
    }, []);

    const getActivityIcon = (type: string) => {
        switch (type) {
            case "course": return BookOpen;
            case "achievement": return Award;
            case "quiz": return CheckCircle;
            default: return Clock;
        }
    };

    const tabs = [
        { id: "activity", label: "Activity", icon: Clock },
        { id: "achievements", label: "Achievements", icon: Award },
        { id: "preferences", label: "Preferences", icon: Settings },
    ] as const;

    return (
        <div className="p-4 sm:p-6 lg:p-8">
            <div className="max-w-6xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6">
                        <div>
                            <h1 className="text-2xl sm:text-3xl font-bold text-foreground">My Profile</h1>
                            <p className="text-muted-foreground">Manage your account and view your progress</p>
                        </div>
                        <Button variant="outline">
                            <Edit size={16} className="mr-2" />
                            Edit Profile
                        </Button>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5, delay: 0.1 }}
                        >
                            <Card className="h-full">
                                <CardHeader className="text-center pb-2">
                                    <div className="w-24 h-24 mx-auto rounded-full bg-violet-100 dark:bg-violet-900/30 flex items-center justify-center text-3xl font-bold text-violet-600 mb-4">
                                        {userProfile.avatar}
                                    </div>
                                    <CardTitle className="text-xl">{userProfile.name}</CardTitle>
                                    <CardDescription className="flex items-center justify-center gap-1">
                                        <Star className="w-4 h-4 text-amber-500 fill-amber-500" />
                                        <span>Level {userProfile.level} • {userProfile.points.toLocaleString()} pts</span>
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="flex justify-center gap-2">
                                        <Badge variant="outline" className="bg-violet-50 dark:bg-violet-950/30">
                                            #{userProfile.rank} Rank
                                        </Badge>
                                        <Badge variant="outline" className="bg-orange-50 dark:bg-orange-950/30">
                                            🔥 {userProfile.streak} day streak
                                        </Badge>
                                    </div>
                                    
                                    <div className="space-y-2 pt-4 border-t">
                                        <div className="flex items-center gap-3 text-sm">
                                            <Mail className="w-4 h-4 text-muted-foreground" />
                                            <span className="truncate">{userProfile.email}</span>
                                        </div>
                                        <div className="flex items-center gap-3 text-sm">
                                            <Phone className="w-4 h-4 text-muted-foreground" />
                                            <span>{userProfile.phone}</span>
                                        </div>
                                        <div className="flex items-center gap-3 text-sm">
                                            <MapPin className="w-4 h-4 text-muted-foreground" />
                                            <span>{userProfile.location}</span>
                                        </div>
                                        <div className="flex items-center gap-3 text-sm">
                                            <Calendar className="w-4 h-4 text-muted-foreground" />
                                            <span>Joined {userProfile.joinedDate}</span>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.2 }}
                            className="lg:col-span-2"
                        >
                            <Card className="h-full">
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <TrendingUp className="text-primary" size={20} />
                                        Learning Statistics
                                    </CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
                                        <div className="text-center p-4 border rounded-lg">
                                            <div className="text-2xl sm:text-3xl font-bold text-primary">{userProfile.completedCourses}</div>
                                            <div className="text-xs sm:text-sm text-muted-foreground">Completed</div>
                                        </div>
                                        <div className="text-center p-4 border rounded-lg">
                                            <div className="text-2xl sm:text-3xl font-bold text-blue-500">{userProfile.inProgressCourses}</div>
                                            <div className="text-xs sm:text-sm text-muted-foreground">In Progress</div>
                                        </div>
                                        <div className="text-center p-4 border rounded-lg">
                                            <div className="text-2xl sm:text-3xl font-bold text-green-500">{userProfile.totalHoursLearned}h</div>
                                            <div className="text-xs sm:text-sm text-muted-foreground">Hours Learned</div>
                                        </div>
                                        <div className="text-center p-4 border rounded-lg">
                                            <div className="text-2xl sm:text-3xl font-bold text-amber-500">{userProfile.certificatesEarned}</div>
                                            <div className="text-xs sm:text-sm text-muted-foreground">Certificates</div>
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <div>
                                            <h4 className="font-medium mb-2 flex items-center gap-2">
                                                <Target className="w-4 h-4 text-violet-500" />
                                                Career Goal
                                            </h4>
                                            <p className="text-sm text-muted-foreground">{userProfile.careerGoal}</p>
                                            <p className="text-sm text-muted-foreground mt-1">Target: {userProfile.targetRoles}</p>
                                        </div>
                                        
                                        <div>
                                            <h4 className="font-medium mb-2 flex items-center gap-2">
                                                <BookOpen className="w-4 h-4 text-blue-500" />
                                                Skills
                                            </h4>
                                            <div className="space-y-3">
                                                {userProfile.skills.map((skill) => (
                                                    <div key={skill.name} className="flex items-center gap-3">
                                                        <span className="text-sm w-24 truncate">{skill.name}</span>
                                                        <Progress value={skill.level} className="flex-1 h-2" />
                                                        <span className="text-xs text-muted-foreground w-8">{skill.level}%</span>
                                                        {skill.certified && (
                                                            <Award className="w-4 h-4 text-amber-500" />
                                                        )}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>

                                        <div>
                                            <h4 className="font-medium mb-2 flex items-center gap-2">
                                                <Star className="w-4 h-4 text-pink-500" />
                                                Interests
                                            </h4>
                                            <div className="flex flex-wrap gap-2">
                                                {userProfile.interests.map((interest) => (
                                                    <Badge key={interest} variant="secondary">
                                                        {interest}
                                                    </Badge>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>
                    </div>

                    <div className="space-y-6">
                        <div className="flex flex-wrap gap-2">
                            {tabs.map((tab) => {
                                const Icon = tab.icon;
                                return (
                                    <Button
                                        key={tab.id}
                                        variant={activeTab === tab.id ? "default" : "outline"}
                                        onClick={() => setActiveTab(tab.id)}
                                        className="flex items-center gap-2"
                                    >
                                        <Icon className="w-4 h-4" />
                                        {tab.label}
                                    </Button>
                                );
                            })}
                        </div>
                        
                        {activeTab === "activity" && (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.3 }}
                            >
                                <Card>
                                    <CardHeader>
                                        <CardTitle>Recent Activity</CardTitle>
                                        <CardDescription>Your latest learning activities</CardDescription>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="space-y-4">
                                            {userProfile.activityLog.map((activity, index) => {
                                                const Icon = getActivityIcon(activity.type);
                                                return (
                                                    <motion.div
                                                        key={activity.id}
                                                        initial={{ opacity: 0, x: -20 }}
                                                        animate={{ opacity: 1, x: 0 }}
                                                        transition={{ duration: 0.3, delay: index * 0.1 }}
                                                        className="flex items-start gap-4 p-3 rounded-lg hover:bg-muted/50 transition-colors"
                                                    >
                                                        <div className="w-10 h-10 rounded-full bg-violet-100 dark:bg-violet-900/30 flex items-center justify-center shrink-0">
                                                            <Icon className="w-5 h-5 text-violet-500" />
                                                        </div>
                                                        <div className="flex-1 min-w-0">
                                                            <p className="font-medium">{activity.action}</p>
                                                            <p className="text-sm text-muted-foreground truncate">{activity.target}</p>
                                                        </div>
                                                        <span className="text-xs text-muted-foreground shrink-0">{activity.date}</span>
                                                    </motion.div>
                                                );
                                            })}
                                        </div>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        )}
                        
                        {activeTab === "achievements" && (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.3 }}
                            >
                                <Card>
                                    <CardHeader>
                                        <CardTitle>Achievements</CardTitle>
                                        <CardDescription>Your earned badges and accomplishments</CardDescription>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                                            {userProfile.achievements.map((achievement, index) => (
                                                <motion.div
                                                    key={achievement.id}
                                                    initial={{ opacity: 0, scale: 0.9 }}
                                                    animate={{ opacity: 1, scale: 1 }}
                                                    transition={{ duration: 0.3, delay: index * 0.1 }}
                                                    className="p-4 border rounded-lg text-center hover:shadow-md transition-shadow"
                                                >
                                                    <div className="text-4xl mb-2">{achievement.icon}</div>
                                                    <h4 className="font-semibold">{achievement.title}</h4>
                                                    <p className="text-sm text-muted-foreground mt-1">{achievement.description}</p>
                                                    <p className="text-xs text-muted-foreground mt-2">{achievement.date}</p>
                                                </motion.div>
                                            ))}
                                        </div>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        )}
                        
                        {activeTab === "preferences" && (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.3 }}
                            >
                                <Card>
                                    <CardHeader>
                                        <CardTitle>Learning Preferences</CardTitle>
                                        <CardDescription>Your personalized learning settings</CardDescription>
                                    </CardHeader>
                                    <CardContent className="space-y-6">
                                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                                            <div className="space-y-2">
                                                <div className="flex items-center gap-2 text-muted-foreground">
                                                    <BookOpen className="w-4 h-4" />
                                                    <span className="text-sm">Preferred Learning Type</span>
                                                </div>
                                                <p className="font-medium">{userProfile.learningPreferences.type}</p>
                                            </div>
                                            <div className="space-y-2">
                                                <div className="flex items-center gap-2 text-muted-foreground">
                                                    <Clock className="w-4 h-4" />
                                                    <span className="text-sm">Learning Style</span>
                                                </div>
                                                <p className="font-medium">{userProfile.learningPreferences.style}</p>
                                            </div>
                                            <div className="space-y-2">
                                                <div className="flex items-center gap-2 text-muted-foreground">
                                                    <Users className="w-4 h-4" />
                                                    <span className="text-sm">Time Commitment</span>
                                                </div>
                                                <p className="font-medium">{userProfile.learningPreferences.timeCommitment}</p>
                                            </div>
                                            <div className="space-y-2">
                                                <div className="flex items-center gap-2 text-muted-foreground">
                                                    <GraduationCap className="w-4 h-4" />
                                                    <span className="text-sm">Education</span>
                                                </div>
                                                <p className="font-medium">{userProfile.education.qualification}</p>
                                                <p className="text-sm text-muted-foreground">{userProfile.education.field} - {userProfile.education.institution}</p>
                                            </div>
                                        </div>
                                        
                                        <div className="pt-4 border-t">
                                            <h4 className="font-medium mb-4">Account Settings</h4>
                                            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                                                <Button variant="outline" className="justify-start">
                                                    <Settings className="w-4 h-4 mr-2" />
                                                    General Settings
                                                </Button>
                                                <Button variant="outline" className="justify-start">
                                                    <Bell className="w-4 h-4 mr-2" />
                                                    Notifications
                                                </Button>
                                                <Button variant="outline" className="justify-start">
                                                    <Shield className="w-4 h-4 mr-2" />
                                                    Privacy
                                                </Button>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        )}
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
