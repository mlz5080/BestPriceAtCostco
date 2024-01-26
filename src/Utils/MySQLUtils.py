import mysql.connector
import os 

class MySQLUtils:

    def __init__(self, mysql, table_name):
        self.mysql = mysql
        self.table_name = table_name

    def get_costco_online_categories_on_sale(self):
        cursor = self.mysql.get_db().cursor()
        query = "SELECT distinct(product_category) FROM {} where product_is_on_sale=1".format(self.table_name)
        cursor.execute(query)
        cfgs = cursor.fetchall()
        return cfgs

    def get_costco_online_on_sale(self):
        cursor = self.mysql.get_db().cursor()
        query = """select * from {}
        where product_category like 'Offers Ending Sunday' or product_is_on_sale=1
        order by product_current_price;
        """.format(self.table_name)
        cursor.execute(query)
        cfgs = cursor.fetchall()
        return cfgs

    def get_costco_online_item_by_id(self, column, product_id):
        cursor = self.mysql.get_db().cursor()
        query = "SELECT * FROM {} where {} = '{}'".format(self.table_name, column, product_id)
        cursor.execute(query)
        cfg = cursor.fetchone()
        return cfg
