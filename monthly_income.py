import os
import json
from setting import BASE_URL, MAIN_HEADERS
from utils import arabic_to_english
from monthly_links import get_report_metadata
from monthly_data import get_monthly_data
import time

def get_monthly_income(data):
    """Extracts the monthly income from the JSON data."""
    for cell in data["sheets"][0]["tables"][0]["cells"]:
        if cell["rowCode"] == 16 and cell["columnCode"] == 17 and cell["value"] != "":
            return data["periodEndToDate"], cell["value"]
    for cell in data["sheets"][0]["tables"][0]["cells"]:
        if cell["rowCode"] == 5 and cell["columnCode"] == 7 and cell["value"] != "":
            return data["periodEndToDate"], cell["value"]
    for cell in data["sheets"][0]["tables"][0]["cells"]:
        if cell["rowCode"] == 12 and cell["columnCode"] == 17 and cell["value"] != "":
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
        if entry.is_file() and not "Total" in entry.path and entry.path.endswith("json"):
            with open(entry.path) as f:
                data = json.load(f)
            income_and_date = get_monthly_income(data)
            print("income is:",income_and_date)
            if income_and_date is not None:
                income_report[income_and_date[0]] = income_and_date[1]
    with open(f"Data/{symbol}/Total.json", "w") as f:
        json.dump(income_report, f)

if __name__ == "__main__":
    main("شکلر")
