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

domain = "https://www.costco.ca"

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
    # print(response.content)
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
    # s = requests.Session()
    # with requests.Session() as s:
    #     s.headers.update({"user-agent": user_agent})
    #     response = s.get(url)
    driver = get_driver()
    driver.get(url)
    # time.sleep(1)
    sauce = BeautifulSoup(driver.page_source, "lxml")
    # print(sauce)
    site_map_div = sauce.find("div", class_="costcoBD-sitemap")
    all_sites = site_map_div.find_all('a', href=True)
    for a in all_sites:
        print(a.string.strip(), a.get("href"))
    get_product("https://www.costco.ca/learning-systems.html")
    # driver.close()

def retrive_name_and_links(div):
    sub_a = div.find_parent().find_next_sibling().a
    return (sub_a.string.strip(), sub_a.get('href'))

def get_product(url):
    driver = get_driver()
    driver.get(url)
    sauce = BeautifulSoup(driver.page_source, "lxml")
    # product_List = sauce.find("div", {"automation-id":"productList"})
    price_divs = sauce.find_all("div", {"class": "price"})
    price_list = [pd.string.strip() for pd in price_divs]
    product_info = [retrive_name_and_links(pd) for pd in price_divs]

    for price, info in zip(price_list, product_info):
        print(info[0], price, info[1])
    driver.close()

if __name__ == '__main__':
    get_url_from_site_map()
    # get_shop_by_category_links(domain)
    # Pool(os.cpu_count()).map(get_title, get_shop_by_category_links(domain))