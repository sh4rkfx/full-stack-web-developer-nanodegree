#!/usr/bin/env python
import psycopg2

# Globals


query_1_result = dict()
query_2_result = dict()
query_3_result = dict()
DBNAME = "news"


# Table structures


'''
articles (author, title, slug, lead, body, "time", id)
authors (name, bio, id)
log (path, ip, method, status, "time", id)
'''


# SQL queries


'''
1. What are the most popular three articles of all time?
Which articles have been accessed the most?
Present this information as a sorted list
with the most popular article at the top.
'''
query1 = """
    SELECT title, views
    FROM view_article
    LIMIT 3;
"""

'''
2. Who are the most popular article authors of all time?
That is, when you sum up all of the articles each author has written,
which authors get the most page views?
Present this as a sorted list with the most popular author at the top.
'''
query2 = """
    SELECT authors.name, sum(view_article.views) AS views
    FROM view_article, authors
    WHERE authors.id = view_article.author
    GROUP BY authors.name
    ORDER BY views DESC;
"""

'''
3. On which day did more than 1% of requests lead to errors?
The log table includes a column status that indicates the HTTP status code
that the news site sent to the user's browser.
'''
query3 = """
    SELECT *
    FROM view_log
    WHERE "Error Percentage" > 1;
"""


# Get results from database


def get_results(query):
    con = psycopg2.connect(database=DBNAME)
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    con.close()
    return results


# Store questions and answers for each query in a dictionary


def store_results():
    global query_1_result, query_2_result, query_3_result

    query_1_result['question'] = """
    \n1. What are the most popular three articles of all time?
    Which articles have been accessed the most?\n
    """
    query_1_result['answer'] = get_results(query1)

    query_2_result['question'] = """
    \n2. Who are the most popular article authors of all time?
    That is, when you sum up all of the articles each author has written,
    which authors get the most page views?\n
    """
    query_2_result['answer'] = get_results(query2)

    query_3_result['question'] = """
    \n3. On which days did more than 1% of requests lead to errors?\n
    """
    query_3_result['answer'] = get_results(query3)


# Format output


def print_results(query_result):
    print(query_result['question'])
    for result in query_result['answer']:
        print(str(result[0]) + ': ' + str(result[1]))


# Print results


store_results()
print_results(query_1_result)
print_results(query_2_result)
print_results(query_3_result)
