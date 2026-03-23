# llm-quant-research-platform

Hiring-ready MVP repository for demonstrating:
- LLM integration for financial text understanding
- Quant research workflow (signal + backtest)
- Backend/API engineering with FastAPI
- Cloud/platform readiness (Docker, Azure deployment docs)
- CI/CD awareness (GitHub Actions)

> **Status:** Phase 1 core APIs are implemented end-to-end (`/analyze`, `/signal`, `/backtest`).
> 
> **Disclaimer:** Research/education only. Not a trading bot and not financial advice.

## 1) Repository inspection (current state)
This repository is being reset to a clean production-style MVP scaffold. Previous implementation code has been replaced with high-quality skeleton modules + TODO markers to guide phased delivery.

## 2) Proposed production-style structure

```text
app/
  api/
    routes.py              # API handlers for health/analyze/signal/backtest
  core/
    config.py              # settings + env var schema
    logging.py             # logging bootstrap
    prompts.py             # LLM prompt templates
  models/
    schemas.py             # pydantic request/response contracts
  services/
    llm_analysis.py        # LLM adapter + validation/retry/fallback
    market_data.py         # market data retrieval abstraction
    indicators.py          # technical features
    signal_engine.py       # score fusion + decision rules
    backtest.py            # simple backtesting engine
  main.py                  # FastAPI app bootstrap

dashboard/
  app.py                   # Streamlit MVP UI

tests/
  test_*.py                # key unit tests for services and API contracts

docs/
  architecture.md          # concise system view
  deployment_azure.md      # Azure startup/env guidance
  execution_plan.md        # ordered MVP build plan

.github/workflows/
  ci.yml                   # lint/test workflow

Dockerfile
requirements.txt
pytest.ini
```

## 3) Phase 1 MVP features (exact scope)
1. ✅ `GET /health`
2. ✅ `POST /analyze` for structured sentiment JSON
3. ✅ `POST /signal` combining sentiment + technical score
4. ✅ `POST /backtest` with simple threshold strategy vs buy-and-hold
5. ✅ LLM reliability primitives in analyze path: prompt template, strict schema validation, retry, fallback
6. ⏳ Streamlit page: ticker + text input, sentiment output, signal output, backtest chart/metrics
7. ✅ Docker image and CI workflow that runs tests
8. ✅ Azure deployment runbook with env vars + startup command
9. ✅ Research/backtesting context only (not trading advice)

## 4) What should be real vs mocked
**Real in MVP:**
- API contracts and endpoint flow
- Quant feature engineering and backtest math
- Error handling and configuration surfaces
- CI + Docker + deployment docs

**Mocked/controlled for speed:**
- Default LLM provider (deterministic mock mode)
- Optional external LLM call behind an interface
- Optional synthetic market data fallback when provider fails

## 5) Minimal viable stack
- Python 3.12
- FastAPI + Uvicorn
- Pydantic + pydantic-settings
- Pandas + NumPy
- yfinance (with fallback path)
- Streamlit + matplotlib
- pytest

## 6) Execution plan
See `docs/execution_plan.md` for ordered tasks.

## 7) Quick start (after implementation phase)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Dashboard:
```bash
streamlit run dashboard/app.py
```
