from flask import Flask , url_for , render_template , request
from flask_sqlalchemy import  SQLAlchemy
import pandas as pd
import yfinance as yf
import json
# from db.test import TableBig3 ,db
from sqlalchemy import func
from sqlalchemy.sql.expression import cast
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:kobe910018@192.168.31.20:3306/stock_analysis"
db = SQLAlchemy(app)
# 三大法人Table
class TableBig3(db.Model):
    __tablename__ = 'big3'
    __table_args__ = {
        'autoload': True,
        'schema': 'stock_analysis',
        'autoload_with': db.engine
    }
    def get_dict(self):
        columns = self.__dict__.keys()
        return { str(col) : getattr(self, col) for col in list(columns)[1:]}


# 異常偵測 Table
class TablePredict(db.Model):
    __tablename__ = 'predict'
    __table_args__ = {
        'autoload': True,
        'schema': 'stock_analysis',
        'autoload_with': db.engine
    }
    def get_dict(self):
        columns = self.__dict__.keys()
        return { str(col) : getattr(self, col) for col in list(columns)[1:]}


def fetch_data(table , stock_id , start_date , end_date):
    Table_data = db.session.query(table).filter(table.stock_id == stock_id , table.date.between(start_date, end_date) ).all()
    Table_datas = []
    for data in Table_data:
        Table_datas.append(data.get_dict())
    df = pd.DataFrame(Table_datas)
    df = df.astype(str)
    df.replace("0E-10", 0, inplace=True)
    df.index = df["date"]
    df.drop(["date"], axis=1, inplace=True)
    return  df


# 三大法人異常網站
@app.route("/")
def stock():
    # 起始日
    start = request.values.get("start")

    # 結束日
    end = request.values.get("end")

    # 股票代號
    stock_id = request.values.get("stock_id")

    # 設定預設值
    if start == None :
        start = "2021-04-20"
        end = "2021-07-20"
    if stock_id == None :
       stock_id = "2330"

    # 透過api獲取股價資料
    stock = yf.Ticker(f'{stock_id}.TW')
    stock_price = stock.history(start=start , end = end)
    stock_price = pd.DataFrame(stock_price.values, index=stock_price.index.astype(str).format(),
                               columns=stock_price.columns)

    # 從資料庫獲取異常偵測結果
    anomaly_table = fetch_data(TablePredict, stock_id ,start , end)

    # 合併資料
    merge_df = pd.concat([stock_price,anomaly_table], join="inner", axis=1)
    merge_df.index = merge_df.index.astype(str).format()


    # 計算報酬
    merge_df["Close_log"] = merge_df["Close"].shift(1)
    merge_df["Close_log"] = (merge_df["Close_log"] - merge_df["Close"]) / merge_df["Close"]

    return render_template("index.html", data =json.dumps(merge_df.to_dict()) ,start =start , end = end , stock_id = stock_id)

# 建立訓練模型時的api
@app.route('/branchApi/<stock_id>')
def branchData(stock_id):
    # 從資料庫取得三大法人資訊
    Table_data = db.session.query(TableBig3).filter(TableBig3.stock_id == stock_id).all()
    Table_datas = []
    for data in Table_data:
        Table_datas.append(data.get_dict())

    # 資料處理
    df = pd.DataFrame(Table_datas)
    df = df.astype(str)
    df.replace("0E-10", 0, inplace=True)
    df.index = df["date"]
    df.drop(["date","index"], axis=1, inplace=True)
    df.index = df.index.astype(str).format()
    return df.to_dict()

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")


