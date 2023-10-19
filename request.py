# all code from tutorial: https://www.youtube.com/watch?v=zSAQxq6YOxg
# API: https://www.alphavantage.co/

import json
import requests
import plotly.express as px
import pandas as pd 

api_key = 'UKYXF61L981EG9X3'

def pretty_print(data: dict):
    print(json.dumps(data, indent=4))

def retrieve_data(function: str, symbol: str, api_key: str) -> dict:
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)

    data = response.text

    parsed = json.loads(data)

    return parsed

# Function to get the function type and symbol 
# def get_input()

# Function to insert results into a chart with user input

# main function to call all functions

# generating html
data = retrieve_data('TIME_SERIES_DAILY', 'IBM', api_key)
# pretty_print(retrieve_data('TIME_SERIES_DAILY', 'IBM', api_key))

# generating chart
def generate_line_chart_html(data, title='Stock Price Chart'):
    
    date_list = []
    close_price_list = [] 
    for date, values in data['Time Series (Daily)'].items():
         date_list.append(date)
         close_price_list.append(float(values['4. close']))

    df = pd.DataFrame({'Date': date_list, 'Close': close_price_list})

    fig = px.line(df, x='Date', y='Close', title=title)
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Close Price')

    # Convert the Plotly figure to HTML
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
     
line_chart_html = generate_line_chart_html(data)
with open("line_chart.html", "w", encoding="utf-8") as file:
        file.write(line_chart_html)

# Knick testing editing this file on October 18, 2023
