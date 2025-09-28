"""WebSocket feed handling for Binance price data.

This module defines a simple asynchronous client that connects to
Binance's WebSocket stream for one-minute candlestick (kline) data.
The feed yields completed candle dictionaries containing OHLCV data.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime

import websockets


class BinanceWS:
    """Simple Binance WebSocket client for 1-minute klines."""

    def __init__(self, symbol: str):
        # Binance expects lowercase symbols in the URL
        self.symbol = symbol.lower()
        self.url = f"wss://stream.binance.com:9443/ws/{self.symbol}@kline_1m"

    async def listen(self):
        """Asynchronously listen for closed kline data and yield it.

        Yields
        ------
        dict
            A dictionary containing symbol, close_time, open, high,
            low, close, and volume for the closed candle.
        """
        async with websockets.connect(self.url) as ws:
            async for msg in ws:
                data = json.loads(msg)
                kline = data.get("k")
                # Only use closed candles (``x`` flag)
                if kline and kline.get("x"):
                    yield {
                        "symbol": self.symbol.upper(),
                        "close_time": datetime.fromtimestamp(kline["t"] / 1000),
                        "open": float(kline["o"]),
                        "high": float(kline["h"]),
                        "low": float(kline["l"]),
                        "close": float(kline["c"]),
                        "volume": float(kline["v"]),
                    }
