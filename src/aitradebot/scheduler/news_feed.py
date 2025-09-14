"""Simple news fetcher stub."""
import requests


def fetch_headlines(url: str) -> list[str]:
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except Exception:
        return []
    return resp.text.splitlines()
