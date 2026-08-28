import * as React from "react";
import { cn } from "./card";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "destructive" | "outline" | "success" | "warning";
}

function Badge({
  className,
  variant = "default",
  ...props
}: BadgeProps) {
  const baseStyles =
    "inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2";
  
  const variants = {
    default: "border-transparent bg-primary text-primary-foreground",
    secondary: "border-transparent bg-secondary text-secondary-foreground",
    destructive: "border-transparent bg-red-600/15 text-red-700 dark:text-red-400 border-red-500/20",
    warning: "border-transparent bg-amber-500/15 text-amber-700 dark:text-amber-400 border-amber-500/20",
    success: "border-transparent bg-emerald-500/15 text-emerald-700 dark:text-emerald-400 border-emerald-500/20",
    outline: "text-foreground border-border",
  };

  return (
    <div className={cn(baseStyles, variants[variant], className)} {...props} />
  );
}

export { Badge };
