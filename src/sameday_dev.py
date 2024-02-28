import threading
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import time


threadLocal = threading.local()
same_day_domain = "https://sameday.costco.ca"


def scroll_to_end(driver):
    prev_height = -1
    max_scrolls = 100
    scroll_count = 0

    while scroll_count < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # give some time for new results to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == prev_height:
            break
        prev_height = new_height
        scroll_count += 1


def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def get_driver():
    driver = getattr(threadLocal, 'driver', None)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0)'
    user_agent += ' Gecko/20100101 Firefox/122.0'
    if driver is None:
        FirefoxOptions = webdriver.FirefoxOptions()
        # FirefoxOptions.add_argument("--headless")
        FirefoxOptions.add_argument('user-agent={0}'.format(user_agent))
        FirefoxOptions.add_argument("--log-level=3")
        driver = webdriver.Firefox(options=FirefoxOptions)
        setattr(threadLocal, 'driver', driver)
    return driver


def same_day_scraper(price, url):
    driver = get_driver()
    driver.get(url)
    time.sleep(3)
    sauce = BeautifulSoup(driver.page_source, "lxml")
    item_div = sauce.find("div", id="item_details")
    image_link = item_div.img.get("src")

    item_id, unit = item_div.div.next_sibling.div.next_sibling.find("h2").next_sibling.next_sibling.find_all("div")

    print(price.split(" Original price: "), item_id.text.split("Item: ")[1], unit.text, image_link)
    price_div = item_div.find("div", attrs={"data-radium": lambda val: val is not None})
    unit_price = price_div.div.div.div.div.next_sibling

    if unit_price:
        unit_price = unit_price.text
    print(unit_price)
    return driver


def get_products_price_and_url():
    driver = get_driver()
    url = "https://sameday.costco.ca"
    
    driver.get(url)

    time.sleep(3)

    sauce = BeautifulSoup(driver.page_source, "lxml")
    weekly_saving = sauce.find("a", href=lambda val: val is not None and "rc-weekly-savings" in val)

    xpath = xpath_soup(weekly_saving)
    selenium_element = driver.find_element(By.XPATH, xpath)
    selenium_element.click()

    time.sleep(3)

    scroll_to_end(driver)
    sauce = BeautifulSoup(driver.page_source, "lxml")
    product_divs = sauce.find_all("div", attrs={"aria-label":lambda val: val is not None and "Product" in val})
    price_divs = [pd.find("div", attrs={"aria-label":lambda val: val is not None and "$" in val and "Original price" in val}) for pd in product_divs]
    product_details = [same_day_domain + pd.a.get("href") for pd in product_divs]
    price_divs = [pd["aria-label"] for pd in price_divs if pd]

    return zip(price_divs, product_details)

    # Pool(os.cpu_count()).map(same_day_scraper, get_products_price_and_url)


def main():
    for price, url in get_products_price_and_url():
        return same_day_scraper(price, url)
        break


if __name__ == '__main__':
    main()
