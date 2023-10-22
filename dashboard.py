import streamlit as st
import sqlite3
import pandas as pd


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def execute_query(conn, query):
    cur = conn.cursor().execute(query)
    return pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])


if __name__ == "__main__":
    conn = create_connection("data/raw/university.db")

    query = f'''
    SELECT *
    FROM university
    LIMIT 10;
    '''

    st.write(execute_query(conn, query))
