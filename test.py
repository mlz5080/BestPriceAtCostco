import requests
from concurrent.futures import ProcessPoolExecutor
from selenium import webdriver
import os
from urllib.parse import urljoin
from multiprocessing.pool import ThreadPool, Pool
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


class CostcoItem:
    def __init__(self, item_id, name, price, price_range, is_on_sale, product_link, image_link):
        self.id = item_id
        self.price = price
        self.price_range = price_range
        self.name = name
        self.link = product_link
        self.is_on_sale = is_on_sale
        self.image_link = image_link

    def __str__(self):
        return " ".join(
            [
                self.id,
                self.name,
                self.price,
                "is on sale" if self.is_on_sale else "not on sale",
                self.link,
                self.image_link,"\n"
            ]
        )

    def to_json(self):
        return 


def get_shop_by_category_links(link):
    # res = requests.get(link)
    # soup = BeautifulSoup(res.text,"lxml")
    # titles = [str(urljoin(url,items.get("href"))) for items in soup.select(".question-hyperlink")]

    driver = get_driver()
    driver.get(link)
    target_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "shop-mt-mobile"))
    )
    target_element.click()
    sauce = BeautifulSoup(driver.page_source,"lxml")
    level1_html = [domain+li.a.get("href") for li in sauce.find('div', id="level1-all-departments").find_all("li")]
    # print(level1_html)
    # driver.close()
    # rq = requests.get("https://www.costco.ca/everlast-1910-classic-training-leather-glove-kit.product.1468886.html",timeout=5)
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
    return all_sites[:2]

def retrive_product_info(div, sauce):
    product_price_str = div.string
    # item_id, name, price, price_range, hmp, is_on_sale, link
    price_range = ""
    if not product_price_str:
        product_price, price_range = div.contents[0].strip(), div.contents[-1].strip()
    else:
        product_price = div.string.strip()
    item_id = re.findall(r'\d+',div.get("id").strip())[0]
    div_parent = div.find_parent()
    span = div_parent.find_next_sibling("span")
    is_on_sale = False
    if div_parent.find_next_sibling("p") and div_parent.find_next_sibling("p").has_attr("automation-id"):
        is_on_sale = "instantSavings" in div_parent.find_next_sibling("p").get("automation-id")
    sub_a = span.find("a")
    product_name = sub_a.string.strip()
    product_link = sub_a.get('href')
    image_link = sauce.find("img", {"alt": product_name}).get("src")
    if not image_link:
        image_link = sauce.find("img", {"alt": product_name}).get("data-src")
    # print(sauce.find("img", {"alt": product_name}))
    return CostcoItem(item_id, product_name, product_price, price_range, is_on_sale, product_link, image_link)

def db_update(costco_product, table_name):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

def get_costco_product(url):
    print("#"*10, url, "#"*10)
    driver = get_driver()
    has_next_page = True
    page = 1
    driver.get(url)
    while has_next_page:
        sauce = BeautifulSoup(driver.page_source, "lxml")
        price_divs = sauce.find_all("div", {"class": "price"})
        if not price_divs:
            print("errors")
            return
        product_info = [retrive_product_info(pd, sauce) for pd in price_divs]
        print("\nProduct Page {}\n".format(page))
        # with open("{}.txt".format(url))
        for product_info in product_info:
            print(product_info)
            # db_update()
        # print("#"*100)
        # print()
        has_next_page = sauce.find("li", class_="forward") != None
        page = page+1 if has_next_page else page
        try:
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i[automation-id='nextPageNavigationLink']"))))
        except:
            print("Done")
    driver.close()

if __name__ == '__main__':
    # get_url_from_site_map()
    # get_shop_by_category_links(domain)
    Pool(1).map(get_costco_product, get_url_from_site_map())