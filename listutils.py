"""
Contains functions for getting Amazon wish lists
"""

import amazon
import json
import pathlib
from typing import Any, Dict, List


def save_list(items: Any) -> None:
    save_dict = amazon.build_items_list(items)
    list_dir_path = pathlib.Path.home().joinpath('bookshelf', 'lists')
    if not list_dir_path.exists():
        list_dir_path.mkdir()
    path = pathlib.Path.home().joinpath('bookshelf', 'lists', 'listdump.json')
    with path.open(mode='w') as f:
        json.dump(save_dict, f)


def get_lists_from_file(file_name: str) -> List:
    """
    Load list of list URLs from text file.
    :param file_name:
    :return:
    """
    list_url_file = pathlib.Path.home().joinpath('bookshelf', file_name)
    if not list_url_file.is_file():
        return []
    # open file and load contents
    with list_url_file.open(mode='r') as f:
        list_urls = [line for line in f]
    return list_urls


def add_list(url: str) -> None:
    """
    Add list url to text file. This file has a default name in the bookshelf folder in the home directory.
    It contains a list of Amazon list urls.
    :param url:
    :return:
    """
    # check if the list file exists
    list_url_file = pathlib.Path.home().joinpath('bookshelf', 'list_urls.txt')
    if not list_url_file.is_file():
        with list_url_file.open(mode='w') as f:
            f.write(url)
    else:
        # open file and load contents
        list_urls = get_lists_from_file('list_urls.txt')
        new_list_urls = list(set(list_urls + [url]))
        # write to file
        with list_url_file.open(mode='w') as f:
            f.write('\n'.join(new_list_urls))


def download_all_lists():
    # open file and load contents
    list_urls = get_lists_from_file('list_urls.txt')
    for url in list_urls:
        try:
            save_list(amazon.get_amazon_list(url))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # test list retrieval
    items_test = amazon.get_amazon_list(url)
    print([amazon.parse_item_name(i) for i in items_test])
    save_list(items_test)