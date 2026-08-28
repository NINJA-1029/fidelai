import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from "@/components/ui/table";
import {
  TrendingDown,
  TrendingUp,
  AlertTriangle,
  ShieldCheck,
  ArrowUpRight,
  Bot,
  Calendar,
  Sparkles,
} from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      {/* Top Header */}
      <div className="flex justify-between items-center pb-4 border-b border-border">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Financial Overview</h2>
          <p className="text-sm text-muted-foreground">
            Canonical Financial State as of August 28, 2026
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Badge variant="outline" className="px-3 py-1 text-xs">
            Data Completeness: 92%
          </Badge>
          <Link href="/simulation">
            <Button size="sm" variant="outline">
              Simulate Scenario
            </Button>
          </Link>
        </div>
      </div>

      {/* Primary Liquidity Risk Alert Banner */}
      <div className="border border-amber-500/30 bg-amber-500/10 p-5 rounded-none flex items-start space-x-4">
        <AlertTriangle className="w-5 h-5 text-amber-500 mt-0.5 flex-shrink-0" />
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h4 className="font-semibold text-sm text-amber-500">
              Active Risk Alert: Projected Buffer Deficit
            </h4>
            <Badge variant="warning">Medium Severity</Badge>
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            An unexpected expense of INR 12,000 has reduced your projected month-end balance to INR 19,400, falling INR 5,600 below your preferred cash buffer of INR 25,000.
          </p>
        </div>
      </div>

      {/* Core Financial Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Current Liquid Balance</CardDescription>
            <CardTitle className="text-2xl font-bold font-mono">INR 30,000.00</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground flex items-center">
              <span className="text-red-500 flex items-center mr-1">
                <TrendingDown className="w-3 h-3 mr-0.5" /> -12,000.00
              </span>
              recent debit
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Available Cash (After Bills)</CardDescription>
            <CardTitle className="text-2xl font-bold font-mono">INR 12,000.00</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground">
              INR 18,000.00 bills due in 6 days
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardDescription>30-Day Projected Balance</CardDescription>
            <CardTitle className="text-2xl font-bold font-mono text-amber-500">
              INR 19,400.00
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-amber-500/90 font-medium">
              Target buffer: INR 25,000.00
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Emergency Fund</CardDescription>
            <CardTitle className="text-2xl font-bold font-mono">2.1 Months</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground">
              INR 50,000.00 in liquid reserve
            </div>
          </CardContent>
        </Card>
      </div>

      {/* AI Advisor Spotlight Card */}
      <Card className="border-primary/40 bg-card/60">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Bot className="w-5 h-5 text-primary" />
              <CardTitle>Autonomous Decision Guidance</CardTitle>
            </div>
            <Badge variant="default" className="text-xs">
              Confidence: 94%
            </Badge>
          </div>
          <CardDescription>
            Synthesized by local Qwen 2.5 on native llama.cpp over deterministic facts
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="p-4 bg-muted/30 border border-border">
            <h4 className="font-semibold text-base">Preserve Near-Term Liquidity</h4>
            <p className="text-sm text-muted-foreground mt-1 leading-relaxed">
              An unexpected medical transaction of INR 12,000 combined with an upcoming obligation of INR 18,000 will compress liquid reserves below your configured INR 25,000 minimum safety threshold.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="p-3 border border-border bg-background">
              <span className="text-xs text-muted-foreground uppercase font-mono">Evidence 1</span>
              <p className="text-sm font-semibold mt-1">Projected: INR 19,400</p>
              <p className="text-xs text-muted-foreground">Deterministic 30-day forecast</p>
            </div>
            <div className="p-3 border border-border bg-background">
              <span className="text-xs text-muted-foreground uppercase font-mono">Evidence 2</span>
              <p className="text-sm font-semibold mt-1">Buffer Floor: INR 25,000</p>
              <p className="text-xs text-muted-foreground">Configured user preference</p>
            </div>
            <div className="p-3 border border-border bg-background">
              <span className="text-xs text-muted-foreground uppercase font-mono">Evidence 3</span>
              <p className="text-sm font-semibold mt-1">Bills Due: INR 18,000</p>
              <p className="text-xs text-muted-foreground">Committed rent & utilities</p>
            </div>
          </div>

          <div className="flex items-center justify-between pt-2">
            <span className="text-xs text-muted-foreground">
              Tradeoff Resolved: Retained INR 140,000 long-term investment compounding while pausing secondary goal pacing.
            </span>
            <Link href="/advisor">
              <Button size="sm">
                Open AI Advisor
                <ArrowUpRight className="w-4 h-4 ml-1.5" />
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>

      {/* Recent Transactions Table */}
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold tracking-tight">Recent Financial Events</h3>
          <Link href="/transactions" className="text-xs text-muted-foreground hover:underline">
            View All Ledger Entries
          </Link>
        </div>

        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Date</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Source</TableHead>
              <TableHead>Confidence</TableHead>
              <TableHead className="text-right">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell className="font-mono text-xs">2026-08-28</TableCell>
              <TableCell className="font-medium">Urgent Medical Treatment & Diagnostics</TableCell>
              <TableCell>
                <Badge variant="destructive">Unexpected</Badge>
              </TableCell>
              <TableCell className="text-xs text-muted-foreground">SMS Feed</TableCell>
              <TableCell>
                <span className="text-xs font-mono">98%</span>
              </TableCell>
              <TableCell className="text-right font-mono text-red-500 font-semibold">
                -INR 12,000.00
              </TableCell>
            </TableRow>

            <TableRow>
              <TableCell className="font-mono text-xs">2026-08-10</TableCell>
              <TableCell className="font-medium">Supermarket Weekly Provisions</TableCell>
              <TableCell>
                <Badge variant="outline">Groceries</Badge>
              </TableCell>
              <TableCell className="text-xs text-muted-foreground">Receipt OCR</TableCell>
              <TableCell>
                <span className="text-xs font-mono">95%</span>
              </TableCell>
              <TableCell className="text-right font-mono text-red-500">
                -INR 9,000.00
              </TableCell>
            </TableRow>

            <TableRow>
              <TableCell className="font-mono text-xs">2026-08-01</TableCell>
              <TableCell className="font-medium">Monthly Salary - Tech Corp</TableCell>
              <TableCell>
                <Badge variant="success">Income</Badge>
              </TableCell>
              <TableCell className="text-xs text-muted-foreground">Bank API</TableCell>
              <TableCell>
                <span className="text-xs font-mono">100%</span>
              </TableCell>
              <TableCell className="text-right font-mono text-emerald-500 font-semibold">
                +INR 65,000.00
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
