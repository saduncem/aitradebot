"""Decision layer for aitradebot.

This module exposes strategy functions and advisory components.
"""

from .rule_engine import TradeSignal, simple_strategy, ema_rsi_strategy  # noqa: F401
from .llm_advisor import LLMAdvisor  # noqa: F401
