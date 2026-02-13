"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  MapPin,
  Trophy,
  MessageSquare,
  BarChart3,
  Sparkles,
  LogOut,
  Settings,
  Bell,
  Search
} from "lucide-react";
import AppUI from "@/components/logos/app_icon";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";

const demoNavItems = [
  {
    title: "Dashboard",
    url: "/demo/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "Career Map",
    url: "/demo/career_map",
    icon: MapPin,
  },
  {
    title: "Achievements",
    url: "/demo/achievements",
    icon: Trophy,
  },
  {
    title: "AI Companion",
    url: "/demo/ai-companion",
    icon: MessageSquare,
  },
  {
    title: "Leaderboard",
    url: "/demo/leaderboard",
    icon: BarChart3,
  },
  {
    title: "Market Insights",
    url: "/demo/insights",
    icon: Sparkles,
  },
];

export default function DemoLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <DemoSidebar>{children}</DemoSidebar>;
}

function DemoSidebar({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  if (pathname === "/demo/onboarding") {
    return <>{children}</>;
  }

  return (
    <SidebarProvider defaultOpen={true}>
      <Sidebar collapsible="offcanvas" className="border-r">
        <SidebarHeader className="py-4">
          <div className="flex items-center gap-3 px-2">
            <AppUI className="w-10 h-10" />
            <div className="flex flex-col">
              <span className="font-semibold text-sm">ShikshaDisha</span>
              <span className="text-xs text-muted-foreground">Demo Mode</span>
            </div>
          </div>
        </SidebarHeader>
        
        <SidebarContent>
          <SidebarGroup>
            <SidebarGroupLabel>Navigation</SidebarGroupLabel>
            <SidebarMenu>
              {demoNavItems.map((item) => {
                const isActive = pathname === item.url;
                return (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild isActive={isActive}>
                      <Link href={item.url} className="flex items-center gap-3">
                        <item.icon className={isActive ? "text-violet-500" : ""} />
                        <span>{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroup>
          
          <SidebarGroup className="mt-auto">
            <SidebarGroupLabel>Quick Links</SidebarGroupLabel>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <Link href="/demo/dashboard" className="flex items-center gap-3">
                    <Search size={18} />
                    <span>Browse Courses</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <Link href="/" className="flex items-center gap-3">
                    <LogOut size={18} />
                    <span>Logout (Exit Demo)</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroup>
        </SidebarContent>
        
        <SidebarFooter className="p-4 border-t">
          <div className="flex items-center gap-3 p-2 rounded-lg bg-muted/50">
            <div className="w-10 h-10 rounded-full bg-violet-100 dark:bg-violet-900/30 flex items-center justify-center font-semibold text-sm">
              SM
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">Saad Mohammed</p>
              <p className="text-xs text-muted-foreground">Level 8 • 2,450 pts</p>
            </div>
          </div>
        </SidebarFooter>
      </Sidebar>
      
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4 sticky top-0 z-10 bg-background/80 backdrop-blur-md">
          <SidebarTrigger />
          <div className="flex-1">
            <h1 className="text-lg font-semibold">
              {demoNavItems.find(item => item.url === pathname)?.title || "Demo"}
            </h1>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon">
              <Bell size={18} />
            </Button>
            <Button variant="ghost" size="icon">
              <Settings size={18} />
            </Button>
          </div>
        </header>
        <div className="flex flex-1 flex-col">
          {children}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
