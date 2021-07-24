from stock_dashboard import db
import pandas as pd

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
