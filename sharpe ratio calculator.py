# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import quandl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


'''this code reads in data from the nasdaq EOD prices for 29 stocks, computes the sharpe ratio for each'''
'''In future would be good to add correlation matrix and ultimately VaR for a porfolio of these stocks'''
'''Also portfolio optimisation/rebalancing, exclusion/extrapolation for missing dates'''

#https://data.nasdaq.com/tables/EOD/QUOTEMEDIA-PRICES
data = quandl.get_table("QUOTEMEDIA/PRICES", paginate=True, api_key='RMujqBvfJxDWGonQ_vkv')


stocks=np.unique(np.array(data['ticker']))

stock_closes = {}
sharpe_ratios = {}
missing_dates = {}

for i in stocks:
    close = data[data['ticker']==i][['date','close']]
    close = close.sort_values(by='date')
    close = close.set_index('date')
   

    #data is missing days -> extrapolation or exclusion?

    #turn data into return (normalised just in divided by original amount), assume allocation of just 1 dollar

    close['normalised return'] = close['close']/close.iloc[0]['close']
    close['daily return'] = close['normalised return'].pct_change(1)
    #need risk free rate from same dates to do the calculation properly

    stock_closes[i] = close
    
    sharpe_zero_RFR = close['daily return'].mean()/close['daily return'].std()
    sharpe_ratios[i] = sharpe_zero_RFR

    #assess data quality of the time series nextm

    x=(close.index[0], close.index[-1], pd.date_range(start = close.index[0], end = close.index[-1] ).difference(close.index))
    missing_dates[i]=x