import numpy as np

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