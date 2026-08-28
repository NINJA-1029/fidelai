import * as React from "react";
import { cn } from "./card";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "ghost-dark" | "ghost-light" | "slate-pill" | "outline" | "destructive";
  size?: "default" | "sm" | "lg" | "icon";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    const baseStyles =
      "inline-flex items-center justify-center whitespace-nowrap text-sm font-medium tracking-tight rounded-full transition-all duration-smooth ease-patient disabled:pointer-events-none disabled:opacity-40 select-none";

    const variants = {
      // Primary Ghost Pill on Light Surface
      default:
        "bg-transparent text-obsidian dark:text-paper border border-obsidian dark:border-paper hover:bg-obsidian hover:text-paper dark:hover:bg-paper dark:hover:text-obsidian",
      // Ghost Pill on Dark / Iridescent Surface
      "ghost-dark":
        "bg-transparent text-paper border border-white/30 hover:border-white hover:bg-white/10 backdrop-blur-sm",
      // Ghost Pill on Light Surface
      "ghost-light":
        "bg-transparent text-obsidian border border-obsidian hover:bg-obsidian/5",
      // Filled Slate Pill
      "slate-pill":
        "bg-[#636363] text-paper border border-paper hover:bg-[#525252]",
      outline:
        "border border-border bg-transparent text-foreground hover:bg-muted",
      destructive:
        "border border-red-500 bg-red-500/10 text-red-600 hover:bg-red-500 hover:text-white",
    };

    const sizes = {
      // Exact Monopo Saigon specification: 11px vertical, 33px horizontal padding
      default: "py-[11px] px-[33px] text-[16px] leading-[1.15]",
      sm: "py-[7px] px-[20px] text-[12px] leading-[1.19]",
      lg: "py-[14px] px-[42px] text-[18px]",
      icon: "h-10 w-10 p-0",
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
