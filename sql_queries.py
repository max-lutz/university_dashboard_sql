def get_perc_uni_top_200_query(country):
    query = f'''
            SELECT(
                (
                    CAST
                    (
                        (
                            SELECT COUNT(country_name)
                            FROM
                                (SELECT country.country_name
                                FROM university
                                INNER JOIN country
                                ON university.country_id = country.id
                                LEFT JOIN university_ranking_year
                                ON university.id = university_ranking_year.university_id
                                WHERE ranking_criteria_id == 21
                                GROUP BY university.university_name
                                ORDER BY AVG(university_ranking_year.score) DESC
                                LIMIT 200
                                )
                            WHERE country_name == '{country}'
                        )
                    AS FLOAT
                    )
                )
                /
                (
                    CAST
                    (
                        (
                            SELECT COUNT(*)
                            FROM university
                            INNER JOIN country
                            ON university.country_id = country.id
                            WHERE country.country_name == '{country}'
                        )
                        AS FLOAT
                    )
                )
            ) as perc_uni_top_200
        '''
    return query


def get_perc_female_students(country):
    query = f'''
        SELECT AVG(university_year.pct_female_students)
        FROM university
        LEFT JOIN country
        ON country.id == university.country_id
        LEFT JOIN university_year
        ON university.id == university_year.university_id
        WHERE country.country_name == '{country}'
    '''

    return query


def get_perc_international_students(country):
    query = f'''
        SELECT AVG(university_year.pct_international_students)
        FROM university
        LEFT JOIN country
        ON country.id == university.country_id
        LEFT JOIN university_year
        ON university.id == university_year.university_id
        WHERE country.country_name == '{country}'
    '''

    return query


def get_avg_student_staff_ratio(country):
    query = f'''
        SELECT AVG(university_year.student_staff_ratio)
        FROM university
        LEFT JOIN country
        ON country.id == university.country_id
        LEFT JOIN university_year
        ON university.id == university_year.university_id
        WHERE country.country_name == '{country}'
    '''

    return query
