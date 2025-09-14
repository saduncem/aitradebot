"""WebSocket feed handling."""
import asyncio
import websockets
import json
from datetime import datetime


class BinanceWS:
    """Simple Binance WebSocket client for 1m klines."""

    def __init__(self, symbol: str):
        self.symbol = symbol.lower()
        self.url = f"wss://stream.binance.com:9443/ws/{self.symbol}@kline_1m"

    async def listen(self):
        async with websockets.connect(self.url) as ws:
            async for msg in ws:
                data = json.loads(msg)
                kline = data["k"]
                if kline["x"]:  # closed candle
                    yield {
                        "symbol": self.symbol.upper(),
                        "close_time": datetime.fromtimestamp(kline["t"] / 1000),
                        "open": float(kline["o"]),
                        "high": float(kline["h"]),
                        "low": float(kline["l"]),
                        "close": float(kline["c"]),
                        "volume": float(kline["v"]),
                    }
