"use client";
import React from 'react';
import { Check, Sparkles, Zap, Users, TrendingUp, Shield, Award, Rocket } from 'lucide-react';

const freemiumFeatures = [
  'AI-powered course recommendations',
  'Basic learning style assessment',
  'Access to 10,000+ courses across platforms',
  'Job market salary insights',
  'Course quality ratings & reviews',
  'Learning path suggestions',
  'Community forum access',
  'Mobile app access'
];

const premiumFeatures = [
  'Everything in Freemium, plus:',
  'Advanced AI personalization engine',
  'Unlimited personalized learning paths',
  'Career trajectory simulator',
  'Skill gap analysis & roadmaps',
  'Progress tracking across all platforms',
  'Weekly accountability emails',
  'Course comparison tools',
  'Downloadable learning reports (PDF)',
  'Priority support (24-hour response)',
  '1-on-1 learning path consultation ($199 value)',
  'Study schedule optimizer',
  'Certificate of completion tracking',
  'Ad-free experience'
];

interface PricingCardsProps {
  className?: string;
  compact?: boolean;
}

export const PricingCards: React.FC<PricingCardsProps> = ({ className = "", compact = false }) => {
  return (
    <div className={className}>
      <div className="flex flex-col lg:flex-row gap-6 lg:gap-8 items-stretch">
        {/* Freemium Card */}
        <div className="flex-1 bg-card text-card-foreground rounded-2xl border border-border overflow-hidden hover:border-primary/50 transition-all duration-300 hover:shadow-lg">
          <div className={compact ? "p-5 lg:p-6" : "p-6 lg:p-8"}>
            {/* Card Header */}
            <div className="mb-5">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 lg:w-12 lg:h-12 bg-muted rounded-xl flex items-center justify-center">
                  <Users className="w-5 h-5 lg:w-6 lg:h-6 text-muted-foreground" />
                </div>
                <h2 className="text-2xl lg:text-3xl font-bold">Freemium</h2>
              </div>
              
              <div className="mb-5">
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl lg:text-5xl font-bold">$0</span>
                  <span className="text-muted-foreground text-lg">/forever</span>
                </div>
                <p className="text-muted-foreground mt-2 text-sm lg:text-base">Perfect for exploring and getting started</p>
              </div>

              <button className="w-full bg-secondary hover:bg-secondary/80 text-secondary-foreground font-semibold py-3 lg:py-4 px-5 lg:px-6 rounded-xl transition-all duration-200 border border-border hover:border-primary/30">
                Get Started Free
              </button>

              <p className="text-center text-muted-foreground text-xs lg:text-sm mt-3">
                Free Forever
              </p>
            </div>

            {/* Features List */}
            <div className="space-y-3 lg:space-y-4">
              <div className="flex items-center gap-2 mb-4 lg:mb-6">
                <div className="h-px flex-1 bg-gradient-to-r from-transparent via-border to-transparent"></div>
                <span className="text-xs text-muted-foreground uppercase tracking-wider font-semibold">Features</span>
                <div className="h-px flex-1 bg-gradient-to-r from-transparent via-border to-transparent"></div>
              </div>
              
              {freemiumFeatures.map((feature, index) => (
                <div key={index} className="flex items-start gap-3 group">
                  <div className="flex-shrink-0 w-5 h-5 rounded-full bg-muted flex items-center justify-center mt-0.5 group-hover:bg-muted/80 transition-colors">
                    <Check className="w-3 h-3 text-muted-foreground" />
                  </div>
                  <span className="text-sm lg:text-base leading-relaxed">{feature}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Premium Card */}
        <div className="flex-1 bg-gradient-to-br from-primary/10 via-card to-card rounded-2xl border-2 border-primary/30 overflow-hidden relative hover:shadow-xl hover:border-primary/50 transition-all duration-300">
          {/* Popular Badge */}
          <div className="absolute top-0 right-0 bg-gradient-to-r from-amber-400 to-amber-500 text-amber-950 text-xs font-bold px-4 lg:px-6 py-1.5 lg:py-2 rounded-bl-xl lg:rounded-bl-2xl flex items-center gap-1">
            <Award className="w-3 h-3" />
            MOST POPULAR
          </div>

          <div className={compact ? "p-5 lg:p-6" : "p-6 lg:p-8"}>
            {/* Card Header */}
            <div className="mb-5">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 lg:w-12 lg:h-12 bg-primary/20 rounded-xl flex items-center justify-center">
                  <Rocket className="w-5 h-5 lg:w-6 lg:h-6 text-primary" />
                </div>
                <h2 className="text-2xl lg:text-3xl font-bold">Premium</h2>
              </div>
              
              <div className="mb-5">
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl lg:text-5xl font-bold">$15</span>
                  <span className="text-primary text-lg">/month</span>
                </div>
                <p className="text-primary/80 mt-2 text-sm lg:text-base">For serious learners ready to transform their career</p>
              </div>

              <button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-3 lg:py-4 px-5 lg:px-6 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl flex items-center justify-center gap-2">
                <Zap className="w-4 h-4 lg:w-5 lg:h-5" />
                Start Premium Trial
              </button>
              
              <p className="text-center text-muted-foreground text-xs lg:text-sm mt-3">
                14-day free trial • Cancel anytime
              </p>
            </div>

            {/* Features List */}
            <div className="space-y-3 lg:space-y-4">
              <div className="flex items-center gap-2 mb-4 lg:mb-6">
                <div className="h-px flex-1 bg-gradient-to-r from-transparent via-primary/30 to-transparent"></div>
                <span className="text-xs text-primary/80 uppercase tracking-wider font-semibold">Everything Included</span>
                <div className="h-px flex-1 bg-gradient-to-r from-transparent via-primary/30 to-transparent"></div>
              </div>
              
              {premiumFeatures.map((feature, index) => (
                <div key={index} className="flex items-start gap-3 group">
                  <div className="flex-shrink-0 w-5 h-5 rounded-full bg-primary/20 flex items-center justify-center mt-0.5 group-hover:bg-primary/30 transition-colors">
                    <Check className="w-3 h-3 text-primary" />
                  </div>
                  <span className={`text-sm lg:text-base leading-relaxed ${index === 0 ? 'font-semibold' : ''}`}>
                    {feature}
                  </span>
                </div>
              ))}
            </div>

            {/* Value Highlight */}
            <div className="mt-6 lg:mt-8 p-4 bg-primary/5 border border-primary/20 rounded-xl">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-4 h-4 text-primary" />
                <span className="text-sm font-semibold text-primary">Premium Value</span>
              </div>
              <p className="text-xs lg:text-sm text-muted-foreground">
                Includes 1 free coaching session worth $199 + unlimited access to all premium features
              </p>
            </div>
          </div>
        </div>
      </div>

      <p className="mt-4 text-xs text-center text-muted-foreground">
        Not satisfied? Check our{' '}
        <a href="/refunds" className="text-primary hover:text-primary/80 underline underline-offset-2">
          Refunds Policy
        </a>
        {' '}for information on cancellations and refunds.
      </p>
    </div>
  );
};

interface PricingSectionProps {
  showHeader?: boolean;
  showBottom?: boolean;
}

export const PricingSection: React.FC<PricingSectionProps> = ({ 
  showHeader = true, 
  showBottom = true 
}) => {
  return (
    <div className="w-full">
      {showHeader && (
        <div className="relative overflow-hidden py-12 lg:py-16">
          <div className="absolute inset-0 "></div>
          <div className="relative max-w-4xl mx-auto px-4 lg:px-6 text-center">
            <div className="inline-flex items-center gap-2 bg-primary/10 border border-primary/20 rounded-full px-4 lg:px-6 py-2 mb-4 lg:mb-6">
              <Sparkles className="w-4 h-4 text-primary" />
              <span className="text-sm font-medium">Transparent Pricing</span>
            </div>
            
            <h1 className="text-3xl lg:text-5xl md:text-4xl lg:text-6xl font-bold mb-4 lg:mb-6">
              Pricing
            </h1>
            
            <p className="text-base lg:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Choose the plan that fits your learning journey. Start free, upgrade when you&apos;re ready to accelerate your career.
            </p>
          </div>
        </div>
      )}

      {/* Pricing Cards */}
      <div className="max-w-6xl mx-auto px-4 lg:px-6 pb-12 lg:pb-20">
        <PricingCards />

        {showBottom && (
          <div className="mt-12 lg:mt-16 text-center">
            <div className="inline-flex items-center gap-2 bg-primary/5 border border-primary/10 rounded-full px-4 lg:px-6 py-2 lg:py-3">
              <Shield className="w-4 lg:w-5 h-4 lg:h-5 text-primary" />
              <span className="text-xs lg:text-sm text-muted-foreground">
                All plans include 256-bit SSL encryption and GDPR compliance
              </span>
            </div>
            
            <p className="mt-6 lg:mt-8 text-muted-foreground max-w-xl mx-auto text-sm lg:text-base">
              Need an enterprise solution for your team? 
              <a href="/contact" className="text-primary hover:text-primary/80 ml-1 lg:ml-2 font-semibold underline underline-offset-4">
                Contact us for custom pricing
              </a>
            </p>
          </div>
        )}
      </div>

      {showBottom && (
        <div className="border-t border-border">
          <div className="max-w-6xl mx-auto px-4 lg:px-6 py-12 lg:py-16">
            <h3 className="text-xl lg:text-2xl font-bold text-center mb-8 lg:mb-12">
              Why Upgrade to Premium?
            </h3>
            
            <div className="grid md:grid-cols-3 gap-6 lg:gap-8">
              <div className="text-center p-5 lg:p-6 bg-card border border-border rounded-2xl hover:border-primary/30 transition-colors">
                <div className="w-10 lg:w-12 h-10 lg:h-12 bg-primary/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <Sparkles className="w-5 lg:w-6 h-5 lg:h-6 text-primary" />
                </div>
                <h4 className="text-lg font-semibold mb-2">Advanced AI</h4>
                <p className="text-sm text-muted-foreground">
                  Our premium AI learns from your behavior and optimizes recommendations for your exact learning style
                </p>
              </div>
              
              <div className="text-center p-5 lg:p-6 bg-card border border-border rounded-2xl hover:border-primary/30 transition-colors">
                <div className="w-10 lg:w-12 h-10 lg:h-12 bg-primary/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <TrendingUp className="w-5 lg:w-6 h-5 lg:h-6 text-primary" />
                </div>
                <h4 className="text-lg font-semibold mb-2">Career Acceleration</h4>
                <p className="text-sm text-muted-foreground">
                  Career simulator and skill gap analysis show you exactly what to learn for your dream job
                </p>
              </div>
              
              <div className="text-center p-5 lg:p-6 bg-card border border-border rounded-2xl hover:border-primary/30 transition-colors">
                <div className="w-10 lg:w-12 h-10 lg:h-12 bg-primary/10 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <Award className="w-5 lg:w-6 h-5 lg:h-6 text-primary" />
                </div>
                <h4 className="text-lg font-semibold mb-2">Expert Guidance</h4>
                <p className="text-sm text-muted-foreground">
                  Included 1-on-1 consultation helps you avoid costly mistakes and wasted time on wrong courses
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PricingSection;
