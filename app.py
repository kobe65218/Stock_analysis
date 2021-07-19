from flask import Flask , url_for , render_template
import pandas as pd
import yfinance as yf
from db.Mysql import  Mysql
from db.Mogodb import Mongodb
import json


app =Flask("__name__")


@app.route('/')
def hello_world():
    # stock = yf.Ticker('2330.TW')
    # stock_price = stock.history(period='max')
    # print(stock_price)
    mogodb = Mongodb()
    # mysql = Mysql()
    branch_data = mogodb.Table_Branch()
    # big3 = mysql.Table_big3()
    # print(mogodb.Table_Branch())

    merge_df = pd.concat([branch_data], join="inner", axis=1)
    merge_df.index = merge_df.index.astype(str).format() #fefgetge


    return render_template("startbootstrap-sb-admin-2-gh-pages/index.html" ,data =json.dumps(merge_df.to_dict()))


if __name__ == '__main__':
    app.run(debug=True)


