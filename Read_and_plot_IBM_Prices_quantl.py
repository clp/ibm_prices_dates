# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 13:28:55 2017

@author: Steve Siegel
"""
from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import datetime as dt
from bokeh.plotting import figure
from bokeh.embed import components
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

#@app.route('/index', methods=['GET','POST'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

def getUserInput():
    #get the stock ticker and make it uppercase
    stockTicker = request.form['ticker'].upper()
    #turn checked features into a list
    features = request.form.getlist('feature')
    print (stockTicker)
    return stockTicker, features

def processData(stockTicker):
#get relevant financial data from QUANDL based on user input

    #get latest 90 days
    now = dt.datetime.now()
    endDate = now.strftime('%Y-%m-%d') 
    startDate = (now - dt.timedelta(days=90)).strftime('%Y-%m-%d')
    
    #get data from QUANDL
    #link = 'https://www.quandl.com/api/v3/datasets/WIKI/'+stockTicker+'.json?start_date='+startDate+'&end_date='+endDate+'&order=asc'
    #jsonData = requests.get(link)
    ibm_prices_df = pd.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/IBM.csv')
    ibm_prices_df.to_csv('/home/ann/tmp/prices0.csv', float_format='%4.2f', index=False)
    # convert jsonData into dataframe
    #dfData = pd.DataFrame(jsonData.json())
    
    #extract relevant data
    #values = dfData.ix['data', 'dataset'] #list of list
    #columnNames = dfData.ix['column_names','dataset'] #list of string
    #relevantData = pd.DataFrame(values, columns = columnNames)
    
    #set date as index and convert date to actual date format
    #relevantData = relevantData.set_index(['Date'])
    #relevantData.index = pd.to_datetime(relevantData.index)
    
    #return dfData



#@app.route('/result',methods=['GET','POST'])
@app.route('/result',methods=['GET'])
def result():
    stockTicker, features = getUserInput()
    data = processData(stockTicker)
   
    
    #return render_template('bokeh.html', script=script, div=div)
	
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
#import pandas as pd
#3import matplotlib.pyplot as plt
#from datetime import datetime

#symbol = input("enter stock symbol:  ")
#start_date = input("enter start date YYYY-MM-DD: ")
#stop_date = input("enter stop date:  YYYY-MM-DD: ")
                   

#ibm_prices_df = pd.read_csv('http://ichart.finance.yahoo.com/table.csv?s='+ symbol)
#ibm_prices_df.to_csv('/tmp/prices0.csv', float_format='%4.2f', index=False)



#start = ibm_prices_df.Date > start_date #'2016-12-1' 
#stop = ibm_prices_df.Date < stop_date #'2017-1-1'
#pred_sr = start & stop

#print(pred_sr)
#prices0_df = ibm_prices_df.copy()[['Date','Adj Close']][pred_sr]

#prices1_df = prices0_df.sort_values('Date')

#prices2_df = prices1_df.set_index('Date')

#prices1_df.columns = ['date_s','price']

#prices2_df = prices1_df.copy()[['date_s','price']]

#date_dt_l = [datetime.strptime(day_s, '%Y-%m-%d') for day_s in prices2_df.date_s]
#prices2_df['Date'] = date_dt_l

#prices3_df = prices2_df.copy()[['Date','price']]
#prices4_df = prices3_df.set_index('Date')

#prices4_df.plot.line(title=symbol + " Prices")
#plt.savefig('IBM_Prices.png')

