import sys
sys.path.insert(0,"/opt/airflow/")
import pymongo
import pickle
import requests
import json
import pandas as pd
import numpy as np
import  datetime
from stock_dashboard.database import TablePredict
from stock_dashboard import db
client = "mongodb://kobe:kobe910018@mongodb:27017/"
conn = pymongo.MongoClient(client)
# 從mongodb 讀取模型
def load_model_dd(db ,coll,stock_id):
    database = conn[db]
    collect = database[coll]
    model_json = collect.find_one({"stock_id":stock_id })

    return pickle.loads(model_json["model"])

# 將更新的時間存入
def save_time_to_mongodb( db, coll, time , stock_id):
    database = conn[db]
    collect = database[coll]
    collect.create_index("stock_id",unique=True)
    collect.insert_one({"update_time": time , "stock_id":stock_id})

# 將更新的時間更新
def update_time_to_mongodb(db, coll, time , stock_id):
    database = conn[db]
    collect = database[coll]
    collect.update_many({"stock_id":stock_id} , {"$set":{"update_time": time}})


# 讀取上次更新的時間
def load_update_time(db ,coll ,stock_id):
    database = conn[db]
    collect = database[coll]
    time = collect.find_one({"stock_id":stock_id})
    return time["update_time"]

stock_id_list =  ["2330" ,"2603","2609","3481","2303","2409","2317","2002"]

def update_model_predict(stock_id):
    # 讀取模型
    model = load_model_dd("stock_analysis", "model", stock_id)

    # save_time_to_mongodb("mongodb://kobe:kobe910018@localhost:27017/"  , "test" , "time" ,"2021-07-24" , "2330")

    # 讀取上次更新的時間
    update_time_plus = datetime.datetime.strptime(load_update_time("stock_analysis", "time", stock_id),
                                                  "%Y-%m-%d") + datetime.timedelta(1)

    last_update_time = update_time_plus.date()

    # 現在時間
    current_time = datetime.date.today()

    # 從api讀取預更新模型預測的變數(從現在到上次更新的期間資料)
    predict_data = requests.get(
        f"http://192.168.31.20:5000/update/stock_id={stock_id}&start={last_update_time}&end={current_time}")
    print(predict_data)

    # 如果沒有資料為休市日則break
    if predict_data.text == "None":
        # 更新上次更新時間
        print(predict_data.text)
        update_time_to_mongodb("stock_analysis", "time", str(current_time), stock_id)
    else:
        predict_data = json.loads(predict_data.text)

        predict_data = pd.DataFrame(predict_data)
        predict_data = predict_data[["外資買進股數", "外資賣出股數", "投信買進股數", "投信賣出股數", "自營商買進股數", "自營商賣出股數"]]

        # 預測
        predict = model.predict(predict_data)

        # date_range = np.arange(last_update_time , current_time , dtype= "datetime64[D]")
        data_to_upgrde = pd.DataFrame({"predict": predict, "date": predict_data.index})
        data_to_upgrde = data_to_upgrde.replace({-1: 1, 1: 0})
        print(data_to_upgrde)

        # 新的預測結果寫入資料庫
        for data in data_to_upgrde.to_numpy():
            print(data)
            update_data = TablePredict(stock_id=stock_id, annomy=data[0], date=data[1])
            db.session.add(update_data)
        db.session.commit()

        # 更新上次更新時間
        update_time_to_mongodb("stock_analysis", "time", str(current_time), stock_id)

def run_predcit(stock_id_list =stock_id_list):
    for stock_id in stock_id_list:
        update_model_predict(stock_id)

if __name__ == "__main__":
    # run_predcit(stock_id_list)
    for  i in stock_id_list:
        save_time_to_mongodb("stock_analysis","time","2021-07-22" ,i)
















