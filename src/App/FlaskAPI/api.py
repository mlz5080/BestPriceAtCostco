from flask import Flask
import os
import json
from DataTypes.BussImpl import DisplayItem
from Utils.MySQLUtils import MySQLUtils
# from flask_cors import CORS  # comment this on deployment
from flaskext.mysql import MySQL
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# CORS(app)  # comment this on deployment

db_name = "bestpriceatcostco"
costco_db_table_name = "costcoonlineproducts_beta"

mysql = MySQL(
    app,
    host='localhost',
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PW'],
    db=db_name,
    autocommit=True)


@app.route('/test')
def test():
    return "test success"


@app.route('/')
def index():
    return {}


@app.route('/api/product_id/<product_id>')
def get_single_item(product_id):
    mysql_dao = MySQLUtils(mysql, costco_db_table_name)
    cfg = mysql_dao.get_costco_online_item_by_id("product_id", product_id)
    if not cfg:
        return {}
    item = [str(c) for c in cfg]
    obj = DisplayItem(*item)
    return json.dumps(obj.obj_dict())


@app.route('/api/on_sale/random')
def get_random_on_sales():
    mysql_dao = MySQLUtils(mysql, costco_db_table_name)
    cfgs = mysql_dao.get_costco_online_random_on_sale()
    res = {}
    if cfgs:
        items = [
            DisplayItem(*[str(c) for c in cfg]).obj_dict() for cfg in cfgs]
        res = json.dumps(items)
    return res


@app.route('/api/on_sale/all')
def get_all_on_sales():
    mysql_dao = MySQLUtils(mysql, costco_db_table_name)
    cfgs = mysql_dao.get_costco_online_on_sale()
    res = {}
    if cfgs:
        items = [
            DisplayItem(*[str(c) for c in cfg]).obj_dict() for cfg in cfgs]
        res = json.dumps(items)
    return res


@app.route('/api/on_sale/categories')
def get_on_sales_categories():
    mysql_dao = MySQLUtils(mysql, costco_db_table_name)
    cfgs = mysql_dao.get_costco_online_categories_on_sale()
    res = {}
    if cfgs:
        items = [str(cfg[0]) for cfg in cfgs]
        res = json.dumps(items)
    return res
