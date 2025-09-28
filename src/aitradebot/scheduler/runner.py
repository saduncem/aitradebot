"""Stream runner to tie together data feed, decision engine and trading.

This asynchronous runner listens to the Binance WebSocket feed, keeps a
rolling history of closing prices, and invokes the EMA/RSI-based
strategy to generate trading signals. When a signal is generated, the
runner executes the trade via the paper trading module and updates
internal state accordingly.
"""

from __future__ import annotations

import asyncio
from typing import List, Optional

from ..data.ws_feed import BinanceWS
from ..decision.rule_engine import ema_rsi_strategy
from ..trading.paper_trading import execute


async def main(symbol: str = "BTCUSDT") -> None:
    """Main event loop for processing streaming data and executing trades.

    Parameters
    ----------
    symbol : str, optional
        Trading pair symbol to subscribe to (default is ``"BTCUSDT"``).

    Notes
    -----
    This function maintains an internal list of closing prices used by
    the EMA/RSI strategy. It tracks whether a position is open via
    ``last_buy``. When the strategy emits a BUY signal, ``last_buy`` is
    updated with the purchase price. When a SELL signal is emitted,
    ``last_buy`` is reset to ``None``.
    """
    ws = BinanceWS(symbol)
    last_buy: Optional[float] = None
    prices: List[float] = []
    async for candle in ws.listen():
        price = candle["close"]
        prices.append(price)
        # Obtain a trading signal based on EMA/RSI
        signal = ema_rsi_strategy(prices, last_buy)
        if signal:
            # Execute trade using paper trading engine
            execute(signal)
            if signal.side == "BUY":
                last_buy = signal.price
            else:
                # Position closed on SELL
                last_buy = None


if __name__ == "__main__":
    asyncio.run(main())
