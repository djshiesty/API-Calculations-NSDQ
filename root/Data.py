import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from time import time

# Calculate dates based on today's date

_cache = {}
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

def get_cached_data(ticker):
    '''
    Caching data is important in this context because fetching historical price data from an external source 
    like Yahoo Finance is time-consuming and involves rate limits in calling. 
    By caching the data, we can avoid unnecessary API calls and improve the performance of our application. 
   
    The cache is set to expire after a certain time of 60 days, ensuring that we get reasonably up-to-date data
    without overwhelming the data source with requests.
    '''
   
    if ticker not in _cache or time() - _cache[ticker]["timestamp"] > CACHE_TTL:
        _cache[ticker] = {"data": get_price_data(ticker), "timestamp": time()}
    return _cache[ticker]["data"]