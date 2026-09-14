import { Metadata } from "next";
import { DemoSidebar } from "./demo-layout-client";

export const metadata: Metadata = {
  robots: {
    index: false,
    follow: false,
  },
};

export default function DemoLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <DemoSidebar>{children}</DemoSidebar>;
}
