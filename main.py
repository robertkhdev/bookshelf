import PySimpleGUI as sg
import json
import amazon
import pathlib
from typing import Dict, List


def load_list(file_name: str) -> List[Dict[str, str]]:
    path= pathlib.Path.home().joinpath('bookshelf', 'lists', file_name)
    with path.open(mode='r') as f:
        return json.loads(f.read())


def main_window():
    """

    :return:
    """
    # layout = [[sg.Text('Hello World')]]
    # window = sg.Window('Window title', layout)

    items = load_list('listdump.json')
    rows = [[sg.Checkbox(item['name'])] for item in items]

    layout = [[sg.Text('TEST')],
              [sg.Text('Input Text: ')], [sg.InputText()],
              [sg.Button("a button")]] + \
              rows + \
              [[sg.Text('')],
              [sg.Submit('Submit'), sg.Cancel('Cancel')]
              ]

    window = sg.Window('Main Window', resizable=True).Layout([[sg.Column(layout, size=(900, 600), scrollable=True)]])

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

    window.close()


if __name__ == '__main__':
    main_window()