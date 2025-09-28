"""FastAPI application serving the trading dashboard.

This module exposes a single endpoint at the root URL that serves
an HTML dashboard. The dashboard is a simple Chart.js line chart
placeholder. To extend, you could load trading history from the
database and pass it into the template.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pathlib


app = FastAPI()


def load_dashboard() -> str:
    """Load the static HTML dashboard file from disk."""
    # Determine the path to the dashboard relative to this file
    dashboard_path = pathlib.Path(__file__).with_name("dashboard.html")
    with open(dashboard_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/")
async def root() -> HTMLResponse:
    """Return the dashboard page as an HTML response."""
    return HTMLResponse(load_dashboard())
