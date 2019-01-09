import sys
import sqlite3

databaseName = "schedule.db"
coursesTable = "courses"
studentsTable = "students"
classroomsTable = "classrooms"
_conn = sqlite3.connect(databaseName)

def createTables():
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
            number_of_students      INTEGER     NOT NULL,
            class_id                INTEGER     REFERENCES classrooms(id),
            course_length           INTEGER     NOT NULL
        );
    """)


def main(args):
    # conn = sqlite3.connect(databaseName)
    createTables()
    print("hello")


if __name__ == "__main__":
    main(sys.argv)
