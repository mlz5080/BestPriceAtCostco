import mysql.connector
import os
from .BussImpl import CostcoItem

class MySQLCostcoItem(CostcoItem):
    
    db_name = "bestpriceatcostco"
    costco_db_table_name = "costcoonlineproducts"

    def __init__(self, item_id, name, price, price_range, is_on_sale, product_link, image_link, category):
        super().__init__(item_id, name, price, price_range, is_on_sale, product_link, image_link, category)
        self.db = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PW'],
            host="localhost",
            database=MySQLCostcoItem.db_name,
        )
        self.db.close()

    def remove_item(self):
        self.db.reconnect()
        cursor = self.db.cursor()
        query = "DELETE FROM costcoonlineproducts where product_id = '{}'".format(self.id)
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        self.db.close()

    def update_item(self):
        self.db.reconnect()
        cursor = self.db.cursor()
        query = "SELECT * FROM costcoonlineproducts where product_id = '{}'".format(self.id)
        cursor.execute(query)
        cfg = cursor.fetchone()
        cursor.close()

        cursor = self.db.cursor()
        if not cfg:
            print("Creating new product", self.name)
            self.insert_mysql_item(cursor)
        else:
            if self.need_update(cfg):
                print("Updating other info", self.name)
                self.update_mysql_basic_info(cursor)
                print("Update complete for", self.name)
            elif cfg[5] > float(self.price):
                print("Updating minimum price", self.name)
                self.update_mysql_min_price(cursor)
                print("Update min price complete for", self.name)
        self.db.commit()
        cursor.close()
        self.db.close()

    def need_update(self, cfg):
        need_update = cfg[1] != self.link
        need_update |= cfg[2] != self.is_on_sale
        need_update |= cfg[3] != self.name
        need_update |= cfg[4] != self.image_link
        need_update |= float(cfg[6]) != float(self.price)
        if cfg[7] and self.price_range:
            need_update |= float(cfg[7]) != float(self.price_range)
        elif not cfg[7] and self.price_range:
            need_update = True
        need_update |= cfg[8] != self.category
        return need_update

    def insert_mysql_item(self, cursor):
        cursor.execute(
            "INSERT INTO costcoonlineproducts "
                "(product_id,"
                "product_link,"
                "product_is_on_sale,"
                "product_name,"
                "product_image_link,"
                "product_history_minimum_price,"
                "product_current_price,"
                "product_current_price_range,"
                "product_category)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                self.id,
                self.link,
                self.is_on_sale,
                self.name,
                self.image_link,
                self.price,
                self.price,
                self.price_range,
                self.category
            ),
        )

    def update_mysql_min_price(self, cursor):
        cursor.execute(
            "UPDATE costcoonlineproducts "
            "SET product_history_minimum_price = %s"
            "WHERE product_id = %s",
            (
                self.price,
                self.id
            ),
        )

    def update_mysql_basic_info(self, cursor):
        sql = """
            UPDATE costcoonlineproducts
                SET product_link = %s,
                    product_is_on_sale = %s,
                    product_name = %s,
                    product_image_link = %s,
                    product_current_price = %s,
                    product_current_price_range = %s,
                    product_category = %s
            WHERE product_id = %s
            """
        cursor.execute(
            sql,
            (
                self.link,
                self.is_on_sale,
                self.name,
                self.image_link,
                self.price,
                self.price_range,
                self.category,
                self.id
            ),
        )