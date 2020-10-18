import PySimpleGUI as sg
import db
import listutils
import logging
from typing import Any, Dict, List


def make_detail_line(item: Any) -> str:
    text = 'Price: ' + item['price_amazon'] + '\tUsed&New: ' + item['price_used_new'] + \
           '\tAvg. Rating: ' + str(item['rating']) + '/5' + \
           '\tReviews: ' + str(item['num_reviews']) + '\tUpdated: ' + item['update_date'] + '\n'
    return text


def make_rows(items: List) -> List:
    double_rows = [make_item_row(item, i+1) for i, item in enumerate(items)]
    rows = [[item] for subrow in double_rows for item in subrow]
    return rows


def make_item_row(item: Any, num: int = 0) -> str:
    if num:
        num_str = str(num)
    else:
        num_str = ''
    row = [sg.Text(num_str + ' ' + item['name'], font=['Arial', 12, 'bold']), sg.Text(item['by_line'] +
                                                                                      '\n' + make_detail_line(item))]
    return row


def main_window():
    """

    :return:
    """
    sort_author_direction = True
    logging.info('Starting GUI')

    items = db.get_current_items()

    rows = make_rows(items)

    layout_top = [[sg.Text(str(len(items)) + ' Items')],
              [sg.Button("Pull Lists"), sg.Button('Add List'), sg.Button('View Lists')],
                  [sg.Button("Sort Author"), sg.Button("Sort Amazon Price"), sg.Button("Sort Rating")]]
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
                          [sg.Button("Pull Lists"), sg.Button('Add List'), sg.Button('View Lists')]]
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
        if event == 'View Lists':
            lists = listutils.get_lists_from_file('list_urls.json')
            layout_popup = [[sg.Text(it['name']), sg.Text(it['url'])] for it in lists] + [[sg.Cancel()]]
            window_popup = sg.Window('View Lists', layout_popup)
            event, values = window_popup.read()
            window_popup.Close()
        if event == 'Sort Author':
            items = sorted(items, key=lambda x: x['by_line'], reverse=sort_author_direction)
            sort_author_direction = not sort_author_direction
            rows = make_rows(items)
            layout_top = [[sg.Text('Text')],
                          [sg.Text('Input Text: ')], [sg.InputText()],
                          [sg.Button("Pull Lists"), sg.Button('Add List'), sg.Button('View Lists')],
                  [sg.Button("Sort Author"), sg.Button("Sort Amazon Price"), sg.Button("Sort Rating")]]
            layout = layout_top + rows
            window1 = sg.Window('Main Window', resizable=True).Layout(
                [[sg.Column(layout, size=(900, 600), scrollable=True)]])
            window.Close()
            window = window1

    window.close()


if __name__ == '__main__':
    main_window()