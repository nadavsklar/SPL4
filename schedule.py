import os
import sqlite3


databaseName = "schedule.db"


def check_if_courses_exist(_conn):
    query_data = _conn.cursor()
    query_data.execute("""
            SELECT * FROM courses
        """)
    if query_data.fetchall().__len__() != 0:
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


def update_num_of_student(selected_course, _conn):
    query_set_num = _conn.cursor()
    query_set_num.execute("""
        UPDATE students
        SET count = count - """ + str(selected_course[3]) + """
        WHERE students.grade = """ + str("'" + selected_course[2] + "'") + """
    """)


def assign_course(classroom, selected_course, _conn):
    query_set_course = _conn.cursor()
    query_set_course.execute("""
        UPDATE classrooms
        SET current_course_time_left = """ + str(selected_course[5]) + """,
        current_course_id = """ + str(selected_course[0]) + """
        WHERE id = """ + str(classroom[0]) + """
    """)


def check_free_classrooms(_conn, iteration_number, fresh_occupied_classes):
    query_get_classrooms = _conn.cursor()
    query_get_classrooms.execute("""
                    SELECT * FROM classrooms
                    WHERE classrooms.current_course_time_left = 0
                """)
    list_of_classrooms = query_get_classrooms.fetchall()
    if list_of_classrooms.__len__() != 0:
        for classroom in list_of_classrooms:  # classroom is available
            query_get_courses = _conn.cursor()
            query_get_courses.execute("""
                SELECT * FROM courses
                WHERE class_id = """ + str(classroom[0]) + """
                AND id NOT IN (SELECT current_course_id FROM classrooms)
            """)
            courses = query_get_courses.fetchall()
            if courses.__len__() != 0:
                selected_course = courses[0]
                update_num_of_student(selected_course, _conn)
                print('(' + str(iteration_number) + ') ' + classroom[1] + ': ' + selected_course[1] +
                      ' is schedule to start')
                assign_course(classroom, selected_course, _conn)
                fresh_occupied_classes.append(classroom[0])


def get_course(_conn, occupied_classroom):
    query_get_course = _conn.cursor()
    query_get_course.execute("""
        SELECT * FROM courses
        WHERE id = """ + str(occupied_classroom[2]) + """
    """)
    return query_get_course.fetchall()


def delete_course(_conn, course):
    query_delete_course = _conn.cursor()
    query_delete_course.execute("""
        DELETE FROM courses
        WHERE id = """ + str(course[0][0]) + """
    """)


def free_classroom(_conn, classroom):
    query_free = _conn.cursor()
    query_free.execute("""
        UPDATE classrooms
        SET current_course_id = 0
        WHERE id = """ + str(classroom[0]) + """
    """)

def update_current_course_time_left(_conn, occupied_classroom, iteration_number, fresh_occupied_classes):
    course = get_course(_conn, occupied_classroom)
    query_update = _conn.cursor()
    query_update.execute("""
        UPDATE classrooms
        SET current_course_time_left = current_course_time_left - 1
        WHERE id = """ + str(occupied_classroom[0]) + """
    """)

    query_update.execute("""
        SELECT current_course_time_left FROM classrooms
        WHERE id = """ + str(occupied_classroom[0]) + """
    """)
    if query_update.fetchall()[0][0] == 0:  #finished
        print('(' + str(iteration_number) + ') ' + occupied_classroom[1] + ': ' + course[0][1] + ' is done')
        delete_course(_conn, course)
        free_classroom(_conn, occupied_classroom)
        check_free_classrooms(_conn, iteration_number, fresh_occupied_classes)
    else:
        print('(' + str(iteration_number) + ') ' + occupied_classroom[1] + ': occupied by ' + course[0][1])


def check_occupied_classrooms(_conn, iteration_number, fresh_occupied_classes):
    query_get_classrooms = _conn.cursor()
    query_get_classrooms.execute("""
        SELECT classrooms.id, classrooms.location, classrooms.current_course_id, classrooms.current_course_time_left
        FROM classrooms
        JOIN courses ON courses.id = classrooms.current_course_id
        WHERE NOT classrooms.current_course_time_left = 0
    """)
    list_of_classrooms = query_get_classrooms.fetchall()
    if list_of_classrooms.__len__() != 0:
        for classroom in list_of_classrooms:
            if not fresh_occupied_classes.__contains__(classroom[0]):
                update_current_course_time_left(_conn, classroom, iteration_number, fresh_occupied_classes)


def main():
    if os.path.isfile(databaseName):
        _conn = sqlite3.connect(databaseName)
        fresh_occupied_classes = []
        iteration_number = 0
        while check_if_courses_exist(_conn):
            check_free_classrooms(_conn, iteration_number, fresh_occupied_classes)
            check_occupied_classrooms(_conn, iteration_number, fresh_occupied_classes)
            print_tables(_conn)
            iteration_number = iteration_number + 1
            fresh_occupied_classes.clear()


if __name__ == "__main__":
    main()
