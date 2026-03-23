"""LLM sentiment analysis service.

Design intent:
- separate prompt generation from orchestration,
- guarantee schema validation,
- provide retry and fallback behavior.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from app.core.config import Settings
from app.core.prompts import build_analysis_prompt
from app.models.schemas import SentimentResult


@dataclass
class LLMAnalysisService:
    """Facade for text-to-structured-sentiment conversion."""

    settings: Settings

    def analyze_texts(self, texts: list[str]) -> SentimentResult:
        """Analyze snippets and return validated structured sentiment.

        Behavior:
        1) Build prompt
        2) Invoke provider (mock by default)
        3) Parse JSON + validate with Pydantic
        4) Retry on malformed payload
        5) Return fallback sentiment on exhaustion
        """

        prompt = build_analysis_prompt(texts)

        for _ in range(self.settings.llm_max_retries + 1):
            raw = self._invoke_model(prompt)
            parsed = self._parse_and_validate(raw)
            if parsed is not None:
                return parsed

        return self._fallback_result(len(texts))

    def _invoke_model(self, prompt: str) -> str:
        """Invoke the configured provider.

        MVP phase-1 keeps deterministic mock mode as the default behavior.
        """

        if self.settings.llm_provider == "mock":
            return self._mock_response(prompt)
        # Keep behavior deterministic for unsupported providers in phase-1.
        return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        """Return deterministic JSON sentiment output based on simple keyword rules."""

        text = prompt.lower()
        bullish_hits = sum(word in text for word in ["beat", "growth", "upgrade", "surge", "raise guidance"])
        bearish_hits = sum(word in text for word in ["miss", "downgrade", "lawsuit", "decline", "recession"])

        if bullish_hits > bearish_hits:
            sentiment = "bullish"
            confidence = min(0.55 + bullish_hits * 0.1, 0.95)
            topic = "positive catalyst"
            rationale = "Positive terms outweighed negative terms in provided snippets."
        elif bearish_hits > bullish_hits:
            sentiment = "bearish"
            confidence = min(0.55 + bearish_hits * 0.1, 0.95)
            topic = "risk pressure"
            rationale = "Negative terms outweighed positive terms in provided snippets."
        else:
            sentiment = "neutral"
            confidence = 0.5
            topic = "mixed outlook"
            rationale = "Positive and negative terms were balanced or absent."

        return json.dumps(
            {
                "sentiment": sentiment,
                "confidence": round(confidence, 2),
                "topic": topic,
                "rationale": rationale,
            }
        )

    def _parse_and_validate(self, raw_output: str) -> SentimentResult | None:
        """Parse JSON output and validate against `SentimentResult` schema."""

        try:
            parsed = json.loads(raw_output)
            return SentimentResult.model_validate(parsed)
        except Exception:  # noqa: BLE001
            return None

    def _fallback_result(self, snippet_count: int) -> SentimentResult:
        """Return safe fallback if all retries fail."""

        return SentimentResult(
            sentiment="neutral",
            confidence=0.4,
            topic="fallback",
            rationale=f"Fallback triggered after malformed model outputs for {snippet_count} snippet(s).",
        )
