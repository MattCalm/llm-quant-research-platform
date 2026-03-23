"""Focused tests for signal scoring and classification."""

import pytest

pytest.importorskip("pydantic")

from app.models.schemas import SentimentResult
from app.services.signal_engine import CompositeSignalEngine, sentiment_to_score


def test_sentiment_to_score_mapping() -> None:
    bullish = SentimentResult(sentiment="bullish", confidence=0.7, topic="x", rationale="y")
    bearish = SentimentResult(sentiment="bearish", confidence=0.6, topic="x", rationale="y")
    neutral = SentimentResult(sentiment="neutral", confidence=0.9, topic="x", rationale="y")

    assert sentiment_to_score(bullish) == 0.7
    assert sentiment_to_score(bearish) == -0.6
    assert sentiment_to_score(neutral) == 0.0


def test_composite_signal_engine_classification() -> None:
    engine = CompositeSignalEngine(technical_weight=0.6, sentiment_weight=0.4, threshold=0.2)

    long_score = engine.composite_score(technical=0.5, sentiment=0.4)
    short_score = engine.composite_score(technical=-0.5, sentiment=-0.4)
    flat_score = engine.composite_score(technical=0.1, sentiment=0.0)

    assert engine.classify(long_score) == "long"
    assert engine.classify(short_score) == "short"
    assert engine.classify(flat_score) == "flat"
