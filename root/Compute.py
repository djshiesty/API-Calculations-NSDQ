import numpy as np
import yfinance as yf
import pandas as pd

def annual_volatility(data):
    
    '''
    Calculate the annualized volatility of a stock based on its historical price data.
    Basically a measure of how much the stock price fluctuates over a year using the 
    standard deviation of daily returns.
    '''
    
    returns = np.log(data["Close"]).diff().dropna()
    volatility = returns.std() * np.sqrt(252)
    return float(volatility)

def maxdrawdown(data):
    cumulative_returns = (1 + data["Close"].pct_change()).cumprod()
    rolling_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    return float(max_drawdown)

def implied_vs_realized(realized_vol):
    vxn = yf.download('^VXN', period = '5d', auto_adjust = True)
    if isinstance(vxn.columns, pd.MultiIndex):
        vxn.columns = vxn.columns.get_level_values(0)
    implied_vol = float(vxn["Close"].iloc[-1]/100)
    spread = implied_vol - realized_vol

    if spread > 0.02:
        interpretation = "Feared options pricing"
    elif spread < -0.02:
        interpretation = "Complacent options pricing"
    else:
        interpretation = "Aligned options pricing"
        
    return {
        "implied_vol": round(implied_vol, 4),
        "realized_vol": round(realized_vol, 4),
        "spread": round(spread, 4),
        "interpretation": interpretation
    }