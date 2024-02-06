import mysql.connector
import os
from .BussImpl import CostcoItem


class MySQLCostcoItem(CostcoItem):

    # db_name = "bestpriceatcostco"
    # costco_db_table_name = "costcoonlineproducts_beta"

    def __init__(
            self,
            item_id,
            name,
            price,
            price_range,
            is_on_sale,
            product_link,
            image_link,
            category,
            db_name,
            table_name,
            user,
            pw,
            host):
        super().__init__(
            item_id,
            name,
            price,
            price_range,
            is_on_sale,
            product_link,
            image_link,
            category)
        self.costco_db_table_name = table_name
        self.db_name = db_name
        self.db = mysql.connector.connect(
            user=user,
            password=pw,
            host=host,
            database=self.db_name,
        )
        self.db.close()
        self.is_on_sale = '1' if self.is_on_sale else '0'

    def remove_item(self):
        self.db.reconnect()
        cursor = self.db.cursor()
        query = "DELETE FROM {} where product_id = '{}'".format(
            self.costco_db_table_name, self.id)
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        self.db.close()

    def update_item(self):
        self.db.reconnect()
        cursor = self.db.cursor()
        query = "SELECT * FROM {} where product_id = '{}'".format(
            self.costco_db_table_name, self.id)
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
            if cfg[5] > float(self.price):
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
        need_update |= float(cfg[7]) != float(self.price_range)
        need_update |= cfg[8] != self.category
        return need_update

    def insert_mysql_item(self, cursor):
        cursor.execute(
            """INSERT INTO {}
                (product_id,
                product_link,
                product_is_on_sale,
                product_name,
                product_image_link,
                product_history_minimum_price,
                product_current_price,
                product_current_price_range,
                product_category)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """.format(self.costco_db_table_name),
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
            """UPDATE {}
            SET product_history_minimum_price = %s
            WHERE product_id = %s""".format(self.costco_db_table_name),
            (
                self.price,
                self.id
            ),
        )

    def update_mysql_basic_info(self, cursor):
        sql = """
            UPDATE {}
                SET product_link = %s,
                    product_is_on_sale = %s,
                    product_name = %s,
                    product_image_link = %s,
                    product_current_price = %s,
                    product_current_price_range = %s,
                    product_category = %s
            WHERE product_id = %s
            """.format(self.costco_db_table_name)
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
