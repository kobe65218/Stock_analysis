
import pymongo
import pickle


# 從mongodb 讀取模型
def load_model_dd(client,db ,coll,stock_id):
    client = pymongo.MongoClient(client)
    database = client[db]
    collect = database[coll]
    model_json = collect.find_one({"stock_id":stock_id })
    print(model_json)
    return pickle.loads(model_json["model"])


model = load_model_dd( "mongodb://kobe:kobe910018@localhost:27017/" ,"test" , "test","2330")