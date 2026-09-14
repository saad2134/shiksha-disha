import { MetadataRoute } from "next";
import { siteConfig } from "@/config/site";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = siteConfig.url || "https://shikshadisha.vercel.app";

  const staticRoutes = [
    "",
    "/overview",
    "/pricing",
    "/plans-n-updates",
    "/contact",
    "/help-center",
    "/blog",
    "/team",
    "/terms",
    "/privacy",
    "/cookies",
    "/refunds",
    "/status",
  ].map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: "weekly" as const,
    priority: route === "" ? 1.0 : 0.8,
  }));

  const blogSlugs = [
    "how-ai-is-transforming-career-guidance-in-india",
    "top-10-in-demand-skills-for-2026",
    "from-classroom-to-career-bridging-the-skills-gap",
    "building-your-personal-learning-roadmap-with-ai",
    "micro-credentials-the-future-of-skill-verification",
    "shikshadisha-at-sudhee-cbit-hackathon-2026",
  ];

  const blogRoutes = blogSlugs.map((slug) => ({
    url: `${baseUrl}/blog/${slug}`,
    lastModified: new Date(),
    changeFrequency: "monthly" as const,
    priority: 0.7,
  }));

  return [...staticRoutes, ...blogRoutes];
}
