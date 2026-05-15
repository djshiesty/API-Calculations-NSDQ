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
def index(ticker: str = "^IXIC"):
    data = get_cached_data(ticker)
    try:
        data = get_cached_data()
        return {
            "ticker": '^IXIC',
            "latest_price": round(float(data["Close"].iloc[-1]), 2),
            "volatility_30d": round(annual_volatility(data), 2),
            "max_drawdown_pct": round(maxdrawdown(data) * 100, 2),
            "as_of": data.index[-1].strftime('%Y-%m-%d')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data fetch failed: {str(e)}")
