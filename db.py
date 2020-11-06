"""
Functions for creating and interacting with the database.

Some parts taken from the SQLite tutorial.
"""

import listutils
import pathlib
import sqlite3
from sqlite3 import Error
from typing import Any, Dict, List, Tuple

DB_COLUMNS_LIST = ('name', 'by_line', 'price_amazon', 'price_used_new', 'rating', 'num_reviews', 'item_id',
                   'item_external_id', 'update_date', 'list_name')
RETURN_COLUMNS_LIST = ('item_id', 'update_date', 'price_amazon', 'price_used_new', 'rating', 'num_reviews',
                       'name', 'by_line', 'item_external_id', 'list_name')

db_path = pathlib.Path.home().joinpath('bookshelf', 'database.db')


def create_connection(db_file: str) -> Any:
    """
    Create a database connection to the SQLite database specified by db_file.
    :param db_file: database file
    :return: connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e, ' in create_connection')

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e, ' in create_table')


def create_items_table(conn):
    """

    :param conn:
    :return:
    """
    sql_create_items_table = """ CREATE TABLE IF NOT EXISTS items (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            by_line text,
                                            price_amazon text,
                                            price_used_new text,
                                            rating double,
                                            num_reviews int,
                                            item_id text,
                                            item_external_id text,
                                            update_date datetime,
                                            list_name text
                                        ); """

    sql_create_items_table = """ CREATE TABLE IF NOT EXISTS items (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                by_line text,
                                                item_id text,
                                                item_external_id text,
                                                list_name text
                                            ); """

    if conn is not None:
        create_table(conn, sql_create_items_table)
    else:
        print("Error! Cannot create database connection.")


def create_records_table(conn):
    """

    :param conn:
    :return:
    """
    sql_create_records_table = """ CREATE TABLE IF NOT EXISTS records (
                                            id integer PRIMARY KEY,
                                            item_id text,
                                            update_date datetime,
                                            price_amazon text,
                                            price_used_new text,
                                            rating double,
                                            num_reviews int
                                        ); """

    if conn is not None:
        create_table(conn, sql_create_records_table)
    else:
        print("Error! Cannot create database connection.")


def load_data(data):
    """
    Load new data to items table.
    :param data: list of dictionaries containing item data
    :return:
    """

    item_columns = ['name', 'by_line', 'item_id', 'item_external_id', 'list_name']
    record_columns = ['item_id', 'update_date', 'price_amazon', 'price_used_new', 'rating', 'num_reviews']
    sql_statement = """INSERT INTO 
                            items
                            (name, by_line, price_amazon, price_used_new, rating, num_reviews, item_id,
                            item_external_id, update_date, list_name)
                        VALUES
                            (:name, :by_line, :price_amazon, :price_used_new, :rating, :num_reviews, :item_id,
                            :item_external_id, :update_date, :list_name)"""

    item_data = [{k: v for k, v in d.items() if k in item_columns} for d in data]
    record_data = [{k: v for k, v in d.items() if k in record_columns} for d in data]

    sql_items = """INSERT INTO items
                        (""" + ','.join(item_columns) + """)
                        VALUES
                        (:""" + ', :'.join(item_columns) + """)"""
    sql_records = """INSERT INTO records
                            (""" + ','.join(record_columns) + """)
                            VALUES
                            (:""" + ', :'.join(record_columns) + """)"""
    conn = create_connection(db_path)
    with conn:
        create_items_table(conn)
        create_records_table(conn)
        try:
            c = conn.cursor()
            # c.executemany(sql_statement, data)
            c.executemany(sql_items, item_data)
            c.executemany(sql_records, record_data)
            conn.commit()
        except Error as e:
            print(e, ' in load_data')


def convert_db_row(row: Tuple) -> Dict:
    """
    SELECT statement returns rows as tuples. Convert tuple to dict.
    :param row: tuple of single result row from database
    :return: dict of item details, column names as keys
    """
    return dict(zip(RETURN_COLUMNS_LIST, row))


def get_current_items() -> List:
    """
    Gets the unique items with the latest update_date from the database.
    :return:
    """
    sql_statement = """SELECT DISTINCT items.""" + ', '.join(RETURN_COLUMNS_LIST) + """ 
                        FROM items LEFT JOIN
                        (SELECT 
                        item_id, update_date, price_amazon, price_used_new, rating, num_reviews
                        FROM records r1
                        WHERE
                            r1.update_date = (SELECT max(update_date) FROM records r2 WHERE r1.item_id = r2.item_id)) rs
                        ON items.item_id=rs.item_id
                            """
    items = []
    try:
        conn = create_connection(db_path)
        c = conn.cursor()
        c.execute(sql_statement)
        rows = c.fetchall()
        items = [convert_db_row(r) for r in rows]
    except Error as e:
        print(e, ' in get_current_items')
    return items


if __name__ == '__main__':
    conn = create_connection(db_path)
    with conn:
        data = listutils.load_list('listdump.json')
        load_data(data, conn)
