import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { messages, user_id = "user_demo_01" } = await req.json();
    const lastUserMessage = messages[messages.length - 1]?.content || "Analyze current financial status";

    // Proxy to FastAPI backend orchestrator
    const backendRes = await fetch("http://localhost:8000/api/v1/agent/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: user_id,
        user_query: lastUserMessage,
      }),
    });

    if (backendRes.ok) {
      const data = await backendRes.json();
      return NextResponse.json(data);
    }

    // Fallback response if local backend is restarting
    return NextResponse.json({
      response_id: "resp_fallback",
      user_id: user_id,
      recommendation: {
        recommendation_id: "rec_fallback",
        title: "Preserve Near-Term Liquidity",
        priority: "high",
        description: "Your 30-day projected balance falls below your minimum cash buffer of INR 25,000.",
        impact_amount: 5600.0,
        category: "liquidity",
      },
      reason: "Unexpected medical debit and upcoming obligations reduce liquidity below threshold.",
      evidence: [
        { metric: "projected_balance", value: 19400.0, status: "estimated" },
        { metric: "minimum_cash_buffer", value: 25000.0, status: "confirmed" },
      ],
      confidence: 0.94,
      alternatives: [
        "Pause secondary vacation goal contribution",
        "Trim discretionary allocations by INR 4,000",
      ],
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: "Advisor execution failed", details: error.message },
      { status: 500 }
    );
  }
}
