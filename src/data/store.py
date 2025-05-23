"""Simple in-memory store for API endpoints."""

from __future__ import annotations

from typing import Any, Dict, List


signals: List[Dict[str, Any]] = []
orders: List[Dict[str, Any]] = []
risk_metrics: Dict[str, Any] = {}
performance: Dict[str, Any] = {}
latency: Dict[str, Any] = {}


def record_signal(signal: Dict[str, Any]):
    signals.append(signal)


def record_order(order: Dict[str, Any]):
    orders.append(order)


def update_risk(data: Dict[str, Any]):
    risk_metrics.update(data)


def update_performance(data: Dict[str, Any]):
    performance.update(data)


def update_latency(data: Dict[str, Any]):
    latency.update(data)
