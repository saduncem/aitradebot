"""Rule-based trading decisions and indicator-driven strategies.

This module defines simple rule-based trading logic as well as a more
advanced EMA/RSI-based strategy. The EMA/RSI strategy calculates
exponential moving averages and relative strength index (RSI) on a
provided price history to determine buy or sell signals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TradeSignal:
    """Represents a trading signal produced by a strategy.

    Attributes
    ----------
    symbol: str
        The trading pair symbol (e.g. 'BTCUSDT').
    side: str
        Either 'BUY' or 'SELL'.
    price: float
        The price at which to execute the trade.
    qty: float
        The quantity to buy or sell.
    """

    symbol: str
    side: str  # BUY or SELL
    price: float
    qty: float


def simple_strategy(price: float, last_buy: Optional[float], tp_pct: float, sl_pct: float) -> Optional[TradeSignal]:
    """Return a TradeSignal based on take profit (TP) / stop loss (SL).

    This strategy simply enters a long position if no position is held,
    and exits when either the TP or SL thresholds are hit. It does not
    incorporate any technical indicators.

    Parameters
    ----------
    price : float
        Current price.
    last_buy : float | None
        Price at which the last buy was executed. If ``None``, no
        position is currently open.
    tp_pct : float
        Take profit percentage (e.g., 0.01 for 1%).
    sl_pct : float
        Stop loss percentage (e.g., 0.01 for 1%).

    Returns
    -------
    Optional[TradeSignal]
        A ``TradeSignal`` if a buy/sell condition is met, otherwise
        ``None``.
    """
    if last_buy is None:
        # No open position, initiate a buy
        return TradeSignal(symbol="BTCUSDT", side="BUY", price=price, qty=0.001)
    change = (price - last_buy) / last_buy
    # Take-profit condition
    if change >= tp_pct:
        return TradeSignal(symbol="BTCUSDT", side="SELL", price=price, qty=0.001)
    # Stop-loss condition
    if change <= -sl_pct:
        return TradeSignal(symbol="BTCUSDT", side="SELL", price=price, qty=0.001)
    return None


def calculate_ema(prices: List[float], period: int) -> Optional[float]:
    """Calculate the Exponential Moving Average (EMA) for a given period.

    Parameters
    ----------
    prices : list[float]
        Sequence of closing prices.
    period : int
        Lookback period for the EMA.

    Returns
    -------
    float | None
        The EMA value if enough data is available, otherwise ``None``.
    """
    if len(prices) < period:
        return None
    # Start with simple moving average for the first EMA value
    sma = sum(prices[-period:]) / period
    multiplier = 2 / (period + 1)
    ema_value = sma
    # Iterate through the subset to update EMA
    for price in prices[-period + 1:]:
        ema_value = (price - ema_value) * multiplier + ema_value
    return ema_value


def calculate_rsi(prices: List[float], period: int = 14) -> Optional[float]:
    """Calculate the Relative Strength Index (RSI).

    The RSI is calculated using the average gains and losses over the
    specified period. A higher RSI indicates overbought conditions,
    whereas a lower RSI suggests oversold conditions.

    Parameters
    ----------
    prices : list[float]
        Sequence of closing prices.
    period : int
        Lookback period for RSI calculation.

    Returns
    -------
    float | None
        The RSI value if enough data is available, otherwise ``None``.
    """
    if len(prices) <= period:
        return None
    gains = 0.0
    losses = 0.0
    # Compute gains and losses for the lookback period
    for i in range(len(prices) - period, len(prices) - 1):
        delta = prices[i + 1] - prices[i]
        if delta > 0:
            gains += delta
        else:
            losses += -delta
    avg_gain = gains / period
    avg_loss = losses / period
    if avg_loss == 0:
        # Prevent division by zero: if no losses, RSI is 100
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def ema_rsi_strategy(
    prices: List[float],
    last_buy: Optional[float],
    short_period: int = 12,
    long_period: int = 26,
    rsi_period: int = 14,
    rsi_overbought: float = 70.0,
    rsi_oversold: float = 30.0,
) -> Optional[TradeSignal]:
    """Generate trading signals based on EMA crossovers and RSI levels.

    This strategy waits until enough price history is available to
    compute both short and long EMAs and the RSI. It then generates
    signals as follows:

    * **Buy** when not already in a position (``last_buy is None``), the
      short EMA crosses above the long EMA, and RSI indicates an
      oversold condition (below ``rsi_oversold``).
    * **Sell** when in a position, and either the short EMA crosses
      below the long EMA or RSI exceeds the overbought threshold
      (above ``rsi_overbought``).

    Parameters
    ----------
    prices : list[float]
        Sequence of closing prices.
    last_buy : float | None
        Price of the most recent buy trade. ``None`` indicates no open
        position.
    short_period : int
        Lookback period for the short EMA (default: 12).
    long_period : int
        Lookback period for the long EMA (default: 26).
    rsi_period : int
        Lookback period for RSI (default: 14).
    rsi_overbought : float
        RSI threshold above which conditions are considered overbought
        (default: 70.0).
    rsi_oversold : float
        RSI threshold below which conditions are considered oversold
        (default: 30.0).

    Returns
    -------
    Optional[TradeSignal]
        A ``TradeSignal`` if a buy or sell condition is met, otherwise
        ``None``. Signals always target a fixed quantity of 0.001 BTC.
    """
    short_ema = calculate_ema(prices, short_period)
    long_ema = calculate_ema(prices, long_period)
    rsi_val = calculate_rsi(prices, rsi_period)
    # Ensure all indicators are available
    if short_ema is None or long_ema is None or rsi_val is None:
        return None
    current_price = prices[-1]
    # Entry condition: bullish crossover and oversold RSI
    if last_buy is None:
        if short_ema > long_ema and rsi_val < rsi_oversold:
            return TradeSignal(symbol="BTCUSDT", side="BUY", price=current_price, qty=0.001)
    else:
        # Exit condition: bearish crossover or overbought RSI
        if short_ema < long_ema or rsi_val > rsi_overbought:
            return TradeSignal(symbol="BTCUSDT", side="SELL", price=current_price, qty=0.001)
    return None
