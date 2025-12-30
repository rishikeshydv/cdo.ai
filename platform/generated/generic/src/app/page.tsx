import React from 'react';

export default function Page() {
  return (
    <>
      <section className="container py-16">
        <div className="grid gap-8 md:grid-cols-2 items-center">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-neutral-900">Trusted Legal Counsel. Practical Results.</h1>
            <p className="mt-4 text-neutral-700">Harrison &amp; Cole provides focused representation in civil litigation, employment, and business disputes. We combine strategic advocacy with clear communication so clients can make informed decisions.</p>

            <div className="mt-8">
              <a href="#contact" className="btn btn-outline mr-3">Get in touch</a>
              <a href="/about" className="btn btn-primary">Our approach</a>
            </div>

            <ul className="mt-6 flex gap-6 text-sm text-neutral-500">
              <li>Established 1998</li>
              <li>Former prosecutors &amp; trial counsel</li>
              <li>Client-focused strategy</li>
            </ul>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold">Brief consultation</h3>
            <p className="mt-2 text-sm text-neutral-600">Schedule a short phone consultation to discuss your matter and next steps. Our intake is confidential and case-specific.</p>

            <div id="contact" className="mt-4 flex flex-col gap-3">
              <a className="btn btn-primary" href="mailto:intake@harrisoncole.law">Email our intake team</a>
              <a className="btn btn-outline" href="tel:+15551234567">Call: (555) 123-4567</a>
              <div className="small-proof mt-2">Licensed attorneys. No guarantees of outcomes; advice based on case facts.</div>
            </div>
          </div>
        </div>
      </section>

      <section className="container py-12">
        <div className="card">
          <h4 className="font-semibold">Practice areas</h4>
          <div className="mt-3 grid gap-2 md:grid-cols-3">
            <div className="text-sm">Civil litigation</div>
            <div className="text-sm">Employment law</div>
            <div className="text-sm">Business disputes</div>
          </div>
        </div>
      </section>
    </>
  );
}
