import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from "@/components/ui/table";
import {
  TrendingDown,
  ArrowUpRight,
  ShieldAlert,
  Bot,
  Activity,
  Layers,
  ArrowRight,
} from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
  return (
    <div className="space-y-[46px]">
      {/* Monopo Saigon Iridescent Hero Environment */}
      <section className="relative overflow-hidden p-12 md:p-16 border border-border/40 text-paper bg-[#000000]">
        {/* Molten Iridescent Light Atmosphere */}
        <div
          className="absolute inset-0 opacity-40 mix-blend-screen pointer-events-none iridescent-hero"
        />

        <div className="relative z-10 space-y-8">
          <div className="flex justify-between items-start">
            <Badge variant="outline" className="text-paper border-white/30 text-[11px] uppercase tracking-widest px-3 py-1">
              Deterministic Analytics // Autonomous AI
            </Badge>
            <span className="text-[12px] text-white/70 font-mono">
              CYCLE: AUG 2026
            </span>
          </div>

          {/* Monumental Hero Headline */}
          <div className="py-6">
            <h2 className="text-[48px] md:text-[78px] font-light leading-[1.05] tracking-[-0.03em] text-paper">
              Preserve Liquidity.
              <br />
              <span className="font-normal opacity-90">Reason Over Tradeoffs.</span>
            </h2>
            <p className="text-[16px] leading-[1.58] text-white/80 max-w-2xl mt-4 font-light">
              Following an unexpected medical outflow of INR 12,000.00, your 30-day projected reserve dips to INR 19,400.00 against your INR 25,000.00 safety buffer.
            </p>
          </div>

          <div className="flex flex-wrap gap-4 pt-2">
            <Link href="/advisor">
              <Button variant="ghost-dark">
                Inspect AI Reasoning
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
            <Link href="/simulation">
              <Button variant="ghost-dark">
                Run What-If Simulation
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Whisper-Weight Editorial Section Divider */}
      <div className="pt-6 border-t border-border">
        <span className="text-[12px] uppercase tracking-[0.15em] text-felt-gray font-normal block mb-2">
          SECTION 01 // FINANCIAL STATE
        </span>
        <h3 className="text-[39px] md:text-[54px] font-light leading-[1.10] tracking-tight text-foreground">
          Canonical Liquidity & Reserves
        </h3>
      </div>

      {/* High-Density Metric Grid (0px Radius, 34px Padding, Flat Hairline) */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardDescription className="uppercase tracking-wider text-[11px]">
            Current Liquid Balance
          </CardDescription>
          <div className="text-[28px] font-mono font-normal tracking-tight mt-3 text-foreground">
            INR 30,000.00
          </div>
          <div className="text-[12px] text-felt-gray mt-2 flex items-center">
            <span className="text-red-500 font-mono mr-1">-12,000.00</span> recent medical debit
          </div>
        </Card>

        <Card>
          <CardDescription className="uppercase tracking-wider text-[11px]">
            Available Cash (Net of Bills)
          </CardDescription>
          <div className="text-[28px] font-mono font-normal tracking-tight mt-3 text-foreground">
            INR 12,000.00
          </div>
          <div className="text-[12px] text-felt-gray mt-2">
            INR 18,000.00 due in 6 days
          </div>
        </Card>

        <Card>
          <CardDescription className="uppercase tracking-wider text-[11px]">
            30-Day Projected Cash
          </CardDescription>
          <div className="text-[28px] font-mono font-normal tracking-tight mt-3 text-amber-600 dark:text-amber-400">
            INR 19,400.00
          </div>
          <div className="text-[12px] text-amber-600/80 dark:text-amber-400/80 mt-2 font-medium">
            Buffer Deficit: INR 5,600.00
          </div>
        </Card>

        <Card>
          <CardDescription className="uppercase tracking-wider text-[11px]">
            Emergency Reserve
          </CardDescription>
          <div className="text-[28px] font-mono font-normal tracking-tight mt-3 text-foreground">
            2.1 Months
          </div>
          <div className="text-[12px] text-felt-gray mt-2">
            INR 50,000.00 liquid buffer
          </div>
        </Card>
      </div>

      {/* AI Advisor Decision Guidance Section */}
      <section className="space-y-6">
        <div className="border-t border-border pt-6 flex justify-between items-end">
          <div>
            <span className="text-[12px] uppercase tracking-[0.15em] text-felt-gray font-normal block mb-2">
              SECTION 02 // AGENTIC SYNTHESIS
            </span>
            <h3 className="text-[39px] md:text-[54px] font-light leading-[1.10] tracking-tight text-foreground">
              Strategic Decision Guidance
            </h3>
          </div>
          <Badge variant="outline" className="text-[11px] px-3 py-1 font-mono">
            CONFIDENCE: 94%
          </Badge>
        </div>

        <Card className="border-obsidian/30 dark:border-paper/30 bg-card">
          <CardHeader>
            <div className="flex justify-between items-start">
              <div>
                <CardDescription className="uppercase tracking-widest text-[11px]">
                  Fidel Autonomous Recommendation
                </CardDescription>
                <CardTitle className="text-[24px] font-normal mt-2">
                  Preserve Near-Term Liquidity
                </CardTitle>
              </div>
              <Badge variant="destructive">HIGH PRIORITY</Badge>
            </div>
          </CardHeader>

          <CardContent className="space-y-6">
            <p className="text-[16px] leading-[1.58] text-felt-gray">
              An unexpected medical transaction of INR 12,000 combined with an upcoming obligation of INR 18,000 will compress liquid reserves below your configured INR 25,000 minimum safety threshold.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 border border-border bg-background">
                <span className="text-[11px] uppercase tracking-wider text-felt-gray block">EVIDENCE 01</span>
                <p className="text-[18px] font-mono mt-1 text-foreground">INR 19,400.00</p>
                <p className="text-[12px] text-felt-gray mt-1">Deterministic 30-day projection</p>
              </div>

              <div className="p-4 border border-border bg-background">
                <span className="text-[11px] uppercase tracking-wider text-felt-gray block">EVIDENCE 02</span>
                <p className="text-[18px] font-mono mt-1 text-foreground">INR 25,000.00</p>
                <p className="text-[12px] text-felt-gray mt-1">Configured user buffer floor</p>
              </div>

              <div className="p-4 border border-border bg-background">
                <span className="text-[11px] uppercase tracking-wider text-felt-gray block">EVIDENCE 03</span>
                <p className="text-[18px] font-mono mt-1 text-foreground">INR 18,000.00</p>
                <p className="text-[12px] text-felt-gray mt-1">Committed bills due in 6 days</p>
              </div>
            </div>

            <div className="p-4 bg-muted/40 border border-border flex items-center justify-between">
              <span className="text-[13px] text-felt-gray leading-relaxed">
                <strong className="text-foreground">Tradeoff Evaluated:</strong> Retained INR 140,000 long-term investment portfolio compounding while temporarily deferring secondary Vacation Goal contribution.
              </span>
              <Link href="/advisor">
                <Button size="sm" variant="default">
                  Review Plan
                  <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Normalized Financial Events Ledger */}
      <section className="space-y-6">
        <div className="border-t border-border pt-6 flex justify-between items-end">
          <div>
            <span className="text-[12px] uppercase tracking-[0.15em] text-felt-gray font-normal block mb-2">
              SECTION 03 // EVENT STREAM
            </span>
            <h3 className="text-[39px] font-light leading-[1.10] tracking-tight text-foreground">
              Recent Financial Ingestion
            </h3>
          </div>
          <Link href="/transactions">
            <Button variant="outline" size="sm">
              View Complete Ledger
            </Button>
          </Link>
        </div>

        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="uppercase text-[11px] tracking-wider">Date</TableHead>
              <TableHead className="uppercase text-[11px] tracking-wider">Description</TableHead>
              <TableHead className="uppercase text-[11px] tracking-wider">Category</TableHead>
              <TableHead className="uppercase text-[11px] tracking-wider">Source</TableHead>
              <TableHead className="uppercase text-[11px] tracking-wider">Confidence</TableHead>
              <TableHead className="text-right uppercase text-[11px] tracking-wider">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell className="font-mono text-[12px]">2026-08-28</TableCell>
              <TableCell className="font-normal text-foreground">Urgent Medical Treatment & Diagnostics</TableCell>
              <TableCell>
                <Badge variant="destructive">UNEXPECTED</Badge>
              </TableCell>
              <TableCell className="text-[12px] text-felt-gray">SMS Feed</TableCell>
              <TableCell className="font-mono text-[12px]">98%</TableCell>
              <TableCell className="text-right font-mono font-medium text-red-600 dark:text-red-400">
                -INR 12,000.00
              </TableCell>
            </TableRow>

            <TableRow>
              <TableCell className="font-mono text-[12px]">2026-08-10</TableCell>
              <TableCell className="font-normal text-foreground">Supermarket Weekly Provisions</TableCell>
              <TableCell>
                <Badge variant="outline">GROCERIES</Badge>
              </TableCell>
              <TableCell className="text-[12px] text-felt-gray">Receipt OCR</TableCell>
              <TableCell className="font-mono text-[12px]">95%</TableCell>
              <TableCell className="text-right font-mono font-medium text-foreground">
                -INR 9,000.00
              </TableCell>
            </TableRow>

            <TableRow>
              <TableCell className="font-mono text-[12px]">2026-08-01</TableCell>
              <TableCell className="font-normal text-foreground">Monthly Salary — Tech Corp</TableCell>
              <TableCell>
                <Badge variant="success">INCOME</Badge>
              </TableCell>
              <TableCell className="text-[12px] text-felt-gray">Bank API</TableCell>
              <TableCell className="font-mono text-[12px]">100%</TableCell>
              <TableCell className="text-right font-mono font-medium text-emerald-600 dark:text-emerald-400">
                +INR 65,000.00
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </section>
    </div>
  );
}
