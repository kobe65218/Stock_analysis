import pandas as pd
import numpy as np
import os
from  sklearn.ensemble import IsolationForest
import requests
import json


## 透過API讀取資料庫爬取的資料
df = requests.get("http://127.0.0.1:5000/branchApi")
print(df)
#%%
data = pd.DataFrame(json.loads(df.text))



## DROP掉股價資訊保留三大法人及分點進出資料
data["Close_log"] = data["Close"].shift(1)
data["Close_log"] = (data["Close_log"] - data["Close"])/data["Close"]
dd = data[["Open","High","Low","Close","Volume","Dividends","Stock Splits","stock_id","Close_log"]]
data.drop(["Open","High","Low","Close","Volume","Dividends","Stock Splits","stock_id","Close_log"],axis=1, inplace=True)
data.fillna(0,inplace=True)

## 測試三種異常
"""
1. 三大法人(bid3_data)
2. 分點進出(branch_data)
3. 三大法人+分點進出(data)
"""

big3_data = data[['三大法人買賣超股數', '外資自營商買賣超股數', '外資自營商買進股數', '外資自營商賣出股數',
       '外資買賣超股數', '外資買進股數', '外資賣出股數', '外陸資買賣超股數(不含外資自營商)', '外陸資買進股數(不含外資自營商)',
       '外陸資賣出股數(不含外資自營商)', '投信買賣超股數', '投信買進股數', '投信賣出股數', '自營商買賣超股數',
       '自營商買賣超股數(自行買賣)', '自營商買賣超股數(避險)', '自營商買進股數', '自營商買進股數(自行買賣)',
       '自營商買進股數(避險)', '自營商賣出股數', '自營商賣出股數(自行買賣)', '自營商賣出股數(避險)']]

branch_data = data.drop(['三大法人買賣超股數', '外資自營商買賣超股數', '外資自營商買進股數', '外資自營商賣出股數',
       '外資買賣超股數', '外資買進股數', '外資賣出股數', '外陸資買賣超股數(不含外資自營商)', '外陸資買進股數(不含外資自營商)',
       '外陸資賣出股數(不含外資自營商)', '投信買賣超股數', '投信買進股數', '投信賣出股數', '自營商買賣超股數',
       '自營商買賣超股數(自行買賣)', '自營商買賣超股數(避險)', '自營商買進股數', '自營商買進股數(自行買賣)',
       '自營商買進股數(避險)', '自營商賣出股數', '自營商賣出股數(自行買賣)', '自營商賣出股數(避險)'],axis = 1)


model_big_3 = IsolationForest(contamination= 0.2 , max_samples="auto",
                        max_features=len(big3_data.columns),n_estimators=1000,
                        n_jobs=-1,bootstrap=False
                        )

#%%

pred_big_3  = model_big_3.fit_predict(big3_data)
data = pd.DataFrame(pred_big_3  ,index=dd["stock_id"] , columns=["annomy"])
data["annomy"] = data["annomy"].replace({1:0, -1:1})
data["date"] = dd.index
print(data)

#%%
from sqlalchemy import create_engine , Table , MetaData
from sqlalchemy.types import VARCHAR, Date , INTEGER
mysql = create_engine("mysql+pymysql://root:kobe910018@192.168.31.20:3306/stock_analysis")
data.to_sql("predict" , mysql ,if_exists='replace', index_label='stock_id',
         dtype={'stock_id':VARCHAR(10) , "date" : Date , "annomy" :INTEGER })

# metadata = MetaData(bind=mysql)
# pred = Table("pred" ,)
