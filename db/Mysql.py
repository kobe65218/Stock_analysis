from sqlalchemy import create_engine , Table , MetaData
import pandas as pd
import numpy as np


class Mysql(object):
    def __init__(self):
        self.mysql = create_engine("mysql+pymysql://root:kobe910018@192.168.31.20:3306/stock_analysis")
        self.metadata = MetaData(bind=self.mysql)

    def Table_big3(self):
        big = Table("big3", self.metadata, autoload_with=self.mysql)
        big3 = big.select().where(big.c.證券代號 == "2330")
        data = self.mysql.execute(big3)
        df = pd.DataFrame(data.all(), columns=big3.columns.keys())
        df.set_index(df.date, inplace=True)
        df.drop("date", axis=1, inplace=True)
        df.drop("index", axis=1, inplace=True)
        df.drop("證券代號", axis=1, inplace=True)
        df.drop("證券名稱", axis=1, inplace=True)
        df.fillna(np.nan, inplace=True)
        df = df.astype(float)
        return df

    def Merge(self):
        annony = Table("predict" ,self.metadata, autoload_with=self.mysql)
        annony = annony.select().where(annony.c.stock_id == "2330")
        data = self.mysql.execute(annony)
        df = pd.DataFrame(data.all(), columns=annony.columns.keys())
        df.index = df["date"].astype(str)
        df.drop(["date","stock_id"] , axis=1 , inplace=True)

        return df










