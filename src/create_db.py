import sys
import sqlite3

databaseName = "schedule.db"
coursesTable = "courses"
studentsTable = "students"
classroomsTable = "classrooms"


def createTables():

    return


def main(args):
    conn = sqlite3.connect(databaseName)


if __name__ == "__main__":
    main(sys.argv)
