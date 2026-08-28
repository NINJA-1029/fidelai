"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Receipt,
  Activity,
  Target,
  TrendingUp,
  Bot,
  SlidersHorizontal,
  ShieldAlert,
} from "lucide-react";
import { cn } from "../ui/card";

const navItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/transactions", label: "Transactions", icon: Receipt },
  { href: "/advisor", label: "AI Advisor", icon: Bot },
  { href: "/goals", label: "Financial Goals", icon: Target },
  { href: "/simulation", label: "What-If Simulation", icon: SlidersHorizontal },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-border bg-card flex flex-col justify-between h-screen fixed left-0 top-0">
      <div>
        <div className="p-6 border-b border-border flex items-center space-x-3">
          <div className="w-8 h-8 bg-primary text-primary-foreground flex items-center justify-center font-bold text-lg">
            F
          </div>
          <div>
            <h1 className="font-bold text-base tracking-tight">FIDEL</h1>
            <p className="text-xs text-muted-foreground">Autonomous Financial AI</p>
          </div>
        </div>

        <nav className="p-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center space-x-3 px-4 py-2.5 text-sm font-medium transition-colors rounded-none",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )}
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="p-4 border-t border-border">
        <div className="p-3 bg-muted/40 border border-border">
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span className="text-xs font-semibold text-foreground">Local Inference Active</span>
          </div>
          <p className="text-xs text-muted-foreground mt-1">Qwen 2.5 on llama.cpp</p>
        </div>
      </div>
    </aside>
  );
}
