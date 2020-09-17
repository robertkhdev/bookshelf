import PySimpleGUI as sg
import json
import amazon
import pathlib
from typing import Any, Dict, List


def load_list(file_name: str) -> List[Dict[str, str]]:
    path= pathlib.Path.home().joinpath('bookshelf', 'lists', file_name)
    with path.open(mode='r') as f:
        return json.loads(f.read())


def make_detail_line(item: Any) -> str:
    text = 'Price: ' + item['price_amazon'] + ' Used&New: ' + item['price_used_new'] + \
           'Avg. Rating: ' + str(item['rating'][0]) + '/' + str(item['rating'][1]) + \
           ' Reviews: ' + item['num_reviews']
    return text


def make_item_row(item: Any) -> str:
    row = [sg.Text(item['name'] + '\n' + item['by_line'] + '\n' + make_detail_line(item))]
    return row


def main_window():
    """

    :return:
    """
    # layout = [[sg.Text('Hello World')]]
    # window = sg.Window('Window title', layout)

    items = load_list('listdump.json')
    # rows = [[sg.Checkbox(item['name'])] for item in items]

    # rows = [[sg.Frame(layout=[[sg.Text(item['name'])], [sg.Text(item['by_line'])],
    #                           [sg.Text(make_detail_line(item))]], title='')] for item in items]

    rows = [make_item_row(item) for item in items]

    layout = [[sg.Text('TEST')],
              [sg.Text('Input Text: ')], [sg.InputText()],
              [sg.Button("a button")]] + \
              rows + \
              [[sg.Text('')],
              [sg.Submit('Submit'), sg.Cancel('Cancel')]]

    window = sg.Window('Main Window', resizable=True).Layout([[sg.Column(layout, size=(900, 600), scrollable=True)]])

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

    window.close()


if __name__ == '__main__':
    main_window()