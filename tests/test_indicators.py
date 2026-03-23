"""Focused tests for indicator computation and technical scoring."""

import pytest

pd = pytest.importorskip("pandas")

from app.services.indicators import compute_indicators, technical_score


def test_compute_indicators_adds_expected_columns() -> None:
    prices = pd.DataFrame({"close": [100 + i for i in range(120)]})
    out = compute_indicators(prices)

    required_cols = {
        "returns",
        "rsi",
        "sma_fast",
        "sma_slow",
        "sma_crossover",
        "macd",
        "macd_signal",
        "macd_hist",
        "volatility_20d",
    }
    assert required_cols.issubset(set(out.columns))


def test_technical_score_is_bounded() -> None:
    prices = pd.DataFrame({"close": [100 + i for i in range(180)]})
    scored_df = compute_indicators(prices)
    score = technical_score(scored_df)

    assert -1.0 <= score <= 1.0
