"""Paper trading simulation."""
from ..data.models import TradeFill
from ..data.database import SessionLocal


def execute(signal):
    """Simulate trade execution and record to DB."""
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
