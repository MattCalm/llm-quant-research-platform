"""Simple backtesting engine for MVP strategy evaluation.

This module is intentionally lightweight and research-oriented.
It is not intended for live trading execution.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from app.models.schemas import BacktestMetrics


def run_backtest(
    price_df: pd.DataFrame,
    composite_score: float,
    threshold: float,
) -> tuple[BacktestMetrics, list[float], list[float]]:
    """Backtest a static long/flat/short strategy versus buy-and-hold.

    Strategy rule:
    - long if score > threshold
    - short if score < -threshold
    - flat otherwise

    Returns metrics + strategy and benchmark equity curves.
    """

    if "close" not in price_df.columns:
        raise ValueError("price_df must include a 'close' column")

    returns = price_df["close"].pct_change().fillna(0.0)

    if composite_score > threshold:
        position = 1.0
    elif composite_score < -threshold:
        position = -1.0
    else:
        position = 0.0

    strategy_returns = position * returns
    benchmark_returns = returns

    strategy_curve = (1.0 + strategy_returns).cumprod()
    benchmark_curve = (1.0 + benchmark_returns).cumprod()

    running_peak = strategy_curve.cummax()
    drawdown = strategy_curve / running_peak - 1.0

    sharpe_like = 0.0
    if strategy_returns.std() > 0:
        sharpe_like = float(np.sqrt(252) * strategy_returns.mean() / strategy_returns.std())

    active_days = (strategy_returns != 0).sum()
    hit_ratio = 0.0
    if active_days > 0:
        hit_ratio = float((strategy_returns > 0).sum() / active_days)

    metrics = BacktestMetrics(
        cumulative_return=float(strategy_curve.iloc[-1] - 1.0),
        buy_and_hold_return=float(benchmark_curve.iloc[-1] - 1.0),
        max_drawdown=float(drawdown.min()),
        sharpe_like=sharpe_like,
        hit_ratio=hit_ratio,
    )

    return metrics, strategy_curve.tolist(), benchmark_curve.tolist()
