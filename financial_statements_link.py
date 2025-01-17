from setting import YEARLY_FS_LINKS,MAIN_HEADERS
import os
import requests as r
import re
from utils import arabic_to_english, modify_url
def get_fs_metadata(symbol,pagenumber=1):
    report_dict = {}
    for page in range(1,pagenumber+1):
        data = r.get(modify_url(YEARLY_FS_LINKS,{
            "PageNumber": pagenumber,
            "Symbol": symbol,
        }),headers=MAIN_HEADERS).json()
        pages = data["Page"]
        total = data["Total"]
        print(data)
        try:
            os.makedirs(f"Data/{symbol}/FS", exist_ok=True)
        except OSError as e:
            print(f"Error creating directory: {e}")
        files = []
        for entry in os.scandir(f"Data/{symbol}/FS"):
            if entry.is_file() and not "Total" in entry.path:
                try:
                    print(entry,entry.path.split("_")[1].split(".")[0])
                    files.append(entry.path.split("_")[1].split(".")[0])
                except Exception as e:
                    print(e)
        for letter in data["Letters"]:
            # print(letter)
            match = re.search(r"منتهی به\s+(\d{4}/\d{2}/\d{2})", letter["Title"])
            if match:
                date = match.group(1)
                jalali_date = arabic_to_english(date.replace("/","-"))
                jalali_date.split("-")[0]
                if jalali_date in files:
                    print(f"File of  {jalali_date} already exist.")
                # elif int(jalali_date.split("-")[0])<=1401:
                    # print("Skikpping years before 1402",jalali_date)
                    # pass
                elif "(اصلاحیه)" in letter["Title"]:
                    report_dict[date] = letter
                elif "(حسابرسی شده)" in letter["Title"]:
                    report_dict[date] = letter
                elif date not in report_dict:
                    report_dict[date] = letter
    return report_dict
