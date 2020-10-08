"""
Functions for creating and interacting with the database.

Some parts taken from the SQLite tutorial.
"""

import listutils
import pathlib
import sqlite3
from sqlite3 import Error
from typing import Any, List

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
        print(e)

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
        print(e)


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
                                            update_date, datetime
                                        ); """

    if conn is not None:
        create_table(conn, sql_create_items_table)
    else:
        print("Error! Cannot create database connection.")


def load_data(data, conn):
    """
    Load new data to items table.
    :param data: list of dictionaries containing item data
    :return:
    """
    sql_statement = """INSERT INTO 
                            items
                            (name, by_line, price_amazon, price_used_new, rating, num_reviews, item_id,
                            item_external_id, update_date)
                        VALUES
                            (:name, :by_line, :price_amazon, :price_used_new, :rating, :num_reviews, :item_id,
                            :item_external_id, :update_date)"""
    create_items_table(conn)
    try:
        c = conn.cursor()
        c.executemany(sql_statement, data)
        conn.commit()
    except Error as e:
        print(e)


def get_current_items() -> List:
    """
    Gets the unique items with the latest update_date from the database.
    :return:
    """
    sql_statment = """SELECT (name, by_line, price_amazon, price_used_new, rating, num_reviews, item_id,
                            item_external_id, update_date)
                        FROM items it1
                        WHERE
                            it1.update_date = (SELECT max(update_date) from items it2 where it1.item_id = it2.item_id"""
    rows = []
    try:
        conn = create_connection(db_path)
        c = conn.cursor()
        c.execute(sql_statment)
        rows = c.fetchall()
    except Error as e:
        print(e)
    return rows


if __name__ == '__main__':
    conn = create_connection(db_path)
    with conn:
        data = listutils.load_list('listdump.json')
        load_data(data, conn)
