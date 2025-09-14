"""Live trading via Binance API (placeholder)."""


class BinanceClient:
    """Placeholder for Binance REST client."""

    def __init__(self, api_key: str = "", api_secret: str = ""):
        self.api_key = api_key
        self.api_secret = api_secret

    def market_order(self, symbol: str, side: str, qty: float):
        """Submit a market order (stub)."""
        return {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": 0.0,
            "status": "FILLED",
        }
