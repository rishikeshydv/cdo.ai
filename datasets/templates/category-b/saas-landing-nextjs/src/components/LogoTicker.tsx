"use client";
import { motion } from "framer-motion";
import Image from "next/image";

export const LogoTicker = () => {
  return (
    <div className="py-8 md:py-12 bg-white">
      <div className="container">
        <div
          className="flex overflow-hidden"
          style={{ maskImage: "linear-gradient(to right, transparent, black, transparent)" }}
        >
          <motion.div
            className="flex gap-14 flex-none pr-14"
            animate={{
              translateX: "-50%",
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear",
              repeatType: "loop",
            }}
          >
            <Image src={"/logo-acme.png"} alt="Acme logo" className="logo-ticker-image" width={100} height={50} />
            <Image src={"/logo-quantum.png"} alt="quantum logo" className="logo-ticker-image" width={100} height={50} />
            <Image src={"/logo-echo.png"} alt="Echo logo" className="logo-ticker-image" width={100} height={50} />
            <Image src={"/logo-celestial.png"} alt="celestial logo" className="logo-ticker-image" width={100} height={50} />
            <Image src={"/logo-pulse.png"} alt="Pulse logo" className="logo-ticker-image" width={100} height={50} />
            <Image src={"/logo-apex.png"} alt="Apex logo" className="logo-ticker-image" width={100} height={50} />

            <Image src={"/logo-acme.png"} alt="Acme logo" className="logo-ticker-image" width={100} height={50} />
            <Image src={"/logo-quantum.png"} alt="quantum logo" className="logo-ticker-image" width={100} height={50} />
            <Image src={"/logo-echo.png"} alt="Echo logo" className="logo-ticker-image" width={100} height={50} />
            <Image src={"/logo-celestial.png"} alt="celestial logo" className="logo-ticker-image" width={100} height={50} />
            <Image src={"/logo-pulse.png"} alt="Pulse logo" className="logo-ticker-image" width={100} height={50} />
            <Image src={"/logo-apex.png"} alt="Apex logo" className="logo-ticker-image" width={100} height={50} />
          </motion.div>
        </div>
      </div>
    </div>
  );
};
