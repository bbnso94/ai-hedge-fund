"""Utility stubs for alternative market data.

These functions simulate calls to satellite imagery,
consumer spending, social sentiment, and web analytics
providers. Real implementations would call vendor APIs,
but these placeholders keep the project self-contained.
"""

from __future__ import annotations

from typing import Any, Dict


def get_orbital_insight_traffic(location: str) -> Dict[str, Any]:
    """Return mocked foot traffic metrics for a location."""
    return {"location": location, "traffic_index": 50}


def get_second_measure_sales(ticker: str) -> Dict[str, Any]:
    """Return mocked credit card sales growth data for a ticker."""
    return {"ticker": ticker, "sales_growth": 0.05}


def get_reddit_mentions(ticker: str) -> Dict[str, Any]:
    """Return mocked Reddit mention counts and sentiment."""
    return {"ticker": ticker, "mention_count": 0, "sentiment": 0.0}


def get_stocktwits_sentiment(ticker: str) -> Dict[str, Any]:
    """Return mocked StockTwits sentiment score."""
    return {"ticker": ticker, "sentiment_score": 0.0}


def get_similarweb_visits(domain: str) -> Dict[str, Any]:
    """Return mocked web traffic numbers for a domain."""
    return {"domain": domain, "visits": 0}
