"""Endpoint tests for POST /backtest."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_post_backtest_returns_expected_payload_shape() -> None:
    response = client.post(
        "/backtest",
        json={
            "ticker": "SPY",
            "texts": ["Company reports steady growth and stable guidance"],
            "threshold": 0.2,
        },
    )

    assert response.status_code == 200
    payload = response.json()

    assert set(payload.keys()) == {"ticker", "metrics", "equity_curve", "benchmark_curve"}
    assert set(payload["metrics"].keys()) == {
        "cumulative_return",
        "buy_and_hold_return",
        "max_drawdown",
        "sharpe_like",
        "hit_ratio",
    }
    assert len(payload["equity_curve"]) == len(payload["benchmark_curve"])
