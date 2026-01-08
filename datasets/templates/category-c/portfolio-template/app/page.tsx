import { About } from "@/components/about";
import { Cta } from "@/components/cta";
import { Experience } from "@/components/experience";
import { Hero } from "@/components/hero";
import { Services } from "@/components/services";
import { Work } from "@/components/work";

export default function Home() {
  return (
      <div>
          <Hero />
      <Services />
      <Work />
      <About />
      <Experience />
      <Cta />
      </div>
  );
}
