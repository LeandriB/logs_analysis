#!/usr/bin/env python3

import psycopg2
# Imports postgresql library
DBNAME = "news"

question_1 = "What are the most popular articles of all time?"
query_1 = """SELECT title, views
             FROM articles
             JOIN
                 (SELECT path, count(path) AS views
                  FROM log
                  GROUP BY log.path) AS log
             ON log.path = '/article/' || articles.slug
             ORDER BY views desc
             LIMIT 3;"""

question_2 = "Who are the most popular authors of all time?"
query_2 = """SELECT name, count(*) AS views
             FROM articles
             JOIN authors
             ON articles.author = authors.id
             JOIN log
             ON concat('/article/', articles.slug) = log.path
             WHERE log.status = '200 OK'
             GROUP BY authors.name
             ORDER BY views desc
             LIMIT 3;"""

question_3 = "On which days did more than 1% of requests lead to errors?"
query_3 = """SELECT errors.date, round(100.0*countError/countLog,2) AS percent
             FROM logs, errors
             WHERE logs.date = errors.date
             AND countError > countLog/100;"""


class newsQuery:
    '''Defining a class with four methods assoctiated with it in
       order to connect to the database, execute queries, fetching
       results and closing the connection.'''
    def __init__(self):
        try:
            self.db = psycopg2.connect(database=DBNAME)
            # Connect to the database
            self.cursor = self.db.cursor()
        except Exception as error:
            # Except statement
            print "Error connecting to database"

    def execute_query(self, query):
        self.cursor.execute(query)
        # Execute query
        results = self.cursor.fetchall()
        # Fetch all results
        return results

    def output(self, question, query, suffix="views"):
        # Runs the query and prints out questions
        result = self.execute_query(query)
        print question
        for i in range(len(result)):
            print "\t", i + 1, ".", result[i][0], "-", result[i][1], suffix

        print "\n"
        # Prints a blank line between questions

    def close(self):
        self.db.commit()
        self.db.close()
        # Closes connection


if __name__ == '__main__':
    # Prints results for queries
    data = newsQuery()
    data.output(question_1, query_1)
    data.output(question_2, query_2)
    data.output(question_3, query_3, "% errors")
    print "Query was successful\n"
