import "@/app/globals.css";
import { Metadata } from "next";

import { Providers } from "@/components/providers";
import { inter } from "@/lib/fonts";
import { siteConfig } from "@/config/site";

export const metadata: Metadata = {
  metadataBase: new URL(siteConfig.url),
  title: {
    default: `${siteConfig.name} ✦ Personalized Roadmaps for Future-ready Skills`,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description,
  keywords: [
    "AI Career Guidance",
    "Skill Roadmaps",
    "Personalized Learning",
    "India Education",
    "SUDHEE CBIT",
    "Upskilling",
  ],
  authors: [{ name: "DevBandits", url: siteConfig.links.github }],
  creator: "DevBandits",
  publisher: siteConfig.name,
  alternates: {
    canonical: "./",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: siteConfig.url,
    title: siteConfig.name,
    description: siteConfig.description,
    siteName: siteConfig.name,
    images: [
      {
        url: "/dashboard-dark.png",
        width: 1200,
        height: 630,
        alt: `${siteConfig.name} Dashboard Preview`,
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: siteConfig.name,
    description: siteConfig.description,
    images: ["/dashboard-dark.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="overflow-x-hidden ">
      <body className={`${inter.className}  antialiased overflow-x-hidden`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
