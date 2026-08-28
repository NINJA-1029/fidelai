"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Bot, Send, ShieldCheck, CheckCircle2, ArrowRight, Sparkles, Scale, RefreshCw } from "lucide-react";

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
        "I have analyzed your updated financial state following the recent INR 12,000 unexpected expense. Here is your deterministic evidence synthesis and recommended action.",
      recommendation: {
        title: "Preserve Near-Term Liquidity",
        priority: "high",
        description:
          "Your 30-day projected balance of INR 19,400 falls INR 5,600 below your preferred cash buffer of INR 25,000. With upcoming bills of INR 18,000 due, we recommend deferring the vacation goal contribution and trimming discretionary spend.",
        impact: "INR 5,600 Deficit Shielded",
      },
      evidence: [
        {
          metric: "current_balance",
          label: "Current Balance",
          value: "INR 30,000.00",
          status: "confirmed",
          detail: "Post-debit liquid funds",
        },
        {
          metric: "projected_balance",
          label: "Projected Balance",
          value: "INR 19,400.00",
          status: "estimated",
          detail: "30-day deterministic run-rate",
        },
        {
          metric: "minimum_cash_buffer",
          label: "Safety Buffer",
          value: "INR 25,000.00",
          status: "confirmed",
          detail: "Configured user preference",
        },
        {
          metric: "upcoming_obligations",
          label: "Upcoming Obligations",
          value: "INR 18,000.00",
          status: "confirmed",
          detail: "Rent & utilities due within 6 days",
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
              label: ev.metric.replace(/_/g, " ").toUpperCase(),
              value: typeof ev.value === "number" ? `INR ${ev.value.toLocaleString()}` : String(ev.value),
              status: ev.status,
              detail: ev.description,
            })),
            alternatives: data.alternatives,
            competing_objectives: data.competing_objectives_considered,
            confidence: data.confidence,
          },
        ]);
      } else {
        throw new Error("Local API unavailable");
      }
    } catch (err) {
      // Offline fallback mock
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Based on deterministic balance projection of INR 19,400 against your INR 25,000 threshold, reducing non-essential commitments preserves liquidity without liquidating investments.",
          recommendation: {
            title: "Maintain Cash Buffer",
            priority: "high",
            description: "Defer secondary goals and reduce discretionary spend by INR 4,000.",
            impact: "INR 4,000 Cash Protected",
          },
          evidence: [
            { metric: "proj", label: "Projected Cash", value: "INR 19,400", status: "estimated", detail: "30-day forecast" },
            { metric: "buf", label: "Buffer Target", value: "INR 25,000", status: "confirmed", detail: "Safety threshold" },
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
    <div className="space-y-8">
      <div className="flex justify-between items-center pb-4 border-b border-border">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Autonomous AI Advisor</h2>
          <p className="text-sm text-muted-foreground">
            Explainable, evidence-backed decision support powered by local Qwen on llama.cpp
          </p>
        </div>
        <Badge variant="outline" className="px-3 py-1">
          Inference: Native Local
        </Badge>
      </div>

      <div className="space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className="space-y-4">
            {msg.role === "user" ? (
              <div className="flex justify-end">
                <div className="bg-primary text-primary-foreground p-4 max-w-lg rounded-none text-sm">
                  {msg.content}
                </div>
              </div>
            ) : (
              <Card className="border-border bg-card">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Bot className="w-5 h-5 text-primary" />
                      <CardTitle className="text-base">Fidel Strategic Reasoner</CardTitle>
                    </div>
                    {msg.confidence && (
                      <Badge variant="default" className="text-xs">
                        Confidence: {Math.round(msg.confidence * 100)}%
                      </Badge>
                    )}
                  </div>
                  <CardDescription className="text-xs mt-1">
                    Grounded strictly in deterministic financial facts
                  </CardDescription>
                </CardHeader>

                <CardContent className="space-y-6">
                  {/* Recommendation banner */}
                  {msg.recommendation && (
                    <div className="p-4 bg-muted/40 border border-border">
                      <div className="flex items-center justify-between">
                        <h4 className="font-bold text-base">{msg.recommendation.title}</h4>
                        <Badge variant="destructive" className="uppercase text-xs">
                          {msg.recommendation.priority}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mt-2 leading-relaxed">
                        {msg.recommendation.description}
                      </p>
                    </div>
                  )}

                  {/* Evidence Matrix */}
                  {msg.evidence && msg.evidence.length > 0 && (
                    <div>
                      <h5 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">
                        Deterministic Evidence Metrics
                      </h5>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                        {msg.evidence.map((ev: any, evIdx: number) => (
                          <div key={evIdx} className="p-3 border border-border bg-background">
                            <div className="flex justify-between items-center text-xs text-muted-foreground">
                              <span>{ev.label}</span>
                              <Badge variant="outline" className="text-[10px] px-1.5 py-0">
                                {ev.status}
                              </Badge>
                            </div>
                            <p className="text-sm font-bold font-mono mt-1.5">{ev.value}</p>
                            <p className="text-xs text-muted-foreground mt-1">{ev.detail}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Tradeoffs Evaluated */}
                  {msg.competing_objectives && msg.competing_objectives.length > 0 && (
                    <div className="p-4 bg-background border border-border">
                      <div className="flex items-center space-x-2 text-xs font-semibold text-muted-foreground uppercase mb-2">
                        <Scale className="w-4 h-4" />
                        <span>Competing Objectives & Tradeoffs Evaluated</span>
                      </div>
                      <ul className="space-y-1 text-sm text-muted-foreground">
                        {msg.competing_objectives.map((obj: string, oIdx: number) => (
                          <li key={oIdx} className="flex items-start space-x-2">
                            <span className="text-primary font-bold mr-1">-</span>
                            <span>{obj}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Actionable Alternatives */}
                  {msg.alternatives && msg.alternatives.length > 0 && (
                    <div>
                      <h5 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">
                        Actionable Alternative Options
                      </h5>
                      <div className="space-y-2">
                        {msg.alternatives.map((alt: string, altIdx: number) => (
                          <div
                            key={altIdx}
                            className="p-3 border border-border bg-muted/20 flex items-center justify-between hover:bg-muted/40 transition-colors"
                          >
                            <span className="text-sm">{alt}</span>
                            <Button size="sm" variant="outline" className="text-xs px-3 py-1 h-7">
                              Select
                              <ArrowRight className="w-3 h-3 ml-1" />
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

      {/* Query Input Box */}
      <form onSubmit={handleSend} className="flex gap-3 sticky bottom-4 bg-background pt-2">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask Fidel about tradeoffs, goal adjustments, or cash flow simulations..."
          disabled={isLoading}
          className="flex-1"
        />
        <Button type="submit" disabled={isLoading || !query.trim()}>
          {isLoading ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <>
              Send
              <Send className="w-4 h-4 ml-1.5" />
            </>
          )}
        </Button>
      </form>
    </div>
  );
}
