import { cn } from "@/lib/utils";
import { Button } from "./ui/button";

export function CtaBanner({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "relative bg-card rounded-lg text-foreground py-20 px-10 overflow-hidden",
        className
      )}
      
      {...props}
    >
      <div className="relative z-1">
        <h2 className="text-4xl sm:text-5xl font-semibold tracking-tighter max-w-3xl mx-auto leading-[1.1]">
          Trust HomeGuardian with Your Home's Security
        </h2>
        <p className="mt-5 text-muted-foreground text-lg">
          We will protect your home in any place in the world with our smart
          assistant.
        </p>

        <Button className="mt-10" size="lg">
          Get a free quote
        </Button>
      </div>

      <div
        className="absolute inset-0 -top-4 -left-px z-0"
      style={{
        backgroundImage: `
        linear-gradient(to right, var(--border) 1px, transparent 1px),
        linear-gradient(to bottom, var(--border) 1px, transparent 1px)
      `,
        backgroundSize: "20px 20px",
        backgroundPosition: "0 0, 0 0",
        maskImage: `
        repeating-linear-gradient(
              to right,
              black 0px,
              black 3px,
              transparent 3px,
              transparent 8px
            ),
            repeating-linear-gradient(
              to bottom,
              black 0px,
              black 3px,
              transparent 3px,
              transparent 8px
            ),
            radial-gradient(ellipse 70% 60% at 50% 0%, #000 60%, transparent 100%)
      `,
        WebkitMaskImage: `
 repeating-linear-gradient(
              to right,
              black 0px,
              black 3px,
              transparent 3px,
              transparent 8px
            ),
            repeating-linear-gradient(
              to bottom,
              black 0px,
              black 3px,
              transparent 3px,
              transparent 8px
            ),
            radial-gradient(ellipse 70% 50% at 50% 0%, #000 60%, transparent 100%)
      `,
        maskComposite: "intersect",
        WebkitMaskComposite: "source-in",
      }}
      />
    </div>
  );
}
