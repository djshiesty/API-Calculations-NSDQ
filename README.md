# API-Calculations-NSDQ — Real-Time Market Analytics API

## Abstract

This application is a Python-based market analytics platform that fetches live index data from Yahoo Finance (from Nasdaq Composite/100, DJI, S&P 500, etc) and computes three risk metrics: annualized volatility, maximum drawdown, and the spread between implied and realized volatility. This is displayed through a FastAPI backend with a lightweight HTML/CSS/JS frontend for aestheticity. The project supports the indices mentioned above and is scalable, additionally refreshing automatically every 60 seconds. It demonstrates a complete full-stack pipeline: data ingestion, quantitative computation, API design, and a responsive web interface.

## Architecture

The code is split into three layers, handling one responsibility each:

**Data layer (`Data.py`)** manages all external data, where the `get_price_data` function pulls 60 days of past data from Yahoo Finance:

```python
data = yf.download(ticker, start=start_str, end=end_str, auto_adjust=True)
```

A per-ticker in-memory cache (`_cache`, TTL 60 seconds) avoids redundancies and protects against yfinance rate limits of computational usage. 

**Compute layer (`Compute.py`)** runs the analysis and math, where annualized volatility uses log returns scaled by √252 (trading days per year):

```python
returns = np.log(data["Close"]).diff().dropna()
volatility = returns.std() * np.sqrt(252)
```

Maximum drawdown tracks deep declines in cumulative returns. The implied-vs-realized function compares computed volatility against the Nasdaq-100 volatility benchmark and categorizes the spread as "feared," "complacent," or "aligned" options pricing, critical to assessing valuations.

**API layer (`Execute.py`)** exposes the analytics through FastAPI, where the main endpoint accepts a ticker query parameter and returns a structured JSON response validated by Pydantic:

```python
@app.get("/index", response_model=IndexResponse)
def index(ticker: str = "^IXIC"):
    data = get_cached_data(ticker)
    realized_vol = annual_volatility(data)
    return { ... }
```

A `FileResponse` at the root serves the frontend; static assets are mounted at `/static`.

## Methodology

Volatility is the annualized standard deviation of daily log returns. Maximum drawdown is the largest peak-to-trough decline throughout the 60-day window. The implied-vs-realized spread uses VXN/100 as the implied volatility proxy; positive spreads suggest the options market is pricing fear ahead of realized moves, while negative spreads suggest complacency. This analyzes speculation and inconsistencies and their prevalence in market moves, pivotal to understanding valuations of indexes and securities once more.

## Running

```
pip install fastapi uvicorn yfinance pandas numpy
uvicorn Execute:app --reload --port 8001
```

The dashboard loads at the root URL; interactive API docs are at `/docs`.

## Reflection

The hardest parts were handling yfinance's inconsistency in column structures and reasoning about cache invalidation per-ticker. This was assisted through AI debugging and Youtube tutorials, helping me complete my project. Another major issue seen was where I pulled my data from, where I was originally planning on doing so from Nasdaq data links (unsuccessful due to failures in accessibility). Given more time, I would add stochastic volatility modeling, persistent historical analytics in a large database, and deploy the service to a cloud host, which I may expand upon later based upon my will.

This project was assisted with the following tutorials and guidelines

"Calculating Historical Stock Volatility with Python and Excel"
https://www.youtube.com/watch?v=lcPZcFZXDNA

"How to download market data with yfinance and Python" — PythonFinTech
https://pythonfintech.com/articles/how-to-download-market-data-yfinance-python/

Library reference:
https://github.com/ranaroussi/yfinance

"How to Calculate Stock Investment Portfolio Volatility with Python, NumPy & Pandas"
https://www.youtube.com/watch?v=GKMSG_3MVGM

"How To Compute Volatility 6 Ways Most People Don't Know"
https://www.pyquantnews.com/the-pyquant-newsletter/how-to-compute-volatility-6-ways

"Analyzing Stock Returns and Volatility with Python"
https://labs.sogeti.com/analyzing-stock-returns-and-volatility-with-python/

"Python In-Memory Caching with Time Limit"
https://www.pythontutorials.net/blog/caching-in-memory-with-a-time-limit-in-python/

"Implementing a Custom Cache in Python"
https://medium.com/@saleem.latif.ee/implementing-a-custom-cache-in-python-68c39ece8a8

"Top 5 Methods to Implement a Python In-Memory Cache with TTL"
https://sqlpey.com/python/top-5-methods-to-implement-a-python-in-memory-cache-with-time-to-live/

"FastAPI Crash Course 2025: Python Tutorial for Absolute Beginners"
https://www.youtube.com/watch?v=nWWPlEO0he8

"Python FastAPI Tutorial Part 1: Getting Started"
https://www.youtube.com/watch?v=7AMjmCTumuo

https://fastapi.tiangolo.com/tutorial/

"Vanilla JS Fetch API Request"
https://daily-dev-tips.com/posts/fetch-api-in-vanilla-javascript/

"Build a CRUD Todo App with Vanilla JavaScript and Fetch API"
https://www.agirlcodes.dev/todo-app-frontend-crud-vanilla-js-fetch-api

https://www.refactoringui.com/
