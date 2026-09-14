export const siteConfig = {
  name: "ShikshaDisha",
  version: "v1.0.0",
  url: process.env.NEXT_PUBLIC_SITE_URL || "https://shikshadisha.vercel.app",
  getStartedUrl:
    "/auth",
  description:
    "Your personalized roadmap to future-ready skills.",
  links: {
    twitter: "https://twitter.com/shikshadisha",
    github: "https://github.com/saad2134/shiksha-disha",
    email: "mailto:reach.saad@outlook.com",
    phone: "",
  },
};

export type SiteConfig = typeof siteConfig;
