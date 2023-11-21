from flask import Flask, render_template, request
import request as stock_request
import webbrowser 
import threading 
import os


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
    # Hardcoded 15min for intraday so it actually displays
    if time_series_str == '1':
        data = stock_request.retrieve_data(time_series, stock_symbol, api_key, time='15min')
        chart_html = stock_request.generate_line_chart_html(data, title=f"Stock Data for {stock_symbol}: {start_date} to {end_date}", bar_chart_type=chart_type, time_series=time_series, start_date=None, end_date=None, time='15min')
    else: 
        data = stock_request.retrieve_data(time_series, stock_symbol, api_key, time=None)
        chart_html = stock_request.generate_line_chart_html(data, title=f"Stock Data for {stock_symbol}: {start_date} to {end_date}", bar_chart_type=chart_type, time_series=time_series, start_date=None, end_date=None, time=None)

    return chart_html






if __name__ == '__main__':
    # Added this to prevent a second window from opening up
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
    