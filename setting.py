LINKS = "https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=true&CompanyState=0&CompanyType=1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=58&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber={pagenumber}&Publisher=false&ReportingType=-1&Symbol={symbol}&TracingNo=-1&search=true"
FS_LINKS = "https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=1&Childs=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=-1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber={pagenumber}&Publisher=false&ReportingType=-1&Symbol={symbol}&TracingNo=-1&search=true"
YEARLY_FS_LINKS = "https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=1&Childs=true&CompanyState=-1&CompanyType=-1&Consolidatable=true&IsNotAudited=false&Length=12&LetterType=6&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber=-1&Publisher=false&ReportingType=-1&Symbol=-1&TracingNo=-1&search=true"
USER_AGENT = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

SEARCH_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'search.codal.ir',
    'Origin': 'https://codal.ir',
    'Referer': 'https://codal.ir/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"'
}

MAIN_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'codal.ir',
    'Origin': 'https://codal.ir',
    'Referer': 'https://codal.ir/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"'
}

BASE_URL = "https://codal.ir"