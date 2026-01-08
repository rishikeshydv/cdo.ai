import { About } from '@/components/about';
import { Process } from '@/components/process';
import { Hero } from '@/components/hero';
import { Services } from '@/components/services';
import { Team } from '@/components/team';
import { Testimonials } from '@/components/testimonials';
import { Values } from '@/components/values';

export default function Home() {
  return (
    <>
      <Hero />
      <About />
      <Values />
      <Services />
      <Team />
      <Process />
      <Testimonials />
    </>
  );
}
