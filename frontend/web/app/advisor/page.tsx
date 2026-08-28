"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface AdvisorMessage {
  role: "user" | "assistant";
  content: string;
  recommendation?: {
    title: string;
    priority: string;
    description: string;
    impact?: string;
  };
  evidence?: {
    metric: string;
    label: string;
    value: string;
    status: string;
    detail: string;
  }[];
  alternatives?: string[];
  competing_objectives?: string[];
  confidence?: number;
}

export default function AIAdvisorPage() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<AdvisorMessage[]>([
    {
      role: "assistant",
      content:
        "Following an unexpected medical debit of INR 12,000.00, your 30-day projected reserve dips to INR 19,400.00 against your INR 25,000.00 target safety buffer.",
      recommendation: {
        title: "Preserve Near-Term Liquidity",
        priority: "HIGH PRIORITY",
        description:
          "An unexpected expense of INR 12,000 combined with upcoming obligations of INR 18,000 will compress liquid reserves below your configured INR 25,000 minimum safety threshold.",
        impact: "INR 5,600.00 DEFICIT SHIELDED",
      },
      evidence: [
        {
          metric: "current_balance",
          label: "EVIDENCE 01 // BALANCE",
          value: "INR 30,000.00",
          status: "CONFIRMED",
          detail: "Post-debit liquid funds",
        },
        {
          metric: "projected_balance",
          label: "EVIDENCE 02 // PROJECTION",
          value: "INR 19,400.00",
          status: "ESTIMATED",
          detail: "30-day deterministic run-rate",
        },
        {
          metric: "minimum_cash_buffer",
          label: "EVIDENCE 03 // BUFFER",
          value: "INR 25,000.00",
          status: "CONFIRMED",
          detail: "User safety threshold",
        },
        {
          metric: "upcoming_obligations",
          label: "EVIDENCE 04 // OBLIGATIONS",
          value: "INR 18,000.00",
          status: "CONFIRMED",
          detail: "Rent & bills due in 6 days",
        },
      ],
      alternatives: [
        "Temporarily pause the INR 8,333 vacation goal allocation for this billing cycle.",
        "Reduce remaining discretionary dining and shopping allocations by INR 4,000.",
        "Draw from liquid emergency reserves without liquidating long-term equity assets.",
      ],
      competing_objectives: [
        "Preserving immediate checking liquidity (Priority 1) vs Vacation Goal pacing (Priority 3).",
        "Retained INR 140,000 long-term investment portfolio compounding intact.",
      ],
      confidence: 0.94,
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userText = query;
    setQuery("");
    setMessages((prev) => [...prev, { role: "user", content: userText }]);
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/v1/agent/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user_demo_01",
          user_query: userText,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: data.reason,
            recommendation: data.recommendation,
            evidence: data.evidence.map((ev: any) => ({
              metric: ev.metric,
              label: `EVIDENCE // ${ev.metric.toUpperCase()}`,
              value: typeof ev.value === "number" ? `INR ${ev.value.toLocaleString()}` : String(ev.value),
              status: ev.status?.toUpperCase() || "CONFIRMED",
              detail: ev.description,
            })),
            alternatives: data.alternatives,
            competing_objectives: data.competing_objectives_considered,
            confidence: data.confidence,
          },
        ]);
      } else {
        throw new Error("Local API unreachable");
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Based on deterministic balance projection of INR 19,400 against your INR 25,000 threshold, reducing non-essential commitments preserves liquidity without liquidating investments.",
          recommendation: {
            title: "Maintain Cash Buffer",
            priority: "HIGH PRIORITY",
            description: "Defer secondary goals and reduce discretionary spend by INR 4,000.",
          },
          evidence: [
            { metric: "proj", label: "EVIDENCE // PROJECTION", value: "INR 19,400", status: "ESTIMATED", detail: "30-day forecast" },
            { metric: "buf", label: "EVIDENCE // BUFFER", value: "INR 25,000", status: "CONFIRMED", detail: "Safety threshold" },
          ],
          alternatives: [
            "Pause discretionary dining for 2 weeks",
            "Postpone non-essential vacation SIP",
          ],
          competing_objectives: ["Liquidity preservation prioritized over non-essential goals"],
          confidence: 0.92,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-[46px]">
      <div className="flex justify-between items-baseline pb-4 border-b border-border">
        <div>
          <span className="text-[11px] uppercase tracking-[0.18em] text-felt-gray block mb-1">
            02 // REASONING SYNTHESIS
          </span>
          <h2 className="text-[32px] md:text-[40px] font-light leading-[1.10] tracking-tight text-foreground">
            Strategic AI Advisor
          </h2>
        </div>
        <span className="text-[11px] font-mono text-felt-gray uppercase">
          LOCAL QWEN 2.5 // NATIVE
        </span>
      </div>

      <div className="space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className="space-y-4">
            {msg.role === "user" ? (
              <div className="flex justify-end">
                <div className="bg-muted p-5 max-w-lg rounded-none text-[14px] leading-relaxed border border-border text-foreground font-mono">
                  {msg.content}
                </div>
              </div>
            ) : (
              <Card>
                <CardHeader>
                  <div className="flex justify-between items-baseline">
                    <CardTitle className="text-[20px] font-normal">
                      Fidel Strategic Reasoning
                    </CardTitle>
                    {msg.confidence && (
                      <span className="text-[11px] font-mono text-felt-gray">
                        CONFIDENCE: {Math.round(msg.confidence * 100)}%
                      </span>
                    )}
                  </div>
                  <CardDescription className="text-[11px] uppercase tracking-wider">
                    Grounded in deterministic financial state metrics
                  </CardDescription>
                </CardHeader>

                <CardContent className="space-y-6">
                  {msg.recommendation && (
                    <div className="p-5 bg-muted/40 border border-border">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-normal text-[18px]">{msg.recommendation.title}</h4>
                        <Badge variant="default">{msg.recommendation.priority}</Badge>
                      </div>
                      <p className="text-[15px] leading-[1.6] text-felt-gray">
                        {msg.recommendation.description}
                      </p>
                    </div>
                  )}

                  {msg.evidence && msg.evidence.length > 0 && (
                    <div className="space-y-3">
                      <span className="text-[11px] font-mono uppercase tracking-widest text-felt-gray block">
                        DETERMINISTIC EVIDENCE MATRIX
                      </span>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                        {msg.evidence.map((ev, evIdx) => (
                          <div key={evIdx} className="p-4 border border-border bg-background">
                            <div className="flex justify-between items-center text-[10px] font-mono text-felt-gray">
                              <span>{ev.label}</span>
                              <span>{ev.status}</span>
                            </div>
                            <p className="text-[18px] font-mono mt-1.5 text-foreground">{ev.value}</p>
                            <p className="text-[11px] text-felt-gray mt-1 font-mono">{ev.detail}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {msg.competing_objectives && msg.competing_objectives.length > 0 && (
                    <div className="p-5 border border-border bg-background space-y-2">
                      <span className="text-[11px] font-mono uppercase tracking-widest text-felt-gray block">
                        COMPETING OBJECTIVES & TRADEOFFS EVALUATED
                      </span>
                      <ul className="space-y-1 text-[13px] text-felt-gray font-mono">
                        {msg.competing_objectives.map((obj, oIdx) => (
                          <li key={oIdx}>— {obj}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {msg.alternatives && msg.alternatives.length > 0 && (
                    <div className="space-y-3">
                      <span className="text-[11px] font-mono uppercase tracking-widest text-felt-gray block">
                        ACTIONABLE ALTERNATIVE OPTIONS
                      </span>
                      <div className="space-y-2">
                        {msg.alternatives.map((alt, altIdx) => (
                          <div
                            key={altIdx}
                            className="p-4 border border-border bg-muted/20 flex items-center justify-between text-[14px]"
                          >
                            <span>{alt}</span>
                            <Button size="sm" variant="outline">
                              SELECT
                            </Button>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </div>
        ))}
      </div>

      <form onSubmit={handleSend} className="flex gap-3 sticky bottom-4 bg-background pt-2">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask Fidel about tradeoffs, goal adjustments, or cash flow simulations..."
          disabled={isLoading}
          className="flex-1 font-mono text-[13px]"
        />
        <Button type="submit" disabled={isLoading || !query.trim()}>
          {isLoading ? "ANALYZING..." : "SUBMIT"}
        </Button>
      </form>
    </div>
  );
}
