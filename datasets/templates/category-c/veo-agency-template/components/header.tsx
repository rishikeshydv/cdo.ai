import { DesktopNav } from "@/components/desktop-nav";
import { MobileNav } from "@/components/mobile-nav";
import Link from "next/link";


export function Header() {
    return (
        <header
        className="flex justify-center z-50 w-full border-b border-border bg-background/50 px-8"

      >
        <div className="container flex h-16 justify-between items-center gap-4">
          <Link className="flex-grow-[1] inline-flex items-center gap-1" href="/">
            <span className="inline-block text-2xl font-bold tracking-tighter">Company Name</span>
          </Link>

        <DesktopNav />
        <MobileNav />
        </div>
      </header>
    )
}