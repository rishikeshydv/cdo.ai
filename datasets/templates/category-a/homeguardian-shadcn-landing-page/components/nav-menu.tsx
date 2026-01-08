"use client";

import Link from "next/link";
import * as React from "react";

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { cn } from "@/lib/utils";

export const NavMenu = ({
  className,
  ...props
}: React.ComponentProps<typeof NavigationMenu>) => {
  const { orientation } = props;
  const triggerStyle = cn(navigationMenuTriggerStyle(), {
    "text-lg sm:text-xl w-full justify-start py-3": orientation === "vertical",
  });

  return (
    <NavigationMenu
      viewport={false}
      {...props}
      className={cn(
        "w-full",
        orientation === "vertical" && "justify-start",
        className
      )}
    >
      <NavigationMenuList
        className={cn({
          "flex-col items-start gap-2 w-full": orientation === "vertical",
        })}
      >
        <NavigationMenuItem>
          <NavigationMenuLink asChild className={triggerStyle}>
            <Link href="/#why-choose-us">Why Choose Us</Link>
          </NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
          <NavigationMenuLink asChild className={triggerStyle}>
            <Link href="/#industries">Industries</Link>
          </NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
          <NavigationMenuLink asChild className={triggerStyle}>
            <Link href="/#features">Features</Link>
          </NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
          <NavigationMenuLink asChild className={triggerStyle}>
            <Link href="/#faq">FAQ</Link>
          </NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
          <NavigationMenuLink asChild className={triggerStyle}>
            <Link href="/#testimonials">Testimonials</Link>
          </NavigationMenuLink>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  );
};
