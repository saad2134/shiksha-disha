"use client";

import * as React from "react";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, User, BookOpen, Target, Settings, Clock, Check, Loader2 } from "lucide-react";
import { siteConfig } from "@/config/site";
import { useEffect } from "react";

const steps = [
  { name: "Personal Info", icon: User },
  { name: "Skills", icon: BookOpen },
  { name: "Career Goals", icon: Target },
  { name: "Preferences", icon: Settings },
];

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    education: "",
    skills: [] as string[],
    interests: [] as string[],
    careerGoal: "",
    timeCommitment: "",
  });

  useEffect(() => {
    document.title = `Get Started ✦ ${siteConfig.name}`;
  }, []);

  const handleNext = () => {
    if (step < steps.length - 1) {
      setStep(step + 1);
    } else {
      handleSubmit();
    }
  };

  const handlePrev = () => {
    if (step > 0) {
      setStep(step - 1);
    }
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      router.push("/dashboard");
    }, 2000);
  };

  const progress = ((step + 1) / steps.length) * 100;

  const handleSkillToggle = (skill: string) => {
    setFormData(prev => ({
      ...prev,
      skills: prev.skills.includes(skill)
        ? prev.skills.filter(s => s !== skill)
        : [...prev.skills, skill]
    }));
  };

  const handleInterestToggle = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold mb-2">Welcome to {siteConfig.name}</h1>
          <p className="text-muted-foreground">Let's personalize your learning journey</p>
        </div>

        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-muted-foreground">
              Step {step + 1} of {steps.length}
            </span>
            <span className="text-sm font-medium text-muted-foreground">
              {Math.round(progress)}%
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        <div className="flex justify-between mb-8 overflow-x-auto pb-2">
          {steps.map((stepItem, index) => {
            const Icon = stepItem.icon;
            return (
              <div key={index} className="flex flex-col items-center shrink-0 min-w-[60px]">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-colors ${
                    index <= step
                      ? "bg-primary border-primary text-primary-foreground"
                      : "bg-muted border-muted text-muted-foreground"
                  }`}
                >
                  {index < step ? <Check size={18} /> : <Icon size={18} />}
                </div>
                <span
                  className={`text-xs mt-2 font-medium ${
                    index <= step ? "text-primary" : "text-muted-foreground"
                  }`}
                >
                  {stepItem.name}
                </span>
              </div>
            );
          })}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>{steps[step].name}</CardTitle>
            <CardDescription>
              {step === 0 && "Tell us about yourself"}
              {step === 1 && "What skills do you have?"}
              {step === 2 && "What do you want to learn?"}
              {step === 3 && "How do you want to learn?"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <AnimatePresence mode="wait">
              {step === 0 && (
                <motion.div
                  key="step0"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-4"
                >
                  <div className="space-y-2">
                    <Label htmlFor="fullName">Full Name</Label>
                    <Input
                      id="fullName"
                      placeholder="John Doe"
                      value={formData.fullName}
                      onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="john@example.com"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="education">Education Level</Label>
                    <Input
                      id="education"
                      placeholder="e.g., Bachelor's Degree"
                      value={formData.education}
                      onChange={(e) => setFormData({ ...formData, education: e.target.value })}
                    />
                  </div>
                </motion.div>
              )}

              {step === 1 && (
                <motion.div
                  key="step1"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-4"
                >
                  <p className="text-sm text-muted-foreground mb-4">
                    Select the skills you already have:
                  </p>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {["HTML/CSS", "JavaScript", "Python", "Java", "SQL", "React", "Node.js", "Data Analysis", "Machine Learning", "UI/UX Design"].map((skill) => (
                      <Button
                        key={skill}
                        variant={formData.skills.includes(skill) ? "default" : "outline"}
                        size="sm"
                        onClick={() => handleSkillToggle(skill)}
                        className="w-full"
                      >
                        {skill}
                      </Button>
                    ))}
                  </div>
                </motion.div>
              )}

              {step === 2 && (
                <motion.div
                  key="step2"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-4"
                >
                  <p className="text-sm text-muted-foreground mb-4">
                    What do you want to learn?
                  </p>
                  <div className="grid grid-cols-2 gap-3">
                    {["Web Development", "Data Science", "Mobile Apps", "Cloud Computing", "AI/ML", "Cybersecurity", "UI/UX Design", "Digital Marketing"].map((interest) => (
                      <Button
                        key={interest}
                        variant={formData.interests.includes(interest) ? "default" : "outline"}
                        size="sm"
                        onClick={() => handleInterestToggle(interest)}
                        className="w-full"
                      >
                        {interest}
                      </Button>
                    ))}
                  </div>
                  <div className="space-y-2 mt-4">
                    <Label htmlFor="careerGoal">What's your career goal?</Label>
                    <Input
                      id="careerGoal"
                      placeholder="e.g., Software Developer"
                      value={formData.careerGoal}
                      onChange={(e) => setFormData({ ...formData, careerGoal: e.target.value })}
                    />
                  </div>
                </motion.div>
              )}

              {step === 3 && (
                <motion.div
                  key="step3"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-4"
                >
                  <p className="text-sm text-muted-foreground mb-4">
                    How much time can you dedicate?
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {[
                      { id: "less1", label: "Less than 1 hour/day" },
                      { id: "1-2", label: "1-2 hours/day" },
                      { id: "2-5", label: "2-5 hours/day" },
                      { id: "5+", label: "5+ hours/day" },
                    ].map((option) => (
                      <Button
                        key={option.id}
                        variant={formData.timeCommitment === option.id ? "default" : "outline"}
                        size="sm"
                        onClick={() => setFormData({ ...formData, timeCommitment: option.id })}
                        className="w-full"
                      >
                        {option.label}
                      </Button>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button
              variant="outline"
              onClick={handlePrev}
              disabled={step === 0}
            >
              <ChevronLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
            <Button onClick={handleNext} disabled={isLoading}>
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Saving...
                </>
              ) : step === steps.length - 1 ? (
                <>
                  Get Started
                  <Check className="ml-2 h-4 w-4" />
                </>
              ) : (
                <>
                  Next
                  <ChevronRight className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          </CardFooter>
        </Card>

        <p className="text-center text-sm text-muted-foreground mt-6">
          <a href="/" className="hover:text-primary">← Back to Home</a>
        </p>
      </div>
    </div>
  );
}
