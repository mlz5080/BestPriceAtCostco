import requests
from concurrent.futures import ProcessPoolExecutor
from selenium import webdriver
import os
from multiprocessing.pool import ThreadPool, Pool
from DataTypes.Dynamo import DynamoCostcoItem
from DataTypes.MySQL import MySQLCostcoItem
from bs4 import BeautifulSoup
import threading
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import boto3

costco_domain = "https://www.costco.ca"
costco_db_table_name = "costco-products-info"

def get_shop_by_category_links(link):

    driver = get_driver()
    driver.get(link)
    target_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "shop-mt-mobile"))
    )
    target_element.click()
    sauce = BeautifulSoup(driver.page_source,"lxml")
    level1_html = [domain+li.a.get("href") for li in sauce.find('div', id="level1-all-departments").find_all("li")]
    selenium_user_agent = driver.execute_script("return navigator.userAgent;")
    s = requests.Session()
    s.headers.update({"user-agent": selenium_user_agent})
    for cookie in driver.get_cookies():
        s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    response = s.get("https://www.costco.ca/everlast-1910-classic-training-leather-glove-kit.product.1468886.html")
    sauce = BeautifulSoup(response.content, "lxml")
    print(sauce.find("div", id="pull-right-price"))
    return level1_html

threadLocal = threading.local()

def get_driver():
    driver = getattr(threadLocal, 'driver', None)
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
    if driver is None:
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('user-agent={0}'.format(user_agent))
        chromeOptions.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=chromeOptions)
        setattr(threadLocal, 'driver', driver)
    return driver

def get_url_from_site_map():
    url = "https://www.costco.ca/SiteMapDisplayView"
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    driver = get_driver()
    driver.get(url)
    sauce = BeautifulSoup(driver.page_source, "lxml")
    site_map_div = sauce.find("div", class_="costcoBD-sitemap")
    all_sites = site_map_div.find_all('a', href=True)
    all_sites = [costco_domain+a.get("href") for a in all_sites]
    # print(all_sites)
    return all_sites

def retrive_product_info(div, sauce):
    product_price_str = div.string
    # item_id, name, price, price_range, hmp, is_on_sale, link
    price_range = "-1"
    if not product_price_str:
        product_price, price_range = div.contents[0].strip(), div.contents[-1].strip()
        thousand_price_list = re.findall(r'\d+\,\d+\.\d+', price_range)
        price_range = thousand_price_list[0].replace(",", "") if thousand_price_list else re.findall(r'\d+.\d+', price_range)[0]
    else:
        product_price = div.string.strip()
    thousand_price_list = re.findall(r'\d+\,\d+\.\d+', product_price)
    product_price = thousand_price_list[0].replace(",", "") if thousand_price_list else re.findall(r'\d+.\d+', product_price)[0]
    
    item_id = re.findall(r'\d+', div.get("id").strip())[0]
    
    div_parent = div.find_parent()
    span = div_parent.find_next_sibling("span")
    is_on_sale = False
    if div_parent.find_next_sibling("p") and div_parent.find_next_sibling("p").has_attr("automation-id"):
        is_on_sale = "instantSavings" in div_parent.find_next_sibling("p").get("automation-id")
    
    sub_a = span.find("a")
    product_name = sub_a.string.strip()
    product_link = sub_a.get('href')

    cat = sauce.find("script", string=lambda val: val is not None and "categoryName" in val).text.strip()
    cat = re.findall(r"categoryName\: '(\w+.*)'", cat)[0]

    image_tag = sauce.find("img", alt=lambda val: val is not None and product_name in val)
    if image_tag and image_tag.get("src"):
        image_link = image_tag.get("src")
    else:
        image_link = image_tag.get("data-src")

    dynamo_dao = DynamoCostcoItem(item_id, product_name, product_price, price_range, is_on_sale, product_link, image_link, cat)
    dynamo_dao.update_item()
    mysql_dao = MySQLCostcoItem(item_id, product_name, product_price, price_range, is_on_sale, product_link, image_link, cat)
    mysql_dao.update_item()

def get_costco_product(url):
    print("#"*10, url, "#"*10)
    category = url.split("https://www.costco.ca/")[1].replace(".html", "")
    driver = get_driver()
    has_next_page = True
    page = 1
    driver.get(url)
    while has_next_page:
        sauce = BeautifulSoup(driver.page_source, "lxml")
        product_div_parent = sauce.find("div", attrs={"automation-id":"productList"})
        if not product_div_parent:
            print("Did not find product div")
            return
        product_div_list = product_div_parent.find_all("div", class_= lambda val: val is not None and "product" in val and "col-xs" in val)
        for pd in product_div_list:
            price_div = pd.find("div", id=lambda val: val is not None and "price" in val)
            retrive_product_info(price_div, pd)
        has_next_page = sauce.find("li", class_="forward") != None
        page = page+1 if has_next_page else page
        try:
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i[automation-id='nextPageNavigationLink']"))))
        except:
            print("Done")
            break

if __name__ == '__main__':
    # get_url_from_site_map()
    # get_shop_by_category_links(domain)
    Pool(os.cpu_count()).map(get_costco_product, get_url_from_site_map())
