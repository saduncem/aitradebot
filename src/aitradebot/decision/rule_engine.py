"""Rule-based trading decisions."""
from dataclasses import dataclass


@dataclass
class TradeSignal:
    symbol: str
    side: str  # BUY or SELL
    price: float
    qty: float


def simple_strategy(price: float, last_buy: float | None, tp_pct: float, sl_pct: float):
    """Return TradeSignal based on TP/SL."""
    if last_buy is None:
        return TradeSignal(symbol="BTCUSDT", side="BUY", price=price, qty=0.001)
    change = (price - last_buy) / last_buy
    if change >= tp_pct:
        return TradeSignal(symbol="BTCUSDT", side="SELL", price=price, qty=0.001)
    if change <= -sl_pct:
        return TradeSignal(symbol="BTCUSDT", side="SELL", price=price, qty=0.001)
    return None
