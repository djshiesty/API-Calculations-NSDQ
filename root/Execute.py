from fastapi import FastAPI, HTTPException
from Data import get_cached_data
from pydantic import BaseModel
from Compute import annual_volatility, maxdrawdown

class IndexResponse(BaseModel):
    ticker: str
    latest_price: float
    volatility_30d: float
    max_drawdown_pct: float
    as_of: str

app = FastAPI(
    title="NDXLive",
    description="Real-time analytics for the Nasdaq Composite:" 
    "Fetches live price data from Yahoo Finance and computes annualized volatility and maximum drawdown.",
)

@app.get("/")
def root():
    return {
        "app": "NDXLive",
        "description": "Real-time Nasdaq Composite analytics",
        "endpoints": ["/index", "/docs"]
    }

@app.get("/index", response_model=IndexResponse)
def index():
    try:
        data = get_cached_data()
        return {
            "ticker": '^IXIC',
            "latest_price": float(data["Close"].iloc[-1]),
            "volatility_30d": annual_volatility(data),
            "max_drawdown_pct": maxdrawdown(data) * 100,
            "as_of": data.index[-1].strftime('%Y-%m-%d')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data fetch failed: {str(e)}")