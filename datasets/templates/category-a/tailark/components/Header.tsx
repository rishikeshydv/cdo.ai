"use client";
import React from 'react'
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Menu, X } from "lucide-react";
export default function Header() {
    const menuItems = [
  { name: "Features", href: "#link" },
  { name: "Solution", href: "#link" },
  { name: "Pricing", href: "#link" },
  { name: "About", href: "#link" },
];
  const [menuState, setMenuState] = React.useState(false);
    const [isScrolled, setIsScrolled] = React.useState(false);

      React.useEffect(() => {
        const handleScroll = () => {
          setIsScrolled(window.scrollY > 50);
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
      }, []);
    
  return (
    <header className="sticky top-0 z-30">
      <nav
        data-state={menuState && "active"}
        className="fixed inset-x-0 top-0 z-30 px-3 sm:px-4"
      >
        <div
          className={cn(
            "mx-auto mt-2 w-full max-w-6xl rounded-2xl bg-background/60 px-4 py-4 shadow-sm backdrop-blur-lg transition-all duration-300 ease-out sm:px-6 lg:px-12",
            isScrolled &&
              "max-w-5xl lg:max-w-4xl bg-background/85 border border-border/70 shadow-lg px-4 sm:px-5 lg:px-8 py-3"
          )}
        >
          <div className="flex items-center justify-between gap-3">
            <div className="text-xl sm:text-2xl font-bold tracking-tighter">
              Company Name
            </div>

            <button
              onClick={() => setMenuState(!menuState)}
              aria-label={menuState ? "Close Menu" : "Open Menu"}
              className="relative z-20 -m-2.5 block cursor-pointer p-2.5 lg:hidden"
            >
              <Menu
                className={cn(
                  "m-auto size-6 transition duration-200",
                  menuState && "rotate-180 scale-0 opacity-0"
                )}
              />
              <X
                className={cn(
                  "absolute inset-0 m-auto size-6 -rotate-180 scale-0 opacity-0 transition duration-200",
                  menuState && "rotate-0 scale-100 opacity-100"
                )}
              />
            </button>

            <div className="hidden lg:flex items-center gap-10 text-sm">
              {menuItems.map((item, index) => (
                <Link
                  key={index}
                  href={item.href}
                  className="text-muted-foreground hover:text-accent-foreground transition"
                >
                  {item.name}
                </Link>
              ))}
            </div>

            <div className="hidden lg:flex items-center gap-3">
              <Button asChild variant="outline" size="sm">
                <Link href="#">
                  <span>Login</span>
                </Link>
              </Button>
              <Button asChild size="sm">
                <Link href="#">
                  <span>Sign Up</span>
                </Link>
              </Button>
            </div>
          </div>
        </div>

        {/* Mobile panel */}
        <div
          className={cn(
            "lg:hidden transition-[max-height,opacity] duration-300 ease-out overflow-hidden",
            menuState ? "max-h-[70vh] opacity-100" : "max-h-0 opacity-0"
          )}
        >
          <div className="mx-auto mt-2 w-full max-w-6xl rounded-2xl border border-border/60 bg-background/90 px-4 py-6 shadow-lg backdrop-blur-lg sm:px-6 lg:px-10">
            <ul className="space-y-4 text-base">
              {menuItems.map((item, index) => (
                <li key={index}>
                  <Link
                    href={item.href}
                    className="block text-foreground hover:text-accent-foreground transition"
                    onClick={() => setMenuState(false)}
                  >
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
            <div className="mt-6 flex flex-col gap-3">
              <Button asChild variant="outline" size="sm">
                <Link href="#">
                  <span>Login</span>
                </Link>
              </Button>
              <Button asChild size="sm">
                <Link href="#">
                  <span>Sign Up</span>
                </Link>
              </Button>
              <Button asChild size="sm" variant="secondary">
                <Link href="#">
                  <span>Get Started</span>
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </nav>
    </header>
  );
}
