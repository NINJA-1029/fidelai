import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

from shared.contracts.contracts import (
    AgentRequest,
    AgentResponse,
    FinancialState,
    Recommendation,
    Evidence,
    RiskSignal,
)
from backend.agent.llm_provider import LLMProvider, MockLLMProvider
from backend.agent.tools import AgentTools

logger = logging.getLogger(__name__)


class AgentWorkflowState(BaseModel):
    user_id: str
    trigger_event: Optional[Dict[str, Any]] = None
    user_query: Optional[str] = None
    financial_state: Optional[FinancialState] = None
    evidence: List[Evidence] = Field(default_factory=list)
    raw_llm_output: Optional[str] = None
    final_response: Optional[AgentResponse] = None


class FinancialReasoningAgent:
    """
    Orchestrates the multi-stage financial reasoning workflow.
    """

    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.llm_provider = llm_provider or MockLLMProvider()

    def run(self, request: AgentRequest, state: FinancialState) -> AgentResponse:
        workflow_state = AgentWorkflowState(
            user_id=request.user_id,
            trigger_event=request.trigger_event.model_dump() if request.trigger_event else None,
            user_query=request.user_query,
            financial_state=state
        )

        # Node 1: Execute deterministic tools to gather evidence
        evidence = AgentTools.gather_evidence_for_liquidity(state)
        workflow_state.evidence = evidence

        # Node 2: Synthesize reasoning via LLMProvider
        system_prompt = (
            "You are a fiduciary AI financial strategist. Reason strictly over the provided factual evidence. "
            "Resolve competing objectives (e.g. liquidity preservation vs goal contributions). "
            "Output valid JSON conforming to the AgentResponse schema."
        )

        user_prompt = self._build_prompt(state, evidence, request.user_query)

        try:
            raw_output = self.llm_provider.generate(prompt=user_prompt, system_prompt=system_prompt)
            workflow_state.raw_llm_output = raw_output
            parsed_json = json.loads(raw_output)
            
            # Node 3: Validate output against schema
            response = AgentResponse(
                response_id=parsed_json.get("response_id", f"resp_{int(datetime.utcnow().timestamp())}"),
                user_id=request.user_id,
                recommendation=Recommendation(**parsed_json["recommendation"]),
                reason=parsed_json.get("reason", "Deterministic synthesis of current cash reserves and obligations."),
                evidence=evidence,
                confidence=float(parsed_json.get("confidence", 0.94)),
                alternatives=parsed_json.get("alternatives", []),
                competing_objectives_considered=parsed_json.get("competing_objectives_considered", []),
                generated_at=datetime.utcnow()
            )
            workflow_state.final_response = response
            return response

        except Exception as e:
            logger.warning(f"LLM parsing/generation failed: {e}. Executing deterministic fallback recommendation.")
            return self._deterministic_fallback(request.user_id, state, evidence)

    def _build_prompt(self, state: FinancialState, evidence: List[Evidence], query: Optional[str]) -> str:
        evidence_str = "\n".join([f"- {e.metric}: {e.value} ({e.description})" for e in evidence])
        return (
            f"FINANCIAL CONTEXT:\n"
            f"- User: {state.user_id}\n"
            f"- Current Liquid Balance: INR {state.current_balance:,.2f}\n"
            f"- Projected Balance: INR {state.projected_balance:,.2f}\n"
            f"- Minimum Cash Buffer: INR {state.minimum_cash_buffer:,.2f}\n"
            f"- Upcoming Obligations: INR {state.upcoming_obligations:,.2f}\n\n"
            f"EVIDENCE METRICS:\n{evidence_str}\n\n"
            f"USER QUERY: {query or 'Analyze recent cash flow changes and recommend necessary adjustments.'}\n\n"
            f"Return JSON conforming to AgentResponse schema."
        )

    def _deterministic_fallback(self, user_id: str, state: FinancialState, evidence: List[Evidence]) -> AgentResponse:
        deficit = max(0.0, state.minimum_cash_buffer - state.projected_balance)
        return AgentResponse(
            response_id=f"resp_fallback_{int(datetime.utcnow().timestamp())}",
            user_id=user_id,
            recommendation=Recommendation(
                recommendation_id=f"rec_fallback_{int(datetime.utcnow().timestamp())}",
                title="Preserve Near-Term Liquidity",
                priority="high",
                description=(
                    f"Your 30-day projected balance of INR {state.projected_balance:,.2f} dips below your "
                    f"INR {state.minimum_cash_buffer:,.2f} reserve buffer by INR {deficit:,.2f}. "
                    f"We recommend deferring non-essential goal contributions and trimming discretionary spending."
                ),
                impact_amount=deficit,
                category="liquidity"
            ),
            reason=f"An unexpected outflow combined with upcoming obligations will reduce liquid reserves below your safety buffer.",
            evidence=evidence,
            confidence=0.92,
            alternatives=[
                "Temporarily pause discretionary entertainment and dining allocations.",
                "Defer non-essential savings goal contributions until the next income cycle."
            ],
            competing_objectives_considered=[
                "Liquidity buffer preservation vs. non-essential goal funding."
            ],
            generated_at=datetime.utcnow()
        )
