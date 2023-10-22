import streamlit as st
import sqlite3
import pandas as pd


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

    query = f'''
    SELECT *
    FROM university
    LIMIT 10;
    '''

    st.write(execute_query(conn, query))

    query = f'''
    SELECT university.id, university.university_name, country.country_name, 
    university_year.year, university_year.num_students, university_year.student_staff_ratio,
    university_year.pct_international_students, university_year.pct_female_students
    FROM university
    LEFT JOIN country
    ON university.country_id = country.id
    INNER JOIN university_year
    ON university.id = university_year.university_id
    WHERE country.country_name == 'France'
    '''

    st.write(execute_query(conn, query))
