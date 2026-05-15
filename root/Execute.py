from fastapi import FastAPI, HTTPException
from Data import get_cached_data
from Compute import annual_volatility, maxdrawdown

app = FastAPI()

@app.get("/index")
def index():
    try:
        data = get_cached_data()
        return {
            "ticker": '^IXIC',
            "latest_price": float(data["Close"].iloc[-1]),
            "30d_volatility": annual_volatility(data),
            "max_drawdown_pct": maxdrawdown(data) * 100,
            "as_of": data.index[-1].strftime('%Y-%m-%d')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data fetch failed: {str(e)}")