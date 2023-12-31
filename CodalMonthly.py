import requests
import json
from Codal import CODAL_MONTHLY,CODAL_DATETIME_FORMAT
import pandas as pd
import jdatetime
import time
from pathlib import Path

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
p = Path("Data/links").mkdir(parents=True, exist_ok=True)
def raw_link_extractor(symbol:str,
                       only_first_page:bool = 0,
                       number:int=50) -> list:
    page = 1
    total_data  = []
    while len(total_data) < number:
        URL = CODAL_MONTHLY.format(symbol=symbol,page=page)
        data = requests.get(URL, headers=headers).json()
        total_data += data["Letters"] 
        page+=1
        if page >= data['Page'] or only_first_page:
            break
    return total_data[:number]


def symbol_links_grabber(symbol:str,
                         only_first_page:bool=0,
                         number:int=50) -> pd.DataFrame:
    raw_data = raw_link_extractor(symbol=symbol,
                              number=number,
                              only_first_page=only_first_page)
    rows = []
    for i in range(len(raw_data)):
        rows.append([raw_data[i]['TracingNo'],
                    raw_data[i]['Symbol'],
                    raw_data[i]['CompanyName'],
                    raw_data[i]['Title'],
                    raw_data[i]['LetterCode'],
                    raw_data[i]['SentDateTime'],
                    raw_data[i]['PublishDateTime'],
                    raw_data[i]['Url']])
    return pd.DataFrame(data=rows,columns=['TracingNo',
                                           'Symbol',
                                           'CompanyName',
                                           'Title',
                                           'LetterCode',
                                           'SentDateTime',
                                           'PublishDateTime',
                                           'Url'])



def links_to_file(df:pd.DataFrame):
    last_link_date = jdatetime.datetime.strptime(df.iloc[0]["SentDateTime"],
                                                 CODAL_DATETIME_FORMAT).strftime("%Y-%m-%d")
    try:
        pre_df = pd.read_csv(Path("Data/links") / f'{df.iloc[0]["Symbol"]}.csv')
        merged_df = pd.concat([pre_df,df]).drop_duplicates().reset_index(drop=True).sort_values(by="TracingNo",ascending=False)
        merged_df.to_csv(Path("Data/links") / f'{df.iloc[0]["Symbol"]}.csv',index=False)
        print(f"file: {df.iloc[0]['Symbol']}.csv founded and updated")
    except FileNotFoundError:
        df.to_csv(Path("Data/links") / f'{df.iloc[0]["Symbol"]}.csv',index=False)
        print(f"file: {df.iloc[0]['Symbol']}.csv not founded so created")


def codal_monthly_link_grabber(symbol_file:str = "All_Symbols.csv"):
    symbols = pd.read_csv(Path("Data")/Path(symbol_file))
    for _,symbol in symbols.iterrows():
            time.sleep(3)
            df = symbol_links_grabber(symbol["Symbol"].strip())
            if len(df)==0:
                print(f"Some problem occured when scraping {symbol['Symbol']} data")
                continue
            data = links_to_file(df)


def codal_monthly_link_grabber(symbol_name:str,update:bool):
    df = symbol_links_grabber(symbol=symbol_name.strip())
    if len(df)==0:
        print(f"Some problem occured when scraping {symbol_name} data")
        return
    data = links_to_file(df)