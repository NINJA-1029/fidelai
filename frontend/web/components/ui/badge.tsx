import * as React from "react";
import { cn } from "./card";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "destructive" | "outline" | "warning" | "success";
}

function Badge({
  className,
  variant = "default",
  ...props
}: BadgeProps) {
  const baseStyles =
    "inline-flex items-center rounded-full border px-3 py-0.5 text-[11px] font-normal tracking-wide transition-colors duration-smooth ease-patient select-none";

  const variants = {
    default: "border-obsidian bg-obsidian text-paper dark:border-paper dark:bg-paper dark:text-obsidian",
    secondary: "border-border bg-secondary text-felt-gray",
    destructive: "border-red-500/40 bg-red-500/10 text-red-600 dark:text-red-400",
    warning: "border-amber-500/40 bg-amber-500/10 text-amber-700 dark:text-amber-300",
    success: "border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300",
    outline: "border-border text-foreground bg-transparent",
  };

  return (
    <div className={cn(baseStyles, variants[variant], className)} {...props} />
  );
}

export { Badge };
