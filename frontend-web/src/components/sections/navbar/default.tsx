import { Menu } from "lucide-react";
import { ReactNode } from "react";

import { siteConfig } from "@/config/site";
import { cn } from "@/lib/utils";

import AppUI from "../../logos/app_icon";
import { Button, type ButtonProps } from "../../ui/button";
import {
  Navbar as NavbarComponent,
  NavbarLeft,
  NavbarRight,
} from "../../ui/navbar";
import Navigation from "../../ui/navigation";
import { Sheet, SheetContent, SheetTrigger } from "../../ui/sheet";

interface NavbarLink {
  text: string;
  href: string;
}

interface NavbarActionProps {
  text: string;
  href: string;
  variant?: ButtonProps["variant"];
  icon?: ReactNode;
  iconRight?: ReactNode;
  isButton?: boolean;
}

interface NavbarProps {
  logo?: ReactNode;
  name?: string;
  homeUrl?: string;
  mobileLinks?: NavbarLink[];
  actions?: NavbarActionProps[];
  showNavigation?: boolean;
  customNavigation?: ReactNode;
  className?: string;
}

export default function Navbar({
  logo = <AppUI />,
  name =  `${siteConfig.name}`,
  homeUrl = '/',
  mobileLinks = [
    { text: "Getting Started", href: '/student/onboarding' },
  ],
  actions = [
    { text: "Sign in", href: '/student/onboarding', isButton: false },
    {
      text: "Get Started",
      href: '/student/onboarding',
      isButton: true,
      variant: "default",
    },
  ],
  showNavigation = true,
  customNavigation,
  className,
}: NavbarProps) {
  return (
    <header className={cn("fixed top-0 left-0 w-full z-50", className)}>
      <div className="max-w-container mx-auto flex items-center justify-between px-4 py-4">
        <NavbarComponent className="bg-violet-500/10 backdrop-blur-sm w-full flex items-center justify-between px-8 rounded-xl">

          <NavbarLeft>
            <a
              href={homeUrl}
              className="flex items-center gap-2 text-xl font-bold"
            >
              {logo}
              {name}
            </a>
          </NavbarLeft>
          {/* NavbarRight buttons hidden on mobile */}
          <NavbarRight className="hidden md:flex items-center gap-4">
            {actions.map((action, index) =>
              action.isButton ? (
                <Button
                  key={index}
                  variant={action.variant || "default"}
                  asChild
                >
                  <a href={action.href}>
                    {action.icon}
                    {action.text}
                    {action.iconRight}
                  </a>
                </Button>
              ) : (
                <a
                  key={index}
                  href={action.href}
                  className="text-sm"
                >
                  {action.text}
                </a>
              ),
            )}
          </NavbarRight>
          {/* Mobile menu toggle always visible on mobile */}
          <Sheet>
            <SheetTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="shrink-0 md:hidden"
              >
                <Menu className="size-5" />
                <span className="sr-only">Toggle navigation menu</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="right">
              <nav className="grid gap-6 text-lg font-medium">
                <a
                  href={homeUrl}
                  className="flex items-center gap-2 text-xl font-bold"
                >
                  <span>{name}</span>
                </a>
                {mobileLinks.map((link, index) => (
                  <a
                    key={index}
                    href={link.href}
                    className="text-muted-foreground hover:text-foreground"
                  >
                    {link.text}
                  </a>
                ))}
              </nav>
            </SheetContent>
          </Sheet>
        </NavbarComponent>
      </div>
    </header>



  );
}
