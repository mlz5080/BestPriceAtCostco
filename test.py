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

domain = "https://www.costco.ca"

class CostcoItem:
    def __init__(self, item_id, name, price, price_range, hmp, is_on_sale, link):
        self.id = item_id
        self.price = price
        self.price_range = price_range
        self.history_minimum_price = hmp
        self.name = name
        self.link = link
        self.is_on_sale = is_on_sale

    def __str__(self):
        return " ".join([self.id, self.name, self.price, "is on sale" if self.is_on_sale else "not on sale", self.link])


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
        driver = webdriver.Chrome(options=chromeOptions)
        setattr(threadLocal, 'driver', driver)
    return driver

def get_url_from_site_map():
    url = "https://www.costco.ca/SiteMapDisplayView"
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    driver = get_driver()
    driver.get(url)
    # time.sleep(1)
    sauce = BeautifulSoup(driver.page_source, "lxml")
    # print(sauce)
    site_map_div = sauce.find("div", class_="costcoBD-sitemap")
    all_sites = site_map_div.find_all('a', href=True)
    # for a in all_sites:
    #     print(a.string.strip(), a.get("href"))
    get_product("https://www.costco.ca/coffee-tea.html")
    # driver.close()

def retrive_product_info(div):
    product_price = div.string.strip()
    item_id = re.findall(r'\d+',div.get("id").strip())[0]
    div_parent = div.find_parent()
    span = div_parent.find_next_sibling("span")
    # print("instantSavings" in div_parent.find_next_sibling("p").get("automation-id"))

    is_on_sale = False

    if div_parent.find_next_sibling("p") and div_parent.find_next_sibling("p").has_attr("automation-id"):
        is_on_sale = "instantSavings" in div_parent.find_next_sibling("p").get("automation-id")
    sub_a = span.find("a")
    product_name = sub_a.string.strip()
    product_link = sub_a.get('href')
    
    return CostcoItem(item_id, product_name, product_price, is_on_sale, product_link)

def get_product(url):
    driver = get_driver()

    has_next_page = True
    while has_next_page:
        driver.get(url)
        sauce = BeautifulSoup(driver.page_source, "lxml")
        price_divs = sauce.find_all("div", {"class": "price"})
        # print(price_divs)
        for pd in price_divs:
            if not pd.string:
                print(pd.contents)
        product_info = [retrive_product_info(pd) for pd in price_divs]
        for product_info in product_info:
            print(product_info)
        print(sauce.find("li", class_="forward"))
        break
    driver.close()

if __name__ == '__main__':
    get_url_from_site_map()
    # get_shop_by_category_links(domain)
    # Pool(os.cpu_count()).map(get_title, get_shop_by_category_links(domain))