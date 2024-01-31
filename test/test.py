from src.DataTypes.Dynamo import DynamoCostcoItem
from src.DataTypes.MySQL import MySQLCostcoItem
from src.DataTypes.BussImpl import CostcoItem
import mysql.connector
import threading
import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import pytest

threadLocal = threading.local()


def get_driver():
    driver = getattr(threadLocal, 'driver', None)
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36" # noqa
    if driver is None:
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('user-agent={0}'.format(user_agent))
        chromeOptions.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=chromeOptions)
        setattr(threadLocal, 'driver', driver)
    return driver


def retrive_product_info(div, sauce):
    product_price_str = div.string
    # item_id, name, price, price_range, hmp, is_on_sale, link
    price_range = "-1"
    if not product_price_str:
        product_price, price_range = div.contents[0].strip(
        ), div.contents[-1].strip()
        thousand_price_list = re.findall(r'\d+\,\d+\.\d+', price_range)
        price_range = thousand_price_list[0].replace(
            ",", "") if thousand_price_list else re.findall(
            r'\d+.\d+', price_range)[0]
    else:
        product_price = div.string.strip()
    thousand_price_list = re.findall(r'\d+\,\d+\.\d+', product_price)
    product_price = thousand_price_list[0].replace(
        ",", "") if thousand_price_list else re.findall(
        r'\d+.\d+', product_price)[0]

    item_id = re.findall(r'\d+', div.get("id").strip())[0]
    div_parent = div.find_parent()
    span = div_parent.find_next_sibling("span")
    is_on_sale = False
    if div_parent.find_next_sibling("p") and div_parent.find_next_sibling(
            "p").has_attr("automation-id"):
        is_on_sale = "instantSavings" in div_parent.find_next_sibling(
            "p").get("automation-id")
    sub_a = span.find("a")
    product_name = sub_a.string.strip()
    product_link = sub_a.get('href')
    cat = sauce.find(
        "script",
        string=lambda val:
            val is not None and "categoryName" in val).text.strip()
    cat = re.findall(r"categoryName\: '(\w+.*)'", cat)[0]
    image_tag = sauce.find(
        "img", alt=lambda val: val is not None and product_name in val)
    if image_tag and image_tag.get("src"):
        image_link = image_tag.get("src")
    else:
        image_link = image_tag.get("data-src")
    obj = CostcoItem(
        item_id,
        product_name,
        product_price,
        price_range,
        is_on_sale,
        product_link,
        image_link,
        cat)

    print(obj)


def get_costco_product(url):
    print("#" * 10, url, "#" * 10)
    driver = get_driver()
    has_next_page = True
    page = 1
    driver.get(url)

    sauce = BeautifulSoup(driver.page_source, "lxml")
    print(sauce)
    product_div_parent = sauce.find(
        "div", attrs={"automation-id": "productList"})
    # print(sauce)
    product_div_list = product_div_parent.find_all(
        "div", class_=lambda val:
            val is not None and "product" in val and "col-xs" in val)
    for pd in product_div_list:
        price_div = pd.find(
            "div", id=lambda val: val is not None and "price" in val)
        retrive_product_info(price_div, pd)
    has_next_page = sauce.find("li", class_="forward") is not None
    page = page + 1 if has_next_page else page
    assert True


def search_mysql_item(product_id):
    db = mysql.connector.connect(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PW'],
        host="localhost",
        database=MySQLCostcoItem.db_name,
    )
    cursor = db.cursor()
    query = "SELECT * FROM costcoonlineproducts_beta"
    query += " where product_id = '{}'".format(product_id)
    cursor.execute(query)
    cfg = cursor.fetchone()
    return cfg


@pytest.mark.dynamo
def test_dynamo_update():
    product_id = "test_insert1"
    obj1 = DynamoCostcoItem(
        product_id,
        "test",
        "8.99",
        "-1",
        True,
        ".com",
        "image.com",
        "test_category")
    obj1.update_item()
    resp = obj1.delete_item()
    assert resp["ResponseMetadata"]['HTTPStatusCode'] == 200


def test_mysql_insert():
    product_id = "test_insert1"
    obj1 = MySQLCostcoItem(
        product_id,
        "test",
        "8.99",
        "-1",
        True,
        ".com",
        "image.com",
        "test_category")
    try:
        obj1.update_item()
        item = search_mysql_item(product_id)
        if item:
            print(item)
        else:
            assert False
        obj1.remove_item()
        item = search_mysql_item(product_id)
        if not item:
            assert True
        else:
            assert False
    except BaseException:
        assert False


def test_mysql_update():
    product_id = "1"
    obj1 = MySQLCostcoItem(
        product_id,
        "test",
        "9.99",
        "-1",
        True,
        ".com",
        "image.com",
        "test_category")
    try:
        obj1.update_item()
        item = search_mysql_item(product_id)
        if float(item[6]) == float("9.99"):
            obj1 = MySQLCostcoItem(
                product_id,
                "test",
                "8.99",
                "-1",
                True,
                ".com",
                "image.com",
                "test_category")
            obj1.update_item()
            assert float(search_mysql_item(product_id)[5]) == float("8.99")
            obj1.remove_item()
        else:
            assert False
    except BaseException:
        assert False


@pytest.mark.slow
def test_selenium_retrieve():
    url = "https://www.costco.ca/mens-clothing.html"
    get_costco_product(url)
