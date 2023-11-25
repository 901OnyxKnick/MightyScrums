# Team 10 Project 3
# 10/27/2023

import json
import requests
import plotly.express as px
import pandas as pd 
import matplotlib.pyplot as plt
import io 
import base64
import numpy as np
import plotly.graph_objects as go
import webbrowser
import os
import yfinance as yf

api_key = 'UKYXF61L981EG9X3'

# checking all the stock symbols
def check_stock_symbol(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        info = stock.info
        if info is not None:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error occurred: {e}.")

def pretty_print(data: dict):
    print(json.dumps(data, indent=4))

# retrieving data from the url/api
def retrieve_data(TimeSeries: int, symbol: str, api_key: str, time: str) -> dict:
    url = None
    if TimeSeries == 1:
        function = 'TIME_SERIES_INTRADAY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval=5min&apikey={api_key}"
        # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
    elif TimeSeries == 2:
        function = 'TIME_SERIES_DAILY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    elif TimeSeries == 3:
        function = 'TIME_SERIES_WEEKLY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
        print(url)
    elif TimeSeries == 4: 
        function = 'TIME_SERIES_MONTHLY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    else:
        raise ValueError(f"Invalid TimeSeries value {TimeSeries}")
    
    if url is not None:
        response = requests.get(url)
    
    response = requests.get(url)

    data = response.text
    print(data)
    parsed = json.loads(data)

    return parsed

def generate_line_chart_html(data, title='Stock Price Chart',bar_chart_type=1, time_series=1, start_date=None, end_date=None, time=None):
    date_list = []
    open_price_list = [] 
    high_price_list = []
    low_price_list = []
    close_price_list = []
     
    if time_series == 1:
        # hopefully this works just hardcoded 5min instead of having an option
        x = f'Time Series (5min)'
    # handling daily
    elif time_series == 2:
        x = 'Time Series (Daily)'
    # handling weekly
    elif time_series == 3:
        x = 'Weekly Time Series'
    # handling monthly 
    elif time_series == 4: 
        x = 'Monthly Time Series'
    else:
    # Handle the case where none of the above conditions are met
        raise ValueError(f"Invalid time_series value: {time_series}")

    # adding all the data from the api to lists to help display the graph
    for date, values in data[x].items():
         date_list.append(pd.to_datetime(date).to_pydatetime())
         open_price_list.append(float(values['1. open']))
         high_price_list.append(float(values['2. high']))
         low_price_list.append(float(values['3. low']))
         close_price_list.append(float(values['4. close']))

    # adding all the lists so its in a dataframe
    df = pd.DataFrame({'Date': date_list, 'Open': open_price_list, 'High': high_price_list, 'Low': low_price_list, 'Close': close_price_list})
    
    # handling the date part
    if start_date and end_date:
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    bar_chart_type = int(bar_chart_type)

    # if bar_chart_type = 1 we display a line chart
    if bar_chart_type == 1: 
        fig = px.line(df, x='Date', y=['Open', 'High', 'Low', 'Close'], title=title)
        fig.update_traces(line=dict(color='#FF5733'), selector=dict(name='Open'))
        fig.update_traces(line=dict(color='#0072B2'), selector=dict(name='High'))
        fig.update_traces(line=dict(color='#228B22'), selector=dict(name='Low'))
        fig.update_traces(line=dict(color='#FFD700'), selector=dict(name='Close'))        
    # if bar_chart_type = 2 we display a bar chart
    if bar_chart_type == 2: 
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['Date'], y=df['Open'], name='Open', marker_color='#FF5733'))
        fig.add_trace(go.Bar(x=df['Date'], y=df['High'], name='High', marker_color='#0072B2'))
        fig.add_trace(go.Bar(x=df['Date'], y=df['Low'], name='Low', marker_color='#228B22'))
        fig.add_trace(go.Bar(x=df['Date'], y=df['Close'], name='Close', marker_color='#FFD700'))
        fig.update_layout(title=title, barmode='group')

    # updating what the axis should look like, ie. the bottom will be date and the left will be price
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="Price Type",
        xaxis_tickformat='%Y-%m-%d',
        xaxis_tickangle=45
    )

    if time_series == 1:
        pass
    elif time_series == 2:
        pass
    # this part should be changing it so it the dates are in a W format for weeks and M for months
    elif time_series == 3:
        df.set_index('Date', inplace=True)
        df = df.resample('W').last()
    elif time_series == 4:
        df.set_index('Date', inplace=True)
        df = df.resample('M').last()
    chart_html = fig.to_html(full_html=False)

    return chart_html

