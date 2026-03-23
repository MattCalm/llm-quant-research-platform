"""Market data access abstractions for historical prices."""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


class MarketDataService:
    """Load market data for a ticker.

    Phase-1 default source is `yfinance` because it is practical for local research.
    If provider access fails, synthetic data is generated to keep the pipeline runnable.
    """

    def __init__(self, period: str = "2y") -> None:
        self.period = period

    def get_price_history(self, ticker: str) -> pd.DataFrame:
        """Return historical close prices as DataFrame with a `close` column."""

        try:
            df = yf.download(ticker, period=self.period, progress=False, auto_adjust=True)
            if df.empty:
                raise ValueError(f"No data returned for ticker={ticker}")

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            return df[["Close"]].rename(columns={"Close": "close"}).dropna()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Market data provider failed for %s: %s. Using synthetic fallback.", ticker, exc)
            return self._synthetic_price_history()

    def _synthetic_price_history(self, periods: int = 260) -> pd.DataFrame:
        """Generate deterministic synthetic prices as local fallback."""

        rng = np.random.default_rng(seed=42)
        returns = rng.normal(loc=0.0002, scale=0.012, size=periods)
        close = 100 * (1 + pd.Series(returns)).cumprod()
        idx = pd.date_range(end=pd.Timestamp.utcnow().normalize(), periods=periods, freq="B")
        return pd.DataFrame({"close": close.values}, index=idx)
