import { Metadata } from "next";
import { StudentSidebar } from "./student-layout-client";

export const metadata: Metadata = {
  robots: {
    index: false,
    follow: false,
  },
};

export default function StudentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <StudentSidebar>{children}</StudentSidebar>;
}
