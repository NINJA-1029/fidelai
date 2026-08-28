"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "../ui/card";

const navItems = [
  { href: "/", label: "OVERVIEW", sublabel: "01" },
  { href: "/advisor", label: "AI ADVISOR", sublabel: "02" },
  { href: "/transactions", label: "LEDGER", sublabel: "03" },
  { href: "/goals", label: "GOALS & PACING", sublabel: "04" },
  { href: "/simulation", label: "WHAT-IF SIMULATION", sublabel: "05" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-border bg-background flex flex-col justify-between h-screen fixed left-0 top-0 select-none z-50">
      <div>
        {/* Wordmark */}
        <div className="p-8 border-b border-border">
          <Link href="/" className="inline-block">
            <h1 className="text-[18px] font-normal tracking-[-0.03em] uppercase text-foreground">
              FIDEL
            </h1>
            <p className="text-[11px] leading-[1.36] text-felt-gray mt-1 font-normal tracking-wide">
              AUTONOMOUS INTELLIGENCE
            </p>
          </Link>
        </div>

        {/* Minimalist Navigation */}
        <nav className="p-6 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center justify-between px-3 py-2.5 text-[12px] tracking-[0.08em] uppercase transition-colors duration-smooth ease-patient rounded-none",
                  isActive
                    ? "text-foreground font-medium bg-muted"
                    : "text-felt-gray hover:text-foreground hover:bg-muted/40"
                )}
              >
                <span>{item.label}</span>
                <span className="font-mono text-[10px] text-felt-gray opacity-70">
                  {item.sublabel}
                </span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Typographic Circular Stamp (Zero Icon) */}
      <div className="p-8 border-t border-border flex flex-col items-center justify-center space-y-4">
        <div className="relative w-20 h-20 flex items-center justify-center">
          <svg className="w-20 h-20 animate-spin-slow" viewBox="0 0 100 100">
            <path
              id="sidebarCircle"
              d="M 50, 50 m -35, 0 a 35,35 0 1,1 70,0 a 35,35 0 1,1 -70,0"
              fill="transparent"
            />
            <text className="text-[8.5px] uppercase tracking-[0.18em] fill-current text-felt-gray font-normal">
              <textPath href="#sidebarCircle" startOffset="0%">
                AUTONOMOUS · FIDEL AGENT ·
              </textPath>
            </text>
          </svg>
          <span className="w-1.5 h-1.5 rounded-full bg-foreground absolute" />
        </div>

        <div className="text-center">
          <span className="text-[10px] uppercase tracking-widest text-felt-gray block font-mono">
            LOCAL INFERENCE // ACTIVE
          </span>
        </div>
      </div>
    </aside>
  );
}
