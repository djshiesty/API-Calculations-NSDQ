import pandas as pd
import numpy as np
import math
from scipy.stats import norm
'''
def newtonian_price_decay(prices, window=20, k=0.1):
    """
    Model aims to price mean reversion rate.
    T_env = Moving Average
    k = speed of mean reversion
    """
    df_calc = pd.DataFrame({'Price': prices})
    df_calc['T_env'] = df_calc['Price'].rolling(window=window).mean()
    
    # Calculate the expected thermal 'force' or price velocity next period
    df_calc['Price_Decay_Force'] = -k * (df_calc['Price'] - df_calc['T_env'])
    return df_calc['Price_Decay_Force'].fillna(0)

df['Thermal_Force'] = newtonian_price_decay(df['amount'])

def black_scholes(S, K, T, r, sigma, option_type = 'call'):
    """
    S: Current stock price ($)
    K: Strike price ($)
    T: Time to expiration (in years)
    r: Risk-free interest rate (e.g., 0.05 for 5%)
    Sigma: Volatility of the stock (annualized)

    """
'''