import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ValidationError

from shared.contracts.contracts import (
    AgentRequest,
    AgentResponse,
    FinancialState,
    Recommendation,
    Evidence,
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
    retry_attempted: bool = False
    final_response: Optional[AgentResponse] = None


class FinancialReasoningAgent:
    """
    Orchestrates the multi-stage financial reasoning workflow:
    1. Tool Execution & Fact Gathering
    2. Structured LLM Synthesis
    3. Schema Validation & Self-Correction Retry
    4. Deterministic Fallback Generation
    """

    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.llm_provider = llm_provider or MockLLMProvider()

    def run(self, request: AgentRequest, state: FinancialState) -> AgentResponse:
        workflow_state = AgentWorkflowState(
            user_id=request.user_id,
            trigger_event=request.trigger_event.model_dump() if request.trigger_event else None,
            user_query=request.user_query,
            financial_state=state,
        )

        # Stage 1: Gather deterministic facts and evidence
        evidence = AgentTools.gather_evidence_for_liquidity(state)
        workflow_state.evidence = evidence

        # Stage 2: Build prompts
        system_prompt = (
            "You are a fiduciary AI financial strategist and decision advisor. "
            "Reason strictly over the provided factual evidence and deterministic calculations. "
            "Never perform financial arithmetic or invent monetary figures. "
            "Resolve competing objectives (such as liquidity preservation vs goal contributions). "
            "Provide actionable alternatives. "
            "Strictly avoid emojis or decorative glyphs. "
            "Output valid JSON conforming exactly to the AgentResponse schema."
        )

        user_prompt = self._build_prompt(state, evidence, request.user_query)

        # Stage 3: LLM Inference with Self-Correction
        try:
            raw_output = self.llm_provider.generate(prompt=user_prompt, system_prompt=system_prompt)
            workflow_state.raw_llm_output = raw_output
            response = self._parse_and_validate(raw_output, request.user_id, evidence)
            workflow_state.final_response = response
            return response

        except (json.JSONDecodeError, ValidationError, KeyError, TypeError) as parse_err:
            logger.warning(f"Initial LLM response failed validation: {parse_err}. Attempting self-correction retry.")
            workflow_state.retry_attempted = True

            try:
                retry_prompt = self._build_retry_prompt(user_prompt, workflow_state.raw_llm_output or "", str(parse_err))
                corrected_output = self.llm_provider.generate(prompt=retry_prompt, system_prompt=system_prompt)
                response = self._parse_and_validate(corrected_output, request.user_id, evidence)
                workflow_state.final_response = response
                return response
            except Exception as retry_err:
                logger.warning(f"Self-correction failed: {retry_err}. Falling back to deterministic synthesizer.")
                return self._deterministic_fallback(request.user_id, state, evidence)

        except Exception as e:
            logger.warning(f"LLM execution error: {e}. Executing deterministic fallback recommendation.")
            return self._deterministic_fallback(request.user_id, state, evidence)

    def _build_prompt(
        self,
        state: FinancialState,
        evidence: List[Evidence],
        query: Optional[str],
    ) -> str:
        evidence_lines = [
            f"- {e.metric}: {e.value} (threshold: {e.threshold}, status: {e.status.value}) - {e.description}"
            for e in evidence
        ]
        evidence_str = "\n".join(evidence_lines)

        goals_str = (
            ", ".join([f"{g.title} (target: INR {g.target_amount:,.0f}, priority: {g.priority})" for g in state.financial_goals])
            if state.financial_goals
            else "No explicit goals configured"
        )

        return (
            f"FINANCIAL CONTEXT:\n"
            f"- User ID: {state.user_id}\n"
            f"- Current Liquid Balance: INR {state.current_balance:,.2f}\n"
            f"- Available Cash: INR {state.available_cash:,.2f}\n"
            f"- 30-Day Projected Balance: INR {state.projected_balance:,.2f}\n"
            f"- Minimum Preferred Cash Buffer: INR {state.minimum_cash_buffer:,.2f}\n"
            f"- Upcoming Obligations (Next 30 Days): INR {state.upcoming_obligations:,.2f}\n"
            f"- Active Goals: {goals_str}\n"
            f"- Investment Portfolio Value: INR {state.investments_total_value:,.2f}\n\n"
            f"DETERMINISTIC EVIDENCE METRICS:\n"
            f"{evidence_str}\n\n"
            f"USER QUERY:\n"
            f"{query or 'Analyze recent financial movements, evaluate liquidity risks, and recommend corrective actions.'}\n\n"
            f"OUTPUT FORMAT REQUIREMENT:\n"
            f"Respond with a single raw JSON object matching this structure:\n"
            f"{{\n"
            f'  "response_id": "resp_<unique_id>",\n'
            f'  "user_id": "{state.user_id}",\n'
            f'  "recommendation": {{\n'
            f'    "recommendation_id": "rec_<unique_id>",\n'
            f'    "title": "<Concise Action Title>",\n'
            f'    "priority": "critical|high|medium|low",\n'
            f'    "description": "<Detailed fiduciary recommendation>",\n'
            f'    "impact_amount": <float or null>,\n'
            f'    "category": "liquidity|savings|investment|debt|budgeting"\n'
            f"  }},\n"
            f'  "reason": "<Evidence-backed explanation>",\n'
            f'  "confidence": <float between 0.8 and 1.0>,\n'
            f'  "alternatives": ["<Actionable alternative 1>", "<Actionable alternative 2>"],\n'
            f'  "competing_objectives_considered": ["<Tradeoff 1>", "<Tradeoff 2>"]\n'
            f"}}"
        )

    def _build_retry_prompt(self, original_prompt: str, bad_output: str, error_msg: str) -> str:
        return (
            f"{original_prompt}\n\n"
            f"PREVIOUS ATTEMPT FAILED WITH ERROR:\n{error_msg}\n\n"
            f"PREVIOUS ATTEMPT OUTPUT:\n{bad_output}\n\n"
            f"CORRECTION INSTRUCTION:\n"
            f"Please output ONLY valid JSON that strictly adheres to the requested schema. Do not enclose in markdown blocks."
        )

    def _parse_and_validate(
        self,
        raw_output: str,
        user_id: str,
        evidence: List[Evidence],
    ) -> AgentResponse:
        cleaned_output = raw_output.strip()
        if cleaned_output.startswith("```json"):
            cleaned_output = cleaned_output[7:]
        if cleaned_output.startswith("```"):
            cleaned_output = cleaned_output[3:]
        if cleaned_output.endswith("```"):
            cleaned_output = cleaned_output[:-3]
        cleaned_output = cleaned_output.strip()

        parsed_json = json.loads(cleaned_output)

        rec_dict = parsed_json["recommendation"]
        recommendation = Recommendation(
            recommendation_id=rec_dict.get("recommendation_id", f"rec_{int(datetime.now(timezone.utc).timestamp())}"),
            title=rec_dict.get("title", "Liquidity Optimization Recommendation"),
            priority=rec_dict.get("priority", "high"),
            description=rec_dict.get("description", "Maintain reserve liquidity."),
            impact_amount=rec_dict.get("impact_amount"),
            category=rec_dict.get("category", "liquidity"),
        )

        alternatives = parsed_json.get("alternatives", [])
        if len(alternatives) < 2:
            alternatives.extend([
                "Temporarily defer non-essential discretionary entertainment spending.",
                "Review and pause non-critical savings goals for the upcoming cycle."
            ])
            alternatives = alternatives[:3]

        competing = parsed_json.get(
            "competing_objectives_considered",
            ["Liquidity buffer preservation vs. non-essential goal funding."]
        )

        return AgentResponse(
            response_id=parsed_json.get("response_id", f"resp_{int(datetime.now(timezone.utc).timestamp())}"),
            user_id=user_id,
            recommendation=recommendation,
            reason=parsed_json.get("reason", "Deterministic synthesis of liquid reserves and obligations."),
            evidence=evidence,
            confidence=max(0.0, min(1.0, float(parsed_json.get("confidence", 0.94)))),
            alternatives=alternatives,
            competing_objectives_considered=competing,
            generated_at=datetime.now(timezone.utc),
        )

    def _deterministic_fallback(
        self,
        user_id: str,
        state: FinancialState,
        evidence: List[Evidence],
    ) -> AgentResponse:
        is_deficit = state.projected_balance < state.minimum_cash_buffer
        deficit = max(0.0, round(state.minimum_cash_buffer - state.projected_balance, 2))
        now_ts = int(datetime.now(timezone.utc).timestamp())

        if is_deficit:
            rec_title = "Preserve Near-Term Liquidity"
            rec_priority = "high"
            rec_desc = (
                f"Your 30-day projected balance of INR {state.projected_balance:,.2f} dips below your "
                f"INR {state.minimum_cash_buffer:,.2f} reserve buffer by INR {deficit:,.2f}. "
                f"With scheduled upcoming obligations of INR {state.upcoming_obligations:,.2f}, we recommend "
                f"pausing non-essential goal contributions and trimming discretionary spending."
            )
            reason = (
                f"Projected month-end cash balance violates the preferred minimum safety buffer by INR {deficit:,.2f}, "
                f"creating potential liquidity exposure before the next income cycle."
            )
            alternatives = [
                "Temporarily pause secondary goal contributions (e.g. vacation fund) for this billing cycle.",
                "Reduce remaining discretionary dining and entertainment allocations by INR 4,000.",
                "Utilize short-term liquid savings to protect primary checking buffer without touching long-term investments.",
            ]
            competing = [
                "Liquidity preservation (Priority 1) vs. Secondary Goal pacing (Priority 3).",
                "Retaining long-term investments rather than liquidating equity for temporary shortfall."
            ]
        else:
            rec_title = "Deploy Surplus Liquidity"
            rec_priority = "medium"
            surplus = round(state.projected_balance - state.minimum_cash_buffer, 2)
            rec_desc = (
                f"Your projected month-end balance of INR {state.projected_balance:,.2f} maintains a healthy "
                f"surplus of INR {surplus:,.2f} above your INR {state.minimum_cash_buffer:,.2f} buffer. "
                f"You can safely allocate excess cash towards your highest priority financial goals."
            )
            reason = (
                f"Deterministic projections confirm full coverage of upcoming obligations with an available "
                f"liquidity buffer of INR {surplus:,.2f}."
            )
            alternatives = [
                "Accelerate primary goal funding with an additional lump-sum allocation.",
                "Direct surplus liquidity into high-yield liquid instruments.",
                "Maintain current pacing while building emergency reserves toward target.",
            ]
            competing = [
                "Surplus deployment to long-term goals vs. building additional liquid safety margin."
            ]

        return AgentResponse(
            response_id=f"resp_fallback_{now_ts}",
            user_id=user_id,
            recommendation=Recommendation(
                recommendation_id=f"rec_fallback_{now_ts}",
                title=rec_title,
                priority=rec_priority,
                description=rec_desc,
                impact_amount=deficit if is_deficit else None,
                category="liquidity",
            ),
            reason=reason,
            evidence=evidence,
            confidence=0.92,
            alternatives=alternatives,
            competing_objectives_considered=competing,
            generated_at=datetime.now(timezone.utc),
        )

