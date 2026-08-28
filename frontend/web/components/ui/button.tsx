import * as React from "react";
import { cn } from "./card";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "ghost-dark" | "ghost-light" | "slate-pill" | "outline";
  size?: "default" | "sm" | "lg";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    const baseStyles =
      "inline-flex items-center justify-center whitespace-nowrap text-[14px] font-normal tracking-[0.02em] rounded-full transition-all duration-smooth ease-patient disabled:pointer-events-none disabled:opacity-40 select-none";

    const variants = {
      default:
        "bg-obsidian text-paper border border-obsidian hover:bg-transparent hover:text-obsidian dark:bg-paper dark:text-obsidian dark:border-paper dark:hover:bg-transparent dark:hover:text-paper",
      "ghost-dark":
        "bg-transparent text-paper border border-white/40 hover:border-white hover:bg-white/10",
      "ghost-light":
        "bg-transparent text-obsidian border border-obsidian hover:bg-obsidian/5 dark:text-paper dark:border-paper dark:hover:bg-paper/5",
      "slate-pill":
        "bg-[#636363] text-paper border border-[#636363] hover:bg-[#525252]",
      outline:
        "border border-border bg-transparent text-foreground hover:border-foreground hover:bg-muted/30",
    };

    const sizes = {
      default: "py-[11px] px-[33px] text-[15px]",
      sm: "py-[7px] px-[22px] text-[12px] uppercase tracking-wider",
      lg: "py-[14px] px-[42px] text-[16px]",
    };

    return (
      <button
        ref={ref}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button };
