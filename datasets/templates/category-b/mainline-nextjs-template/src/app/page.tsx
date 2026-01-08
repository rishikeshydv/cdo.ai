import { Background } from "@/components/background";
import { FAQ } from "@/components/faq";
import { Features } from "@/components/features";
import { Hero } from "@/components/hero";
import { Logos } from "@/components/logos";
import { Pricing } from "@/components/pricing";
import { ResourceAllocation } from "@/components/resource-allocation";
import { Testimonials } from "@/components/testimonials";

export default function Home() {
  return (
    <>
      <Background className="via-muted to-muted/80">
        <Hero />
        <Logos />
        <Features />
        <ResourceAllocation />
      </Background>
      <Testimonials />
      <Background variant="bottom">
        <Pricing />
        <FAQ />
      </Background>
    </>
  );
}
