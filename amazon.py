"""
Contains functions for getting Amazon wish lists
"""

from bs4 import BeautifulSoup
import json
import pathlib
import re
from seleniumwire import webdriver
import time
from typing import Any, Dict


***REMOVED***


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
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '\
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


def save_list(items: Any) -> None:
    names = [parse_item_name(i) for i in items]
    by_lines = [parse_item_byline(i) for i in items]
    combos = zip(names, by_lines)
    save_dict = [{'name': i[0], 'by_line': i[1]} for i in combos]
    list_dir_path = pathlib.Path.home().joinpath('bookshelf', 'lists')
    if not list_dir_path.exists():
        list_dir_path.mkdir()
    path = pathlib.Path.home().joinpath('bookshelf', 'lists', 'listdump.json')
    with path.open(mode='w') as f:
        json.dump(save_dict, f)


if __name__ == '__main__':
    # test list retrieval
    items = get_amazon_list(url)
    print([parse_item_name(i) for i in items])
    save_list(items)