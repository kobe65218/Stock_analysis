import datetime

from stock_dashboard import app , db
from flask import render_template , request
import pandas as pd
import yfinance as yf
import json
from stock_dashboard.database import TablePredict , TableBig3 , fetch_data

# 三大法人異常網站
@app.route("/")
def stock():
    # 起始日
    start = request.values.get("start")

    # 結束日
    end = request.values.get("end")

    # 股票代號
    stock_id = request.values.get("stock_id")

    #
    date_after = request.values.get('date_after')

    # 設定預設值
    if start == None :
        start = "2020-04-20"
        end = datetime.date.today() + datetime.timedelta(1)
    if stock_id == None :
       stock_id = "2330"

    if date_after == None:
        date_after = 5

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

    return render_template("stock_html/bar_chart.html", data =json.dumps(merge_df.to_dict()), start =start, end = end, stock_id = stock_id , date_after = date_after )

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


# 自動更新時的api
@app.route('/update/stock_id=<stock_id>&start=<start>&end=<end>')
def update(stock_id ,start ,end):
    # 從資料庫取得三大法人資訊
    Table_data = db.session.query(TableBig3).filter(TableBig3.stock_id == stock_id , TableBig3.date.between(start,end)).all()
    if Table_data == []:
        return "None"
    else:
        Table_datas = []
        for data in Table_data:
            Table_datas.append(data.get_dict())

        print(start)
        print(end)

        # 資料處理
        df = pd.DataFrame(Table_datas)
        df = df.astype(str)
        df.replace("0E-10", 0, inplace=True)
        df.index = df["date"]
        df.drop(["date", "index"], axis=1, inplace=True)
        df.index = df.index.astype(str).format()
        return df.to_dict()

