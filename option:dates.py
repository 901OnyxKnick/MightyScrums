import json
import requests
import webbrowser
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def retrieve_data(TimeSeries: int, symbol: str, api_key: str, time: str) -> dict:
    url = None
    if TimeSeries == 1:
        function = 'TIME_SERIES_INTRADAY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={time}&apikey={api_key}"
    elif TimeSeries == 2:
        function = 'TIME_SERIES_DAILY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    elif TimeSeries == 3:
        function = 'TIME_SERIES_WEEKLY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    elif TimeSeries == 4:
        function = 'TIME_SERIES_MONTHLY'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    else:
        raise ValueError(f"Invalid TimeSeries value {TimeSeries}")

    if url is not None:
        response = requests.get(url)
        data = response.json()
        print(json.dumps(data, indent=4))
        return data

def generate_line_chart_html(data, title='Stock Price Chart', bar_chart_type=1, time_series=1, start_date=None, end_date=None, time=None):
    if time_series == 1:
        x = 'Time Series (1min)'
    elif time_series == 2:
        x = 'Time Series (Daily)'
    elif time_series == 3:
        x = 'Weekly Time Series'
    elif time_series == 4:
        x = 'Monthly Time Series'
    else:
        raise ValueError(f"Invalid time_series value: {time_series}")

    date_list = []
    open_price_list = []
    high_price_list = []
    low_price_list = []
    close_price_list = []

    for date, values in data[x].items():
        date_list.append(pd.to_datetime(date).to_pydatetime())
        open_price_list.append(float(values['1. open']))
        high_price_list.append(float(values['2. high']))
        low_price_list.append(float(values['3. low']))
        close_price_list.append(float(values['4. close']))

    df = pd.DataFrame({'Date': date_list, 'Open': open_price_list, 'High': high_price_list, 'Low': low_price_list, 'Close': close_price_list})

    if bar_chart_type == 1:
        fig = px.line(df, x='Date', y=['Open', 'High', 'Low', 'Close'], title=title)
    elif bar_chart_type == '2':
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'])])
    else:
        raise ValueError(f"Invalid bar_chart_type value: {bar_chart_type}")

    chart_html = fig.to_html(full_html=False)

    return chart_html

def get_input():
    stock_symbol = input("Enter stock symbol: ")
    time_series = int(input("Enter time series (1: Intraday, 2: Daily, 3: Weekly, 4: Monthly): "))
    chart_type = input("Enter chart type (1: Line chart, 2: Candlestick chart): ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    api_key = 'UKYXF61L981EG9X3'
    time = '1min' if time_series == 1 else None  

    data = retrieve_data(time_series, stock_symbol, api_key, time)
    chart_html = generate_line_chart_html(data, title=f"Stock Data for {stock_symbol}: {start_date} to {end_date}", bar_chart_type=chart_type, time_series=time_series, start_date=start_date, end_date=end_date, time=time)

    with open("chart.html", "w", encoding="utf-8") as file:
        file.write(chart_html)
        file.close()
        filename = 'file:///'+os.getcwd()+'/' + 'chart.html'
        webbrowser.open_new_tab(filename)

if __name__ == '__main__':
    get_input()
