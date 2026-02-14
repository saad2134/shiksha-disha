"use client";
import React from 'react';
import { Check, Sparkles, Zap, Users, TrendingUp, Shield, Award, Rocket } from 'lucide-react';

const PricingPage: React.FC = () => {
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-purple-950 to-black text-white">
      {/* Header Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-purple-600/20 to-transparent"></div>
        <div className="relative max-w-7xl mx-auto px-6 py-16 text-center">
          <div className="inline-flex items-center gap-2 bg-purple-500/20 border border-purple-500/30 rounded-full px-6 py-2 mb-6">
            <Sparkles className="w-4 h-4 text-purple-400" />
            <span className="text-sm font-medium text-purple-300">Transparent Pricing</span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-purple-300 to-white bg-clip-text text-transparent">
            Pricing
          </h1>
          
          <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
            Choose the plan that fits your learning journey. Start free, upgrade when you're ready to accelerate your career.
          </p>
        </div>
      </div>

      {/* Pricing Cards */}
      <div className="max-w-7xl mx-auto px-6 pb-24">
        <div className="flex flex-col lg:flex-row gap-8 items-stretch">
          
          {/* Freemium Card */}
          <div className="flex-1 bg-gradient-to-br from-gray-900 to-black rounded-3xl border border-gray-800 overflow-hidden hover:border-purple-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/20">
            <div className="p-8">
              {/* Card Header */}
              <div className="mb-8">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-12 h-12 bg-gray-800 rounded-xl flex items-center justify-center">
                    <Users className="w-6 h-6 text-gray-400" />
                  </div>
                  <h2 className="text-3xl font-bold text-white">Freemium</h2>
                </div>
                
                <div className="mb-6">
                  <div className="flex items-baseline gap-2">
                    <span className="text-5xl font-bold text-white">$0</span>
                    <span className="text-gray-400 text-lg">/forever</span>
                  </div>
                  <p className="text-gray-400 mt-2">Perfect for exploring and getting started</p>
                </div>

                <button className="w-full bg-gray-800 hover:bg-gray-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-200 border border-gray-700 hover:border-gray-600">
                  Get Started Free
                </button>
              </div>

              {/* Features List */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 mb-6">
                  <div className="h-px flex-1 bg-gradient-to-r from-transparent via-gray-700 to-transparent"></div>
                  <span className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Features</span>
                  <div className="h-px flex-1 bg-gradient-to-r from-transparent via-gray-700 to-transparent"></div>
                </div>
                
                {freemiumFeatures.map((feature, index) => (
                  <div key={index} className="flex items-start gap-3 group">
                    <div className="flex-shrink-0 w-5 h-5 rounded-full bg-gray-800 flex items-center justify-center mt-0.5 group-hover:bg-gray-700 transition-colors">
                      <Check className="w-3 h-3 text-gray-400" />
                    </div>
                    <span className="text-gray-300 leading-relaxed">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Premium Card */}
          <div className="flex-1 bg-gradient-to-br from-purple-900 via-purple-800 to-purple-900 rounded-3xl border-2 border-purple-500 overflow-hidden relative hover:shadow-2xl hover:shadow-purple-500/40 transition-all duration-300 transform hover:scale-105">
            {/* Popular Badge */}
            <div className="absolute top-0 right-0 bg-gradient-to-r from-yellow-400 to-yellow-500 text-black text-xs font-bold px-6 py-2 rounded-bl-2xl flex items-center gap-1">
              <Award className="w-3 h-3" />
              MOST POPULAR
            </div>

            <div className="p-8">
              {/* Card Header */}
              <div className="mb-8">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-12 h-12 bg-purple-700 rounded-xl flex items-center justify-center">
                    <Rocket className="w-6 h-6 text-purple-200" />
                  </div>
                  <h2 className="text-3xl font-bold text-white">Premium</h2>
                </div>
                
                <div className="mb-6">
                  <div className="flex items-baseline gap-2">
                    <span className="text-5xl font-bold text-white">$15</span>
                    <span className="text-purple-200 text-lg">/month</span>
                  </div>
                  <p className="text-purple-200 mt-2">For serious learners ready to transform their career</p>
                </div>

                <button className="w-full bg-white hover:bg-gray-100 text-purple-900 font-bold py-4 px-6 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl flex items-center justify-center gap-2">
                  <Zap className="w-5 h-5" />
                  Start Premium Trial
                </button>
                
                <p className="text-center text-purple-200 text-sm mt-3">
                  14-day free trial • Cancel anytime
                </p>
              </div>

              {/* Features List */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 mb-6">
                  <div className="h-px flex-1 bg-gradient-to-r from-transparent via-purple-400/50 to-transparent"></div>
                  <span className="text-xs text-purple-200 uppercase tracking-wider font-semibold">Everything Included</span>
                  <div className="h-px flex-1 bg-gradient-to-r from-transparent via-purple-400/50 to-transparent"></div>
                </div>
                
                {premiumFeatures.map((feature, index) => (
                  <div key={index} className="flex items-start gap-3 group">
                    <div className="flex-shrink-0 w-5 h-5 rounded-full bg-purple-700 flex items-center justify-center mt-0.5 group-hover:bg-purple-600 transition-colors">
                      <Check className="w-3 h-3 text-purple-200" />
                    </div>
                    <span className={`leading-relaxed ${index === 0 ? 'text-purple-100 font-semibold' : 'text-purple-100'}`}>
                      {feature}
                    </span>
                  </div>
                ))}
              </div>

              {/* Value Highlight */}
              <div className="mt-8 p-4 bg-purple-950/50 border border-purple-500/30 rounded-xl">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-4 h-4 text-purple-300" />
                  <span className="text-sm font-semibold text-purple-300">Premium Value</span>
                </div>
                <p className="text-xs text-purple-200">
                  Includes 1 free coaching session worth $199 + unlimited access to all premium features
                </p>
              </div>
            </div>
          </div>

        </div>

        {/* Bottom Section */}
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-2 bg-purple-500/10 border border-purple-500/20 rounded-full px-6 py-3">
            <Shield className="w-5 h-5 text-purple-400" />
            <span className="text-sm text-purple-300">
              All plans include 256-bit SSL encryption and GDPR compliance
            </span>
          </div>
          
          <p className="mt-8 text-gray-400 max-w-2xl mx-auto">
            Need an enterprise solution for your team? 
            <a href="#" className="text-purple-400 hover:text-purple-300 ml-2 font-semibold underline underline-offset-4">
              Contact us for custom pricing
            </a>
          </p>
        </div>
      </div>

      {/* FAQ or Additional Info Section */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-6 py-16">
          <h3 className="text-2xl font-bold text-center mb-12 text-white">
            Why Upgrade to Premium?
          </h3>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-gradient-to-br from-purple-900/20 to-transparent rounded-2xl border border-purple-500/20">
              <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mx-auto mb-4">
                <Sparkles className="w-6 h-6 text-purple-400" />
              </div>
              <h4 className="text-lg font-semibold mb-2 text-white">Advanced AI</h4>
              <p className="text-gray-400 text-sm">
                Our premium AI learns from your behavior and optimizes recommendations for your exact learning style
              </p>
            </div>
            
            <div className="text-center p-6 bg-gradient-to-br from-purple-900/20 to-transparent rounded-2xl border border-purple-500/20">
              <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-6 h-6 text-purple-400" />
              </div>
              <h4 className="text-lg font-semibold mb-2 text-white">Career Acceleration</h4>
              <p className="text-gray-400 text-sm">
                Career simulator and skill gap analysis show you exactly what to learn for your dream job
              </p>
            </div>
            
            <div className="text-center p-6 bg-gradient-to-br from-purple-900/20 to-transparent rounded-2xl border border-purple-500/20">
              <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mx-auto mb-4">
                <Award className="w-6 h-6 text-purple-400" />
              </div>
              <h4 className="text-lg font-semibold mb-2 text-white">Expert Guidance</h4>
              <p className="text-gray-400 text-sm">
                Included 1-on-1 consultation helps you avoid costly mistakes and wasted time on wrong courses
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingPage;