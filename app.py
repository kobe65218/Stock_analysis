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
#
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

# @app.route("/")
# def test():
#     Table_data = db.session.query(TableBig3).filter(TableBig3.證券代號 == "2330").all()
#     Table_datas = []
#     for data in Table_data:
#         Table_datas.append(data.get_list())
#     df = pd.DataFrame(Table_datas)
#     print(df)
#     df = df.astype(str )
#     df.replace("0E-10",0,inplace=True)
#     df.index = df["date"]
#     df.drop(["date","index"],axis=1 ,inplace=True)
#     return df.to_dict()
# #


@app.route("/")
def index():
    start = request.values.get("start")
    end = request.values.get("end")
    stock_id = request.values.get("stock_id")
    print(stock_id)
    if start == None :
        start = "2021-04-20"
        end = "2021-07-20"
    if stock_id == None :
       stock_id = "2330"

    stock = yf.Ticker(f'{stock_id}.TW')
    stock_price = stock.history(start=start , end = end)
    stock_price = pd.DataFrame(stock_price.values, index=stock_price.index.astype(str).format(),
                               columns=stock_price.columns)

    anomaly_table = fetch_data(TablePredict, stock_id ,start , end)


    merge_df = pd.concat([stock_price,anomaly_table], join="inner", axis=1)
    merge_df.index = merge_df.index.astype(str).format()
    print(merge_df)
    return render_template("index.html", data =json.dumps(merge_df.to_dict()) ,start =start , end = end , stock_id = stock_id)


@app.route('/branchApi/<stock_id>')
def branchData(stock_id):
    Table_data = db.session.query(TableBig3).filter(TableBig3.stock_id == stock_id).all()
    Table_datas = []
    for data in Table_data:
        Table_datas.append(data.get_dict())
    df = pd.DataFrame(Table_datas)
    df = df.astype(str)
    df.replace("0E-10", 0, inplace=True)
    df.index = df["date"]
    df.drop(["date","index"], axis=1, inplace=True)
    print(df)
    # merge_df = pd.concat([stock_price,df], join="inner", axis=1)
    df.index = df.index.astype(str).format()
    return df.to_dict()


# @app.route("/test")
# def test2():
#     Table_data = db.session.query(TablePredict).filter(TablePredict.stock_id == "2330").all()
#     Table_datas = []
#     for data in Table_data:
#         Table_datas.append(data.get_list())
#     df = pd.DataFrame(Table_datas)
#     print(df)
#     df = df.astype(str)
#     df.replace("0E-10", 0, inplace=True)
#     df.index = df["date"]
#     df.drop(["date"], axis=1, inplace=True)
#     return df.to_dict()
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")


