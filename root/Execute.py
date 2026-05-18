from fastapi import FastAPI, HTTPException
from Data import get_cached_data
from pydantic import BaseModel
from Compute import annual_volatility, maxdrawdown, implied_vs_realized

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="NDXLive",
    description="Real-time analytics for the Nasdaq Composite:" 
    "Fetches live price data from Yahoo Finance and computes annualized volatility and maximum drawdown.",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class volspread(BaseModel):
    implied_vol: float
    realized_vol: float
    spread: float
    interpretation: str
    

class IndexResponse(BaseModel):
    Ticker: str
    Latest_price: float
    Volatility_30_days: float
    Max_drawdown_pct: float
    Implied_and_Realized: volspread
    As_of: str

@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/index", response_model=IndexResponse)
def index(ticker: str = "^IXIC"):
    try:
        data = get_cached_data(ticker)
        realized_vol = annual_volatility(data)
        return {
            "Ticker": ticker,
            "Latest_price": round(float(data["Close"].iloc[-1]), 2),
            "Volatility_30_days": round(realized_vol, 4),
            "Max_drawdown_pct": round(maxdrawdown(data) * 100, 2),
            "Implied_and_Realized": implied_vs_realized(realized_vol),
            "As_of": data.index[-1].strftime('%Y-%m-%d')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data fetch failed: {str(e)}")
