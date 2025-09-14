"""LLM-based advisory component."""
import random


class LLMAdvisor:
    """Placeholder for an LLM that suggests strategy tweaks."""

    def suggest(self, context: str) -> str:
        suggestions = [
            "Increase TAKE_PROFIT_PCT to 0.015",
            "Reduce STOP_LOSS_PCT to 0.01",
            "Rotate profits into ETHUSDT",
        ]
        return random.choice(suggestions)
