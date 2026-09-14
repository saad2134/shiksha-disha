import { siteConfig } from "@/config/site";
import CTA from "../components/sections/cta/default";
import FAQ from "../components/sections/faq/default";
import Footer from "../components/sections/footer/default";
import Hero from "../components/sections/hero/default";
import Items from "../components/sections/items/default";
import LearningEfficiency from "../components/sections/learning-efficiency/default";
import Navbar from "../components/sections/navbar/default";
import ProgrammingComputerSection from "../components/sections/programming-computer/default";
import MagicBento from '@/components/MagicBento'
import PricingSection from "@/components/pricing/pricing-card";
import { JsonLd } from "@/components/seo/json-ld";

export const metadata = {
  title: `${siteConfig.name} ✦ Personalized Roadmaps for Future-ready Skills`,
  description:
    "Discover your future-ready career journey with personalized training recommendations.",
  alternates: {
    canonical: "/",
  },
};

export default function Home() {
  const websiteSchema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: siteConfig.name,
    url: siteConfig.url,
    description: siteConfig.description,
  };

  const organizationSchema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: siteConfig.name,
    url: siteConfig.url,
    logo: `${siteConfig.url}/favicon.svg`,
    sameAs: [siteConfig.links.github],
  };

  return (
    <>
      <JsonLd data={websiteSchema} />
      <JsonLd data={organizationSchema} />
      <main className="min-h-screen w-full bg-background text-foreground overflow-x-hidden">
        <Navbar />
        <Hero />
        {/* <Logos /> */}
        {/* <Items /> */}
        <MagicBento
          textAutoHide={true}
          enableStars
          enableSpotlight
          enableBorderGlow={true}
          enableTilt={true}
          enableMagnetism={false}
          clickEffect
          spotlightRadius={400}
          particleCount={12}
          glowColor="145, 60, 255"
          disableAnimations={false}
        />
        <ProgrammingComputerSection />
        <LearningEfficiency />
        {/* <Stats /> */}
        <PricingSection />
        <FAQ />
        <CTA />
        <Footer />
      </main>
    </>

  );
}
