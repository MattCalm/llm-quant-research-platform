"""Focused tests for LLM analyze behavior."""

import pytest

pytest.importorskip("pydantic")

from app.core.config import Settings
from app.services.llm_analysis import LLMAnalysisService


def test_mock_analyze_returns_valid_schema() -> None:
    """Mock mode should return a valid `SentimentResult` payload."""

    service = LLMAnalysisService(settings=Settings(llm_provider="mock"))
    result = service.analyze_texts(["Company beats earnings and raises guidance"])

    assert result.sentiment in {"bullish", "bearish", "neutral"}
    assert 0 <= result.confidence <= 1
    assert result.topic
    assert result.rationale


def test_analyze_retries_then_fallback_on_malformed_json() -> None:
    """Invalid model outputs should trigger fallback after retries."""

    service = LLMAnalysisService(settings=Settings(llm_provider="mock", llm_max_retries=1))

    def bad_output(_: str) -> str:
        return "not-json"

    service._invoke_model = bad_output  # type: ignore[method-assign]
    result = service.analyze_texts(["Any snippet"])

    assert result.sentiment == "neutral"
    assert result.topic == "fallback"
    assert result.confidence == 0.4
