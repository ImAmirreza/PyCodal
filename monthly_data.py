import re
import json
import requests
from setting import BASE_URL, MAIN_HEADERS

def get_html(url):
    """Makes a GET request to the specified URL and returns the HTML response."""
    return requests.get(url, headers=MAIN_HEADERS).text

def get_json(url):
    """Extracts a JSON string from the HTML response using a regular expression and parses it into a Python object."""
    html_source = get_html(url)
    pattern = r"var datasource = (.*?)</script>"
    match = re.search(pattern, html_source, re.DOTALL)
    if match:
        json_string = match.group(1).strip().replace(";","")
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print(json_string)
            return None
    else:
        print("No match found.")
        return None
    return data

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