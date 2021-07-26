import pandas as pd
import numpy as np
import os
from  sklearn.ensemble import IsolationForest
import requests
import json
import pickle
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine , Table , MetaData , Column
from sqlalchemy.types import VARCHAR, Date , INTEGER
import pymongo

# stock_id = pd.read_csv("/home/kobe/PycharmProjects/flaskProject/data/stock_id.csv")
# print(stock_id)


stock_ids = ["2330" ,"2603","2609","3481","2303","2409","2317","2002"]



for stock_id in stock_ids:
    ## 透過API讀取資料庫爬取的資料
    df = requests.get(f"http://127.0.0.1:5000/branchApi/{stock_id}")
    data_from_api = pd.DataFrame(json.loads(df.text))
    print(data_from_api)
    data_from_api.drop(["stock_id", "證券名稱"],
              axis=1, inplace=True)
    data_from_api.replace("None" , np.nan ,inplace=True)
    data_from_api.dropna(inplace=True)



    big3_data = data_from_api[["外資買進股數", "外資賣出股數", "投信買進股數", "投信賣出股數", "自營商買進股數", "自營商賣出股數"]]
    big3_data = big3_data.astype(float)
    # 訓練模型
    model_big_3 = IsolationForest(contamination=0.1, max_samples="auto",
                                  max_features=len(big3_data.columns), n_estimators=1000,
                                  n_jobs=-1, bootstrap=False
                                  )
    pred_big_3 = model_big_3.fit_predict(big3_data)


    # 將預測結果存入資料庫
    data = pd.DataFrame(pred_big_3, columns=["annomy"])
    data["annomy"] = data["annomy"].replace({1: 0, -1: 1})
    data["date"] = data_from_api.index
    data["stock_id"] = stock_id
    save_to_db = data.to_numpy()

    Base = declarative_base()


    class annomy(Base):
        __tablename__ = 'predict'
        stock_id = Column(VARCHAR(10), primary_key=True)
        annomy = Column(INTEGER)
        date = Column(Date, primary_key=True)


    engine = create_engine("mysql+pymysql://root:kobe910018@192.168.31.20:3306/stock_analysis")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    with session:
        for data in save_to_db:
            need_to_save = annomy(annomy=data[0], date=data[1], stock_id=data[2])
            session.add(need_to_save)
        session.commit()


    # 將模型存入mongodb
    def save_to_mongodb(model, client, db, coll, stock_id):
        need_save_model = pickle.dumps(model)
        client = pymongo.MongoClient(client)
        database = client[db]
        collect = database[coll]
        collect.insert_one({"stock_id": stock_id, "model": need_save_model})


    save_to_mongodb(model_big_3, "mongodb://kobe:kobe910018@localhost:27017/", "stock_analysis", "model", stock_id)













