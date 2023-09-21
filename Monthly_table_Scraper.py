import requests
from bs4 import BeautifulSoup
import requests.exceptions 
import re
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from Codal import BASE_CODAL
import os
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

Path("Data/raw_json").mkdir(exist_ok=True,parents=True)
raw_json_files_path = Path("Data/raw_json")
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
        data = requests.get(BASE_CODAL + link,headers=HEADERS).text
        title = BeautifulSoup(data,"html.parser").find(attrs={"id":"ctl00_txbSymbol"}).text.replace("ي","ی")
            # Use regular expressions to find the 'datasource' variable
        match = re.search(r'var datasource = ({.*?});', data, re.DOTALL)

        if match:
            datasource_str = match.group(1)
            datasource_str = datasource_str.replace("\'","\"")
        else:
            logging.error("Unable to find 'datasource' variable")
            raise requests.exceptions.MissingSchema
        # raw = datasource_str

        datasource_str = json.loads(datasource_str)
        
        return datasource_str,title
        
     
    def data_converter(self,datasource:dict[str,any],title):
        data_dict={}
        for i in datasource["sheets"][0]["tables"][0]["cells"]:
            if (i["rowCode"] == 16) and (i["columnCode"] == 17):
                # logging.("sum of sells in rials: ",i)
                try:
                    data_dict["ISP"]
                except KeyError:
                    data_dict["ISP"] = {"value" : i["value"], "row":i["rowSequence"], "column":i["columnSequence"]}
                
            if (i["rowCode"] == 5) and (i["columnCode"] == 15):
                # logging.("internal sell(count): ",i)
                try:
                    data_dict["ISA"]
                except KeyError:
                    data_dict["ISA"] = {"value" : i["value"], "row":i["rowSequence"], "column":i["columnSequence"]}
                
            if (i["rowCode"] == 4) and (i["columnCode"] == 2) and i["value"] != "":
                # logging.("vahed: ",i)

                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.vahed = pd.concat([self.vahed,s])


            if (i["rowCode"] == 4) and (i["columnCode"] == 14) and i["value"] != "":
                # logging.("kala: ",i)

                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.tolid = pd.concat([self.tolid,s])
            if (i["rowCode"] == 4) and (i["columnCode"] == 1) and i["value"] != "":
                # logging.("tedad tolid",i)

                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.name = pd.concat([self.name,s])
            if (i["rowCode"] == 4) and (i["columnCode"] == 15) and i["value"] != "":
                # logging.("tedad foroosh: ",i)
                # logging.(i)
                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.foroosh = pd.concat([self.foroosh,s])
            if (i["rowCode"] == 4) and (i["columnCode"] == 16) and i["value"] != "":
                # logging.("nerkh_foroosh: ",i)
                # logging.(i)
                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.nerkh_foroosh = pd.concat([self.nerkh_foroosh,s])
            if (i["rowCode"] == 4) and (i["columnCode"] == 17) and i["value"] != "":
                # logging.("nerkh_foroosh: ",i)
                # logging.(i)
                s = pd.Series([i["value"]],index=[i["rowSequence"]])
                self.mablagh_foroosh = pd.concat([self.mablagh_foroosh,s])
        
        data = pd.concat([self.vahed,self.name,self.tolid,self.foroosh,self.nerkh_foroosh,self.mablagh_foroosh],axis=1).dropna().rename(columns={0:"vahed",1:"esm",2:"tolid",3:"foroosh",4:"nerkh_foroosh",5:"mablagh_forosh"})
        periodEndToDate = datasource["periodEndToDate"].split("/")
        data["Year"] = periodEndToDate[0]
        data["Month"] = periodEndToDate[1]
        data["Day"] = periodEndToDate[2]
        data["nemad"] = title
        return data,data_dict

def download_link_as_json(update:bool=False):

    for file in Path("Data/links").glob("*.csv"):
        obj = Monthly_table()
        if file.name.split(".")[0].replace("ی","ي") in list(map(lambda p: p.parts[-1],Path("Data/raw_json").glob("**/**"))):
            logging.info(file.name.split(".")[0]," founded")
            update = True
        if update:
            try:
                TrackNoLst = list(map(lambda p: int(p.parts[-1].split("-")[-1]),(Path("Data/raw_json")/file.name.split(".")[0]).glob("*")))
            except Exception as e:
                logging.error("Something is wrong in updating raw json files", exc_info=True)
            logging.info(TrackNoLst)
            for _,row in pd.read_csv(file).sort_values(by="SentDateTime" ,ascending=False).iterrows(): 
                if not (row["TracingNo"] in TrackNoLst):
                    logging.info("Updating:",row["TracingNo"])
                    try:
                        datasource_str,title = obj.read_from_web(row["Url"])
                        periodEndToDate = datasource_str["periodEndToDate"].replace("/","-")
                        Path(f"Data/raw_json/{title}").mkdir(exist_ok=True,parents=True)
                        with open(raw_json_files_path/title/f"{title}-{periodEndToDate}-{datasource_str['tracingNo']}",'w+') as f:
                            json.dump(datasource_str,f,indent=6)
                            logging.info(title +"-"+periodEndToDate+" saved")
                    except Exception as e:
                        logging.error("Somthing is wrong 14",exc_info=True)
        else:
            for _,row in pd.read_csv(file).sort_values(by="SentDateTime").iterrows():
                logging.info(row["Url"])
                try:
                    datasource_str,title = obj.read_from_web(row["Url"])
                    periodEndToDate = datasource_str["periodEndToDate"].replace("/","-")
                    Path(f"Data/raw_json/{title}").mkdir(exist_ok=True,parents=True)
                    with open(raw_json_files_path/title/f"{title}-{periodEndToDate}-{datasource_str['tracingNo']}",'w+') as f:
                        json.dump(datasource_str,f,indent=6)
                        logging.info(title +"-"+periodEndToDate+" saved")
                except Exception as e:
                    logging.error("somthing is wrong 13",exc_info=True)



def transform_json_to_csv():
    for file in Path("Data/raw_json").glob("**/*"):
        if not file.is_file():
            continue
        with open(file,"r") as f:
            daatasource = json.load(f)
            try:
                obj = Monthly_table()
                df, _ = obj.data_converter(daatasource,file.parts[-2])
                total_data = pd.concat([total_data,df])
            except ValueError:
                logging.error(f"somthing is wrong with {file}",exc_info=True)
    total_data.to_csv("TotalData.csv")





download_link_as_json()