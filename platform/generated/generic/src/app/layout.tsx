import './globals.css';
import React from 'react';

export const metadata = {
  title: 'Harrison & Cole LLP — Law Firm',
  description: 'Harrison & Cole: Experienced trial attorneys focused on client-first solutions.'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="container header-compact">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-md bg-brand flex items-center justify-center text-white font-semibold">HC</div>
            <div>
              <div className="text-lg font-semibold">Harrison &amp; Cole LLP</div>
              <div className="text-xs text-neutral-500">Trusted legal counsel</div>
            </div>
          </div>
          <nav className="text-sm">
            <a href="#contact" className="text-neutral-700 hover:underline">Contact</a>
          </nav>
        </header>

        <main>{children}</main>

        <footer className="container py-8">
          <div className="small-proof">© {new Date().getFullYear()} Harrison &amp; Cole LLP. All rights reserved.</div>
        </footer>
      </body>
    </html>
  );
}
