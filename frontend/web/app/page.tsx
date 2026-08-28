import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from "@/components/ui/table";
import Link from "next/link";

export default function DashboardPage() {
  return (
    <div className="space-y-[46px]">
      {/* Top Header / Metadata Status */}
      <div className="flex justify-between items-center pb-4 border-b border-border text-[12px] font-mono uppercase text-felt-gray">
        <span>CANONICAL STATE // USER_DEMO_01</span>
        <span>DATA COMPLETENESS: 92%</span>
      </div>

      {/* Monopo Saigon Iridescent Atmospheric Hero Section */}
      <section className="relative overflow-hidden p-12 md:p-16 border border-border text-paper bg-[#000000]">
        <div className="absolute inset-0 opacity-35 mix-blend-screen pointer-events-none iridescent-hero" />

        <div className="relative z-10 space-y-8">
          <div className="flex justify-between items-center">
            <span className="text-[11px] uppercase tracking-[0.2em] font-mono text-white/70">
              01 // LIQUIDITY ALERT
            </span>
            <span className="text-[11px] font-mono uppercase text-white/70">
              BUFFER DEFICIT: INR 5,600.00
            </span>
          </div>

          <div className="py-4">
            <h2 className="text-[44px] md:text-[72px] font-light leading-[1.05] tracking-[-0.03em] text-paper">
              Preserve Liquidity.
              <br />
              <span className="font-normal opacity-90">Reason Over Tradeoffs.</span>
            </h2>
            <p className="text-[16px] leading-[1.58] text-white/80 max-w-2xl mt-4 font-light">
              Following an unexpected medical debit of INR 12,000.00, your 30-day projected reserve dips to INR 19,400.00 against your INR 25,000.00 target safety buffer.
            </p>
          </div>

          <div className="flex flex-wrap gap-4 pt-2">
            <Link href="/advisor">
              <Button variant="ghost-dark">
                INSPECT AI ADVISOR
              </Button>
            </Link>
            <Link href="/simulation">
              <Button variant="ghost-dark">
                RUN SIMULATION
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Section 01: Canonical State Metrics */}
      <section className="space-y-6">
        <div className="border-t border-border pt-6 flex justify-between items-baseline">
          <div>
            <span className="text-[11px] uppercase tracking-[0.18em] text-felt-gray block mb-1">
              02 // CANONICAL LEDGER STATE
            </span>
            <h3 className="text-[32px] md:text-[40px] font-light leading-[1.10] tracking-tight text-foreground">
              Reserves & Projections
            </h3>
          </div>
          <span className="text-[11px] font-mono text-felt-gray">
            DETERMINISTIC ENGINE
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardDescription className="uppercase tracking-wider text-[11px]">
              Current Liquid Balance
            </CardDescription>
            <div className="text-[26px] font-mono font-normal tracking-tight mt-3 text-foreground">
              INR 30,000.00
            </div>
            <div className="text-[12px] text-felt-gray mt-2 font-mono">
              -12,000.00 RECENT DEBIT
            </div>
          </Card>

          <Card>
            <CardDescription className="uppercase tracking-wider text-[11px]">
              Available (Net of Bills)
            </CardDescription>
            <div className="text-[26px] font-mono font-normal tracking-tight mt-3 text-foreground">
              INR 12,000.00
            </div>
            <div className="text-[12px] text-felt-gray mt-2 font-mono">
              18,000.00 DUE IN 6 DAYS
            </div>
          </Card>

          <Card>
            <CardDescription className="uppercase tracking-wider text-[11px]">
              30-Day Projected Cash
            </CardDescription>
            <div className="text-[26px] font-mono font-normal tracking-tight mt-3 text-foreground">
              INR 19,400.00
            </div>
            <div className="text-[12px] text-felt-gray mt-2 font-mono">
              FLOOR: INR 25,000.00
            </div>
          </Card>

          <Card>
            <CardDescription className="uppercase tracking-wider text-[11px]">
              Emergency Fund
            </CardDescription>
            <div className="text-[26px] font-mono font-normal tracking-tight mt-3 text-foreground">
              2.1 Months
            </div>
            <div className="text-[12px] text-felt-gray mt-2 font-mono">
              INR 50,000.00 LIQUID
            </div>
          </Card>
        </div>
      </section>

      {/* Section 02: AI Advisor Decision Support */}
      <section className="space-y-6">
        <div className="border-t border-border pt-6 flex justify-between items-baseline">
          <div>
            <span className="text-[11px] uppercase tracking-[0.18em] text-felt-gray block mb-1">
              03 // REASONING SYNTHESIS
            </span>
            <h3 className="text-[32px] md:text-[40px] font-light leading-[1.10] tracking-tight text-foreground">
              Strategic Decision Support
            </h3>
          </div>
          <span className="text-[11px] font-mono text-felt-gray">
            LOCAL QWEN 2.5 // 94% CONFIDENCE
          </span>
        </div>

        <Card>
          <CardHeader>
            <div className="flex justify-between items-baseline">
              <div>
                <CardDescription className="uppercase tracking-widest text-[11px]">
                  Primary Action Strategy
                </CardDescription>
                <CardTitle className="text-[22px] font-normal mt-1">
                  Preserve Near-Term Liquidity
                </CardTitle>
              </div>
              <Badge variant="default">HIGH PRIORITY</Badge>
            </div>
          </CardHeader>

          <CardContent className="space-y-6">
            <p className="text-[15px] leading-[1.6] text-felt-gray">
              An unexpected medical transaction of INR 12,000 combined with an upcoming obligation of INR 18,000 will compress liquid reserves below your configured INR 25,000 minimum safety threshold.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 border border-border bg-background">
                <span className="text-[10px] font-mono uppercase tracking-wider text-felt-gray block">
                  EVIDENCE 01
                </span>
                <p className="text-[17px] font-mono mt-1 text-foreground">INR 19,400.00</p>
                <p className="text-[11px] text-felt-gray mt-1 font-mono">30-day forecast</p>
              </div>

              <div className="p-4 border border-border bg-background">
                <span className="text-[10px] font-mono uppercase tracking-wider text-felt-gray block">
                  EVIDENCE 02
                </span>
                <p className="text-[17px] font-mono mt-1 text-foreground">INR 25,000.00</p>
                <p className="text-[11px] text-felt-gray mt-1 font-mono">User buffer threshold</p>
              </div>

              <div className="p-4 border border-border bg-background">
                <span className="text-[10px] font-mono uppercase tracking-wider text-felt-gray block">
                  EVIDENCE 03
                </span>
                <p className="text-[17px] font-mono mt-1 text-foreground">INR 18,000.00</p>
                <p className="text-[11px] text-felt-gray mt-1 font-mono">Obligations due in 6d</p>
              </div>
            </div>

            <div className="p-4 bg-muted/40 border border-border flex items-center justify-between">
              <span className="text-[13px] text-felt-gray leading-relaxed">
                <strong className="text-foreground">Tradeoff Resolved:</strong> Retained INR 140,000 investment portfolio compounding while pausing secondary Vacation Goal pacing for this cycle.
              </span>
              <Link href="/advisor">
                <Button size="sm" variant="default">
                  OPEN ADVISOR
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Section 03: Recent Ingestion Stream */}
      <section className="space-y-6">
        <div className="border-t border-border pt-6 flex justify-between items-baseline">
          <div>
            <span className="text-[11px] uppercase tracking-[0.18em] text-felt-gray block mb-1">
              04 // EVENT STREAM
            </span>
            <h3 className="text-[32px] font-light leading-[1.10] tracking-tight text-foreground">
              Recent Transactions
            </h3>
          </div>
          <Link href="/transactions">
            <Button variant="outline" size="sm">
              VIEW COMPLETE LEDGER
            </Button>
          </Link>
        </div>

        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="uppercase text-[11px] tracking-wider font-mono">Date</TableHead>
              <TableHead className="uppercase text-[11px] tracking-wider font-mono">Description</TableHead>
              <TableHead className="uppercase text-[11px] tracking-wider font-mono">Category</TableHead>
              <TableHead className="uppercase text-[11px] tracking-wider font-mono">Source</TableHead>
              <TableHead className="uppercase text-[11px] tracking-wider font-mono">Confidence</TableHead>
              <TableHead className="text-right uppercase text-[11px] tracking-wider font-mono">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell className="font-mono text-[12px]">2026-08-28</TableCell>
              <TableCell className="font-normal text-foreground">Urgent Medical Treatment & Diagnostics</TableCell>
              <TableCell>
                <Badge variant="default">UNEXPECTED</Badge>
              </TableCell>
              <TableCell className="text-[12px] text-felt-gray font-mono">SMS Feed</TableCell>
              <TableCell className="font-mono text-[12px]">98%</TableCell>
              <TableCell className="text-right font-mono font-medium text-foreground">
                -INR 12,000.00
              </TableCell>
            </TableRow>

            <TableRow>
              <TableCell className="font-mono text-[12px]">2026-08-10</TableCell>
              <TableCell className="font-normal text-foreground">Supermarket Weekly Provisions</TableCell>
              <TableCell>
                <Badge variant="outline">GROCERIES</Badge>
              </TableCell>
              <TableCell className="text-[12px] text-felt-gray font-mono">Receipt OCR</TableCell>
              <TableCell className="font-mono text-[12px]">95%</TableCell>
              <TableCell className="text-right font-mono font-medium text-foreground">
                -INR 9,000.00
              </TableCell>
            </TableRow>

            <TableRow>
              <TableCell className="font-mono text-[12px]">2026-08-01</TableCell>
              <TableCell className="font-normal text-foreground">Monthly Salary — Tech Corp</TableCell>
              <TableCell>
                <Badge variant="solid">INCOME</Badge>
              </TableCell>
              <TableCell className="text-[12px] text-felt-gray font-mono">Bank API</TableCell>
              <TableCell className="font-mono text-[12px]">100%</TableCell>
              <TableCell className="text-right font-mono font-medium text-foreground">
                +INR 65,000.00
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </section>
    </div>
  );
}
