import { siteConfig } from "@/config/site";
import CTA from "../components/sections/cta/default";
import FAQ from "../components/sections/faq/default";
import Footer from "../components/sections/footer/default";
import Hero from "../components/sections/hero/default";
import Items from "../components/sections/items/default";
import Navbar from "../components/sections/navbar/default";
import Pricing from "../components/sections/pricing/default";

export const metadata = {
  title: `${siteConfig.name} ✦ Personalized Roadmaps for Future-ready Skills`,
  description:
    "Discover your future-ready career journey with personalized training recommendations.",
};

export default function Home() {
  return (
    <>
      <main className="min-h-screen w-full overflow-hidden bg-background text-foreground">
        <Navbar />
        <Hero />
        {/* <Logos /> */}
        <Items />
        {/* <Stats /> */}
        {/* <Pricing /> */}
        <FAQ />
        <CTA />
        <Footer />
      </main>
    </>

  );
}
