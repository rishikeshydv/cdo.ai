"use client";

import { useState } from "react";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { ChevronRight, Github } from "lucide-react";

import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu";
import { cn } from "@/lib/utils";

const ITEMS = [
  {
    label: "Features",
    href: "#features",
    dropdownItems: [
      {
        title: "Modern product teams",
        href: "/#feature-modern-teams",
        description:
          "Mainline is built on the habits that make the best product teams successful",
      },
      {
        title: "Resource Allocation",
        href: "/#resource-allocation",
        description: "Mainline your resource allocation and execution",
      },
    ],
  },
  { label: "About Us", href: "/about" },
  { label: "Pricing", href: "/pricing" },
  { label: "FAQ", href: "/faq" },
  { label: "Contact", href: "/contact" },
];

export const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 bg-background/80 backdrop-blur-lg border-b border-border/60">
      <div className="relative mx-auto flex max-w-screen-xl flex-col px-4 sm:px-6 lg:px-10">
        <div className="flex h-16 sm:h-20 items-center justify-between gap-3">
          <Link href="/" className="text-xl sm:text-2xl font-bold tracking-tighter">
            Company Name
          </Link>

          {/* Desktop Navigation */}
          <NavigationMenu className="hidden lg:flex">
            <NavigationMenuList>
              {ITEMS.map((link) =>
                link.dropdownItems ? (
                  <NavigationMenuItem key={link.label}>
                    <NavigationMenuTrigger className="data-[state=open]:bg-accent/50 bg-transparent px-2 text-sm font-medium">
                      {link.label}
                    </NavigationMenuTrigger>
                    <NavigationMenuContent>
                      <ul className="w-[360px] space-y-2 p-4">
                        {link.dropdownItems.map((item) => (
                          <li key={item.title}>
                            <NavigationMenuLink asChild>
                              <Link
                                href={item.href}
                                className="group hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground flex items-center gap-4 rounded-md p-3 leading-none no-underline outline-hidden transition-colors select-none"
                              >
                                <div className="space-y-1.5 transition-transform duration-300 group-hover:translate-x-1">
                                  <div className="text-sm leading-none font-medium">
                                    {item.title}
                                  </div>
                                  <p className="text-muted-foreground line-clamp-2 text-sm leading-snug">
                                    {item.description}
                                  </p>
                                </div>
                              </Link>
                            </NavigationMenuLink>
                          </li>
                        ))}
                      </ul>
                    </NavigationMenuContent>
                  </NavigationMenuItem>
                ) : (
                  <NavigationMenuItem key={link.label}>
                    <Link
                      href={link.href}
                      className={cn(
                        "relative bg-transparent px-2 text-sm font-medium transition-opacity hover:opacity-75",
                        pathname === link.href && "text-muted-foreground",
                      )}
                    >
                      {link.label}
                    </Link>
                  </NavigationMenuItem>
                ),
              )}
            </NavigationMenuList>
          </NavigationMenu>

          {/* Right controls */}
          <div className="flex items-center gap-2.5">
            <ThemeToggle />
            <Link href="/login" className="hidden lg:inline-flex">
              <Button variant="outline" size="sm">
                <span className="relative z-10">Login</span>
              </Button>
            </Link>
            <a
              href="https://github.com/shadcnblocks/mainline-nextjs-template"
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              <Github className="size-4" />
              <span className="sr-only">GitHub</span>
            </a>

            {/* Hamburger Menu Button (Mobile/Tablet) */}
            <button
              className="text-muted-foreground relative flex size-10 items-center justify-center rounded-md border border-border/60 lg:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-expanded={isMenuOpen}
              aria-label="Toggle navigation"
            >
              <div className="block w-[18px]">
                <span
                  aria-hidden="true"
                  className={`absolute block h-0.5 w-[18px] rounded-full bg-current transition duration-500 ease-in-out ${isMenuOpen ? "translate-y-0 rotate-45" : "-translate-y-1.5"}`}
                ></span>
                <span
                  aria-hidden="true"
                  className={`absolute block h-0.5 w-[18px] rounded-full bg-current transition duration-500 ease-in-out ${isMenuOpen ? "opacity-0" : ""}`}
                ></span>
                <span
                  aria-hidden="true"
                  className={`absolute block h-0.5 w-[18px] rounded-full bg-current transition duration-500 ease-in-out ${isMenuOpen ? "translate-y-0 -rotate-45" : "translate-y-1.5"}`}
                ></span>
              </div>
            </button>
          </div>
        </div>

        {/* Mobile / Tablet menu */}
        <div
          className={cn(
            "lg:hidden overflow-hidden transition-[max-height,opacity] duration-300 ease-in-out",
            isMenuOpen ? "max-h-[520px] opacity-100" : "max-h-0 opacity-0",
          )}
        >
          <div className="mt-3 rounded-2xl border border-border/70 bg-background/95 p-6 shadow-lg">
            <nav className="divide-border flex flex-1 flex-col divide-y">
              {ITEMS.map((link) =>
                link.dropdownItems ? (
                  <div key={link.label} className="py-4 first:pt-0 last:pb-0">
                    <button
                      onClick={() =>
                        setOpenDropdown(
                          openDropdown === link.label ? null : link.label,
                        )
                      }
                      className="text-primary flex w-full items-center justify-between text-base font-medium"
                    >
                      {link.label}
                      <ChevronRight
                        className={cn(
                          "size-4 transition-transform duration-200",
                          openDropdown === link.label ? "rotate-90" : "",
                        )}
                      />
                    </button>
                    <div
                      className={cn(
                        "overflow-hidden transition-all duration-300",
                        openDropdown === link.label
                          ? "mt-4 max-h-[1000px] opacity-100"
                          : "max-h-0 opacity-0",
                      )}
                    >
                      <div className="bg-muted/50 space-y-3 rounded-lg p-4">
                        {link.dropdownItems.map((item) => (
                          <Link
                            key={item.title}
                            href={item.href}
                            className="group hover:bg-accent block rounded-md p-2 transition-colors"
                            onClick={() => {
                              setIsMenuOpen(false);
                              setOpenDropdown(null);
                            }}
                          >
                            <div className="transition-transform duration-200 group-hover:translate-x-1">
                              <div className="text-primary font-medium">
                                {item.title}
                              </div>

                              <p className="text-muted-foreground mt-1 text-sm">
                                {item.description}
                              </p>
                            </div>
                          </Link>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : (
                  <Link
                    key={link.label}
                    href={link.href}
                    className={cn(
                      "text-primary hover:text-primary/80 py-4 text-base font-medium transition-colors first:pt-0 last:pb-0",
                      pathname === link.href && "text-muted-foreground",
                    )}
                    onClick={() => setIsMenuOpen(false)}
                  >
                    {link.label}
                  </Link>
                ),
              )}
            </nav>
            <div className="mt-6 flex flex-col gap-3">
              <Button asChild variant="outline" size="sm">
                <Link href="/login">
                  <span>Login</span>
                </Link>
              </Button>
              <Button asChild size="sm">
                <Link href="/signup">
                  <span>Sign Up</span>
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
