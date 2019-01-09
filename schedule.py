import os
import sqlite3

databaseName = 'schedule.db'


def check_if_courses_exist(_conn):
    query_data = _conn.cursor()
    query_data.execute("""
            SELECT * FROM courses
        """)
    if query_data.rowcount != 0:
        return True
    return False


def print_table(table_name, list_of_tuples):
    print(table_name)
    for item in list_of_tuples:
        print(item)


def print_tables(_conn):
    query_data = _conn.cursor()
    query_data.execute("""
        SELECT * FROM courses
    """)
    print_table("courses", query_data.fetchall())
    query_data = _conn.cursor()
    query_data.execute("""
            SELECT * FROM classrooms
        """)
    print_table("classrooms", query_data.fetchall())
    query_data = _conn.cursor()
    query_data.execute("""
            SELECT * FROM students
        """)
    print_table("students", query_data.fetchall())


def main():
    if os.path.isfile(databaseName):
        _conn = sqlite3.connect(databaseName)
        while check_if_courses_exist():
            print_tables(_conn)


if __name__ == "__main__":
    main()
