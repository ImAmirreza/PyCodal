import requests
import json


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

def raw_link_extractor(symbol:str,only_first_page:bool = 0,number:int=50)-> list:
    page = 1
    total_data  = []
    while len(total_data) < number:
        URL = f"https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=3&Childs=false&CompanyState=0&CompanyType=1&Consolidatable=true&IsNotAudited=false&Isic=132004&Length=-1&LetterType=58&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber={page}&Publisher=false&Symbol={symbol}&TracingNo=-1&search=true"
        data = requests.get(URL, headers=headers).json()
        total_data += data["Letters"] 
        page+=1
        if page >= data['Page'] or only_first_page:
            break
    return total_data[:number]