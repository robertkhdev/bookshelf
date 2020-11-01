"""
Contains functions for getting Amazon wish lists
"""

from bs4 import BeautifulSoup
import datetime as dt
import pathlib
import re
from seleniumwire import webdriver
import time
from typing import Any, Dict, List


class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class ItemNotFoundError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def load_cookie() -> str:
    path = pathlib.Path.home().joinpath('bookshelf', 'cookie.txt')
    with path.open(mode='r') as f:
        cookie = f.read()
    return cookie


def construct_headers() -> Dict[str, str]:
    cookie = load_cookie()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'cookie': cookie,
        'viewType': 'list'
    }
    return headers


def parse_item_name(item: Any) -> str:
    """
    Extract name (e.g. book title) from html soup.
    TODO: return type should be EITHER str or None
    :param item: bs4.element.Tag
    :return: string
    """
    for element in item.find_all('a', class_='a-link-normal', id=re.compile('^itemName_(.*)')):
        if 'title' in element.attrs:
            return element['title']
    raise ItemNotFoundError('Item Name', 'Item name not found')


def parse_item_byline(item: Any) -> str:
    """
    Extract by-line (e.g., author name) from html soup.
    :param item: bs4.element.Tag
    :return: string
    """
    return item.find_all('span', class_="a-size-base", id=re.compile('^item-byline-(.*)'))[0].contents[0]


def parse_item_amazon_price(item: Any) -> str:
    """
    Extract price by components of currency symbol, whole value (e.g., dollar), and fraction value (e.g. cents).
    :param item: bs4.element.Tag
    :return: string
    """
    try:
        price_symbol = item.find_all('span', class_="a-price-symbol")[0].contents[0]
        price_whole = item.find_all('span', class_="a-price-whole")[0].contents[0]
        price_fraction = item.find_all('span', class_="a-price-fraction")[0].contents[0]
        return price_symbol + price_whole + '.' + price_fraction
    except IndexError:
        return r'N/A'


def parse_item_used_new_price(item: Any) -> str:
    """
    Extract the "Used & New" price of an item.
    :param item: bs4.element.Tag
    :return: string
    """
    price_used_new = r'N/A'
    try:
        price_used_new = item.find_all('span', class_="a-color-price itemUsedAndNewPrice")[0].contents[0]
    except:
        pass
    return price_used_new


def parse_rating(item: Any) -> str:
    """
    Extract the average star rating of the item.
    :param item: bs4.element.Tag
    :return: string
    """
    rating = 'N/A'
    try:
        stars_str = item.find_all('span', class_="a-icon-alt")[0].contents[0]
        rating = (float(stars_str.split()[0]), float(stars_str.split()[3]))
    except:
        pass
    return rating


def parse_num_reviews(item: Any) -> str:
    """
    Extract number of reviews for the tiem.
    :param item: bs4.element.Tag
    :return: string
    """
    num_reviews_str = '0'
    try:
        num_reviews_str = item.find_all('a', class_="a-size-base a-link-normal")[0].contents[0].strip()
    except:
        pass
    return num_reviews_str


def parse_item_id(item: Any) -> str:
    item_id = ''
    try:
        item_id = item.find_all('input', attrs={'name':"itemId"})[0]['value']
    except:
        pass
    return item_id


def parse_item_external_id(item: Any) -> str:
    item_external_id = ''
    try:
        item_external_id = item.find_all('input', attrs={'name':"itemExternalId"})[0]['value']
    except:
        pass
    return item_external_id


def get_amazon_list(url: str, webdriver_path: str = 'C:/Users/rober/Desktop/chromedriver.exe') -> Any:
    """
    Use Selenium webdriver for Chrome in headless mode to retrieve the page for an Amazon Wish List.
    The list expands dynamically as the use scrolls down the page if the list is long enough to go past one page.
    After requesting the page, the webdriver scrolls to the bottom of the page as much as it can, and waits 5
    seconds to allow time for the rest of the content to load. Then the html of the page, which now includes the
    entire list is fetched from the webdriver.
    :param url: url of Amazon wish list
    :param webdriver_path: path to the websdriver executable
    :return: bs4.element.ResultSet
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=webdriver_path, chrome_options=options)
    # browser.implicitly_wait(5)
    browser.header_overrides = construct_headers()
    browser.get(url)

    # scroll to bottom of page to get it all to load
    while True:
        try:
            # Action scroll down
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            break
        except:
            pass

    time.sleep(5)
    html_source: str = browser.page_source
    # TODO: separate code that parses html string with bs4
    soup = BeautifulSoup(html_source, 'html.parser')
    items = soup.find_all('div', class_='a-fixed-left-grid-inner', style='padding-left:220px')
    browser.quit()
    return items


def build_items_list(items: Any, list_name: str = '') -> List[Dict[str, str]]:
    names = [parse_item_name(i) for i in items]
    by_lines = [parse_item_byline(i) for i in items]
    prices_amazon = [parse_item_amazon_price(i) for i in items]
    prices_used_new = [parse_item_used_new_price(i) for i in items]
    ratings = [parse_rating(i) for i in items]
    num_reviews = [parse_num_reviews(i) for i in items]
    item_ids = [parse_item_id(i) for i in items]
    item_external_ids = [parse_item_external_id(i) for i in items]
    update_time = str(dt.datetime.now())
    combos = zip(names, by_lines, prices_amazon, prices_used_new, ratings, num_reviews, item_ids, item_external_ids)
    list_dict = [{'name': i[0],
                  'by_line': i[1],
                  'price_amazon': i[2],
                  'price_used_new': i[3],
                  'rating': i[4][0],
                  'num_reviews': i[5],
                  'item_id': i[6],
                  'item_external_id': i[7],
                  'update_date': update_time,
                  'list_name': list_name} for i in combos]
    return list_dict


if __name__ == '__main__':
    pass
