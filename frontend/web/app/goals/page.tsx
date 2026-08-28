import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const goals = [
  {
    id: "goal_emergency_01",
    title: "Emergency Fund Reserve",
    target: 72000.0,
    current: 50000.0,
    targetDate: "2026-12-31",
    requiredMonthly: 5500.0,
    priority: 1,
    status: "ON TRACK",
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
    status: "AT RISK // PAUSE RECOMMENDED",
    description: "Domestic vacation fund. Advisor recommends pausing this cycle to protect liquidity.",
  },
];

export default function GoalsPage() {
  return (
    <div className="space-y-[46px]">
      <div className="flex justify-between items-baseline pb-4 border-b border-border">
        <div>
          <span className="text-[11px] uppercase tracking-[0.18em] text-felt-gray block mb-1">
            04 // PACING ENGINE
          </span>
          <h2 className="text-[32px] md:text-[40px] font-light leading-[1.10] tracking-tight text-foreground">
            Financial Goals & Pacing
          </h2>
        </div>
        <span className="text-[11px] font-mono text-felt-gray uppercase">
          2 ACTIVE TARGETS
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {goals.map((goal) => {
          const progress = Math.round((goal.current / goal.target) * 100);
          return (
            <Card key={goal.id}>
              <CardHeader>
                <div className="flex items-baseline justify-between">
                  <CardTitle className="text-[20px] font-normal">{goal.title}</CardTitle>
                  <span className="text-[11px] font-mono text-felt-gray">{goal.status}</span>
                </div>
                <CardDescription className="text-[12px]">{goal.description}</CardDescription>
              </CardHeader>

              <CardContent className="space-y-6">
                <div>
                  <div className="flex justify-between text-[12px] font-mono mb-2 text-felt-gray">
                    <span>INR {goal.current.toLocaleString()}</span>
                    <span>INR {goal.target.toLocaleString()} ({progress}%)</span>
                  </div>
                  <div className="w-full h-1.5 bg-muted rounded-none overflow-hidden border border-border">
                    <div
                      className="h-full bg-foreground"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 border border-border bg-background">
                    <span className="text-[10px] font-mono uppercase text-felt-gray block">MONTHLY PACING</span>
                    <p className="text-[16px] font-mono font-normal mt-1 text-foreground">
                      INR {goal.requiredMonthly.toLocaleString()}/mo
                    </p>
                  </div>
                  <div className="p-4 border border-border bg-background">
                    <span className="text-[10px] font-mono uppercase text-felt-gray block">TARGET DEADLINE</span>
                    <p className="text-[16px] font-mono font-normal mt-1 text-foreground">{goal.targetDate}</p>
                  </div>
                </div>

                <div className="text-[11px] font-mono text-felt-gray flex items-center justify-between pt-2 border-t border-border">
                  <span>PRIORITY: P{goal.priority}</span>
                  <span>CONFIDENCE: 94%</span>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
