import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Target, Plus, AlertCircle, CheckCircle2, Clock } from "lucide-react";

const goals = [
  {
    id: "goal_emergency_01",
    title: "Emergency Fund Reserve",
    target: 72000.0,
    current: 50000.0,
    targetDate: "2026-12-31",
    requiredMonthly: 5500.0,
    priority: 1,
    status: "on_track",
    description: "3 months of essential fixed costs to weather income shocks.",
  },
  {
    id: "goal_vacation_02",
    title: "Annual Family Vacation",
    target: 40000.0,
    current: 15000.0,
    targetDate: "2026-11-30",
    requiredMonthly: 8333.0,
    priority: 3,
    status: "at_risk",
    description: "Year-end domestic vacation fund. At risk due to liquidity shock.",
  },
];

export default function GoalsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center pb-4 border-b border-border">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Financial Goals & Pacing</h2>
          <p className="text-sm text-muted-foreground">
            Deterministic goal timeline calculations and competing priority tracking
          </p>
        </div>
        <Button size="sm">
          <Plus className="w-4 h-4 mr-1.5" />
          Create New Goal
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {goals.map((goal) => {
          const progress = Math.round((goal.current / goal.target) * 100);
          return (
            <Card key={goal.id} className="border-border bg-card">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Target className="w-5 h-5 text-primary" />
                    <CardTitle className="text-lg">{goal.title}</CardTitle>
                  </div>
                  <Badge
                    variant={goal.status === "on_track" ? "success" : "warning"}
                    className="capitalize text-xs"
                  >
                    {goal.status === "on_track" ? "On Track" : "At Risk"}
                  </Badge>
                </div>
                <CardDescription className="text-xs">{goal.description}</CardDescription>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Progress bar */}
                <div>
                  <div className="flex justify-between text-xs font-mono mb-1.5">
                    <span>INR {goal.current.toLocaleString()}</span>
                    <span>INR {goal.target.toLocaleString()} ({progress}%)</span>
                  </div>
                  <div className="w-full h-2 bg-muted rounded-none overflow-hidden">
                    <div
                      className={`h-full ${
                        goal.status === "on_track" ? "bg-emerald-500" : "bg-amber-500"
                      }`}
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3 pt-2">
                  <div className="p-3 border border-border bg-background">
                    <span className="text-xs text-muted-foreground">Monthly Required</span>
                    <p className="text-sm font-bold font-mono mt-1">
                      INR {goal.requiredMonthly.toLocaleString()}/mo
                    </p>
                  </div>
                  <div className="p-3 border border-border bg-background">
                    <span className="text-xs text-muted-foreground">Target Deadline</span>
                    <p className="text-sm font-bold font-mono mt-1">{goal.targetDate}</p>
                  </div>
                </div>

                <div className="text-xs text-muted-foreground flex items-center justify-between pt-2 border-t border-border">
                  <span>Priority Rank: P{goal.priority}</span>
                  {goal.status === "at_risk" && (
                    <span className="text-amber-500 font-medium">
                      Advisor recommends pausing this cycle
                    </span>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
