# API-Calculations-NSDQ — Real-Time Market Analytics API

## Abstract

This application is a Python-based market analytics platform that fetches live index data from Yahoo Finance (from Nasdaq Composite/100, DJI, S&P 500, etc) and computes three risk metrics: annualized volatility, maximum drawdown, and the spread between implied and realized volatility. This is displayed through a FastAPI backend with a lightweight HTML/CSS/JS frontend. The project supports the indices mentioned above and is scalable, additionally refreshing automatically every 60 seconds. It demonstrates a complete full-stack pipeline: data ingestion, quantitative computation, API design, and a responsive web interface.

## Architecture

The codebase is split into three layers, each handling one responsibility:

**Data layer (`Data.py`)** manages all external data fetching and caching. The `get_price_data` function pulls 60 days of past data from Yahoo Finance:

```python
data = yf.download(ticker, start=start_str, end=end_str, auto_adjust=True)
```

A per-ticker in-memory cache (`_cache`, TTL 60 seconds) avoids redundant API calls and protects against yfinance rate limits. 

**Compute layer (`Compute.py`)** runs the analytics math. Annualized volatility uses log returns scaled by √252 (trading days per year):

```python
returns = np.log(data["Close"]).diff().dropna()
volatility = returns.std() * np.sqrt(252)
```

Maximum drawdown tracks deep declines in cumulative returns. The implied-vs-realized function compares computed volatility against the VXN index (the Nasdaq-100 volatility benchmark) and categorizes the spread as "feared," "complacent," or "aligned" options pricing, critical to assessing valuations.

**API layer (`Execute.py`)** exposes the analytics through FastAPI. The main endpoint accepts a ticker query parameter and returns a structured JSON response validated by Pydantic models:

```python
@app.get("/index", response_model=IndexResponse)
def index(ticker: str = "^IXIC"):
    data = get_cached_data(ticker)
    realized_vol = annual_volatility(data)
    return { ... }
```

A `FileResponse` at the root serves the frontend; static assets are mounted at `/static`.

## Methodology

Volatility is the annualized standard deviation of daily log returns. Maximum drawdown is the largest peak-to-trough decline throughout the 60-day window. The implied-vs-realized spread uses VXN/100 as the implied volatility proxy; positive spreads suggest the options market is pricing fear ahead of realized moves, while negative spreads suggest complacency.

## Running

```
pip install fastapi uvicorn yfinance pandas numpy
uvicorn Execute:app --reload --port 8001
```

The dashboard loads at the root URL; interactive API docs are at `/docs`.

## Reflection

The hardest parts were handling yfinance's inconsistent column structures (multi-index headers required flattening) and reasoning about cache invalidation per-ticker. This was assisted through AI debugging and Youtube tutorials, helping me complete my project. Another major issue seen was where I pulled my data from, where I was originally planning on pulling data from Nasdaq data links (unsuccessful due to failures in accessibility). Given more time, I would add stochastic volatility modeling, persistent historical analytics in a large database, and deploy the service to a cloud host, which I may expand upon later based upon my will.


