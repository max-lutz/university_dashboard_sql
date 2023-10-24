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


def get_ranking_criteria_list(conn):
    query = f'''
        SELECT ranking_criteria.criteria_name
        FROM ranking_criteria
        WHERE ranking_criteria.id > 13
    '''
    df_criterias = execute_query(conn, query)
    return df_criterias.iloc[:, 0].to_list()


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


def plot_gauge(value, title, suffix):
    fig = go.Figure(
        go.Indicator(
            value=value,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": "green"},
            },
            title={
                "text": title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)


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

    with row_1_col_3:
        df = execute_query(conn, get_perc_female_students(country))
        plot_metric(df.iloc[0, 0], "% of female students")
    with row_1_col_4:
        st.text("", help=get_perc_female_students(country))

    with row_1_col_5:
        df = execute_query(conn, get_perc_international_students(country))
        plot_metric(df.iloc[0, 0], "% of international students")
    with row_1_col_6:
        st.text("", help=get_perc_international_students(country))

    with row_1_col_7:
        df = execute_query(conn, get_avg_student_staff_ratio(country))
        plot_metric(df.iloc[0, 0], "Average student staff ratio")
    with row_1_col_8:
        st.text("", help=get_avg_student_staff_ratio(country))

    row_2_col_1, row_2_col_2, row_2_col_3, row_2_col_4, row_2_col_5, row_2_col_6 = st.columns(
        (ROW, 0.1, ROW, 0.1, ROW, 0.1))
    with row_2_col_1:
        ranking_criterias = get_ranking_criteria_list(conn)
        row_3_col_1, row_3_col_2 = st.columns(2)
        with row_3_col_1:
            criteria_1 = st.selectbox('Criteria 1', ranking_criterias)
        with row_3_col_2:
            criteria_2 = st.selectbox('Criteria 2', ranking_criterias)

        query = f'''
            SELECT 
                country.country_name,
                university.university_name,
                university_ranking_year.year, 
                ranking_criteria.criteria_name,
                university_ranking_year.score
            FROM university
            LEFT JOIN country
            ON country.id == university.country_id
            RIGHT JOIN university_ranking_year
            ON university.id = university_ranking_year.university_id
            LEFT JOIN ranking_criteria
            ON ranking_criteria.id == university_ranking_year.ranking_criteria_id
            
            WHERE country.country_name == '{country}' AND university_ranking_year.year == 2015
            AND (ranking_criteria.criteria_name == '{criteria_1}' OR ranking_criteria.criteria_name == '{criteria_2}')
        '''
        df_scores = execute_query(conn, query)
        df_scores = df_scores[['university_name', 'criteria_name', 'score']]

        if (len(df_scores['criteria_name'].unique()) == 1):
            pass
        else:
            df_scores = df_scores.pivot(index='university_name', columns='criteria_name')['score']

            fig = px.scatter(df_scores, x=criteria_1, y=criteria_2)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            st.write(df_scores)

    with row_2_col_2:
        pass

    # query = f'''
    # SELECT university_ranking_year.ranking_criteria_id, university_ranking_year.year, COUNT(university.id)
    # FROM university
    # INNER JOIN university_ranking_year
    # ON university.id = university_ranking_year.university_id
    # GROUP BY university_ranking_year.ranking_criteria_id, university_ranking_year.year
    # '''

    # st.write(execute_query(conn, query))
