import requests
from bs4 import BeautifulSoup
import re
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

total_data = pd.DataFrame()


class Monthly_table:
    
    
    def __init__(self):
        self.vahed = pd.Series(dtype=str)
        self.tolid = pd.Series(dtype=float)
        self.name = pd.Series(dtype=str)
        self.foroosh = pd.Series(dtype=float)
        self.nerkh_foroosh = pd.Series(dtype=float)
        self.mablagh_foroosh = pd.Series(dtype=float)

    def read_from_web(self,link:str) -> dict:
        data = requests.get(link,headers=HEADERS).text
        title = BeautifulSoup(data,"html.parse").find(attrs={"id":"ctl00_txbSymbol"}).text
            # Use regular expressions to find the 'datasource' variable
        match = re.search(r'var datasource = ({.*?});', data, re.DOTALL)

        if match:
            datasource_str = match.group(1)
            datasource_str = datasource_str.replace("\'","\"")
        else:
            print("Unable to find 'datasource' variable")
        # raw = datasource_str

        datasource_str = json.loads(datasource_str)
        periodEndToDate = datasource_str["periodEndToDate"]
        with open(title +"-"+periodEndToDate,'w') as f:
            json.dump(datasource_str,f,indent=6)
            print(title +"-"+periodEndToDate+" saved")
        return datasource_str,title
        
            
    def data_converter(self,datasource:dict[str,any],title):
        data_dict={}
        for i in datasource["sheets"][0]["tables"][0]["cells"]:
            if (i["rowCode"] == 16) and (i["columnCode"] == 17):
                # print("sum of sells in rials: ",i)
                try:
                    data_dict["ISP"]
                except KeyError:
                    data_dict["ISP"] = {"value" : i["value"], "row":i["rowSequence"], "column":i["columnSequence"]}
                
            if (i["rowCode"] == 5) and (i["columnCode"] == 15):
                # print("internal sell(count): ",i)
                try:
                    data_dict["ISA"]
                except KeyError:
                    data_dict["ISA"] = {"value" : i["value"], "row":i["rowSequence"], "column":i["columnSequence"]}
                
            if (i["rowCode"] == 4) and (i["columnCode"] == 2) and i["value"] != "":
                # print("vahed: ",i)

                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.vahed = pd.concat([self.vahed,s])


            if (i["rowCode"] == 4) and (i["columnCode"] == 14) and i["value"] != "":
                # print("kala: ",i)

                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.tolid = pd.concat([self.tolid,s])
            if (i["rowCode"] == 4) and (i["columnCode"] == 1) and i["value"] != "":
                # print("tedad tolid",i)

                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.name = pd.concat([self.name,s])
            if (i["rowCode"] == 4) and (i["columnCode"] == 15) and i["value"] != "":
                # print("tedad foroosh: ",i)
                # print(i)
                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.foroosh = pd.concat([self.foroosh,s])
            if (i["rowCode"] == 4) and (i["columnCode"] == 16) and i["value"] != "":
                # print("nerkh_foroosh: ",i)
                # print(i)
                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.nerkh_foroosh = pd.concat([self.nerkh_foroosh,s])
            if (i["rowCode"] == 4) and (i["columnCode"] == 17) and i["value"] != "":
                # print("nerkh_foroosh: ",i)
                # print(i)
                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.mablagh_foroosh = pd.concat([self.mablagh_foroosh,s])
        data = pd.concat([self.vahed,self.name,self.tolid,self.foroosh,self.nerkh_foroosh,self.mablagh_foroosh],axis=1).dropna().reset_index(drop=True).rename(columns={0:"vahed",1:"esm",2:"tolid",3:"foroosh",4:"nerkh_foroosh",5:"mablagh_forosh"})
        periodEndToDate = datasource["periodEndToDate"].split("/")
        data["Year"] = periodEndToDate[0]
        data["Month"] = periodEndToDate[1]
        data["Day"] = periodEndToDate[2]
        data["nemad"] = title
        return data,data_dict

  
for i in Path("Data/links/*.csv"):
    obj = Monthly_table()
    # df, data_dict = obj.data_converter(obj.read_from_web(i))
    # total_data = pd.concat([total_data,df])
    obj.read_from_web(i)
# total_data.to_csv("kegohar.csv",index=False)

