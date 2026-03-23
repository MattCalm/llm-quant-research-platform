"""Technical indicator utilities for quant research MVP."""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_indicators(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute RSI, SMA crossover, MACD, and volatility features."""

    df = prices.copy()
    if "close" not in df.columns:
        raise ValueError("Input price DataFrame must include a 'close' column")

    df["returns"] = df["close"].pct_change().fillna(0)

    delta = df["close"].diff()
    gains = delta.clip(lower=0).rolling(14).mean()
    losses = -delta.clip(upper=0).rolling(14).mean()
    rs = gains / losses.replace(0, np.nan)
    df["rsi"] = 100 - (100 / (1 + rs))

    df["sma_fast"] = df["close"].rolling(20).mean()
    df["sma_slow"] = df["close"].rolling(50).mean()
    df["sma_crossover"] = df["sma_fast"] - df["sma_slow"]

    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    df["volatility_20d"] = df["returns"].rolling(20).std() * np.sqrt(252)
    return df


def technical_score(df: pd.DataFrame) -> float:
    """Convert latest indicators into a normalized technical score in [-1, 1]."""

    clean = df.dropna()
    if clean.empty:
        return 0.0

    row = clean.iloc[-1]

    rsi_component = (50 - row["rsi"]) / 50
    sma_component = np.sign(row["sma_crossover"])
    macd_component = np.sign(row["macd_hist"])
    vol_component = -min(max(row["volatility_20d"], 0.0), 1.0)

    score = 0.35 * rsi_component + 0.30 * sma_component + 0.25 * macd_component + 0.10 * vol_component
    return float(np.clip(score, -1.0, 1.0))
