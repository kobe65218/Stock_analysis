from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import  SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:kobe910018@mysql:3306/stock_analysis"
db = SQLAlchemy(app)
from stock_dashboard import route
