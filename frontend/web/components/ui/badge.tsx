import * as React from "react";
import { cn } from "./card";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "outline" | "solid";
}

function Badge({
  className,
  variant = "default",
  ...props
}: BadgeProps) {
  const baseStyles =
    "inline-flex items-center justify-center rounded-full px-3 py-1 text-[11px] leading-none uppercase tracking-[0.08em] font-normal transition-colors duration-smooth ease-patient select-none";

  const variants = {
    default: "border border-obsidian bg-transparent text-obsidian dark:border-paper dark:text-paper",
    outline: "border border-border text-felt-gray bg-transparent",
    secondary: "border border-transparent bg-muted text-foreground",
    solid: "border border-transparent bg-obsidian text-paper dark:bg-paper dark:text-obsidian",
  };

  return (
    <div className={cn(baseStyles, variants[variant], className)} {...props} />
  );
}

export { Badge };
