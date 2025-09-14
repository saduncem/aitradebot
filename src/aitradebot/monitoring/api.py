"""FastAPI app serving dashboard."""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


def load_dashboard() -> str:
    with open(__file__.replace("api.py", "dashboard.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.get("/")
async def root():
    return HTMLResponse(load_dashboard())
