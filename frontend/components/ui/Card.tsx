import { cn } from "@/lib/utils/cn";
import { HTMLAttributes, forwardRef } from "react";

const Card = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "rounded-xl border border-slate-800 bg-slate-900/50",
          "backdrop-blur-sm",
          className
        )}
        {...props}
      />
    );
  }
);

Card.displayName = "Card";

export { Card };
