import sqlite3

connect = sqlite3.connect('studentDB.db', check_same_thread=False)
cursor = connect.cursor()

# Создание таблицы
cursor.execute("CREATE TABLE IF NOT EXISTS students"
               "(fac TEXT NOT NULL,"
               "course TEXT NOT NULL,"
               "class TEXT NOT NULL,"
               "student TEXT NOT NULL)")


def add_to_db(student_lst):
    # Добавление в БД
    cursor.executemany("INSERT INTO students VALUES (?,?,?,?)", student_lst)
    connect.commit()


def update_db(student_lst):
    # Полное обновление БД
    cursor.execute("DELETE FROM students")
    add_to_db(student_lst)


def get_from_db(column, arg):
    # Возваращает список из БД столбца column со значением arg
    req = "SELECT * FROM students WHERE {col_name}=?"
    cursor.execute(req.format(col_name=column), [arg])
    answer = cursor.fetchall()
    return answer


def get_student(name):
    # Возвращает список студентов со значением name
    args = ['%%', '%%', '%%', '%%', '%%', '%%']
    name = ['%'+i+'%' for i in name.split()]
    args[:len(name)] = name
    req = "SELECT * FROM students WHERE " \
          "student LIKE ?" \
          "AND student LIKE ?" \
          "AND student LIKE ?" \
          "AND student LIKE ?" \
          "AND student LIKE ?" \
          "AND student LIKE ?"
    cursor.execute(req, args)
    answer = cursor.fetchall()
    return answer


def get_courses(fac):
    # Возвращает список курсов факультета fac
    req = "SELECT course FROM students WHERE fac=?"
    cursor.execute(req, [fac])
    answer = cursor.fetchall()
    return answer


def get_groups(fac, course):
    # Возвращает список групп факультета fac и курса course
    req = "SELECT class FROM students WHERE fac=? AND course=?"
    cursor.execute(req, [fac, course])
    answer = cursor.fetchall()
    return answer


def get_group_list(group):
    # Возвращает список студентов группы group
    args = [group[0], group[1], group[2] + group[3]]
    req = "SELECT * FROM students WHERE " \
          "fac LIKE ? " \
          "AND course LIKE ? " \
          "AND class LIKE ?"
    cursor.execute(req, args)
    answer = cursor.fetchall()
    return answer


def count():
    # Возвращает количество строк в БД
    req = "SELECT COUNT(*) FROM students"
    cursor.execute(req)
    answer = cursor.fetchall()
    return answer
