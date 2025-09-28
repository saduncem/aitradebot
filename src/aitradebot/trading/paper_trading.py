"""Paper trading simulation module.

This module provides a simple function to simulate trade execution.
Trades are recorded in the database without executing on a real
exchange. It is intended for backtesting and paper trading.
"""

from __future__ import annotations

from ..data.models import TradeFill
from ..data.database import SessionLocal


def execute(signal) -> TradeFill:
    """Simulate trade execution and record the result to the database.

    Parameters
    ----------
    signal : TradeSignal
        A trading signal containing the symbol, side, price, and quantity.

    Returns
    -------
    TradeFill
        The recorded trade fill object.
    """
    with SessionLocal() as db:
        fill = TradeFill(
            symbol=signal.symbol,
            side=signal.side,
            price=signal.price,
            qty=signal.qty,
            fee=0.0,
        )
        db.add(fill)
        db.commit()
        return fill
