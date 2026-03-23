"""Pydantic API/data contracts.

Contract-first development helps keep APIs stable and testable.
"""

from typing import Literal

from pydantic import BaseModel, Field

SentimentLabel = Literal["bullish", "bearish", "neutral"]


class AnalyzeRequest(BaseModel):
    """Input payload for /analyze."""

    texts: list[str] = Field(..., min_length=1, max_length=20)


class SentimentResult(BaseModel):
    """Structured LLM sentiment output."""

    sentiment: SentimentLabel
    confidence: float = Field(..., ge=0, le=1)
    topic: str = Field(..., min_length=1, max_length=80)
    rationale: str = Field(..., min_length=1, max_length=240)


class SignalRequest(BaseModel):
    """Input payload for /signal."""

    ticker: str = Field(..., min_length=1, max_length=10)
    texts: list[str] = Field(..., min_length=1)


class SignalResponse(BaseModel):
    """Output payload for /signal."""

    ticker: str
    sentiment: SentimentResult
    technical_score: float
    sentiment_score: float
    composite_score: float
    threshold: float
    signal: Literal["long", "flat", "short"]


class BacktestRequest(BaseModel):
    """Input payload for /backtest."""

    ticker: str = Field(..., min_length=1, max_length=10)
    texts: list[str] = Field(..., min_length=1)
    threshold: float = 0.2


class BacktestMetrics(BaseModel):
    """Performance outputs for strategy evaluation."""

    cumulative_return: float
    buy_and_hold_return: float
    max_drawdown: float
    sharpe_like: float
    hit_ratio: float


class BacktestResponse(BaseModel):
    """Output payload for /backtest."""

    ticker: str
    metrics: BacktestMetrics
    equity_curve: list[float]
    benchmark_curve: list[float]


class HealthResponse(BaseModel):
    """Output payload for /health."""

    status: Literal["ok"]
    app_name: str
