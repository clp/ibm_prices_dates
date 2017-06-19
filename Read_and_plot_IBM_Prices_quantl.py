from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import datetime as dt
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET','POST'])
def index():
    return render_template('index.html')


def getUserInput():
    #get the stock ticker and make it uppercase
    stockTicker = request.form['ticker'].upper()
    #turn checked features into a list
    features = request.form.getlist('feature')
    
    return stockTicker, features

def processData(stockTicker):
#get relevant financial data from QUANDL based on user input

    #get latest 90 days
    now = dt.datetime.now()
    endDate = now.strftime('%Y-%m-%d') 
    startDate = (now - dt.timedelta(days=90)).strftime('%Y-%m-%d')
    
    #get data from QUANDL
    link = 'https://www.quandl.com/api/v3/datasets/WIKI/'+stockTicker+'.json?start_date='+startDate+'&end_date='+endDate+'&order=asc'
    #D print("#D, link: ", link)
    jsonData = requests.get(link)
    
    # convert jsonData into dataframe
    dfData = pd.DataFrame(jsonData.json())
    #D print("#D, dfData.head(): ", dfData.head())
    
    #extract relevant data
    values = dfData.ix['data', 'dataset'] #list of list
    columnNames = dfData.ix['column_names','dataset'] #list of string
    relevantData = pd.DataFrame(values, columns = columnNames)
    
    #set date as index and convert date to actual date format
    relevantData = relevantData.set_index(['Date'])
    relevantData.index = pd.to_datetime(relevantData.index)
    
    return relevantData


def createPlot(data, features, stockTicker):
    # Create a Bokeh plot from the dataframe
    plot = figure(x_axis_type = "datetime")
    plot.title.text = 'Stock Ticker: ' + stockTicker
    if 'Open' in features:
        plot.line(data.index, data['Open'], color='green', legend='Opening Price')
    if 'High' in features:
        plot.line(data.index, data['High'], color='red', legend='Highest Price')
    if 'Low' in features:
        plot.line(data.index, data['Low'], color ='blue', legend = 'Lowest Price')
    if 'Close' in features:
        plot.line(data.index, data['Close'], color='black', legend='Closing Price')
    
    return plot


@app.route('/result',methods=['GET','POST'])
def result():
    stockTicker, features = getUserInput()
    data = processData(stockTicker)
    print("#D, data.head(): ", data.head())
    
    # Send output to static HTML file.
    # The plot should appear in the browser.
    output_file("bokeh.html")
    p = createPlot (data, features, stockTicker)
    show(p)
    
    return 'OK'
	
if __name__ == '__main__':
    app.run(host='0.0.0.0')
