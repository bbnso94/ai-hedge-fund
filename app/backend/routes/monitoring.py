from fastapi import APIRouter
from src.data import store

router = APIRouter(prefix="/monitor")


@router.get("/signals")
def get_signals():
    return {"signals": store.signals}


@router.get("/orders")
def get_orders():
    return {"orders": store.orders}


@router.get("/risk")
def get_risk():
    return {"risk": store.risk_metrics}


@router.get("/performance")
def get_performance():
    return {"performance": store.performance}


@router.get("/latency")
def get_latency():
    return {"latency": store.latency}


@router.get("/health")
def get_health():
    return {"status": "ok"}
