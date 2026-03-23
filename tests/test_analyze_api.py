"""Endpoint tests for POST /analyze."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_post_analyze_returns_structured_payload() -> None:
    """/analyze should return required sentiment fields and valid ranges."""

    response = client.post(
        "/analyze",
        json={"texts": ["Analysts upgrade the stock after strong growth"]},
    )

    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"sentiment", "confidence", "topic", "rationale"}
    assert payload["sentiment"] in {"bullish", "bearish", "neutral"}
    assert 0 <= payload["confidence"] <= 1


def test_post_analyze_rejects_empty_input() -> None:
    """/analyze should enforce schema-level minimum list length."""

    response = client.post("/analyze", json={"texts": []})
    assert response.status_code == 422
