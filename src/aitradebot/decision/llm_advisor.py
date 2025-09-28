"""LLM-based advisory component for strategy suggestions.

This advisory component no longer returns random recommendations. Instead,
it derives suggestions based on recent price history (on-chain data).
The logic uses the existing EMA and RSI calculations from the decision
engine to infer market conditions and recommend adjustments to the
trading strategy.

If sufficient price data is not available, it returns a placeholder
message. The context parameter is expected to be a dictionary with a
`prices` key containing a list of recent closing prices.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .rule_engine import calculate_ema, calculate_rsi


class LLMAdvisor:
    """Advisory component that derives suggestions from on-chain data.

    The advisor analyzes recent price history (provided in the
    ``context`` argument) to produce high-level strategy recommendations.
    It uses short and long EMAs and the RSI to infer bullish or bearish
    momentum as well as overbought or oversold conditions.
    """

    def suggest(self, context: Dict[str, List[float]] | None) -> str:
        """Return a strategy suggestion derived from price data.

        Parameters
        ----------
        context : dict
            A dictionary that may contain a ``prices`` key mapping to a
            list of closing prices. If the context is ``None`` or
            insufficient data is provided, the method returns a generic
            message.

        Returns
        -------
        str
            A human-readable suggestion based on EMA crossovers and RSI
            levels.
        """
        # Validate context and extract price history
        if not context or not isinstance(context, dict):
            return "Insufficient context for recommendation."
        prices: List[float] = context.get("prices", [])
        if not prices or len(prices) < 30:
            # Require at least long_period + RSI period worth of data
            return "Not enough price history to derive a recommendation."

        # Compute short and long EMAs and RSI using existing utilities
        short_ema = calculate_ema(prices, 12)
        long_ema = calculate_ema(prices, 26)
        rsi = calculate_rsi(prices, 14)
        # Fall back if indicators cannot be computed
        if short_ema is None or long_ema is None or rsi is None:
            return "Waiting for more data to form a market view."

        # Build a recommendation based on EMA cross and RSI thresholds
        # Determine trend direction
        trend = "uptrend" if short_ema > long_ema else "downtrend"
        # Determine RSI state
        if rsi > 60:
            rsi_state = "overbought"
        elif rsi < 40:
            rsi_state = "oversold"
        else:
            rsi_state = "neutral"

        # Derive suggestion based on combined indicators
        if trend == "uptrend" and rsi_state == "oversold":
            return (
                "The market shows upward momentum and is oversold; you may consider "
                "increasing your take‑profit target or opening additional positions."
            )
        if trend == "downtrend" and rsi_state == "overbought":
            return (
                "The market is trending downward and appears overbought; tightening stop‑loss "
                "levels or closing positions may reduce drawdown risk."
            )
        if trend == "uptrend" and rsi_state == "overbought":
            return (
                "Uptrend with overbought conditions detected; consider trailing stops to lock "
                "in gains or scaling out of positions."
            )
        if trend == "downtrend" and rsi_state == "oversold":
            return (
                "Downtrend with oversold conditions; caution is advised—market could reverse "
                "but momentum remains weak."
            )
        # Neutral scenario
        return (
            "No clear signal from the on‑chain indicators; maintain current strategy and "
            "await stronger market cues."
        )

