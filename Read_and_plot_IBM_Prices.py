# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 13:28:55 2017

@author: Steve Siegel
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

symbol = input("enter stock symbol:  ")
start_date = input("enter start date YYYY-MM-DD: ")
stop_date = input("enter stop date:  YYYY-MM-DD: ")
                   

ibm_prices_df = pd.read_csv('http://ichart.finance.yahoo.com/table.csv?s='+ symbol)
ibm_prices_df.to_csv('/tmp/prices0.csv', float_format='%4.2f', index=False)

prices1_df = pd.read_csv('/tmp/prices0.csv')

start = ibm_prices_df.Date > start_date #'2016-12-1' 
stop = ibm_prices_df.Date < stop_date #'2017-1-1'
pred_sr = start & stop

print(pred_sr)
prices0_df = ibm_prices_df.copy()[['Date','Adj Close']][pred_sr]

prices1_df = prices0_df.sort_values('Date')

#prices2_df = prices1_df.set_index('Date')

prices1_df.columns = ['date_s','price']

prices2_df = prices1_df.copy()[['date_s','price']]

date_dt_l = [datetime.strptime(day_s, '%Y-%m-%d') for day_s in prices2_df.date_s]
prices2_df['Date'] = date_dt_l

prices3_df = prices2_df.copy()[['Date','price']]
prices4_df = prices3_df.set_index('Date')

prices4_df.plot.line(title=symbol + " Prices")
#plt.savefig('IBM_Prices.png')

