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

# generating line chart
def generate_line_chart_html(data, title='Stock Price Chart'):
    
    date_list = []
    open_price_list = [] 
    high_price_list = []
    low_price_list = []
    close_price_list = [] 
    for date, values in data['Time Series (Daily)'].items():
         date_list.append(date)
         open_price_list.append(float(values['1. open']))
         high_price_list.append(float(values['2. high']))
         low_price_list.append(float(values['3. low']))
         close_price_list.append(float(values['4. close']))

    df = pd.DataFrame({'Date': date_list, 'Open': open_price_list, 'High': high_price_list, 'Low': low_price_list, 'Close': close_price_list})

    fig = px.line(df, x='Date', y=['Open', 'High', 'Low', 'Close'], title=title)

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

# def generate_bar_chart_html(data, title='Bar Chart'):
#     date_list = []
#     close_price_list = []

#     for date, values in data['Time Series (Daily)'].items():
#         date_list.append(date)
#         close_price_list.append(float(values['4. close']))

#     df = pd.DataFrame({'Date': date_list, 'Close': close_price_list})

#     plt.figure(figsize=(12, 6))
#     plt.bar(df['Date'], df['Close'], color='blue', width=0.5)
#     plt.xlabel('Date')
#     plt.ylabel('Close Price')
#     plt.title(title)
#     plt.xticks(range(0, len(df['Date']), 5), df['Date'][::5], rotation=45)
#     plt.tight_layout()

#     # Convert the Matplotlib figure to HTML
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_base64 = base64.b64encode(buffer.read()).decode()
#     chart_html = f'<img src="data:image/png;base64,{image_base64}">'

#     # Wrap the chart HTML in a complete HTML page
#     html = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>{title}</title>
#     </head>
#     <body>
#         <h1>{title}</h1>
#         {chart_html}
#     </body>
#     </html>
#     """

#     return html 

# bar_chart_html = generate_bar_chart_html(data)
line_chart_html = generate_line_chart_html(data)
with open("line_chart.html", "w", encoding="utf-8") as file:
        file.write(line_chart_html)
# with open("bar_chart.html", "w", encoding="utf-8") as file: 
#      file.write(bar_chart_html)



# Knick testing editing this file on October 18, 2023
