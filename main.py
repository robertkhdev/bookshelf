import PySimpleGUI as sg
import db
import listutils
from typing import Any, Dict, List


def make_detail_line(item: Any) -> str:
    text = 'Price: ' + item['price_amazon'] + ' Used&New: ' + item['price_used_new'] + \
           'Avg. Rating: ' + str(item['rating'][0]) + '/' + str(item['rating'][1]) + \
           ' Reviews: ' + item['num_reviews'] + '\n'
    return text


def make_rows(items: List) -> List:
    double_rows = [make_item_row(item) for item in items]
    rows = [[item] for subrow in double_rows for item in subrow]
    return rows


def make_item_row(item: Any) -> str:
    row = [sg.Text(item['name'], font=['Arial', 12, 'bold']), sg.Text(item['by_line'] + '\n' + make_detail_line(item))]
    return row


def main_window():
    """

    :return:
    """

    items = db.get_current_items()

    rows = make_rows(items)

    layout_top = [[sg.Text('Text')],
              [sg.Text('Input Text: ')], [sg.InputText()],
              [sg.Button("Pull Lists"), sg.Button('Add List')]]
    layout = layout_top + rows

    window = sg.Window('Main Window', resizable=True).Layout([[sg.Column(layout, size=(900, 600), scrollable=True)]])

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Pull Lists':
            listutils.download_all_lists()
            items = db.get_current_items()
            rows = make_rows(items)
            layout_top = [[sg.Text('Text')],
                          [sg.Text('Input Text: ')], [sg.InputText()],
                          [sg.Button("Pull Lists"), sg.Button('Add List')]]
            layout = layout_top + rows
            window1 = sg.Window('Main Window', resizable=True).Layout(
                [[sg.Column(layout, size=(900, 600), scrollable=True)]])
            window.Close()
            window = window1
        if event == 'Add List':
            # list_url = sg.popup_get_text('Add List', 'Paste URL for list from your browser')
            layout_popup = [
                [sg.Text('Enter the url and a name for the Amazon List')],
                [sg.Text('List URL', size=(15, 1)), sg.InputText()],
                [sg.Text('List name', size=(15, 1)), sg.InputText()],
                [sg.Submit(), sg.Cancel()]
            ]
            window_popup = sg.Window('Add List', layout_popup)
            event, values = window_popup.read()
            listutils.add_list_to_file(values[0], values[1])
            window_popup.Close()

    window.close()


if __name__ == '__main__':
    main_window()