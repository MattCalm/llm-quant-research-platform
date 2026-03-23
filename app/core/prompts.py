"""Prompt templates for financial text analysis.

Keeping prompt construction separate from service/business logic simplifies
maintenance and prompt iteration.
"""

from textwrap import dedent

SYSTEM_PROMPT = dedent(
    """
    You are a financial sentiment extraction assistant.
    Always return strict JSON with: sentiment, confidence, topic, rationale.
    """
).strip()


def build_analysis_prompt(snippets: list[str]) -> str:
    """Create the user prompt for aggregated snippet analysis.

    TODO(phase1): add guardrails for max snippet length and token budget.
    """

    numbered = "\n".join(f"{idx + 1}. {text}" for idx, text in enumerate(snippets))
    return dedent(
        f"""
        Analyze these snippets and return one aggregate JSON output.

        Snippets:
        {numbered}

        Required schema:
        {{
          "sentiment": "bullish|bearish|neutral",
          "confidence": 0.0,
          "topic": "short label",
          "rationale": "concise explanation"
        }}
        """
    ).strip()
