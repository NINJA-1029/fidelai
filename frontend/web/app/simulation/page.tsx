"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

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
        throw new Error("Local simulation offline");
      }
    } catch (err) {
      const numAmt = parseFloat(amount) || 0;
      const base = 31400.0;
      const sim = base - numAmt;
      setResult({
        baseline_projected_balance: base,
        simulated_projected_balance: sim,
        buffer_violation_risk: sim < 25000.0,
        impact_summary: `An outflow of INR ${numAmt.toLocaleString()} projects end-balance at INR ${sim.toLocaleString()}. ${
          sim < 25000 ? "Violates INR 25,000 buffer by INR " + (25000 - sim).toLocaleString() + "." : "Buffer preserved."
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
    <div className="space-y-[46px]">
      <div className="flex justify-between items-baseline pb-4 border-b border-border">
        <div>
          <span className="text-[11px] uppercase tracking-[0.18em] text-felt-gray block mb-1">
            05 // DETERMINISTIC SIMULATION
          </span>
          <h2 className="text-[32px] md:text-[40px] font-light leading-[1.10] tracking-tight text-foreground">
            What-If Scenario Analysis
          </h2>
        </div>
        <span className="text-[11px] font-mono text-felt-gray uppercase">
          DELTA CALCULATOR
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Controls */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardDescription className="uppercase text-[11px] tracking-wider">
              Input Parameters
            </CardDescription>
            <CardTitle className="text-[20px] font-normal">
              Configure Scenario
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSimulate} className="space-y-5">
              <div>
                <label className="text-[10px] font-mono uppercase text-felt-gray block mb-1">
                  SCENARIO TYPE
                </label>
                <select
                  value={scenarioType}
                  onChange={(e) => setScenarioType(e.target.value)}
                  className="w-full h-10 border border-border bg-background px-3 py-2 text-[13px] rounded-none focus:outline-none focus:border-foreground font-mono"
                >
                  <option value="unexpected_expense">Unexpected Outflow / Expense</option>
                  <option value="income_change">Income Change / Reduction</option>
                  <option value="expense_reduction">Discretionary Expense Trim</option>
                  <option value="investment_sip">New Investment Contribution</option>
                </select>
              </div>

              <div>
                <label className="text-[10px] font-mono uppercase text-felt-gray block mb-1">
                  AMOUNT (INR)
                </label>
                <Input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="font-mono text-[13px]"
                />
              </div>

              <div>
                <label className="text-[10px] font-mono uppercase text-felt-gray block mb-1">
                  DESCRIPTION / CONTEXT
                </label>
                <Input
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="font-mono text-[13px]"
                />
              </div>

              <Button type="submit" className="w-full mt-2" disabled={isLoading}>
                {isLoading ? "CALCULATING..." : "RUN SIMULATION"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Results */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-baseline">
                <div>
                  <CardDescription className="uppercase text-[11px] tracking-wider">
                    Trajectory Comparison
                  </CardDescription>
                  <CardTitle className="text-[20px] font-normal mt-1">
                    Projected Impact
                  </CardTitle>
                </div>
                <span className="text-[11px] font-mono text-felt-gray uppercase">
                  {result.buffer_violation_risk ? "[ BUFFER VIOLATION ]" : "[ BUFFER PRESERVED ]"}
                </span>
              </div>
            </CardHeader>

            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border border-border bg-background">
                  <span className="text-[10px] font-mono uppercase text-felt-gray block">
                    BASELINE 30-DAY PROJECTED
                  </span>
                  <p className="text-[22px] font-mono font-normal mt-1 text-foreground">
                    INR {result.baseline_projected_balance?.toLocaleString()}
                  </p>
                </div>

                <div className="p-4 border border-border bg-background">
                  <span className="text-[10px] font-mono uppercase text-felt-gray block">
                    SIMULATED POST-SHOCK
                  </span>
                  <p className="text-[22px] font-mono font-normal mt-1 text-foreground">
                    INR {result.simulated_projected_balance?.toLocaleString()}
                  </p>
                </div>
              </div>

              <div className="p-5 bg-muted/40 border border-border">
                <span className="text-[10px] font-mono uppercase text-felt-gray block mb-1">
                  IMPACT SUMMARY
                </span>
                <p className="text-[15px] leading-[1.6] text-felt-gray">
                  {result.impact_summary}
                </p>
              </div>

              {result.recommendation && (
                <div className="p-5 border border-border bg-background">
                  <span className="text-[10px] font-mono uppercase text-felt-gray block mb-1">
                    STRATEGIC GUIDANCE
                  </span>
                  <p className="text-[15px] text-foreground leading-[1.6]">{result.recommendation}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
