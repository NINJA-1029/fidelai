import json
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import httpx

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """
    Abstract interface for LLM inference providers.
    The Agent depends solely on this abstraction, never directly on vendor SDKs.
    """

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate completion from LLM provider.
        """
        pass


class LlamaCppProvider(LLMProvider):
    """
    Native llama.cpp HTTP server provider for local GGUF execution.
    """

    def __init__(self, endpoint: str = "http://localhost:8080/completion", timeout_seconds: float = 30.0):
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        full_prompt = f"<|im_start|>system\n{system_prompt or 'You are an expert financial advisor.'}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        payload = {
            "prompt": full_prompt,
            "temperature": 0.1,
            "n_predict": 1024,
            "stop": ["<|im_end|>", "<|endoftext|>"]
        }

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(self.endpoint, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("content", "").strip()
        except Exception as e:
            logger.error(f"LlamaCpp inference error: {e}. Falling back to deterministic synthesizer.")
            raise e


class MockLLMProvider(LLMProvider):
    """
    Deterministic mock provider for offline testing, CI/CD, and instant unit verification.
    """

    def __init__(self, canned_response_dict: Optional[Dict[str, Any]] = None):
        self.canned_response_dict = canned_response_dict

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if self.canned_response_dict:
            return json.dumps(self.canned_response_dict)

        # Default structured mock conforming to AgentResponse schema
        default_payload = {
            "response_id": "resp_mock_001",
            "user_id": "user_demo_01",
            "recommendation": {
                "recommendation_id": "rec_mock_001",
                "title": "Preserve Near-Term Liquidity",
                "priority": "high",
                "description": "An unexpected expense of INR 12,000 has reduced your projected month-end balance to INR 19,400, falling INR 5,600 below your preferred cash buffer of INR 25,000.",
                "impact_amount": 5600.0,
                "category": "liquidity"
            },
            "reason": "An unexpected medical transaction of INR 12,000 combined with upcoming obligations will compress liquid reserves below your INR 25,000 safety threshold.",
            "evidence": [
                {
                    "metric": "current_balance",
                    "value": 30000.0,
                    "threshold": 42000.0,
                    "status": "confirmed",
                    "description": "Liquid bank balance after recent debit"
                },
                {
                    "metric": "projected_balance",
                    "value": 19400.0,
                    "threshold": 25000.0,
                    "status": "estimated",
                    "description": "Deterministic 30-day forecast considering fixed costs and bills"
                },
                {
                    "metric": "minimum_cash_buffer",
                    "value": 25000.0,
                    "threshold": None,
                    "status": "confirmed",
                    "description": "User preference target safety buffer"
                }
            ],
            "confidence": 0.94,
            "alternatives": [
                "Temporarily pause the vacation goal contribution for this billing cycle.",
                "Reduce remaining discretionary dining and shopping allocations by INR 4,000."
            ],
            "competing_objectives_considered": [
                "Liquidity preservation vs Vacation Goal contribution pacing.",
                "Retaining long-term investments rather than liquidating equity for temporary shortfall."
            ]
        }
        return json.dumps(default_payload)
