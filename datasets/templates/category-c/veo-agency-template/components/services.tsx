import {
  CardsStackContainer,
  CardSticky,
} from '@/components/systaliko-ui/cards/cards-stack';

const SERVICES_CARDS = [
  {
    id: 'service-starategy-identity-service',
    title: 'Brand Strategy & Identity',
    description:
      'help teams uncover a clear brand position and translate it into a concise voice and visual system. From naming and messaging to logo systems and brand guidelines.',
  },
  {
    id: 'UX-Product-design-service',
    title: 'UX & Product Design',
    description:
      'focus on user research, information architecture, and product flows that solve real problems. Our designs are tested with prototypes and guided by metrics so you ship features that move KPIs.',
  },
  {
    id: 'web-development-service',
    title: 'Web Development',
    description:
      'build modern web products using component-driven development, automated testing, and performance-first best practices. Our code is documented and deliverable-ready.',
  },
  {
    id: 'Motion-interaction-service',
    title: 'Motion & Interaction',
    description:
      'Motion should inform, not distract. We design micro-interactions and page-level transitions that guide attention, improve perceived performance, and make products feel polished.',
  },
  {
    id: 'content-copywriting-service',
    title: 'Content & Copywriting',
    description:
      'We craft messaging that fits your brand and speaks to real user needs — from hero lines and product microcopy to onboarding flows and launch email sequences.',
  },
  {
    id: 'growth-anilytics-service',
    title: 'Growth & Analytics',
    description:
      'We instrument analytics, design experiments, and run A/B tests that answer the questions behind growth. We build dashboards and recommend prioritized experiments that directly tie to business goals.',
  },
];

export function Services() {
  return (
    <section className="px-4 sm:px-6">
      <CardsStackContainer className="min-h-[320vh] sm:min-h-[360vh] flex flex-col gap-12">
        {SERVICES_CARDS.map((service, index) => (
          <CardSticky
            key={service.id}
            index={index}
            className="min-h-[45vh] py-8 px-6 sm:px-10 flex gap-6 justify-between flex-wrap even:border bg-card odd:bg-muted rounded-xl shadow-sm"
            incrementY={72}
            incrementZ={0}
          >
            <div className="md:basis-1/3 flex items-start gap-2">
              <sup className="font-black text-muted-foreground">
                {index + 1}
              </sup>
              <h3 className="text-3xl sm:text-4xl md:text-5xl max-w-[20ch] font-bold leading-tight">
                {service.title}
              </h3>
            </div>

            <p className="text-base sm:text-lg md:text-xl md:basis-1/2 leading-relaxed">
              {service.description}
            </p>
          </CardSticky>
        ))}
      </CardsStackContainer>
    </section>
  );
}
