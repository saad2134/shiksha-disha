"use client";

import * as React from "react";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { 
  LogOut, 
  ChevronLeft, 
  MapPin, 
  Target, 
  BookOpen, 
  Briefcase, 
  Award, 
  CheckCircle2,
  Clock,
  Users,
  Star,
  ArrowRight
} from "lucide-react";
import { siteConfig } from "@/config/site";

export default function CareerMap() {
  const router = useRouter();
  const [selectedMilestone, setSelectedMilestone] = React.useState<any>(null);

  const handleLogout = () => {
    router.push("/");
  };

  const handleBack = () => {
    router.push("/student/dashboard");
  };

  const careerPath = {
    goal: "Software Developer",
    duration: "9-12 months",
    level: "Beginner to Job-Ready",
    match: 92
  };

  const milestones = [
    {
      id: 1,
      title: "Profile Setup",
      status: "completed",
      type: "onboarding",
      description: "Career assessment and goal setting completed",
      duration: "Completed",
      progress: 100,
      icon: CheckCircle2,
      color: "text-green-600",
      bgColor: "bg-green-50",
      details: {
        skills: ["Self-assessment", "Goal setting"],
        resources: ["Career assessment test", "Profile completion"],
        nextSteps: "Begin foundational courses"
      }
    },
    {
      id: 2,
      title: "Web Development Fundamentals",
      status: "current",
      type: "course",
      description: "Learn HTML, CSS, and JavaScript basics",
      duration: "6 weeks",
      progress: 40,
      icon: BookOpen,
      color: "text-blue-600",
      bgColor: "bg-blue-50",
      details: {
        skills: ["HTML5", "CSS3", "JavaScript", "Responsive Design"],
        resources: ["NSQF Level 4 Course", "Interactive tutorials", "Practice projects"],
        nextSteps: "Complete module 3 of 6",
        provider: "Digital Skills Institute",
        level: "Beginner"
      }
    },
    {
      id: 3,
      title: "Python Programming",
      status: "upcoming",
      type: "course",
      description: "Master Python programming and algorithms",
      duration: "8 weeks",
      progress: 0,
      icon: BookOpen,
      color: "text-blue-600",
      bgColor: "bg-blue-50",
      details: {
        skills: ["Python Syntax", "Data Structures", "Algorithms", "Problem Solving"],
        resources: ["Python Basics Course", "Coding exercises", "Mini-projects"],
        nextSteps: "Start after completing Web Dev fundamentals",
        provider: "Code Academy",
        level: "Beginner to Intermediate"
      }
    },
    {
      id: 4,
      title: "Frontend Internship",
      status: "upcoming",
      type: "internship",
      description: "Real-world experience with a tech company",
      duration: "3 months",
      progress: 0,
      icon: Briefcase,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
      details: {
        skills: ["React.js", "Team Collaboration", "Project Management", "Code Review"],
        resources: ["Mentor guidance", "Real projects", "Industry exposure"],
        nextSteps: "Apply after completing core courses",
        provider: "Tech Solutions Ltd.",
        level: "Intermediate"
      }
    },
    {
      id: 5,
      title: "Full-Stack Certification",
      status: "upcoming",
      type: "certification",
      description: "Advanced full-stack development skills",
      duration: "10 weeks",
      progress: 0,
      icon: Award,
      color: "text-orange-600",
      bgColor: "bg-orange-50",
      details: {
        skills: ["Node.js", "Database Design", "API Development", "Deployment"],
        resources: ["Advanced curriculum", "Capstone project", "Industry certification"],
        nextSteps: "Prepare for final certification exam",
        provider: "Full-Stack Institute",
        level: "Advanced"
      }
    },
    {
      id: 6,
      title: "Job Ready: Software Developer",
      status: "upcoming",
      type: "job",
      description: "Start your career as a professional developer",
      duration: "Permanent",
      progress: 0,
      icon: Target,
      color: "text-green-600",
      bgColor: "bg-green-50",
      details: {
        skills: ["Full-Stack Development", "Problem Solving", "Teamwork", "Continuous Learning"],
        resources: ["Job placement support", "Interview preparation", "Career counseling"],
        nextSteps: "Begin job applications and interviews",
        salary: "₹6-12 LPA starting",
        companies: ["Tech Startups", "IT Services", "Product Companies"]
      }
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed": return "bg-green-500 border-green-500 text-white";
      case "current": return "bg-blue-500 border-blue-500 text-white animate-pulse";
      case "upcoming": return "bg-gray-300 border-gray-300 text-gray-600";
      default: return "bg-gray-300 border-gray-300 text-gray-600";
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case "completed": return "Completed";
      case "current": return "In Progress";
      case "upcoming": return "Upcoming";
      default: return "Not Started";
    }
  };

  useEffect(() => {
          document.title = `My Career Map ✦ ${siteConfig.name}`;
      }, []);

  return (
    <div className="min-h-screen bg-background p-4 pt-18 pb-24">
      {/* Header */}
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div className="flex items-center gap-4">
            <Button variant="outline" onClick={handleBack} className="flex items-center gap-2">
              <ChevronLeft size={16} />
              Back to Dashboard
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-foreground">Career Journey Map</h1>
              <p className="text-muted-foreground">Your personalized path to becoming a {careerPath.goal}</p>
            </div>
          </div>
          <Button variant="outline" onClick={handleLogout} className="flex items-center gap-2">
            <LogOut size={16} />
            Logout
          </Button>
        </div>

        {/* Career Path Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <Card className="bg-primary/5 border-primary/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-primary/10 rounded-lg">
                    <Target className="text-primary" size={24} />
                  </div>
                  <div>
                    <h2 className="text-xl font-semibold">Your Path to {careerPath.goal}</h2>
                    <p className="text-muted-foreground">
                      Estimated duration: {careerPath.duration} • Level: {careerPath.level}
                    </p>
                  </div>
                </div>
                <Badge variant="secondary" className="text-lg px-4 py-2">
                  {careerPath.match}% Path Match
                </Badge>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Journey Timeline - 3/4 width */}
          <div className="lg:col-span-3">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <MapPin className="text-primary" size={20} />
                    Your Learning Journey
                  </CardTitle>
                  <CardDescription>
                    Follow this step-by-step path to achieve your career goals
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-8">
                    {milestones.map((milestone, index) => {
                      const Icon = milestone.icon;
                      return (
                        <motion.div
                          key={milestone.id}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.5, delay: 0.1 * index }}
                        >
                          <div 
                            className={`flex gap-6 p-6 border rounded-lg cursor-pointer transition-all hover:shadow-md ${
                              selectedMilestone?.id === milestone.id ? 'ring-2 ring-primary' : ''
                            }`}
                            onClick={() => setSelectedMilestone(milestone)}
                          >
                            {/* Progress Connector */}
                            <div className="flex flex-col items-center">
                              <div className={`w-12 h-12 rounded-full flex items-center justify-center border-2 ${getStatusColor(milestone.status)}`}>
                                <Icon size={20} />
                              </div>
                              {index < milestones.length - 1 && (
                                <div className={`flex-1 w-0.5 mt-2 ${
                                  milestone.status === "completed" ? 'bg-green-500' : 
                                  milestone.status === "current" ? 'bg-blue-500' : 'bg-gray-300'
                                }`} style={{ height: '80px' }} />
                              )}
                            </div>

                            {/* Content */}
                            <div className="flex-1">
                              <div className="flex items-start justify-between mb-3">
                                <div>
                                  <h3 className="text-lg font-semibold flex items-center gap-2">
                                    {milestone.title}
                                    <Badge 
                                      variant={
                                        milestone.status === "completed" ? "default" :
                                        milestone.status === "current" ? "secondary" : "outline"
                                      }
                                    >
                                      {getStatusText(milestone.status)}
                                    </Badge>
                                  </h3>
                                  <p className="text-muted-foreground mt-1">{milestone.description}</p>
                                </div>
                                <div className="text-right">
                                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                                    <Clock size={14} />
                                    <span>{milestone.duration}</span>
                                  </div>
                                  {milestone.progress > 0 && (
                                    <div className="w-32 mt-2">
                                      <Progress value={milestone.progress} className="h-2" />
                                      <span className="text-xs text-muted-foreground">{milestone.progress}%</span>
                                    </div>
                                  )}
                                </div>
                              </div>

                              {/* Skills Preview */}
                              <div className="flex flex-wrap gap-2">
                                {milestone.details.skills.slice(0, 3).map((skill, skillIndex) => (
                                  <Badge key={skillIndex} variant="outline" className="text-xs">
                                    {skill}
                                  </Badge>
                                ))}
                                {milestone.details.skills.length > 3 && (
                                  <Badge variant="outline" className="text-xs">
                                    +{milestone.details.skills.length - 3} more
                                  </Badge>
                                )}
                              </div>

                              {/* Action Button */}
                              {milestone.status === "current" && (
                                <Button className="mt-4 flex items-center gap-2">
                                  Continue Learning
                                  <ArrowRight size={16} />
                                </Button>
                              )}
                              {milestone.status === "upcoming" && (
                                <Button variant="outline" className="mt-4">
                                  Preview Content
                                </Button>
                              )}
                            </div>
                          </div>
                        </motion.div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>

          {/* Sidebar - Milestone Details */}
          <div className="space-y-6">
            {/* Selected Milestone Details */}
            {selectedMilestone ? (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      {React.createElement(selectedMilestone.icon, { 
                        className: selectedMilestone.color,
                        size: 20 
                      })}
                      {selectedMilestone.title}
                    </CardTitle>
                    <CardDescription>
                      {selectedMilestone.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* Status */}
                    <div>
                      <h4 className="font-medium mb-2">Status</h4>
                      <Badge 
                        variant={
                          selectedMilestone.status === "completed" ? "default" :
                          selectedMilestone.status === "current" ? "secondary" : "outline"
                        }
                      >
                        {getStatusText(selectedMilestone.status)}
                      </Badge>
                    </div>

                    {/* Duration */}
                    <div>
                      <h4 className="font-medium mb-2">Duration</h4>
                      <p className="text-sm text-muted-foreground">{selectedMilestone.duration}</p>
                    </div>

                    {/* Skills */}
                    <div>
                      <h4 className="font-medium mb-2">Skills You'll Learn</h4>
                      <div className="flex flex-wrap gap-1">
                        {selectedMilestone.details.skills.map((skill: string | number | bigint | boolean | React.ReactElement<unknown, string | React.JSXElementConstructor<any>> | Iterable<React.ReactNode> | React.ReactPortal | Promise<string | number | bigint | boolean | React.ReactPortal | React.ReactElement<unknown, string | React.JSXElementConstructor<any>> | Iterable<React.ReactNode> | null | undefined> | null | undefined, index: React.Key | null | undefined) => (
                          <Badge key={index} variant="secondary" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Resources */}
                    <div>
                      <h4 className="font-medium mb-2">Resources</h4>
                      <ul className="text-sm text-muted-foreground space-y-1">
                        {selectedMilestone.details.resources.map((resource: string | number | bigint | boolean | React.ReactElement<unknown, string | React.JSXElementConstructor<any>> | Iterable<React.ReactNode> | React.ReactPortal | Promise<string | number | bigint | boolean | React.ReactPortal | React.ReactElement<unknown, string | React.JSXElementConstructor<any>> | Iterable<React.ReactNode> | null | undefined> | null | undefined, index: React.Key | null | undefined) => (
                          <li key={index}>• {resource}</li>
                        ))}
                      </ul>
                    </div>

                    {/* Next Steps */}
                    <div>
                      <h4 className="font-medium mb-2">Next Steps</h4>
                      <p className="text-sm text-muted-foreground">{selectedMilestone.details.nextSteps}</p>
                    </div>

                    {/* Provider/Level if available */}
                    {selectedMilestone.details.provider && (
                      <div>
                        <h4 className="font-medium mb-2">Provider</h4>
                        <p className="text-sm text-muted-foreground">{selectedMilestone.details.provider}</p>
                        <p className="text-xs text-muted-foreground">Level: {selectedMilestone.details.level}</p>
                      </div>
                    )}

                    {/* Salary info for job milestone */}
                    {selectedMilestone.details.salary && (
                      <div>
                        <h4 className="font-medium mb-2">Expected Salary</h4>
                        <p className="text-sm text-muted-foreground">{selectedMilestone.details.salary}</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
              >
                <Card>
                  <CardContent className="p-6 text-center">
                    <Star className="mx-auto text-muted-foreground mb-4" size={32} />
                    <h3 className="font-medium mb-2">Select a Milestone</h3>
                    <p className="text-sm text-muted-foreground">
                      Click on any milestone in your journey to see detailed information and next steps.
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {/* Quick Stats */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Journey Summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Total Milestones</span>
                    <span className="font-semibold">{milestones.length}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Completed</span>
                    <span className="font-semibold text-green-600">
                      {milestones.filter(m => m.status === "completed").length}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">In Progress</span>
                    <span className="font-semibold text-blue-600">
                      {milestones.filter(m => m.status === "current").length}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Remaining</span>
                    <span className="font-semibold">
                      {milestones.filter(m => m.status === "upcoming").length}
                    </span>
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