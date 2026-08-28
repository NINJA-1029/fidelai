"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { SlidersHorizontal, AlertTriangle, CheckCircle2, RefreshCw } from "lucide-react";

export default function SimulationPage() {
  const [scenarioType, setScenarioType] = useState("unexpected_expense");
  const [amount, setAmount] = useState("12000");
  const [description, setDescription] = useState("Emergency Medical Treatment");
  const [result, setResult] = useState<any>({
    baseline_projected_balance: 31400.0,
    simulated_projected_balance: 19400.0,
    buffer_violation_risk: true,
    impact_summary:
      "An immediate outflow of INR 12,000 reduces 30-day projected liquidity from INR 31,400 to INR 19,400, falling below your INR 25,000 safety threshold by INR 5,600.",
    goal_impacts: [
      {
        goal_id: "goal_vacation_02",
        title: "Annual Family Vacation",
        delay_months: 1,
        impact: "Requires pausing contribution for 30 days to protect cash reserves",
      },
    ],
    recommendation:
      "Maintain emergency buffer by deferring discretionary allocations and non-essential savings goals.",
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSimulate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/simulation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user_demo_01",
          scenario_type: scenarioType,
          amount: parseFloat(amount) || 0,
          description: description,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setResult(data);
      } else {
        throw new Error("Failed to reach simulation endpoint");
      }
    } catch (err) {
      // Local fallback calculation
      const numAmt = parseFloat(amount) || 0;
      const base = 31400.0;
      const sim = base - numAmt;
      setResult({
        baseline_projected_balance: base,
        simulated_projected_balance: sim,
        buffer_violation_risk: sim < 25000.0,
        impact_summary: `An outflow of INR ${numAmt.toLocaleString()} projects end-balance at INR ${sim.toLocaleString()}. ${
          sim < 25000 ? "Violates INR 25,000 buffer." : "Buffer preserved."
        }`,
        goal_impacts: [
          {
            goal_id: "goal_vacation_02",
            title: "Annual Family Vacation",
            impact: sim < 25000 ? "Pause contribution" : "Pacing maintained",
          },
        ],
        recommendation:
          sim < 25000
            ? "Defer secondary goals and reduce discretionary dining."
            : "Proceed with planned contributions.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center pb-4 border-b border-border">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">What-If Scenario Simulation</h2>
          <p className="text-sm text-muted-foreground">
            Test hypothetical cash flow shocks and evaluate buffer & goal impact before committing funds
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Simulation Controls */}
        <Card className="lg:col-span-1 border-border bg-card">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <SlidersHorizontal className="w-5 h-5 text-primary" />
              <CardTitle className="text-lg">Scenario Parameters</CardTitle>
            </div>
            <CardDescription>Configure hypothetical financial events</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSimulate} className="space-y-4">
              <div>
                <label className="text-xs font-semibold uppercase text-muted-foreground">
                  Scenario Type
                </label>
                <select
                  value={scenarioType}
                  onChange={(e) => setScenarioType(e.target.value)}
                  className="w-full mt-1.5 h-10 border border-input bg-background px-3 py-2 text-sm rounded-none focus:outline-none focus:ring-1 focus:ring-ring"
                >
                  <option value="unexpected_expense">Unexpected Outflow / Expense</option>
                  <option value="income_change">Income Change / Reduction</option>
                  <option value="expense_reduction">Discretionary Expense Trim</option>
                  <option value="investment_sip">New Investment Allocation</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold uppercase text-muted-foreground">
                  Amount (INR)
                </label>
                <Input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="mt-1.5 font-mono"
                />
              </div>

              <div>
                <label className="text-xs font-semibold uppercase text-muted-foreground">
                  Description / Context
                </label>
                <Input
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="mt-1.5"
                />
              </div>

              <Button type="submit" className="w-full mt-2" disabled={isLoading}>
                {isLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : "Run Deterministic Simulation"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Simulation Output */}
        <div className="lg:col-span-2 space-y-4">
          <Card className="border-border bg-card">
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle className="text-lg">Projected Trajectory Impact</CardTitle>
                <Badge
                  variant={result.buffer_violation_risk ? "destructive" : "success"}
                  className="text-xs"
                >
                  {result.buffer_violation_risk ? "Buffer Violation Triggered" : "Buffer Preserved"}
                </Badge>
              </div>
              <CardDescription>Deterministic comparison against baseline financial state</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border border-border bg-background">
                  <span className="text-xs text-muted-foreground">Baseline 30-Day Projected</span>
                  <p className="text-xl font-bold font-mono mt-1">
                    INR {result.baseline_projected_balance?.toLocaleString()}
                  </p>
                </div>

                <div className="p-4 border border-border bg-background">
                  <span className="text-xs text-muted-foreground">Simulated Post-Shock Balance</span>
                  <p
                    className={`text-xl font-bold font-mono mt-1 ${
                      result.buffer_violation_risk ? "text-amber-500" : "text-emerald-500"
                    }`}
                  >
                    INR {result.simulated_projected_balance?.toLocaleString()}
                  </p>
                </div>
              </div>

              <div className="p-4 bg-muted/40 border border-border">
                <h5 className="font-semibold text-sm">Deterministic Impact Summary</h5>
                <p className="text-sm text-muted-foreground mt-1 leading-relaxed">
                  {result.impact_summary}
                </p>
              </div>

              {result.recommendation && (
                <div className="p-4 border border-border bg-background">
                  <span className="text-xs text-primary font-bold uppercase tracking-wide">
                    Agent Decision Strategy
                  </span>
                  <p className="text-sm mt-1">{result.recommendation}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
