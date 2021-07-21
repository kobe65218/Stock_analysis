from flask import Flask , url_for , render_template , request
import pandas as pd
import yfinance as yf
from db.Mysql import  Mysql
from db.Mogodb import Mongodb
import json


app =Flask("__name__")


@app.route('/')
def index():
    start = request.values.get("start")
    end = request.values.get("end")
    stock = yf.Ticker('2330.TW')
    stock_price = stock.history(start=start , end = end)
    stock_price = pd.DataFrame(stock_price.values,index=stock_price.index.astype(str).format() , columns=stock_price.columns )
    mysql = Mysql()
    annony = mysql.Merge()
    merge_df = pd.concat([stock_price,annony], join="inner", axis=1)
    merge_df.index = merge_df.index.astype(str).format() #31344


    return render_template("startbootstrap-sb-admin-2-gh-pages/index.html" ,data =json.dumps(merge_df.to_dict()))

@app.route('/branchApi')
def branchData():
    stock = yf.Ticker('2330.TW')
    stock_price = stock.history(period="max")
    mogodb = Mongodb()
    mysql = Mysql()
    branch_data = mogodb.Table_Branch()
    big3 = mysql.Table_big3()
    merge_df = pd.concat([stock_price,branch_data,big3], join="inner", axis=1)
    merge_df.index = merge_df.index.astype(str).format() #31344
    return merge_df.to_dict()

@app.route('/<data>')
def hello(data):
    print(data)
    return render_template("startbootstrap-sb-admin-2-gh-pages/"+data)


if __name__ == '__main__':
    app.run(debug=True)


