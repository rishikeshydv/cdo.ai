"use client";
import Header from "@/components/Header";
import Hero from "@/components/Hero";
import LogoCloud from "@/components/Logo-Cloud";
import Stats from "@/components/Stats";
import Features from "@/components/Features";
import Integration from "@/components/Integration";
import Pricing from "@/components/Pricing";
import FAQ from "@/components/FAQ";
import CTA from "@/components/CTA";
import Footer from "@/components/Footer";
export default function Home() {

  return (
    <>
      <Header />
      <main className="overflow-hidden">
        <div
          aria-hidden
          className="absolute inset-0 isolate hidden opacity-65 contain-strict lg:block"
        >
          <div className="w-140 h-320 -translate-y-87.5 absolute left-0 top-0 -rotate-45 rounded-full bg-[radial-gradient(68.54%_68.72%_at_55.02%_31.46%,hsla(0,0%,85%,.08)_0,hsla(0,0%,55%,.02)_50%,hsla(0,0%,45%,0)_80%)]" />
          <div className="h-320 absolute left-0 top-0 w-60 -rotate-45 rounded-full bg-[radial-gradient(50%_50%_at_50%_50%,hsla(0,0%,85%,.06)_0,hsla(0,0%,45%,.02)_80%,transparent_100%)] [translate:5%_-50%]" />
          <div className="h-320 -translate-y-87.5 absolute left-0 top-0 w-60 -rotate-45 bg-[radial-gradient(50%_50%_at_50%_50%,hsla(0,0%,85%,.04)_0,hsla(0,0%,45%,.02)_80%,transparent_100%)]" />
        </div>
        {/* Hero Section */}
        <Hero />
        {/* Logo Cloud */}
        <LogoCloud />
        {/* Stats */}
        <Stats />
        {/* Features */}
        <Features />
        {/* Integration */}
        <Integration />
        {/* Pricing */}
        <Pricing />
        {/* FAQ */}
        <FAQ />
        {/* CTA */}
        <CTA />
        {/* Footer */}
        <Footer />
      </main>
    </>
  );
}

