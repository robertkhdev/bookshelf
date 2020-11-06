"""
Contains functions for getting Amazon wish lists
"""

import amazon
import db
import json
import pathlib
from typing import Any, Dict, List


def save_list_to_file(items: Any, name: str = None) -> None:
    print('Saving list: ', name)
    save_items = amazon.build_items_list(items, name)
    list_dir_path = pathlib.Path.home().joinpath('bookshelf', 'lists')
    if not list_dir_path.exists():
        list_dir_path.mkdir()

    path = pathlib.Path.home().joinpath('bookshelf', 'lists', 'listdump.json')
    if path.exists():
        with path.open(mode='r') as f:
            existing_items = json.load(f)
        save_items = existing_items + save_items
    with path.open(mode='w') as f:
        json.dump(save_items, f)


def save_list(items: Any, name: str = None) -> None:
    print('Saving list to database: ', name)
    save_items = amazon.build_items_list(items, name)
    db.load_data(save_items)


def get_lists_from_file(file_name: str) -> List:
    """
    Load list of list URLs from json file.
    :param file_name:
    :return: list of dicts of names and urls
    """
    list_url_file = pathlib.Path.home().joinpath('bookshelf', file_name)
    if not list_url_file.is_file():
        return []
    # open file and load contents
    with list_url_file.open(mode='r') as f:
        list_urls = json.load(f)
    return list_urls


def add_list_to_file(url: str, name: str) -> None:
    """
    Add list url to json file. This file has a default name in the bookshelf folder in the home directory.
    It contains a list of Amazon list urls.
    :param url:
    :return:
    """
    # check if the list file exists and create it if not
    list_url_file = pathlib.Path.home().joinpath('bookshelf', 'list_urls.json')
    url_to_save = [{'name': name, 'url': url}]
    if not list_url_file.exists():
        with list_url_file.open(mode='w') as f:
            json.dump(url_to_save, f)
    else:
        # open file and load contents
        list_urls = get_lists_from_file('list_urls.json')
        new_list_urls = list_urls + url_to_save
        # write to file
        with list_url_file.open(mode='w') as f:
            json.dump(new_list_urls, f)


def download_all_lists():
    # open file and load contents
    list_urls = get_lists_from_file('list_urls.json')
    for url in list_urls:
        print('Downloading list: ', url['name'])
        try:
            save_list(amazon.get_amazon_list(url['url']), url['name'])
        except Exception as e:
            print(e, ' in download_all_lists')


def load_list(file_name: str) -> List[Dict[str, str]]:
    path = pathlib.Path.home().joinpath('bookshelf', 'lists', file_name)
    if not path.exists():
        return []
    with path.open(mode='r') as f:
        return json.loads(f.read())


if __name__ == '__main__':
    # test list retrieval
    ***REMOVED***
    items_test = amazon.get_amazon_list(url)
    print([amazon.parse_item_name(i) for i in items_test])
    save_list(items_test)