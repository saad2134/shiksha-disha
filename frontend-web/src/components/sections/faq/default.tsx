import Link from "next/link";
import { ReactNode } from "react";

import { siteConfig } from "@/config/site";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "../../ui/accordion";
import { Section } from "../../ui/section";

interface FAQItemProps {
  question: string;
  answer: ReactNode;
  value?: string;
}

interface FAQProps {
  title?: string;
  items?: FAQItemProps[] | false;
  className?: string;
}

export default function FAQ({
  title = "Questions and Answers",
  items = [
    {
      question:
        "What is the purpose of this AI-powered learning path generator?",
      answer: (
        <>
          <p className="text-muted-foreground mb-4 max-w-[640px] text-balance">
            It helps learners discover personalized vocational training paths aligned to their background, skills, and career goals, dynamically updating as they progress or job market demands change.
          </p>
        </>
      ),
    },
    {
      question: "How does the system create personalized learning paths?",
      answer: (
        <>
          <p className="text-muted-foreground mb-4 max-w-[600px]">
            Using AI/ML, it analyzes learner profiles including education, skills, social context, and aspirations, then matches requirements with NSQF-aligned courses and industry needs.
          </p>
        </>
      ),
    },
    {
      question:
        "Who can use this platform?",
      answer: (
        <>
          <p className="text-muted-foreground mb-4 max-w-[580px]">
            Learners seeking career guidance, trainers monitoring learner progress, and policymakers tracking skill demand and training outcomes.
          </p>
        </>
      ),
    },
    {
      question: 'Is this platform accessible in multiple languages?',
      answer: (
        <>
          <p className="text-muted-foreground mb-4 max-w-[580px]">
            Yes, it supports several Indian languages with simple, inclusive UI designed for easy mobile use.
          </p>
        </>
      ),
    },
    {
      question: "How does the platform ensure alignment with current job market needs?",
      answer: (
        <p className="text-muted-foreground mb-4 max-w-[580px]">
          It continuously integrates real-time labor market data to adjust course and skill recommendations.
        </p>
      ),
    },
    {
      question: "What types of training and credentials are recommended?",
      answer: (
        <>
          <p className="text-muted-foreground mb-4 max-w-[580px]">
            Vocational courses, micro-credentials, certifications, internships, apprenticeships, and on-the-job training opportunities.
          </p>
        </>
      ),
    },
    {
      question: "Can trainers and policymakers access learner progress and skill demand data?",
      answer: (
        <>
          <p className="text-muted-foreground mb-4 max-w-[580px]">
            Yes, dedicated dashboards provide progress insights for trainers and demand-supply analytics for policymakers.
          </p>
        </>
      ),
    },
    {
      question: "Is this solution scalable to handle millions of learners?",
      answer: (
        <>
          <p className="text-muted-foreground mb-4 max-w-[580px]">
            The system is designed with scalable architecture to manage large user volumes efficiently.
          </p>
        </>
      ),
    },
  ],
  className,
}: FAQProps) {
  return (
    <Section className={className}>
      <div className="max-w-container mx-auto flex flex-col items-center gap-8 px-4">
        <h2 className="text-center text-3xl font-semibold sm:text-5xl">
          {title}
        </h2>
        {items !== false && items.length > 0 && (
          <Accordion type="single" collapsible className="w-full max-w-[800px]">
            {items.map((item, index) => (
              <AccordionItem
                key={index}
                value={item.value || `item-${index + 1}`}
              >
                <AccordionTrigger>{item.question}</AccordionTrigger>
                <AccordionContent>{item.answer}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        )}
      </div>
    </Section>
  );
}
