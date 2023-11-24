from flask import Flask, render_template, request
import webbrowser
import threading
import os
import plotly.express as px
import pandas as pd
import requests

api_key = 'UKYXF61L981EG9X3'
app = Flask(__name__)

def open_browser():
    print("Opening browser")
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    stock_symbol = request.form['stock_symbol']
    time_series_str = request.form['time_series']
    chart_type = request.form['chart_type']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    time_series = int(time_series_str)

    # Retrieve stock data using your function
    data = stock_request.retrieve_data(time_series, stock_symbol, api_key, time=None)

    # Process the data to a DataFrame
    df = pd.DataFrame(data['Time Series (Daily)']).T
    df.index = pd.to_datetime(df.index)
    df['4. close'] = pd.to_numeric(df['4. close'])

    # Create a line chart using Plotly Express
    fig = px.line(df, x=df.index, y='4. close', title=f"Stock Data for {stock_symbol}: {start_date} to {end_date}")

    # Convert the Plotly chart to HTML
    chart_html = fig.to_html(full_html=False)

    return chart_html

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
