import streamlit as st
import sqlite3
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from sql_queries import *

# configuration of the page
st.set_page_config(layout="wide")

SPACER = .2
ROW = 1


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


def get_country_list(conn):
    query = f'''
    SELECT country.country_name
    FROM university
    INNER JOIN country
    ON university.country_id = country.id
    GROUP BY country.country_name
    ORDER BY COUNT(university.id) DESC
    '''

    df_countries = execute_query(conn, query)
    return df_countries.iloc[:, 0].to_list()


def plot_metric(number, title):
    config = {'staticPlot': True, 'displayModeBar': False}

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number",
        value=number,
        title={"text": title, "font": {"size": 24}},
        domain={'row': 0, 'column': 0}))

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True, config=config)


def hide_streamlit_header_footer():
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    css = '''
        <style>
        section.main > div:has(~ footer ) {
            padding-bottom: 0px;
        }
        </style>
        '''
    st.markdown(css, unsafe_allow_html=True)


if __name__ == "__main__":
    hide_streamlit_header_footer()

    conn = create_connection("data/raw/university.db")

    # HEADER
    title, _, header_button = st.columns((ROW, .05, ROW*1.5))
    with title:
        st.title('University ranking dashboard')

    with header_button:
        button_1, _, _, _ = st.columns(4)
        with button_1:
            country_list = get_country_list(conn)
            country = st.selectbox('Country', country_list)

    st.write("")

    row_1_col_1, row_1_col_2, row_1_col_3, row_1_col_4, row_1_col_5, row_1_col_6, row_1_col_7, row_1_col_8 = st.columns(
        (ROW, 0.1, ROW, 0.1, ROW, 0.1, ROW, 0.1))
    with row_1_col_1:
        df = execute_query(conn, get_perc_uni_top_200_query(country))
        plot_metric(df.iloc[0, 0]*100, "% of Universities in top 200")
    with row_1_col_2:
        st.text("", help=get_perc_uni_top_200_query(country))

    # with row_1_col_2:
    #     plot_metric(len(df_orders["order_id"].unique()), len(df_orders_prev["order_id"].unique()), "Total orders")

    # with row_1_col_3:
    #     plot_metric(df_orders["basket_size"].mean(), df_orders_prev["basket_size"].mean(), "Average basket size")

    # with row_1_col_4:
    #     plot_metric(df_orders["days_since_prior_order"].mean(),
    #                 df_orders_prev["days_since_prior_order"].mean(), "Days between orders")

    # query = f'''
    # SELECT *
    # FROM university
    # LIMIT 10;
    # '''

    # st.write(execute_query(conn, query))

    # query = f'''
    # SELECT university.id, university.university_name, country.country_name,
    # university_year.year, university_year.num_students, university_year.student_staff_ratio,
    # university_year.pct_international_students, university_year.pct_female_students
    # FROM university
    # LEFT JOIN country
    # ON university.country_id = country.id
    # INNER JOIN university_year
    # ON university.id = university_year.university_id
    # WHERE country.country_name == 'France'
    # '''

    # st.write(execute_query(conn, query))
