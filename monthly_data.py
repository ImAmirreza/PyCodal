import re
import json
import requests
from setting import BASE_URL, MAIN_HEADERS
from utils import get_json

def get_monthly_data(url, symbol):
    """Downloads a JSON file from the specified URL and saves it to a file in the specified directory."""
    data = get_json(url)
    if data is None:
        return
    if "Investment" in data["title_En"]:
        print("For now this tools is not for Investemt companies")
        raise NotImplementedError("Investment companies not supported")
    filename = f"Data/{symbol}/{data['sheets'][0]['title_En']}_{data['periodEndToDate'].replace('/', '-')}.json"
    with open(filename, "w") as f:
        json.dump(data, f)