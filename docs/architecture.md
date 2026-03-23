# Architecture (MVP)

## Overview
The platform converts unstructured finance/news text into structured sentiment, fuses it with technical indicators, and evaluates a simple strategy.

## Dataflow
1. User submits text snippets and ticker.
2. LLM service returns validated structured sentiment JSON.
3. Market data service loads prices.
4. Indicator service computes RSI/MA/MACD/volatility features.
5. Signal engine computes composite score + action.
6. Backtest engine computes strategy and benchmark metrics.
7. FastAPI returns JSON; Streamlit renders outputs.

## Reliability principles
- Contract-first Pydantic schemas
- Prompt/business logic separation
- Retry and fallback behavior for LLM output invalidity
- Deterministic mock mode for local/demo reliability
