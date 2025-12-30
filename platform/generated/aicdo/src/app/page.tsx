import Testimonial from '../components/Testimonial';
import Badge from '../components/Badge';

export default function Page() {
  return (
    <div className="container mx-auto px-6 py-12">
      {/* Hero: headline, benefits, subheadline (no CTA here per delayed timing) */}
      <section className="pt-6 pb-12">
        <div className="max-w-3xl">
          <h1 className="text-3xl font-semibold leading-tight">Payments that meet compliance and stay simple</h1>
          <p className="mt-4 text-slate-700">Process payments with clear pricing and proven security. Integrate in days, not months.</p>

          <ul className="mt-6 space-y-3 text-sm text-slate-700">
            <li className="flex items-start gap-3">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden>
                <path d="M20 6L9 17l-5-5" stroke="#0b6e4f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              PCI DSS Level 1 compliance
            </li>
            <li className="flex items-start gap-3">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden>
                <path d="M20 6L9 17l-5-5" stroke="#0b6e4f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              Minimal integration code and clear docs
            </li>
            <li className="flex items-start gap-3">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden>
                <path d="M20 6L9 17l-5-5" stroke="#0b6e4f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              Predictable, transparent fees
            </li>
          </ul>

          <p className="mt-6 text-sm text-slate-600">We limit choices to what matters: security, clarity, and support.</p>
        </div>
      </section>

      {/* Proof: testimonials then security/compliance then CTA */}
      <section className="mt-8 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Testimonial
            quote="ClearPay handled our compliance needs with no surprises. Setup was quick."
            author="A. Romero"
            role="CFO, Harbor Retail"
          />
          <Testimonial
            quote="Reliable settlement and clear reporting. We reduced disputes in weeks."
            author="M. Singh"
            role="Head of Ops, Marketline"
          />
        </div>

        <div className="flex flex-col md:flex-row items-start md:items-center gap-4 mt-2">
          <Badge label="PCI DSS Level 1" />
          <Badge label="ISO 27001" />
          <div className="text-sm text-slate-600">Independent audits and public security reports available.</div>
        </div>

        {/* Primary CTA is intentionally below the hero/proof per delayed CTA policy */}
        <div className="mt-8">
          <a
            href="mailto:sales@clearpay.example.com?subject=Request%20a%20demo"
            className="inline-flex items-center gap-3 px-4 py-2 rounded bg-brand text-white text-sm hover:bg-brand-light transition-colors duration-150"
            aria-label="Request a demo"
          >
            Request a demo
          </a>
        </div>
      </section>

      {/* FAQ: low density, plain language */}
      <section id="faq" className="mt-12">
        <h2 className="text-lg font-medium">FAQ</h2>
        <div className="mt-4 space-y-4 text-sm text-slate-700">
          <div>
            <div className="font-medium">How long does integration take?</div>
            <div>Most teams integrate in under two weeks with our SDKs and guides.</div>
          </div>
          <div>
            <div className="font-medium">Do you handle chargebacks?</div>
            <div>We provide dispute tools and guidance; final liability depends on card network rules.</div>
          </div>
          <div>
            <div className="font-medium">Can you support international payments?</div>
            <div>Yes. We support payments in major currencies and provide settlement options.</div>
          </div>
        </div>
      </section>
    </div>
  );
}
