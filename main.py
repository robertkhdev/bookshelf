import PySimpleGUI as sg
import db
import listutils
import logging
from typing import Any, Dict, List


# def make_detail_line(item: Any) -> str:
#     text = 'Price: ' + item['price_amazon'] + '\tUsed&New: ' + item['price_used_new'] + \
#            '\tAvg. Rating: ' + str(item['rating']) + '/5' + \
#            '\tReviews: ' + str(item['num_reviews']) + '\tUpdated: ' + item['update_date'] + '\n'
#     return text


# def make_rows(items: List) -> List:
#     double_rows = [make_item_row(item, i+1) for i, item in enumerate(items)]
#     rows = [[item] for subrow in double_rows for item in subrow]
#     return rows


# def make_item_row(item: Any, num: int = 0) -> List:
#     if num:
#         num_str = str(num)
#     else:
#         num_str = ''
#     row = [sg.Text(num_str + ' ' + item['name'], font=['Arial', 12, 'bold']), sg.Text(item['by_line'] +
#                                                                                       '\n' + make_detail_line(item))]
#     return row


def wrap_text(text: str, n=60) -> str:
    return '\n'.join(list(text[i: i+n] for i in range(0, len(text), n)))


def make_headers_and_rows(items: List) -> (List, List):
    headers = ['Title', 'Author', 'Price', 'New & Used', 'Rating', 'Reviews', 'List', 'Updated', 'Item ID', 'Ext. Item ID']
    row_data = [[wrap_text(it['name']), it['by_line'], it['price_amazon'], it['price_used_new'], str(it['rating']),
                 str(it['num_reviews']), it['list_name'], it['update_date'], it['item_id'], it['item_external_id']] for it in items]
    return headers, row_data


def make_main_layout(items: List) -> List:
    headers, row_data = make_headers_and_rows(items)

    menu_def = [['Lists', ['Pull Lists', 'Add List', 'View Lists']]]

    layout_top = [[sg.Menu(menu_def)], [sg.Text(str(len(items)) + ' Items')],
                  [sg.Button("Sort Title"),
                  sg.Button("Sort Author"), sg.Button("Sort Amazon Price"), sg.Button("Sort Rating")]]
    if len(items) == 0:
        row_data = [['', '', '', '', '', '', '', '', '', '']]

    # layout = layout_top + rows
    layout_table = [[sg.Table(values=row_data, headings=headers, max_col_width=30,
                              # background_color='light blue',
                              enable_events=True,
                              auto_size_columns=True,
                              display_row_numbers=True,
                              justification='left',
                              num_rows=15,
                              # alternating_row_color='lightyellow',
                              key='-TABLE-',
                              row_height=35,
                              tooltip='This is a table')]]
    layout = layout_top + layout_table
    return layout


def main_window():
    """

    :return:
    """
    sort_title_direction = True
    sort_author_direction = True
    sort_amazon_price_direction = True
    sort_rating_direction = True
    logging.info('Starting GUI')

    items = db.get_current_items()
    layout = make_main_layout(items)

    window = sg.Window('Main Window', resizable=True).Layout([[sg.Column(layout, size=(1300, 700), scrollable=True)]])

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Pull Lists':
            listutils.download_all_lists()
            items = db.get_current_items()
            headers, row_data = make_headers_and_rows(items)
            window['-TABLE-'].update(row_data)
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
        if event == 'Sort Title':
            items = sorted(items, key=lambda x: x['name'], reverse=sort_title_direction)
            sort_title_direction = not sort_title_direction
            headers, row_data = make_headers_and_rows(items)
            window['-TABLE-'].update(row_data)
        if event == 'Sort Author':
            items = sorted(items, key=lambda x: x['by_line'], reverse=sort_author_direction)
            sort_author_direction = not sort_author_direction
            headers, row_data = make_headers_and_rows(items)
            window['-TABLE-'].update(row_data)
        if event == 'Sort Amazon Price':
            items = sorted(items, key=lambda x: x['price_amazon'], reverse=sort_amazon_price_direction)
            sort_amazon_price_direction = not sort_amazon_price_direction
            headers, row_data = make_headers_and_rows(items)
            window['-TABLE-'].update(row_data)
        if event == 'Sort Rating':
            items = sorted(items, key=lambda x: str(x['rating']), reverse=sort_rating_direction)
            sort_rating_direction = not sort_rating_direction
            headers, row_data = make_headers_and_rows(items)
            window['-TABLE-'].update(row_data)


    window.close()


if __name__ == '__main__':
    main_window()