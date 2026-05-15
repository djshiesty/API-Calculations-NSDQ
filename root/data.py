import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from time import time
from fastapi import FastAPI, HTTPException

# Calculate dates based on today's date

_cache = {"data": None, "timestamp": 0}
CACHE_TTL = 60

def get_price_data(ticker = '^IXIC', daysbf = 59):
    """
    Fetch historical price data for a given ticker and date range.
    
    Parameters:
    ticker (str): Stock ticker symbol (e.g., 'AAPL')
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    
    Returns:
    pd.DataFrame: DataFrame containing historical price data
    """
    today = datetime.now()
    start_date = today - timedelta(days = daysbf)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = today.strftime('%Y-%m-%d')
    
    data = yf.download(ticker, start = start_str, end = end_str, auto_adjust=True)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data

def get_cached_data():
    '''
    Caching data is important in this context because fetching historical price data from an external source 
    like Yahoo Finance is time-consuming and involves rate limits in calling. 
    By caching the data, we can avoid unnecessary API calls and improve the performance of our application. 
   
    The cache is set to expire after a certain time of 60 days, ensuring that we get reasonably up-to-date data
    without overwhelming the data source with requests.
    '''
   
    if _cache["data"] is None or time() - _cache["timestamp"] > CACHE_TTL:
        _cache["data"] = get_price_data()
        _cache["timestamp"] = time()
    return _cache["data"]

def annual_volatility(data):
    
    '''
    Calculate the annualized volatility of a stock based on its historical price data.
    Basically a measure of how much the stock price fluctuates over a year using the 
    standard deviation of daily returns.
    '''
    
    returns = np.log(data["Close"]).diff().dropna()
    volatility = returns.std() * np.sqrt(252)
    return float(volatility)

app = FastAPI()

def maxdrawdown(data):
   
   #Calculate the maximum drawdown of a stock based on its historical price data.
    
    cumulative_returns = (1 + data["Close"].pct_change()).cumprod()
    rolling_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    return float(max_drawdown)

# Define the API endpoint to fetch the latest price, volatility, and max drawdown

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

