import json
import logging
import os
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
    Native llama.cpp HTTP server provider for local Qwen 3.8 27B GGUF execution.
    Communicates natively with the completion endpoint using Qwen ChatML tokens.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        timeout_seconds: float = 30.0,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ):
        self.endpoint = endpoint or os.getenv("LLAMA_CPP_ENDPOINT", "http://localhost:8080/completion")
        self.timeout_seconds = timeout_seconds
        self.max_tokens = max_tokens if max_tokens is not None else int(os.getenv("LLM_MAX_TOKENS", "1024"))
        self.temperature = temperature if temperature is not None else float(os.getenv("LLM_TEMPERATURE", "0.1"))
        self._client: Optional[httpx.Client] = None

    def _get_client(self) -> httpx.Client:
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                timeout=httpx.Timeout(self.timeout_seconds, connect=5.0),
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
            )
        return self._client

    @staticmethod
    def format_chatml_prompt(prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Formats prompt with standard Qwen ChatML tokens.
        """
        system = system_prompt or "You are an expert financial advisor."
        return (
            f"<|im_start|>system\n{system}<|im_end|>\n"
            f"<|im_start|>user\n{prompt}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        full_prompt = self.format_chatml_prompt(prompt=prompt, system_prompt=system_prompt)
        payload = {
            "prompt": full_prompt,
            "temperature": self.temperature,
            "n_predict": self.max_tokens,
            "stop": ["<|im_end|>", "<|endoftext|>"],
        }

        try:
            client = self._get_client()
            response = client.post(self.endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("content", "").strip()
        except httpx.HTTPError as e:
            logger.error(f"LlamaCpp HTTP inference error: {e}. Triggering fallback.")
            raise e
        except Exception as e:
            logger.error(f"LlamaCpp unexpected inference error: {e}. Triggering fallback.")
            raise e

    def close(self) -> None:
        if self._client is not None and not self._client.is_closed:
            self._client.close()



class MockLLMProvider(LLMProvider):
    """
    Deterministic mock provider for offline testing, CI/CD, and instant unit verification.
    Supports simulated failure modes for verifying self-correction and fallback.
    """

    def __init__(
        self,
        canned_response_dict: Optional[Dict[str, Any]] = None,
        should_fail: bool = False,
        fail_malformed_json_once: bool = False,
    ):
        self.canned_response_dict = canned_response_dict
        self.should_fail = should_fail
        self.fail_malformed_json_once = fail_malformed_json_once
        self._calls_count = 0

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        self._calls_count += 1

        if self.should_fail:
            raise RuntimeError("Simulated LLM server connection failure.")

        if self.fail_malformed_json_once and self._calls_count == 1:
            return "MALFORMED_JSON_NOT_VALID_SYNTAX {incomplete: true"

        if self.canned_response_dict:
            return json.dumps(self.canned_response_dict)

        default_payload = {
            "response_id": "resp_mock_001",
            "user_id": "user_demo_01",
            "recommendation": {
                "recommendation_id": "rec_mock_001",
                "title": "Preserve Near-Term Liquidity",
                "priority": "high",
                "description": "An unexpected expense of INR 12,000 has reduced your projected month-end balance to INR 19,400, falling INR 5,600 below your preferred cash buffer of INR 25,000.",
                "impact_amount": 5600.0,
                "category": "liquidity",
            },
            "reason": "An unexpected medical transaction of INR 12,000 combined with upcoming obligations will compress liquid reserves below your INR 25,000 safety threshold.",
            "evidence": [
                {
                    "metric": "current_balance",
                    "value": 30000.0,
                    "threshold": 42000.0,
                    "status": "confirmed",
                    "description": "Liquid bank balance after recent debit",
                },
                {
                    "metric": "projected_balance",
                    "value": 19400.0,
                    "threshold": 25000.0,
                    "status": "estimated",
                    "description": "Deterministic 30-day forecast considering fixed costs and bills",
                },
                {
                    "metric": "minimum_cash_buffer",
                    "value": 25000.0,
                    "threshold": None,
                    "status": "confirmed",
                    "description": "User preference target safety buffer",
                },
            ],
            "confidence": 0.94,
            "alternatives": [
                "Temporarily pause the vacation goal contribution for this billing cycle.",
                "Reduce remaining discretionary dining and shopping allocations by INR 4,000.",
            ],
            "competing_objectives_considered": [
                "Liquidity preservation vs Vacation Goal contribution pacing.",
                "Retaining long-term investments rather than liquidating equity for temporary shortfall.",
            ],
        }
        return json.dumps(default_payload)


def get_llm_provider(provider_type: Optional[str] = None) -> LLMProvider:
    """
    Factory resolving the LLMProvider from environment or explicit argument.
    Production runtime defaults to 'llamacpp' unless explicitly configured.
    Raises ValueError on missing/invalid provider to prevent silent mock usage.
    """
    provider_name = (provider_type or os.getenv("LLM_PROVIDER", "llamacpp")).strip().lower()

    if provider_name == "llamacpp":
        endpoint = os.getenv("LLAMA_CPP_ENDPOINT", "http://localhost:8080/completion")
        return LlamaCppProvider(endpoint=endpoint)
    elif provider_name == "mock":
        return MockLLMProvider()
    else:
        raise ValueError(
            f"Invalid or unsupported LLM_PROVIDER '{provider_name}'. "
            f"Supported options are: 'llamacpp', 'mock'."
        )

