import sys
import sqlite3
import os

databaseName = "schedule.db"
coursesTable = "courses"
studentsTable = "students"
classroomsTable = "classrooms"

def createTables(_conn):
    _conn.executescript("""
        CREATE TABLE students (
            grade      TEXT      PRIMARY KEY,
            count      INTEGER   NOT NULL
        );

        CREATE TABLE classrooms (
            id                          INTEGER         PRIMARY KEY,
            location                    TEXT            NOT NULL,
            current_course_id           INTEGER         NOT NULL,
            current_course_time_left    INTEGER         NOT NULL
        );

        CREATE TABLE courses (
            id                      INTEGER     PRIMARY KEY,
            course_name             TEXT        NOT NULL,
            student                 TEXT        NOT NULL,
            number_of_students      INTEGER     NOT NULL,
            class_id                INTEGER     REFERENCES classrooms(id),
            course_length           INTEGER     NOT NULL
        );
    """)


def insert_to_students(details, _conn):
    _conn.execute("""
        INSERT INTO students (grade, count) VALUES (?, ?)
    """, [details[1], details[2]])


def insert_to_courses(details, _conn):
    _conn.execute("""
            INSERT INTO courses (id, course_name, student, number_of_students, class_id, course_length) 
                VALUES (?, ?, ?, ?, ?, ?)
        """, [details[1], details[2], details[3], details[4], details[5], details[6]])


def insert_to_classrooms(details, _conn):
    _conn.execute("""
            INSERT INTO classrooms (id, location, current_course_id, current_course_time_left) VALUES (?, ?, 0, 0)
        """, [details[1], details[2]])


def initiate_tables_with_values(config_file_path, _conn):
    file = open(config_file_path, "r")
    for line in file:
        line = line.strip()
        details = line.split(', ')
        if details[0] == 'S':
            insert_to_students(details, _conn)
        elif details[0] == 'R':
            insert_to_classrooms(details, _conn)
        elif details[0] == 'C':
            insert_to_courses(details, _conn)


def main(args):
    if os.path.isfile(databaseName):
        print("db exists")
    _conn = sqlite3.connect(databaseName)
#    createTables(_conn)
    initiate_tables_with_values("/home/nadavsklar/PycharmProjects/SPL4/src/config1.txt", _conn)


if __name__ == "__main__":
    main(sys.argv)
