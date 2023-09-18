import requests
import json
from Codal import CODAL_MONTHLY
import pandas as pd
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

def raw_link_extractor(symbol:str,only_first_page:bool = 0,number:int=50)-> list:
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
        rows.append(raw_data[i]['TracingNo'],
                    raw_data[i]['Symbol'],
                    raw_data[i]['CompanyName'],
                    raw_data[i]['Title'],
                    raw_data[i]['LetterCode'],
                    raw_data[i]['SentDateTime'],
                    raw_data[i]['PublishDateTime'],
                    raw_data[i]['Url'])
    return pd.DataFrame(data=rows,columns=['TracingNo',
                                           'Symbol',
                                           'CompanyName',
                                           'Title',
                                           'LetterCode',
                                           'SentDateTime',
                                           'PublishDateTime',
                                           'Url'])