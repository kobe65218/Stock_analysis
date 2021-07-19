from pymongo import MongoClient
import pandas as pd

class Mongodb(object):
    def __init__(self):
        self.mongo = MongoClient("mongodb://kobe:kobe910018@localhost:27017/")


    def Table_Branch(self):
        db = self.mongo["stock"]
        branch_data = db.branch_buy_sell.find({"stock_id": "2330"})
        # data2 = mongo.db.branch_buy_sell.find({"stock_id" : 2330})
        branch_data = [i for i in branch_data]
        branch_data = pd.DataFrame(branch_data)
        branch_data.drop("_id", axis=1, inplace=True)
        branch_data.index = branch_data["time"]
        branch_data.drop(["time"], axis= 1 , inplace=True)
        return branch_data