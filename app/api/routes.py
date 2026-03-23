"""API routes for phase-1 MVP."""

from fastapi import APIRouter

from app.core.config import get_settings
from app.models.schemas import (
    AnalyzeRequest,
    BacktestRequest,
    BacktestResponse,
    HealthResponse,
    SentimentResult,
    SignalRequest,
    SignalResponse,
)
from app.services.backtest import run_backtest
from app.services.indicators import compute_indicators, technical_score
from app.services.llm_analysis import LLMAnalysisService
from app.services.market_data import MarketDataService
from app.services.signal_engine import CompositeSignalEngine, sentiment_to_score

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return service liveness status."""

    settings = get_settings()
    return HealthResponse(status="ok", app_name=settings.app_name)


@router.post("/analyze", response_model=SentimentResult)
def analyze(req: AnalyzeRequest) -> SentimentResult:
    """Analyze text and return structured sentiment."""

    settings = get_settings()
    service = LLMAnalysisService(settings=settings)
    return service.analyze_texts(req.texts)


@router.post("/signal", response_model=SignalResponse)
def signal(req: SignalRequest) -> SignalResponse:
    """Generate composite signal from sentiment and technical indicators."""

    settings = get_settings()

    llm_service = LLMAnalysisService(settings=settings)
    sentiment = llm_service.analyze_texts(req.texts)
    sentiment_score = sentiment_to_score(sentiment)

    market_data_service = MarketDataService(period=settings.data_period)
    prices = market_data_service.get_price_history(req.ticker)

    indicator_df = compute_indicators(prices)
    tech_score = technical_score(indicator_df)

    engine = CompositeSignalEngine(
        technical_weight=settings.technical_weight,
        sentiment_weight=settings.sentiment_weight,
        threshold=settings.signal_threshold,
    )
    composite = engine.composite_score(technical=tech_score, sentiment=sentiment_score)

    return SignalResponse(
        ticker=req.ticker.upper(),
        sentiment=sentiment,
        technical_score=tech_score,
        sentiment_score=sentiment_score,
        composite_score=composite,
        threshold=settings.signal_threshold,
        signal=engine.classify(composite),
    )


@router.post("/backtest", response_model=BacktestResponse)
def backtest(req: BacktestRequest) -> BacktestResponse:
    """Run research backtest for a static composite signal versus buy-and-hold."""

    settings = get_settings()

    llm_service = LLMAnalysisService(settings=settings)
    sentiment = llm_service.analyze_texts(req.texts)
    sentiment_score = sentiment_to_score(sentiment)

    market_data_service = MarketDataService(period=settings.data_period)
    prices = market_data_service.get_price_history(req.ticker)

    indicator_df = compute_indicators(prices)
    tech_score = technical_score(indicator_df)

    engine = CompositeSignalEngine(
        technical_weight=settings.technical_weight,
        sentiment_weight=settings.sentiment_weight,
        threshold=req.threshold,
    )
    composite = engine.composite_score(technical=tech_score, sentiment=sentiment_score)

    metrics, equity_curve, benchmark_curve = run_backtest(
        price_df=prices,
        composite_score=composite,
        threshold=req.threshold,
    )

    return BacktestResponse(
        ticker=req.ticker.upper(),
        metrics=metrics,
        equity_curve=equity_curve,
        benchmark_curve=benchmark_curve,
    )
