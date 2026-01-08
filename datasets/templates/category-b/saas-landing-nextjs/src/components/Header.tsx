"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowRight, Menu, X } from "lucide-react";

const links = [
  { label: "About", href: "#about" },
  { label: "Features", href: "#features" },
  { label: "Customers", href: "#customers" },
  { label: "Updates", href: "#updates" },
  { label: "Help", href: "#help" },
];

export const Header = () => {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-20 backdrop-blur-lg">
      <div className="py-4 px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between gap-4">
          <Link href="/" className="font-semibold text-lg sm:text-xl tracking-tight text-black">
            Company Name
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1 px-3 py-1.5 rounded-full bg-black/5 text-sm text-black/70 shadow-[0_10px_40px_-25px_rgba(0,0,0,0.35)]">
            {links.map((link) => (
              <a
                key={link.label}
                className="px-3 py-1 rounded-full transition hover:bg-white hover:text-black"
                href={link.href}
              >
                {link.label}
              </a>
            ))}
          </nav>

          {/* Right actions (desktop) */}
          <div className="hidden md:flex items-center gap-3">
            <a
              className="text-sm font-medium text-black/70 transition hover:text-black"
              href="#login"
            >
              Log in
            </a>
            <button className="inline-flex items-center gap-2 bg-black text-white px-4 py-2.5 rounded-full text-sm font-semibold tracking-tight shadow-lg shadow-black/10 transition hover:-translate-y-0.5">
              Get for free
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>

          {/* Mobile toggle */}
          <button
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-label="Toggle navigation"
            className="md:hidden inline-flex h-10 w-10 items-center justify-center rounded-md border border-black/10"
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      <div
        className={`md:hidden overflow-hidden transition-[max-height,opacity] duration-300 ease-out ${
          open ? "max-h-96 opacity-100" : "max-h-0 opacity-0"
        }`}
      >
        <div className="px-4 pb-6 sm:px-6">
          <nav className="flex flex-col gap-3 rounded-xl border border-black/10 bg-white/95 p-4 shadow-lg">
            {links.map((link) => (
              <a
                key={link.label}
                className="text-base font-medium text-black hover:text-black/70 transition"
                href={link.href}
                onClick={() => setOpen(false)}
              >
                {link.label}
              </a>
            ))}
            <div className="pt-3 flex flex-col gap-3">
              <a
                className="text-sm font-medium text-black/70 transition hover:text-black"
                href="#login"
                onClick={() => setOpen(false)}
              >
                Log in
              </a>
              <button className="inline-flex items-center justify-center gap-2 bg-black text-white px-4 py-2.5 rounded-full text-sm font-semibold tracking-tight shadow-lg shadow-black/10">
                Get for free
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
};
