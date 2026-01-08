import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'ClearPay — Compliant payments for small teams',
  description: 'Simple, compliant payment processing with clear pricing and proven security.'
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen flex flex-col">
          <header className="border-b border-slate-100">
            <div className="container mx-auto px-6 py-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
                  <rect width="24" height="24" rx="6" fill="#0b6e4f" />
                  <path d="M7 12.5l3 3 7-8" stroke="#fff" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <span className="font-semibold">ClearPay</span>
              </div>
              <nav className="text-sm text-muted">
                <a href="#faq" className="mr-6 hover:underline transition-colors duration-150">FAQ</a>
                <a href="#footer" className="hover:underline transition-colors duration-150">Legal</a>
              </nav>
            </div>
          </header>

          <main className="flex-1">
            {children}
          </main>

          <footer id="footer" className="border-t border-slate-100">
            <div className="container mx-auto px-6 py-6 text-sm text-muted">
              © {new Date().getFullYear()} ClearPay. All rights reserved.
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
