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
    vxn = yf.dounload('VXN', period = '5d', auto_adjust = True)
    if isinstance(vxn.columns, pd.MultiIndex):
        vxn.columns = vxn.columns.get_level_values(0)
    implied_vol = float(vxn["Close"].iloc[-1]/100)
    spread = implied_vol - realized_vol
    return {
        "Implied volilitity:": implied_vol,
        "Realized volitility:": realized_vol,
        "Spread of Values:": spread,
        "Interpretation": "Options pricing fear" if spread > 0.02 else "Options pricing complacency" if spread < -0.02 else "Aligned"
    }