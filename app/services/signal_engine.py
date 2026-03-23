"""Signal fusion logic between sentiment and technical components."""

from dataclasses import dataclass

from app.models.schemas import SentimentResult


SENTIMENT_MAP: dict[str, float] = {
    "bullish": 1.0,
    "neutral": 0.0,
    "bearish": -1.0,
}


def sentiment_to_score(sentiment: SentimentResult) -> float:
    """Map sentiment labels + confidence to a numeric score in [-1, 1]."""

    base = SENTIMENT_MAP[sentiment.sentiment]
    return float(base * sentiment.confidence)


@dataclass
class CompositeSignalEngine:
    """Fuse technical and sentiment scores into one actionable signal."""

    technical_weight: float
    sentiment_weight: float
    threshold: float

    def composite_score(self, technical: float, sentiment: float) -> float:
        """Calculate weighted composite score and clip into [-1, 1]."""

        combined = self.technical_weight * technical + self.sentiment_weight * sentiment
        return float(max(-1.0, min(1.0, combined)))

    def classify(self, score: float) -> str:
        """Convert score to long/flat/short classification."""

        if score > self.threshold:
            return "long"
        if score < -self.threshold:
            return "short"
        return "flat"
