"""Focused tests for backtest output shape and basic correctness."""

import pytest

pd = pytest.importorskip("pandas")

from app.services.backtest import run_backtest


def test_backtest_output_shape_matches_input_length() -> None:
    prices = pd.DataFrame({"close": [100, 101, 99, 102, 103, 101, 104]})

    metrics, strategy_curve, benchmark_curve = run_backtest(
        price_df=prices,
        composite_score=0.7,
        threshold=0.2,
    )

    assert len(strategy_curve) == len(prices)
    assert len(benchmark_curve) == len(prices)
    assert isinstance(metrics.cumulative_return, float)
    assert isinstance(metrics.buy_and_hold_return, float)


def test_flat_signal_returns_zero_strategy_return() -> None:
    prices = pd.DataFrame({"close": [100, 101, 102, 103, 104]})

    metrics, strategy_curve, _ = run_backtest(
        price_df=prices,
        composite_score=0.0,
        threshold=0.2,
    )

    assert metrics.cumulative_return == pytest.approx(0.0)
    assert strategy_curve[-1] == pytest.approx(1.0)
