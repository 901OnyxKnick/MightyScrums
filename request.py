# all code from tutorial: https://www.youtube.com/watch?v=zSAQxq6YOxg

import json
import requests

api_key = 'UKYXF61L981EG9X3'

def pretty_print(data: dict):
    print(json.dumps(data, indent=4))

def retrieve_data(function: str, symbol: str, api_key: str) -> dict:
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)

    data = response.text

    parsed = json.loads(data)

    return parsed

pretty_print(retrieve_data('TIME_SERIES_DAILY', 'IBM', api_key))