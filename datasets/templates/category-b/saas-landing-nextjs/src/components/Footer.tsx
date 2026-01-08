import {Twitter, Instagram, Linkedin} from "lucide-react";

export const Footer = () => {
  return (
    <footer className="bg-black text-[#BCBCBC] text-sm py-10 text-center">
      <div className="container">
                <div className="font-semibold text-lg tracking-tight text-white">
                  Company Name
                </div>
        <nav className="flex flex-col md:flex-row md:justify-center gap-6 mt-6">
          <a href="">About</a>
          <a href="">Features</a>
          <a href="">Custmers</a>
          <a href="">Pricing</a>
          <a href="">Help</a>
          <a href="">Careers</a>
        </nav>

        <div className="flex justify-center gap-6 mt-6">
          <Twitter />
          <Instagram />
          <Linkedin />
        </div>
        <p className="mt-6">&copy; 2024 Your Company, Inc. All rights reserved.</p>
      </div>
    </footer>
  );
};
