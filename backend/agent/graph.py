import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ValidationError
from langgraph.graph import StateGraph, START, END

from shared.contracts.contracts import (
    AgentRequest,
    AgentResponse,
    FinancialState,
    Recommendation,
    Evidence,
)
from backend.agent.llm_provider import LLMProvider, MockLLMProvider, get_llm_provider
from backend.agent.tools import AgentTools
from backend.repositories.financial_repository import repo

logger = logging.getLogger(__name__)


class AgentWorkflowState(BaseModel):
    """
    Canonical LangGraph workflow state tracking execution across all nodes.
    """
    user_id: str
    trigger_event: Optional[Dict[str, Any]] = None
    user_query: Optional[str] = None
    financial_state: Optional[FinancialState] = None
    evidence: List[Evidence] = Field(default_factory=list)
    past_memories: List[AgentResponse] = Field(default_factory=list)
    raw_llm_output: Optional[str] = None
    validation_error: Optional[str] = None
    is_valid: bool = False
    retry_attempted: bool = False
    final_response: Optional[AgentResponse] = None


class FinancialReasoningAgent:
    """
    Orchestrates the multi-stage financial reasoning workflow with Long-Term Memory:
    1. Retrieve Past Decision Memories
    2. Tool Execution & Fact Gathering
    3. Structured LLM Synthesis
    4. Schema Validation & Self-Correction Retry
    5. Deterministic Fallback Generation & Memory Persistence
    """

    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.llm_provider = llm_provider or get_llm_provider()
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentWorkflowState)

        # Register Graph Nodes
        workflow.add_node("gather_evidence", self._node_gather_evidence)
        workflow.add_node("synthesize_prompt", self._node_synthesize_prompt)
        workflow.add_node("llm_inference", self._node_llm_inference)
        workflow.add_node("validate_output", self._node_validate_output)
        workflow.add_node("self_correct_retry", self._node_self_correct_retry)
        workflow.add_node("deterministic_fallback", self._node_deterministic_fallback)

        # Standard Sequential Edges
        workflow.add_edge(START, "gather_evidence")
        workflow.add_edge("gather_evidence", "synthesize_prompt")
        workflow.add_edge("synthesize_prompt", "llm_inference")
        workflow.add_edge("llm_inference", "validate_output")

        # Conditional Routing Edge after Output Validation
        workflow.add_conditional_edges(
            "validate_output",
            self._route_after_validation,
            {
                "end": END,
                "self_correct_retry": "self_correct_retry",
                "deterministic_fallback": "deterministic_fallback",
            },
        )

        # Stage 1: Gather deterministic facts, evidence, and long-term memory
        evidence = AgentTools.gather_evidence_for_liquidity(state)
        workflow_state.evidence = evidence
        past_memories = repo.get_agent_memories(request.user_id, limit=3)
        workflow_state.past_memories = past_memories

        return {
            "evidence": evidence,
            "past_memories": past_memories,
        }

    def _node_synthesize_prompt(self, state: AgentWorkflowState) -> Dict[str, Any]:
        system_prompt = (
            "You are a fiduciary AI financial strategist and decision advisor. "
            "Reason strictly over the provided factual evidence, past advice history, and deterministic calculations. "
            "Never perform financial arithmetic or invent monetary figures. "
            "Resolve competing objectives (such as liquidity preservation vs goal contributions). "
            "Provide actionable alternatives. "
            "Strictly avoid emojis or decorative glyphs. "
            "Output valid JSON conforming exactly to the AgentResponse schema."
        )

        user_prompt = self._build_prompt(state, evidence, request.user_query, past_memories)

        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
        }

    def _node_llm_inference(self, state: AgentWorkflowState) -> Dict[str, Any]:
        try:
            raw_output = self.llm_provider.generate(prompt=user_prompt, system_prompt=system_prompt)
            workflow_state.raw_llm_output = raw_output
            response = self._parse_and_validate(raw_output, request.user_id, evidence)
            workflow_state.final_response = response
            repo.save_agent_memory(request.user_id, response, request.user_query)
            return response

        try:
            response = self._parse_and_validate(state.raw_llm_output, state.user_id, state.evidence)
            return {
                "final_response": response,
                "is_valid": True,
                "validation_error": None,
            }
        except (json.JSONDecodeError, ValidationError, KeyError, TypeError) as parse_err:
            logger.warning(f"Initial LLM response failed validation: {parse_err}. Attempting self-correction retry.")
            workflow_state.retry_attempted = True

            try:
                retry_prompt = self._build_retry_prompt(user_prompt, workflow_state.raw_llm_output or "", str(parse_err))
                corrected_output = self.llm_provider.generate(prompt=retry_prompt, system_prompt=system_prompt)
                response = self._parse_and_validate(corrected_output, request.user_id, evidence)
                workflow_state.final_response = response
                repo.save_agent_memory(request.user_id, response, request.user_query)
                return response
            except Exception as retry_err:
                logger.warning(f"Self-correction failed: {retry_err}. Falling back to deterministic synthesizer.")
                fallback_resp = self._deterministic_fallback(request.user_id, state, evidence)
                repo.save_agent_memory(request.user_id, fallback_resp, request.user_query)
                return fallback_resp

        result = self.graph.invoke(initial_state)

        if isinstance(result, dict):
            final_response = result.get("final_response")
        elif hasattr(result, "final_response"):
            final_response = result.final_response
        else:
            final_response = None

        if final_response is None:
            evidence = AgentTools.gather_evidence_for_liquidity(state)
            final_response = self._deterministic_fallback(request.user_id, state, evidence)

        try:
            repo.save_agent_memory(request.user_id, final_response, request.user_query)
        except Exception as e:
            logger.warning(f"LLM execution error: {e}. Executing deterministic fallback recommendation.")
            fallback_resp = self._deterministic_fallback(request.user_id, state, evidence)
            repo.save_agent_memory(request.user_id, fallback_resp, request.user_query)
            return fallback_resp

    def _build_prompt(
        self,
        state: FinancialState,
        evidence: List[Evidence],
        query: Optional[str],
        past_memories: Optional[List[AgentResponse]] = None,
    ) -> str:
        evidence_lines = [
            f"- {e.metric}: {e.value} (threshold: {e.threshold}, status: {e.status.value}) - {e.description}"
            for e in evidence
        ]
        evidence_str = "\n".join(evidence_lines)

        tradeoff_ctx = AgentTools.gather_tradeoff_context(state)
        goals_lines = [
            f"  * [Priority {g['priority']}] {g['title']} (Monthly: INR {g['monthly_req']:,.2f}, Target: INR {g['target_amount']:,.2f}, Saved: INR {g['current_amount']:,.2f})"
            for g in tradeoff_ctx["goals_ranked"]
        ]
        goals_block = "\n".join(goals_lines) if goals_lines else "  * No active goals configured"

        if tradeoff_ctx["is_deficit"]:
            buffer_status = f"DEFICIT of INR {tradeoff_ctx['shortfall_amount']:,.2f}"
        else:
            buffer_status = f"SURPLUS of INR {tradeoff_ctx['surplus_amount']:,.2f}"

        memory_section = ""
        if past_memories:
            mem_lines = [
                f"- Past Recommendation: {m.recommendation.title} (Priority: {m.recommendation.priority}, Category: {m.recommendation.category})"
                for m in past_memories
            ]
            memory_section = f"\nHISTORICAL ADVICE MEMORY:\n" + "\n".join(mem_lines) + "\n"

        memory_section = ""
        if past_memories:
            mem_lines = [
                f"- Past Recommendation: {m.recommendation.title} (Priority: {m.recommendation.priority}, Category: {m.recommendation.category})"
                for m in past_memories
            ]
            memory_section = f"\nHISTORICAL ADVICE MEMORY:\n" + "\n".join(mem_lines) + "\n"

        return (
            f"FINANCIAL CONTEXT:\n"
            f"- User ID: {state.user_id}\n"
            f"- Current Liquid Balance: INR {state.current_balance:,.2f}\n"
            f"- Available Cash: INR {state.available_cash:,.2f}\n"
            f"- 30-Day Projected Balance: INR {state.projected_balance:,.2f}\n"
            f"- Minimum Preferred Cash Buffer: INR {state.minimum_cash_buffer:,.2f}\n"
            f"- Upcoming Obligations (Next 30 Days): INR {state.upcoming_obligations:,.2f}\n"
            f"- Active Goals: {goals_str}\n"
            f"- Investment Portfolio Value: INR {state.investments_total_value:,.2f}\n"
            f"{memory_section}\n"
            f"DETERMINISTIC EVIDENCE METRICS:\n"
            f"{evidence_str}\n\n"
            f"USER QUERY:\n"
            f"{query or 'Analyze recent financial movements, evaluate liquidity risks vs competing goals, and recommend optimal trade-offs.'}\n\n"
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
            f'  "reason": "<Evidence-backed explanation articulating the core trade-off rationale>",\n'
            f'  "confidence": <float between 0.8 and 1.0>,\n'
            f'  "alternatives": [\n'
            f'    "<Actionable alternative 1 with specific trade-off or amount>",\n'
            f'    "<Actionable alternative 2 with specific trade-off or amount>"\n'
            f"  ],\n"
            f'  "competing_objectives_considered": [\n'
            f'    "<Explicit trade-off 1, e.g. Liquidity buffer defense vs pausing secondary goal>",\n'
            f'    "<Explicit trade-off 2, e.g. Protecting compounding investments vs trimming discretionary spending>"\n'
            f"  ]\n"
            f"}}"
        )

    def _build_retry_prompt(self, original_prompt: str, bad_output: str, error_msg: str) -> str:
        return (
            f"{original_prompt}\n\n"
            f"PREVIOUS ATTEMPT FAILED WITH ERROR:\n{error_msg}\n\n"
            f"PREVIOUS ATTEMPT OUTPUT:\n{bad_output}\n\n"
            f"CORRECTION INSTRUCTION:\n"
            f"Please output ONLY valid JSON that strictly adheres to the requested schema. Ensure at least two distinct alternatives and explicit competing objectives. Do not enclose in markdown blocks."
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
        if not isinstance(alternatives, list):
            alternatives = []
        if len(alternatives) < 2:
            alternatives.extend([
                "Temporarily pause lower-priority goal contributions for the upcoming billing cycle.",
                "Reduce monthly discretionary lifestyle allocations by 25% to restore liquidity buffer.",
            ])
            alternatives = alternatives[:3]

        competing = parsed_json.get("competing_objectives_considered", [])
        if not isinstance(competing, list) or len(competing) < 1:
            competing = [
                "Liquidity buffer preservation vs. non-essential goal funding pacing.",
                "Protecting compounding investment portfolio vs. cash flow deficit resolution.",
            ]

        return AgentResponse(
            response_id=parsed_json.get("response_id", f"resp_{int(datetime.now(timezone.utc).timestamp())}"),
            user_id=user_id,
            recommendation=recommendation,
            reason=parsed_json.get("reason", "Deterministic synthesis of liquid reserves, goals, and obligations."),
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
        tradeoff_ctx = AgentTools.gather_tradeoff_context(state)
        is_deficit = tradeoff_ctx["is_deficit"]
        deficit = tradeoff_ctx["shortfall_amount"]
        surplus = tradeoff_ctx["surplus_amount"]
        goals = tradeoff_ctx["goals_ranked"]
        now_ts = int(datetime.now(timezone.utc).timestamp())

        if is_deficit:
            rec_title = "Preserve Near-Term Liquidity"
            rec_priority = "high"
            rec_desc = (
                f"Your 30-day projected balance of INR {state.projected_balance:,.2f} dips below your "
                f"INR {state.minimum_cash_buffer:,.2f} reserve buffer by INR {deficit:,.2f}. "
                f"With scheduled upcoming obligations of INR {state.upcoming_obligations:,.2f}, we recommend "
                f"temporarily adjusting lower-priority allocations to defend your cash floor."
            )
            reason = (
                f"Projected month-end cash balance violates the preferred minimum safety buffer by INR {deficit:,.2f}, "
                f"creating potential liquidity exposure before the next income cycle."
            )

            # Formulate goal-specific alternative if active goals exist
            if goals:
                lowest_goal = goals[-1]
                highest_goal = goals[0]
                alt_goal = (
                    f"Temporarily pause monthly contribution of INR {lowest_goal['monthly_req']:,.2f} to "
                    f"'{lowest_goal['title']}' (Priority {lowest_goal['priority']}) while maintaining "
                    f"'{highest_goal['title']}' (Priority {highest_goal['priority']})."
                )
            else:
                alt_goal = "Defer non-essential savings allocations until liquid reserves recover."

            alternatives = [
                alt_goal,
                f"Trim discretionary lifestyle and entertainment spending by up to INR {min(4000.0, state.discretionary_expenses):,.2f}.",
                "Utilize short-term liquid savings to protect checking buffer rather than liquidating compounding investments.",
            ]

            competing = [
                "Liquidity Buffer Defense (Priority 1) vs. Secondary Goal Funding (Priority 3).",
                f"Preserving Long-Term Investments (INR {state.investments_total_value:,.2f}) vs. Selling Assets for Temporary Shortfall.",
                "Discretionary Lifestyle Freedom vs. Strict Reserve Protection.",
            ]
        else:
            rec_title = "Deploy Surplus Liquidity"
            rec_priority = "medium"
            rec_desc = (
                f"Your projected month-end balance of INR {state.projected_balance:,.2f} maintains a healthy "
                f"surplus of INR {surplus:,.2f} above your INR {state.minimum_cash_buffer:,.2f} buffer. "
                f"You can safely allocate excess cash towards your highest priority financial goals."
            )
            reason = (
                f"Deterministic projections confirm full coverage of upcoming obligations with an available "
                f"liquidity buffer of INR {surplus:,.2f}."
            )

            if goals:
                primary_goal = goals[0]
                alt_primary = (
                    f"Accelerate '{primary_goal['title']}' (Priority {primary_goal['priority']}) with an extra "
                    f"lump-sum allocation of INR {min(surplus, 10000.0):,.2f}."
                )
            else:
                alt_primary = "Direct surplus liquidity into high-yield liquid instruments or index funds."

            alternatives = [
                alt_primary,
                "Increase recurring investment SIP allocation to maximize long-term compound growth.",
                "Maintain current pacing while expanding emergency fund months toward target.",
            ]

            competing = [
                "Accelerating Primary Goal Milestone vs. Deploying Surplus into Compounding Investments.",
                "Maximizing Investment Yield vs. Retaining Higher Liquid Safety Margins.",
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
