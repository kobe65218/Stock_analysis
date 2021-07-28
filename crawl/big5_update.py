import sys
sys.path.insert(0,"/opt/airflow/")
import time
import numpy as np
import pandas as pd
import requests
import random
import csv
import datetime
from datetime import timedelta
from sqlalchemy import create_engine , text ,MetaData

#%%

username = "root"
password = "kobe910018"
host = "mysql"
port = "3306"
database = "stock_analysis"
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}', echo=False)

#%%
now = datetime.date.today() + timedelta(days=1)
print("Current Time =", now)

def fetch_data (date_range):
    for date in date_range:
        url = requests.get(
            f"https://www.twse.com.tw/fund/T86?response=html&date={str(date).replace('-', '')}&selectType=ALL").text
        time.sleep(random.randint(1, 10))
        check = [i in url.split() for i in ["查詢日期大於可查詢最大日期，請重新查詢!", "很抱歉，沒有符合條件的資料!"]]
        if not True in check:
            try:
                df = pd.read_html(url)
                print(df)
            except:
                with open("crawl/log/big3_erro.csv", mode="a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([date])
                continue
            df2 = df[0]
            df2 = feature_change(df2, date)
            print(df2)
            df2.to_sql("big3", con=engine, if_exists="append")
            with open("crawl/log/big3_check.csv", mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["date"])
                writer.writerow([date])
            print(date)

def feature_change(df ,date):
    miss = ["自營商買賣超股數(自行買賣)", "自營商買賣超股數(避險)", "自營商買進股數(自行買賣)", "自營商買進股數(避險)", "自營商賣出股數(自行買賣)", "自營商賣出股數(避險)", "自營商買進股數",
            "自營商賣出股數", "外資自營商買賣超股數", "外資自營商買進股數", "外資自營商賣出股數", "外資買賣超股數", "外資買進股數", "外資賣出股數", "外陸資買進股數(不含外資自營商)",
            "外陸資賣出股數(不含外資自營商)", "外陸資買賣超股數(不含外資自營商)", "自營商買進股數(自行買賣)", "自營商賣出股數(自行買賣)", "自營商買賣超股數(自行買賣)", "自營商買進股數(避險)",
            "自營商賣出股數(避險)", "自營商買賣超股數(避險)"]
    df.columns = df.columns.get_level_values(1)
    # df.drop(0,axis=0 , inplace=True)
    df["date"] = date
    for m in miss:
        if m not in df.columns:
            df[m] = np.nan
    df["外資買進股數"] = df["外資買進股數"].fillna(df["外資自營商買進股數"] + df["外陸資買進股數(不含外資自營商)"])
    df["外資賣出股數"] = df["外資賣出股數"].fillna(df["外資自營商賣出股數"] + df["外陸資賣出股數(不含外資自營商)"])
    df["外資買賣超股數"] = df["外資賣出股數"].fillna(df["外資自營商買賣超股數"] + df["外陸資買賣超股數(不含外資自營商)"])
    df["自營商買進股數"] = df["自營商買進股數"].fillna(df["自營商買進股數(避險)"] + df["自營商買進股數(自行買賣)"])
    df["自營商賣出股數"] = df["自營商賣出股數"].fillna(df["自營商賣出股數(避險)"] + df["自營商賣出股數(自行買賣)"])
    df["stock_id"] = df["證券代號"]
    df.drop("證券代號",axis= 1,inplace=True)
    df.sort_index(axis=1, inplace=True)
    return df

def run_crawl(update=True ,start = "2012-05-02" ):
    if update :
        read_log = pd.read_csv("crawl/log/big3_check.csv")
        start = np.array(read_log.iloc[-1, 0], dtype='M8[D]') + 1
        print("start : ", start)
        date_range = np.arange(start, now, dtype='M8[D]')
        busy_date = np.is_busday(date_range, weekmask='Sun Sat')
        date_range = date_range[~busy_date]
        fetch_data(date_range)
    else :
        date_range = np.arange(start, now, dtype='M8[D]')
        busy_date = np.is_busday(date_range, weekmask='Sun Sat')
        date_range = date_range[~busy_date]
        fetch_data(date_range)

if __name__ == "__main__":
    run_crawl(update =True)


