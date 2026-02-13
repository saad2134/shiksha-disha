import Link from "next/link";
import { ReactNode } from "react";

import { siteConfig } from "@/config/site";
import { faqConfig } from "@/config/faqConfig";

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
  items = faqConfig.map((item) => ({
    ...item,
    answer: (
      <p className="text-muted-foreground mb-4 max-w-[580px]">
        {item.answer}
      </p>
    ),
  })),
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
