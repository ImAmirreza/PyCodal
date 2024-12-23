import requests as r
from setting import SEARCH_HEADERS,LINKS
import re
import os
from utils import arabic_to_english
def get_report_metadata(symbol:str,pagenumber:int=1):
    report_dict = {}
    for page in range(1,pagenumber+1):
        data = r.get(LINKS.format(pagenumber=page,symbol=symbol),headers=SEARCH_HEADERS).json()
        pages = data["Page"]
        total = data["Total"]
        try:
            os.makedirs(f"Data/{symbol}", exist_ok=True)
        except OSError as e:
            print(f"Error creating directory: {e}")
        files = []
        for entry in os.scandir(f"Data/{symbol}"):
            if entry.is_file() and not "Total" in entry.path:
                files.append(entry.path.split("_")[1].split(".")[0])
        for letter in data["Letters"]:
            match = re.search(r"منتهی به\s+(\d{4}/\d{2}/\d{2})", letter["Title"])
            if match:
                date = match.group(1)
                jalali_date = arabic_to_english(date.replace("/","-"))
                jalali_date.split("-")[0]
                if jalali_date in files:
                    print(f"File of  {jalali_date} already exist.")
                elif int(jalali_date.split("-")[0])<=1401:
                    # print("Skikpping years before 1402",jalali_date)
                    pass
                elif "(اصلاحیه)" in letter["Title"]:
                    report_dict[date] = letter
                elif date not in report_dict:
                    report_dict[date] = letter
    return report_dict


