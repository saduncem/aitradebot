"""Stream runner to tie components together."""
import asyncio
from ..data.ws_feed import BinanceWS
from ..decision.rule_engine import simple_strategy
from ..trading.paper_trading import execute


async def main(symbol: str = "BTCUSDT"):
    ws = BinanceWS(symbol)
    last_buy = None
    async for candle in ws.listen():
        price = candle["close"]
        signal = simple_strategy(price, last_buy, 0.01, 0.01)
        if signal:
            execute(signal)
            if signal.side == "BUY":
                last_buy = signal.price
            else:
                last_buy = None


if __name__ == "__main__":
    asyncio.run(main())
