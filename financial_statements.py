
from utils import get_json
import json
from financial_statements_link import get_fs_metadata, arabic_to_english
from setting import BASE_URL
import time 

sheets = {
    "income_statement":"&sheetId=1",
    "balance_sheet":""
    ""
}


def get_statement_data(url, symbol):
    """Downloads a JSON file from the specified URL and saves it to a file in the specified directory."""
    data = get_json(url)
    if data is None:
        return
    if "Investment" in data["title_En"]:
        print("For now this tools is not for Investemt companies")
        raise NotImplementedError("Investment companies not supported")
    filename = f"Data/{symbol}/FS/{data['sheets'][0]['title_En']}_{data['periodEndToDate'].replace('/', '-')}_p{data['period']}.json"
    with open(filename, "w") as f:
        json.dump(data, f)
    print(filename)

def get_fs_json(symbol,update=False,sheetname="profitloss"):
    reports = get_fs_metadata(symbol, 1)
    if len(reports)==0:
        print("There is no new data to downlod")
        if not update:
            return
    satetment = {}
    for key, value in reports.items():
        print(f"Getting data of date {arabic_to_english(key.replace('/', '-'))}")
        get_statement_data(BASE_URL + value["Url"]+ sheets[sheetname], symbol)
        time.sleep(5)
    

def get_eps(data):
    
    for cell in data["sheets"][0]["tables"][0]["cells"]:
        if cell["rowCode"] == 41 and cell["columnCode"] == 2 and cell["value"] != "":
            return data["periodEndToDate"], cell["value"]
    for cell in data["sheets"][0]["tables"][1]["cells"]:
        if cell["rowCode"] == 41 and cell["columnCode"] == 2 and cell["value"] != "":
            return data["periodEndToDate"], cell["value"]
    return None


# get_fs_json("شکلر")
import os 
symbol = "شکلر"
for entry in os.scandir(f"Data/{symbol}/FS"):
        if entry.is_file() and not "Total" in entry.path and entry.path.endswith("json"):
            with open(entry.path) as f:
                data = json.load(f)
            eps = get_eps(data)
            print("eps is:",eps)
            