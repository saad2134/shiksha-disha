"use client";

import * as React from "react";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import {
    Brain,
    Clock,
    Target,
    Zap,
    ChevronRight,
    CheckCircle2,
    Sparkles,
    Palette,
    TrendingUp
} from "lucide-react";
import { siteConfig } from "@/config/site";

export default function QuickQuiz() {
    const router = useRouter();

    useEffect(() => {
        document.title = `Quick Quiz ✦ ${siteConfig.name}`;
    }, []);

    const quizCategories = [
        {
            id: 1,
            title: "Web Development",
            description: "Test your knowledge of HTML, CSS, JavaScript",
            questions: 10,
            duration: "5 min",
            difficulty: "Beginner",
            icon: <Target className="w-6 h-6" />
        },
        {
            id: 2,
            title: "Programming Basics",
            description: "Core programming concepts and logic",
            questions: 8,
            duration: "4 min",
            difficulty: "Beginner",
            icon: <Brain className="w-6 h-6" />
        },
        {
            id: 3,
            title: "Problem Solving",
            description: "Critical thinking and analytical skills",
            questions: 12,
            duration: "6 min",
            difficulty: "Intermediate",
            icon: <Zap className="w-6 h-6" />
        },
        {
            id: 4,
            title: "Digital Marketing",
            description: "SEO, social media, and marketing fundamentals",
            questions: 10,
            duration: "5 min",
            difficulty: "Beginner",
            icon: <TrendingUp className="w-6 h-6" />
        },
        {
            id: 5,
            title: "Graphic Design",
            description: "Design principles, tools, and creativity",
            questions: 8,
            duration: "4 min",
            difficulty: "Beginner",
            icon: <Palette className="w-6 h-6" />
        }
    ];

    const benefits = [
        { text: "Instant results", icon: <Clock className="w-4 h-4" /> },
        { text: "Skill assessment", icon: <Target className="w-4 h-4" /> },
        { text: "Personalized recommendations", icon: <Sparkles className="w-4 h-4" /> },
        { text: "Track your progress", icon: <CheckCircle2 className="w-4 h-4" /> }
    ];

    return (
        <div className="flex flex-col min-h-full">
            {/* Purple Hero Section */}
            <section className="relative overflow-hidden bg-gradient-to-br from-violet-600 via-purple-600 to-violet-800 dark:from-violet-900 dark:via-purple-900 dark:to-violet-950 py-16 sm:py-20 lg:py-24">
                {/* Background decorations */}
                <div className="absolute inset-0 overflow-hidden">
                    <motion.div
                        className="absolute top-10 left-10 w-32 h-32 rounded-full bg-white/10 blur-2xl"
                        animate={{
                            scale: [1, 1.2, 1],
                            opacity: [0.3, 0.5, 0.3],
                        }}
                        transition={{
                            duration: 5,
                            repeat: Infinity,
                            ease: "easeInOut",
                        }}
                    />
                    <motion.div
                        className="absolute bottom-10 right-10 w-48 h-48 rounded-full bg-purple-400/20 blur-3xl"
                        animate={{
                            scale: [1, 1.3, 1],
                            opacity: [0.2, 0.4, 0.2],
                        }}
                        transition={{
                            duration: 7,
                            repeat: Infinity,
                            ease: "easeInOut",
                            delay: 1,
                        }}
                    />
                    <motion.div
                        className="absolute top-1/2 left-1/3 w-24 h-24 rounded-full bg-violet-400/15 blur-xl"
                        animate={{
                            x: [0, 20, 0],
                            y: [0, -20, 0],
                        }}
                        transition={{
                            duration: 6,
                            repeat: Infinity,
                            ease: "easeInOut",
                            delay: 2,
                        }}
                    />
                </div>

                {/* Hero Content */}
                <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 text-white/90 text-sm font-medium mb-6">
                            <Sparkles className="w-4 h-4" />
                            <span>AI-Powered Assessment</span>
                        </div>
                    </motion.div>

                    <motion.h1
                        className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight"
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.1 }}
                    >
                        Take a Quick Quiz
                    </motion.h1>

                    <motion.p
                        className="text-lg sm:text-xl text-white/80 max-w-2xl mx-auto mb-8"
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                    >
                        Discover your strengths and get personalized course recommendations in minutes
                    </motion.p>

                    <motion.div
                        className="flex flex-wrap justify-center gap-4"
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.3 }}
                    >
                        <div className="flex flex-wrap justify-center gap-3">
                            {benefits.map((benefit, index) => (
                                <motion.div
                                    key={index}
                                    className="flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm text-white/90 text-sm"
                                    initial={{ opacity: 0, scale: 0.8 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ duration: 0.4, delay: 0.4 + index * 0.1 }}
                                >
                                    {benefit.icon}
                                    <span>{benefit.text}</span>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Quiz Categories Section */}
            <div className="flex-1 p-4 sm:p-6 lg:p-8 bg-muted/30">
                <div className="max-w-7xl mx-auto">
                    <motion.div
                        className="text-center mb-8"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-2">
                            Choose a Quiz
                        </h2>
                        <p className="text-muted-foreground">
                            Select a category to start your assessment
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {quizCategories.map((category, index) => (
                            <motion.div
                                key={category.id}
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5, delay: 0.1 * index }}
                            >
                                <Card className="h-full hover:shadow-lg transition-all duration-300 hover:scale-[1.02] cursor-pointer group border-violet-100 dark:border-violet-900/30">
                                    <CardHeader>
                                        <div className="flex items-center gap-3 mb-2">
                                            <div className="p-3 rounded-xl bg-violet-100 dark:bg-violet-900/30 text-violet-600 dark:text-violet-400 group-hover:bg-violet-600 group-hover:text-white transition-colors duration-300">
                                                {category.icon}
                                            </div>
                                            <CardTitle className="text-xl">{category.title}</CardTitle>
                                        </div>
                                        <CardDescription className="text-base">
                                            {category.description}
                                        </CardDescription>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="flex flex-wrap gap-3 mb-6">
                                            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-muted text-sm text-muted-foreground">
                                                <Brain className="w-4 h-4" />
                                                <span>{category.questions} Questions</span>
                                            </div>
                                            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-muted text-sm text-muted-foreground">
                                                <Clock className="w-4 h-4" />
                                                <span>{category.duration}</span>
                                            </div>
                                            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-violet-100 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300 text-sm font-medium">
                                                <Target className="w-4 h-4" />
                                                <span>{category.difficulty}</span>
                                            </div>
                                        </div>
                                        <Button className="w-full group/btn">
                                            Start Quiz
                                            <ChevronRight className="w-4 h-4 ml-2 group-hover/btn:translate-x-1 transition-transform" />
                                        </Button>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        ))}
                    </div>

                    {/* Additional Info Section */}
                    <motion.div
                        className="mt-12"
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.5 }}
                    >
                        <Card className="bg-gradient-to-br from-violet-50 to-purple-50 dark:from-violet-950/20 dark:to-purple-950/20 border-violet-100 dark:border-violet-900/30">
                            <CardContent className="p-6 sm:p-8">
                                <div className="flex flex-col md:flex-row items-center gap-6">
                                    <div className="p-4 rounded-2xl bg-violet-100 dark:bg-violet-900/30">
                                        <Sparkles className="w-8 h-8 text-violet-600 dark:text-violet-400" />
                                    </div>
                                    <div className="flex-1 text-center md:text-left">
                                        <h3 className="text-xl font-semibold mb-2">
                                            Why take a quick quiz?
                                        </h3>
                                        <p className="text-muted-foreground">
                                            Our AI analyzes your responses to understand your knowledge level and learning style, 
                                            then recommends the perfect courses tailored just for you. It only takes 5 minutes 
                                            and helps you discover the best path forward!
                                        </p>
                                    </div>
                                    <Button 
                                        variant="outline" 
                                        className="shrink-0"
                                        onClick={() => router.push('/demo/recommendations')}
                                    >
                                        View Recommendations
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    </motion.div>
                </div>
            </div>
        </div>
    );
}
