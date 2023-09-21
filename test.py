import pandas as pd
import requests as r

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
fetch("http://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch?market=0&industrialGroup=&paperTypes%5B0%5D=1&paperTypes%5B1%5D=2&showTraded=false&withBestLimits=true&hEven=0&RefID=0", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.8",
    "sec-gpc": "1"
  },
  "referrer": "http://main.tsetmc.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
});
data = r.get("http://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx?h=180435&r=12252060525",headers=HEADERS).text
print(data)
http://cdn.tsetmc.com/api/StaticData/GetStaticData