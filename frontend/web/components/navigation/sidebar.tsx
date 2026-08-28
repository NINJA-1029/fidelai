"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Receipt,
  Bot,
  Target,
  SlidersHorizontal,
} from "lucide-react";
import { cn } from "../ui/card";

const navItems = [
  { href: "/", label: "OVERVIEW", icon: LayoutDashboard },
  { href: "/advisor", label: "AI ADVISOR", icon: Bot },
  { href: "/transactions", label: "LEDGER", icon: Receipt },
  { href: "/goals", label: "GOALS & PACING", icon: Target },
  { href: "/simulation", label: "WHAT-IF SIMULATION", icon: SlidersHorizontal },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-border bg-background flex flex-col justify-between h-screen fixed left-0 top-0 select-none z-50">
      <div>
        {/* Editorial Wordmark Header */}
        <div className="p-8 border-b border-border">
          <Link href="/" className="inline-block group">
            <h1 className="text-[18px] font-normal tracking-[-0.03em] uppercase text-obsidian dark:text-paper">
              Fidel
            </h1>
            <p className="text-[11px] leading-[1.36] text-felt-gray mt-1 font-normal">
              Autonomous Financial Intelligence
            </p>
          </Link>
        </div>

        {/* Minimalist Editorial Menu */}
        <nav className="p-6 space-y-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "block px-3 py-2 text-[12px] tracking-[0.05em] uppercase transition-colors duration-smooth ease-patient rounded-none",
                  isActive
                    ? "text-obsidian dark:text-paper font-semibold bg-muted/60"
                    : "text-felt-gray hover:text-obsidian dark:hover:text-paper hover:bg-muted/30"
                )}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Monopo Saigon Typographic Rotating Badge */}
      <div className="p-8 border-t border-border flex flex-col items-center justify-center space-y-4">
        <div className="relative w-20 h-20 flex items-center justify-center">
          {/* Circular SVG text tracing circumference */}
          <svg className="w-20 h-20 animate-spin-slow" viewBox="0 0 100 100">
            <path
              id="circlePath"
              d="M 50, 50 m -35, 0 a 35,35 0 1,1 70,0 a 35,35 0 1,1 -70,0"
              fill="transparent"
            />
            <text className="text-[8.5px] uppercase tracking-[0.18em] fill-current text-felt-gray font-normal">
              <textPath href="#circlePath" startOffset="0%">
                AUTONOMOUS · FIDEL AGENT ·
              </textPath>
            </text>
          </svg>
          <span className="w-2 h-2 rounded-full bg-obsidian dark:bg-paper absolute" />
        </div>

        <div className="text-center">
          <span className="text-[11px] leading-[1.36] text-felt-gray block">
            LOCAL QWEN 2.5 // NATIVE
          </span>
        </div>
      </div>
    </aside>
  );
}
