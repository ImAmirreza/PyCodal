import os
import re
import json
import requests
from setting import BASE_URL, MAIN_HEADERS
from utils import arabic_to_english
from monthly_links import get_report_metadata
import time
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

def get_monthly_income(data):
    """Extracts the monthly income from the JSON data."""
    for cell in data["sheets"][0]["tables"][0]["cells"]:
        if cell["rowCode"] == 16 and cell["columnCode"] == 17 and cell["value"] != "":
            return data["periodEndToDate"], cell["value"]
    for cell in data["sheets"][0]["tables"][0]["cells"]:
        if cell["rowCode"] == 5 and cell["columnCode"] == 7 and cell["value"] != "":
            return data["periodEndToDate"], cell["value"]
    return None

def main(symbol,update=False):
    reports = get_report_metadata(symbol, 2)
    if len(reports)==0:
        print("There is no new data to downlod")
        if not update:
            return
    income_report = {}
    for key, value in reports.items():
        print(f"Getting data of date {arabic_to_english(key.replace('/', '-'))}")
        get_monthly_data(BASE_URL + value["Url"], symbol)
        time.sleep(5)
    for entry in os.scandir(f"Data/{symbol}"):
        if entry.is_file() and not "Total" in entry.path:
            with open(entry.path) as f:
                data = json.load(f)
            income_and_date = get_monthly_income(data)
            print(income_and_date)
            if income_and_date is not None:
                income_report[income_and_date[0]] = income_and_date[1]
    with open(f"Data/{symbol}/Total.json", "w") as f:
        json.dump(income_report, f)

if __name__ == "__main__":
    main("شکلر")
