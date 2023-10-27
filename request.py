# all code from tutorial: https://www.youtube.com/watch?v=zSAQxq6YOxg
# API: https://www.alphavantage.co/

import json
import requests
import plotly.express as px
import pandas as pd 
import matplotlib.pyplot as plt
import io 
import base64
import numpy as np
import plotly.graph_objects as go

api_key = 'UKYXF61L981EG9X3'

def pretty_print(data: dict):
    print(json.dumps(data, indent=4))


# def retrieve_data(function: str, symbol: str, api_key: str) -> dict:

#     url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
#     response = requests.get(url)

#     data = response.text

#     parsed = json.loads(data)

#     return parsed

# Testing changes


def retrieve_data(TimeSeries: int, symbol: str, api_key: str, time: str) -> dict:
    if TimeSeries == 1:
        function = 'TIME_SERIES_INTRADAY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={time}&apikey={api_key}"
        # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
    elif TimeSeries == 2:
        function = 'TIME_SERIES_DAILY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    elif TimeSeries == 3:
        function = 'TIME_SERIES_WEEKLY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    elif TimeSeries == 4: 
        function = 'TIME_SERIES_MONTHLY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    
    response = requests.get(url)

    data = response.text

    parsed = json.loads(data)

    return parsed


# time series: TIME_SERIES_INTRADAY, TIME_SERIES_DAILY, TIME_SERIES_WEEKLY, TIME_SERIES_MONTHLY
# Function to get the function type and symbol 
def get_input():
    while True:
        try:
            print("Stock Data Visualizer")
            print("-----------------------")
            stock_symbol = input("\nEnter the stock symbol you are looking for: ")
            break
        except Exception as e:
            print(f"Error occurred: {e}.")

    while True:
        try:
            print("\nChart Types")
            print("----------------")
            print("1. Bar\n2. Candlestick")
            bar_chart_type = int(input("\nEnter the bar chart type (1, 2): "))
            if bar_chart_type not in [1,2]:
                raise ValueError("Please enter 1 or 2 for chart type.")
            break
        except ValueError as e:
            print(f"Value error occurred: {e}.")
        except Exception as e:
            print(f"Error occurred: {e}.")

    while True:
        try:
            print("\nSelect the Time Series of the chart you want to generate")
            print("---------------------------------------------------------")
            print("1. Intraday\n2. Daily\n3. Weekly\n4. Monthly")
            time_series = int(input("\nEnter the time series (1, 2, 3, 4): "))
            if time_series not in [1, 2, 3, 4]:
                raise ValueError("Please enter 1, 2, 3, or 4 for time series.")
            break
        except ValueError as e:
            print(f"Value error occurred: {e}.")
        except Exception as e:
            print(f"Error occurred: {e}.")

    while True:
        try:
            start_date = input("\nEnter the start date (YYYY-MM-DD): ")
            end_date = input("\nEnter the end date (YYYY-MM-DD): ")
            if start_date > end_date:
                raise ValueError("Start date cannot be later than end date. Enter the dates again.")
            break
        except ValueError as e:
            print(f"Value error occurred: {e}.")
        except Exception as e:
            print(f"Error Occured: {e}.")

    while True:
        try:
            data = retrieve_data(time_series, stock_symbol, api_key)
            if data is None:
                raise ValueError("Failed to retrieve data.")
            break
        except ValueError as e:
            print(f"Value error occurred: {e}.")
        except Exception as e:
            print(f"Error occurred: {e}.")

    # with open('output.json', 'w') as json_file:
    #     json.dump(data, json_file, indent=4)
    chart_html = generate_line_chart_html(data,bar_chart_type=bar_chart_type,time_series=time_series,start_date=start_date,end_date=end_date,time=time)

    with open("chart.html", "w", encoding="utf-8") as file:
        file.write(chart_html)

def generate_line_chart_html(data, title='Stock Price Chart',bar_chart_type=1, time_series=1, start_date=None, end_date=None, time=None):
    
    date_list = []
    open_price_list = [] 
    high_price_list = []
    low_price_list = []
    close_price_list = []
     
    if time_series == 1:
        # Time Series (60min)
        x = f'Time Series ({time})'

    elif time_series == 2:
        x = 'Time Series (Daily)'
    elif time_series == 3:
        x = 'Weekly Time Series'
    elif time_series == 4: 
        x = 'Monthly Time Series'
    # ['Time Series (Daily)']
    for date, values in data[x].items():
         date_list.append(pd.to_datetime(date).to_pydatetime())
         open_price_list.append(float(values['1. open']))
         high_price_list.append(float(values['2. high']))
         low_price_list.append(float(values['3. low']))
         close_price_list.append(float(values['4. close']))

    df = pd.DataFrame({'Date': date_list, 'Open': open_price_list, 'High': high_price_list, 'Low': low_price_list, 'Close': close_price_list})

    if bar_chart_type == 1:
        fig = px.line(df, x='Date', y=['Open', 'High', 'Low', 'Close'], title=title)
    elif bar_chart_type == 2:
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
        fig.update_layout(title=title)

    fig.update_traces(line=dict(color='#FF5733'), selector=dict(name='Open'))
    fig.update_traces(line=dict(color='#0072B2'), selector=dict(name='High'))
    fig.update_traces(line=dict(color='#228B22'), selector=dict(name='Low'))
    fig.update_traces(line=dict(color='#FFD700'), selector=dict(name='Close'))

    fig.update_xaxes(title='Date', tickformat='%Y-%m-%d', tickangle=45)
    fig.update_yaxes(title='Price')

    fig.update_layout(legend=dict(
            orientation='v', 
            x=-.1,               
            y=1.05,
            bgcolor='white',
            bordercolor='gray',
            borderwidth=1          
        ))
    
    y_values = [130, 135, 140, 145, 150]
    fig.update_layout(shapes=[
        dict(
            type='line',
            x0=df['Date'].min(),
            x1=df['Date'].max(),
            y0=y,
            y1=y,
            xref='x',
            yref='y',
            line=dict(
                color='gray',       
                width=1,            
                dash='dot'          
            )
        ) for y in y_values  
    ])
    
    if start_date and end_date:
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    if time_series == 1:
        pass
    elif time_series == 2:
        pass
    elif time_series == 3:
        df.set_index('Date', inplace=True)
        df = df.resample('W').last()
    elif time_series == 4:
        df.set_index('Date', inplace=True)
        df = df.resample('M').last()
    chart_html = fig.to_html(full_html=False)

    # Wrap the chart HTML in a complete HTML page
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        {chart_html}
    </body>
    </html>
    """

    return html

get_input()