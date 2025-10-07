"use client";

import * as React from "react";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";
import { ChevronLeft, ChevronRight, User, BookOpen, Target, Settings, Clock, Star, Send, LogOut } from "lucide-react";


const steps = [
    { name: "Personal Info", icon: User },
    { name: "Skills & Assessment", icon: BookOpen },
    { name: "Career Goals", icon: Target },
    { name: "Learning Preferences", icon: Settings },
    { name: "Availability & Motivation", icon: Clock },
    { name: "Feedback", icon: Send },
];

export default function OnboardingForm() {
    const [step, setStep] = React.useState(0);
    const [formData, setFormData] = React.useState<any>({
        comfortableSubjects: [],
        skills: [],
        interests: [],
        learningGoals: [],
        learningTypes: [],
        motivations: [],
        familiarWith: [],
    });
    const router = useRouter();

    const nextStep = () => setStep((prev) => Math.min(prev + 1, steps.length - 1));
    const prevStep = () => setStep((prev) => Math.max(prev - 1, 0));

    const handleChange = (key: string, value: any) => {
        setFormData((prev: any) => ({ ...prev, [key]: value }));
    };

    const handleArrayChange = (key: string, value: string, checked: boolean) => {
        setFormData((prev: any) => ({
            ...prev,
            [key]: checked
                ? [...(prev[key] || []), value]
                : (prev[key] || []).filter((item: string) => item !== value)
        }));
    };

    const handleSubmit = () => {
        console.log("Collected Data:", formData);
        router.push("/student/dashboard");
    };

    const handleLogout = () => {
        router.push("/");
    };

    const progress = (step / (steps.length - 1)) * 100;

    useEffect(() => {
              document.title = "Onboarding Questionaire | ShikshaDisha";
          }, []);

    return (
        <div className="min-h-screen flex items-center justify-center bg-background p-4 relative">
            {/* Logout Button */}
            <Button
                variant="outline"
                onClick={handleLogout}
                className="absolute top-4 right-4 flex items-center gap-2"
            >
                <LogOut size={16} />
                Logout
            </Button>

            



            <div className="w-full max-w-4xl p-8 bg-card rounded-lg shadow-sm border">

                <h1 className="text-3xl font-bold mb-2 text-foreground text-center">
                    Welcome to Your Learning Journey
                </h1>
                <p className="text-muted-foreground text-center mb-8">
                    Help us personalize your experience by answering a few questions
                </p>

                {/* Progress Bar */}
                <div className="mb-8">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium text-muted-foreground">Progress</span>
                        <span className="text-sm font-medium text-muted-foreground">{step + 1} of {steps.length}</span>
                    </div>
                    <Progress value={progress} className="h-2" />
                </div>

                {/* Step Indicators */}
                <div className="flex justify-between mb-8 relative">
                    {steps.map((stepItem, index) => {
                        const Icon = stepItem.icon;
                        return (
                            <div key={index} className="flex flex-col items-center z-10">
                                <div
                                    className={`w-10 h-10 rounded-full flex items-center justify-center border-2 ${index <= step
                                            ? "bg-primary border-primary text-primary-foreground"
                                            : "bg-card border-muted text-muted-foreground"
                                        } transition-colors duration-300`}
                                >
                                    <Icon size={18} />
                                </div>
                                <span
                                    className={`text-xs mt-2 font-medium ${index <= step ? "text-primary" : "text-muted-foreground"
                                        }`}
                                >
                                    {stepItem.name}
                                </span>
                            </div>
                        );
                    })}
                    <div className="absolute top-5 left-0 right-0 h-0.5 bg-muted -z-10"></div>
                    <div
                        className="absolute top-5 left-0 h-0.5 bg-primary -z-10 transition-all duration-500"
                        style={{ width: `${progress}%` }}
                    ></div>
                </div>



                <AnimatePresence mode="wait">
                    <motion.div
                        key={step}
                        initial={{ opacity: 0, x: 50 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -25 }}
                        transition={{ duration: 0.4 }}
                    >
                        {/* Step 1: Personal Info */}
                        {step === 0 && (
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <User className="text-primary" size={24} />
                                        Basic Personal and Academic Information
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-6">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div className="space-y-2">
                                            <Label htmlFor="fullName">Full Name</Label>
                                            <Input
                                                id="fullName"
                                                placeholder="Enter your full name"
                                                value={formData.fullName || ""}
                                                onChange={(e) => handleChange("fullName", e.target.value)}
                                            />
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="contact">Email or Mobile Number</Label>
                                            <Input
                                                id="contact"
                                                placeholder="email@example.com or +1234567890"
                                                value={formData.contact || ""}
                                                onChange={(e) => handleChange("contact", e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div className="space-y-2">
                                            <Label htmlFor="education">Current Educational Qualification</Label>
                                            <Select
                                                onValueChange={(value) => handleChange("education", value)}
                                                value={formData.education || ""}
                                            >
                                                <SelectTrigger id="education">
                                                    <SelectValue placeholder="Select your qualification" />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    <SelectItem value="highSchool">High School/12th Grade</SelectItem>
                                                    <SelectItem value="diploma">Diploma</SelectItem>
                                                    <SelectItem value="bachelor">Bachelor's Degree</SelectItem>
                                                    <SelectItem value="master">Master's Degree</SelectItem>
                                                    <SelectItem value="phd">PhD</SelectItem>
                                                    <SelectItem value="other">Other</SelectItem>
                                                </SelectContent>
                                            </Select>
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="fieldOfStudy">Major/Field of Study</Label>
                                            <Input
                                                id="fieldOfStudy"
                                                placeholder="e.g., Computer Science, Business Administration"
                                                value={formData.fieldOfStudy || ""}
                                                onChange={(e) => handleChange("fieldOfStudy", e.target.value)}
                                            />
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        )}

                        {/* Step 2: Skills & Assessment */}
                        {step === 1 && (
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <BookOpen className="text-primary" size={24} />
                                        Prerequisite Knowledge & Skill Assessment
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-6">
                                    <div className="space-y-4">
                                        <Label>Which subjects/topics are you already comfortable with?</Label>
                                        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                                            {["Basic Math", "Programming in Python", "Data Structures", "Algorithms", "Web Development", "Database Management", "Statistics", "Machine Learning", "UI/UX Design"].map((subject) => (
                                                <div key={subject} className="flex items-center gap-2">
                                                    <Checkbox
                                                        id={subject}
                                                        checked={formData.comfortableSubjects?.includes(subject) || false}
                                                        onCheckedChange={(checked) =>
                                                            handleArrayChange("comfortableSubjects", subject, checked as boolean)
                                                        }
                                                    />
                                                    <Label htmlFor={subject} className="text-sm cursor-pointer">{subject}</Label>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <Label>Rate your proficiency in these foundational skills (1-5):</Label>
                                        <div className="space-y-4">
                                            {["Computer basics", "Internet navigation", "Mathematics", "English communication", "Programming fundamentals"].map((skill) => (
                                                <div key={skill} className="flex items-center justify-between">
                                                    <span className="font-medium">{skill}</span>
                                                    <RadioGroup
                                                        value={formData[`proficiency_${skill.replace(/\s+/g, '_')}`] || ""}
                                                        onValueChange={(value) => handleChange(`proficiency_${skill.replace(/\s+/g, '_')}`, value)}
                                                        className="flex gap-2"
                                                    >
                                                        {[1, 2, 3, 4, 5].map((num) => (
                                                            <div key={num} className="flex items-center gap-1">
                                                                <RadioGroupItem value={num.toString()} id={`${skill}_${num}`} />
                                                                <Label htmlFor={`${skill}_${num}`} className="cursor-pointer">{num}</Label>
                                                            </div>
                                                        ))}
                                                    </RadioGroup>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <Label>Are you familiar with (choose all that apply):</Label>
                                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                                            {["Online learning platforms", "Coding environments (IDEs)", "Project-based learning", "Version Control (Git)", "Cloud platforms", "Agile methodologies"].map((item) => (
                                                <div key={item} className="flex items-center gap-2">
                                                    <Checkbox
                                                        id={item}
                                                        checked={formData.familiarWith?.includes(item) || false}
                                                        onCheckedChange={(checked) =>
                                                            handleArrayChange("familiarWith", item, checked as boolean)
                                                        }
                                                    />
                                                    <Label htmlFor={item} className="text-sm cursor-pointer">{item}</Label>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <Label>Technical or soft skills you possess:</Label>
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                            {["C++", "Java", "HTML/CSS", "JavaScript", "Python", "SQL", "Public speaking", "Team leadership", "Problem solving", "Project management"].map((skill) => (
                                                <div key={skill} className="flex items-center gap-2">
                                                    <Checkbox
                                                        id={`skill_${skill}`}
                                                        checked={formData.skills?.includes(skill) || false}
                                                        onCheckedChange={(checked) =>
                                                            handleArrayChange("skills", skill, checked as boolean)
                                                        }
                                                    />
                                                    <Label htmlFor={`skill_${skill}`} className="text-sm cursor-pointer">{skill}</Label>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="certifications">Completed certifications or courses</Label>
                                        <Textarea
                                            id="certifications"
                                            placeholder="List any certifications or courses you've completed"
                                            value={formData.certifications || ""}
                                            onChange={(e) => handleChange("certifications", e.target.value)}
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="resume">Resume or LinkedIn profile URL (optional)</Label>
                                        <Input
                                            id="resume"
                                            placeholder="https://linkedin.com/in/yourprofile or https://yourportfolio.com"
                                            value={formData.resume || ""}
                                            onChange={(e) => handleChange("resume", e.target.value)}
                                        />
                                    </div>
                                </CardContent>
                            </Card>
                        )}

                        {/* Step 3: Career Goals */}
                        {step === 2 && (
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Target className="text-primary" size={24} />
                                        Interests and Career Goals
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-6">
                                    <div className="space-y-4">
                                        <Label>What are the main skills or subjects you wish to learn or improve?</Label>
                                        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                                            {["Web Development", "Data Science", "Mobile App Development", "Cloud Computing", "AI/ML", "Cybersecurity", "UI/UX Design", "Digital Marketing", "Project Management", "Data Analysis", "Software Engineering", "DevOps"].map((interest) => (
                                                <div key={interest} className="flex items-center gap-2">
                                                    <Checkbox
                                                        id={`interest_${interest}`}
                                                        checked={formData.interests?.includes(interest) || false}
                                                        onCheckedChange={(checked) =>
                                                            handleArrayChange("interests", interest, checked as boolean)
                                                        }
                                                    />
                                                    <Label htmlFor={`interest_${interest}`} className="text-sm cursor-pointer">{interest}</Label>
                                                </div>
                                            ))}
                                        </div>
                                        <div className="mt-2">
                                            <Input
                                                placeholder="Other (please specify)"
                                                value={formData.otherInterest || ""}
                                                onChange={(e) => handleChange("otherInterest", e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <Label>What are your primary learning goals?</Label>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                            {["Getting a job/internship", "Cracking competitive exams", "Building projects", "Gaining practical knowledge", "Career advancement", "Personal interest"].map((goal) => (
                                                <div key={goal} className="flex items-center gap-2">
                                                    <Checkbox
                                                        id={`goal_${goal}`}
                                                        checked={formData.learningGoals?.includes(goal) || false}
                                                        onCheckedChange={(checked) =>
                                                            handleArrayChange("learningGoals", goal, checked as boolean)
                                                        }
                                                    />
                                                    <Label htmlFor={`goal_${goal}`} className="text-sm cursor-pointer">{goal}</Label>
                                                </div>
                                            ))}
                                        </div>
                                        <div className="mt-2">
                                            <Input
                                                placeholder="Other goal (please specify)"
                                                value={formData.otherGoal || ""}
                                                onChange={(e) => handleChange("otherGoal", e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="targetRoles">Which industries or roles are you interested in?</Label>
                                        <Textarea
                                            id="targetRoles"
                                            placeholder="e.g., Software Development, Data Science, Networking, UI/UX Design, etc."
                                            value={formData.targetRoles || ""}
                                            onChange={(e) => handleChange("targetRoles", e.target.value)}
                                        />
                                    </div>
                                </CardContent>
                            </Card>
                        )}

                        {/* Step 4: Learning Preferences */}
                        {step === 3 && (
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Settings className="text-primary" size={24} />
                                        Learning Preferences
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-6">
                                    <div className="space-y-4">
                                        <Label>What type of learning best suits you?</Label>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            {[
                                                { id: "videos", label: "Videos", desc: "Visual and auditory learning" },
                                                { id: "reading", label: "Reading articles", desc: "Text-based content" },
                                                { id: "projects", label: "Hands-on projects", desc: "Learning by doing" },
                                                { id: "quizzes", label: "Quizzes", desc: "Testing knowledge" },
                                                { id: "notes", label: "Short notes", desc: "Concise summaries" },
                                                { id: "interactive", label: "Interactive exercises", desc: "Engaging activities" },
                                            ].map((type) => (
                                                <div key={type.id} className="flex items-start gap-3 p-3 border rounded-lg hover:bg-muted/50 transition-colors">
                                                    <Checkbox
                                                        id={type.id}
                                                        checked={formData.learningTypes?.includes(type.id) || false}
                                                        onCheckedChange={(checked) =>
                                                            handleArrayChange("learningTypes", type.id, checked as boolean)
                                                        }
                                                    />
                                                    <div>
                                                        <Label htmlFor={type.id} className="font-medium cursor-pointer">{type.label}</Label>
                                                        <p className="text-sm text-muted-foreground">{type.desc}</p>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <Label>Do you prefer guided paths or self-paced learning?</Label>
                                        <RadioGroup
                                            value={formData.learningStyle || ""}
                                            onValueChange={(value) => handleChange("learningStyle", value)}
                                            className="flex flex-col gap-4"
                                        >
                                            <div className="flex items-center gap-3 p-3 border rounded-lg hover:bg-muted/50 transition-colors">
                                                <RadioGroupItem value="guided" id="guided" />
                                                <Label htmlFor="guided" className="cursor-pointer">
                                                    <span className="font-medium">Guided paths with deadlines</span>
                                                    <p className="text-sm text-muted-foreground">Structured learning with set timelines</p>
                                                </Label>
                                            </div>
                                            <div className="flex items-center gap-3 p-3 border rounded-lg hover:bg-muted/50 transition-colors">
                                                <RadioGroupItem value="selfPaced" id="selfPaced" />
                                                <Label htmlFor="selfPaced" className="cursor-pointer">
                                                    <span className="font-medium">Self-paced learning</span>
                                                    <p className="text-sm text-muted-foreground">Learn at your own convenience</p>
                                                </Label>
                                            </div>
                                            <div className="flex items-center gap-3 p-3 border rounded-lg hover:bg-muted/50 transition-colors">
                                                <RadioGroupItem value="mixed" id="mixed" />
                                                <Label htmlFor="mixed" className="cursor-pointer">
                                                    <span className="font-medium">Mixed approach</span>
                                                    <p className="text-sm text-muted-foreground">Some structure with flexibility</p>
                                                </Label>
                                            </div>
                                        </RadioGroup>
                                    </div>

                                    <div className="space-y-4">
                                        <Label>Are you open to collaborative/group learning?</Label>
                                        <RadioGroup
                                            value={formData.collaborativeLearning || ""}
                                            onValueChange={(value) => handleChange("collaborativeLearning", value)}
                                            className="flex gap-6"
                                        >
                                            <div className="flex items-center gap-2">
                                                <RadioGroupItem value="yes" id="collabYes" />
                                                <Label htmlFor="collabYes" className="cursor-pointer">Yes, I enjoy learning with others</Label>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <RadioGroupItem value="no" id="collabNo" />
                                                <Label htmlFor="collabNo" className="cursor-pointer">No, I prefer learning alone</Label>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <RadioGroupItem value="sometimes" id="collabSometimes" />
                                                <Label htmlFor="collabSometimes" className="cursor-pointer">Sometimes, for specific activities</Label>
                                            </div>
                                        </RadioGroup>
                                    </div>
                                </CardContent>
                            </Card>
                        )}

                        {/* Step 5: Availability & Motivation */}
                        {step === 4 && (
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Clock className="text-primary" size={24} />
                                        Time Commitment & Motivation
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-6">
                                    <div className="space-y-4">
                                        <Label>How much time can you dedicate to learning?</Label>
                                        <RadioGroup
                                            value={formData.timeCommitment || ""}
                                            onValueChange={(value) => handleChange("timeCommitment", value)}
                                            className="grid grid-cols-1 md:grid-cols-2 gap-4"
                                        >
                                            {[
                                                { id: "less1hr", label: "<1 hour/day", desc: "Light learning" },
                                                { id: "1-2hrs", label: "1-2 hours/day", desc: "Regular commitment" },
                                                { id: "2-5hrs", label: "2-5 hours/week", desc: "Moderate pace" },
                                                { id: "weekends", label: "Weekends only", desc: "Focused weekend learning" },
                                                { id: "flexible", label: "Flexible/No preference", desc: "Varies by week" },
                                                { id: "intensive", label: "Full-time (5+ hrs/day)", desc: "Intensive learning" },
                                            ].map((option) => (
                                                <div key={option.id} className="flex items-start gap-3 p-3 border rounded-lg hover:bg-muted/50 transition-colors">
                                                    <RadioGroupItem value={option.id} id={option.id} />
                                                    <div>
                                                        <Label htmlFor={option.id} className="font-medium cursor-pointer">{option.label}</Label>
                                                        <p className="text-sm text-muted-foreground">{option.desc}</p>
                                                    </div>
                                                </div>
                                            ))}
                                        </RadioGroup>
                                    </div>

                                    <div className="space-y-4">
                                        <Label>What is your target completion timeline?</Label>
                                        <RadioGroup
                                            value={formData.timeline || ""}
                                            onValueChange={(value) => handleChange("timeline", value)}
                                            className="flex flex-wrap gap-4"
                                        >
                                            {[
                                                { id: "1month", label: "<1 month" },
                                                { id: "1-3months", label: "1-3 months" },
                                                { id: "3-6months", label: "3-6 months" },
                                                { id: "6+months", label: "6+ months" },
                                                { id: "noTimeline", label: "No fixed timeline" },
                                            ].map((option) => (
                                                <div key={option.id} className="flex items-center gap-2">
                                                    <RadioGroupItem value={option.id} id={option.id} />
                                                    <Label htmlFor={option.id} className="cursor-pointer">{option.label}</Label>
                                                </div>
                                            ))}
                                        </RadioGroup>
                                    </div>

                                    <div className="space-y-4">
                                        <Label>What motivates you to learn?</Label>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                            {[
                                                "Certificates",
                                                "Skill advancement",
                                                "Community recognition",
                                                "Earning potential",
                                                "Building things",
                                                "Career growth",
                                                "Personal satisfaction",
                                                "Problem solving"
                                            ].map((motivation) => (
                                                <div key={motivation} className="flex items-center gap-2">
                                                    <Checkbox
                                                        id={`motivation_${motivation}`}
                                                        checked={formData.motivations?.includes(motivation) || false}
                                                        onCheckedChange={(checked) =>
                                                            handleArrayChange("motivations", motivation, checked as boolean)
                                                        }
                                                    />
                                                    <Label htmlFor={`motivation_${motivation}`} className="cursor-pointer">{motivation}</Label>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div className="space-y-4">
                                            <Label>Do you have stable internet access and a personal computer/laptop?</Label>
                                            <RadioGroup
                                                value={formData.hasResources || ""}
                                                onValueChange={(value) => handleChange("hasResources", value)}
                                                className="flex gap-4"
                                            >
                                                <div className="flex items-center gap-2">
                                                    <RadioGroupItem value="yes" id="resourcesYes" />
                                                    <Label htmlFor="resourcesYes" className="cursor-pointer">Yes</Label>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <RadioGroupItem value="no" id="resourcesNo" />
                                                    <Label htmlFor="resourcesNo" className="cursor-pointer">No</Label>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <RadioGroupItem value="limited" id="resourcesLimited" />
                                                    <Label htmlFor="resourcesLimited" className="cursor-pointer">Limited access</Label>
                                                </div>
                                            </RadioGroup>
                                        </div>

                                        <div className="space-y-2">
                                            <Label htmlFor="accommodations">Accessibility needs or learning accommodations</Label>
                                            <Input
                                                id="accommodations"
                                                placeholder="e.g., larger fonts, screen readers, etc."
                                                value={formData.accommodations || ""}
                                                onChange={(e) => handleChange("accommodations", e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div className="space-y-4">
                                            <Label>Do you want to receive regular reminders/motivational nudges?</Label>
                                            <RadioGroup
                                                value={formData.reminders || ""}
                                                onValueChange={(value) => handleChange("reminders", value)}
                                                className="flex gap-4"
                                            >
                                                <div className="flex items-center gap-2">
                                                    <RadioGroupItem value="yes" id="remindersYes" />
                                                    <Label htmlFor="remindersYes" className="cursor-pointer">Yes</Label>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <RadioGroupItem value="no" id="remindersNo" />
                                                    <Label htmlFor="remindersNo" className="cursor-pointer">No</Label>
                                                </div>
                                            </RadioGroup>
                                        </div>

                                        <div className="space-y-4">
                                            <Label>Are you interested in gamified elements?</Label>
                                            <RadioGroup
                                                value={formData.gamification || ""}
                                                onValueChange={(value) => handleChange("gamification", value)}
                                                className="flex gap-4"
                                            >
                                                <div className="flex items-center gap-2">
                                                    <RadioGroupItem value="yes" id="gamificationYes" />
                                                    <Label htmlFor="gamificationYes" className="cursor-pointer">Yes</Label>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <RadioGroupItem value="no" id="gamificationNo" />
                                                    <Label htmlFor="gamificationNo" className="cursor-pointer">No</Label>
                                                </div>
                                            </RadioGroup>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        )}

                        {/* Step 6: Feedback */}
                        {step === 5 && (
                            <Card>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Send className="text-primary" size={24} />
                                        Final Feedback & Custom Requests
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-6">
                                    <div className="space-y-2">
                                        <Label htmlFor="featureRequests">Are there any topics or features you want to see on the platform?</Label>
                                        <Textarea
                                            id="featureRequests"
                                            placeholder="Tell us what you'd like to see in our learning platform..."
                                            value={formData.featureRequests || ""}
                                            onChange={(e) => handleChange("featureRequests", e.target.value)}
                                            rows={4}
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="additionalComments">Any additional comments or preferences?</Label>
                                        <Textarea
                                            id="additionalComments"
                                            placeholder="Share any other thoughts or special requirements..."
                                            value={formData.additionalComments || ""}
                                            onChange={(e) => handleChange("additionalComments", e.target.value)}
                                            rows={4}
                                        />
                                    </div>

                                    <div className="p-4 bg-muted rounded-lg border">
                                        <div className="flex items-start gap-3">
                                            <Star className="text-primary mt-0.5" size={20} />
                                            <div>
                                                <h3 className="font-medium">Thank you for completing the questionnaire!</h3>
                                                <p className="text-muted-foreground text-sm mt-1">
                                                    Your responses will help us create a personalized learning path just for you.
                                                    Click submit to get started on your learning journey.
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        )}
                    </motion.div>
                </AnimatePresence>

                {/* Navigation */}
                <div className={`flex ${step > 0 ? 'justify-between' : 'justify-end'} mt-8 gap-4`}>
                    {step > 0 && (
                        <Button variant="outline" onClick={prevStep} className="flex items-center gap-2">
                            <ChevronLeft size={20} />
                            Back
                        </Button>
                    )}

                    {step < steps.length - 1 ? (
                        <Button onClick={nextStep} className="flex items-center gap-2 ml-auto">
                            Next
                            <ChevronRight size={20} />
                        </Button>
                    ) : (
                        <Button onClick={handleSubmit} className="flex items-center gap-2">
                            Submit & Get Started
                            <ChevronRight size={20} />
                        </Button>
                    )}
                </div>
            </div>
        </div>
    );
}