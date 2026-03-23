"""Streamlit dashboard for the LLM Quant Research Platform.

Simple demo UI that calls backend APIs:
- POST /analyze
- POST /signal
- POST /backtest
"""

from __future__ import annotations

import os
from typing import Any

import matplotlib.pyplot as plt
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def _post_json(path: str, payload: dict[str, Any], timeout: int = 60) -> dict[str, Any]:
    """POST JSON to backend and return parsed response.

    Raises `RuntimeError` with API detail for non-2xx responses.
    """

    response = requests.post(f"{API_BASE_URL}{path}", json=payload, timeout=timeout)
    if response.status_code >= 400:
        raise RuntimeError(f"{path} failed ({response.status_code}): {response.text}")
    return response.json()


st.set_page_config(page_title="LLM Quant Research Platform", layout="wide")
st.title("LLM Quant Research Platform")
st.caption("Research and backtesting tool only. Not trading advice.")

with st.sidebar:
    st.header("Inputs")
    ticker = st.text_input("Ticker", value="SPY", max_chars=10).upper().strip()
    threshold = st.slider("Backtest threshold", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

raw_text = st.text_area(
    "Financial/news text snippets (one per line)",
    value=(
        "Company beats earnings estimates and raises guidance\n"
        "Macro uncertainty remains elevated despite strong demand"
    ),
    height=180,
)

snippets = [line.strip() for line in raw_text.splitlines() if line.strip()]

if st.button("Run analysis", type="primary"):
    if not ticker:
        st.error("Please enter a ticker.")
        st.stop()
    if not snippets:
        st.error("Please enter at least one text snippet.")
        st.stop()

    analyze_payload = {"texts": snippets}
    signal_payload = {"ticker": ticker, "texts": snippets}
    backtest_payload = {"ticker": ticker, "texts": snippets, "threshold": threshold}

    with st.spinner("Calling backend services..."):
        try:
            sentiment = _post_json("/analyze", analyze_payload, timeout=45)
            signal = _post_json("/signal", signal_payload, timeout=60)
            backtest = _post_json("/backtest", backtest_payload, timeout=90)
        except Exception as exc:  # noqa: BLE001
            st.error(f"Request failed: {exc}")
            st.stop()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment")
        st.metric("Label", sentiment["sentiment"])
        st.metric("Confidence", f"{sentiment['confidence']:.2f}")
        st.write(f"**Topic:** {sentiment['topic']}")
        st.write(f"**Rationale:** {sentiment['rationale']}")

    with col2:
        st.subheader("Signal")
        st.metric("Action", signal["signal"].upper())
        st.metric("Composite score", f"{signal['composite_score']:.3f}")
        st.write(f"Technical score: `{signal['technical_score']:.3f}`")
        st.write(f"Sentiment score: `{signal['sentiment_score']:.3f}`")
        st.write(f"Threshold: `{signal['threshold']:.2f}`")

    st.divider()
    st.subheader("Backtest")

    metrics = backtest["metrics"]
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Cumulative return", f"{metrics['cumulative_return']:.2%}")
    m2.metric("Buy & hold return", f"{metrics['buy_and_hold_return']:.2%}")
    m3.metric("Max drawdown", f"{metrics['max_drawdown']:.2%}")
    m4.metric("Sharpe-like", f"{metrics['sharpe_like']:.2f}")
    m5.metric("Hit ratio", f"{metrics['hit_ratio']:.2%}")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(backtest["equity_curve"], label="Strategy", linewidth=2)
    ax.plot(backtest["benchmark_curve"], label="Buy & Hold", linewidth=2, alpha=0.8)
    ax.set_title(f"{ticker} Backtest Equity Curve")
    ax.set_xlabel("Time step")
    ax.set_ylabel("Equity")
    ax.grid(alpha=0.25)
    ax.legend()
    st.pyplot(fig, clear_figure=True)
else:
    st.info("Enter a ticker and snippets, then click **Run analysis**.")
