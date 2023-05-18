#IMPORTS
import sqlite3 as sql

#DATA
db_file = "student.sqlite"


sql_create_table_students ="""
CREATE TABLE IF NOT EXISTS student (
    fname TEXT,
    lname TEXT,
    score INT    
);
"""
sql_select_all_students = """
SELECT rowid, *
FROM student;
"""

sql_insert_student = """
INSERT INTO STUDENT VALUES
(?, ?, ?);
"""

sql_select_gt_score = """
SELECT rowid, *
FROM student
WHERE score >= ?;
"""

#MAIN

#check if database exists, if not create it
with sql.connect(db_file) as conn:

    conn.execute(sql_create_table_students)

    while 1:
        print("\nStudent Database:\n\n"
              "1) Show All\n"
              "2) Add Student\n"
              "3) Show by Score\n"
              "0) Quit\n\n"
        )
        option = input("Select Option:")

        if option == "1":

            cur = conn.execute(sql_select_all_students)
            students = cur.fetchall()

            if students:
                for student in students:
                    # *student extracts the student tuple into individual values
                    print("{:3}) {:10} {:10} {:10}".format(*student))

            else:
                print("students table is empty")


        elif option == "2":

            fname = input("enter first name:")
            lname = input("enter last name:")
            score = int(input("enter score:"))

            conn.execute(sql_insert_student, (fname, lname, score))

        elif option == "3":
            score = int(input("enter minimum score:"))
            cur = conn.execute(sql_select_gt_score, (score,))

            students = cur.fetchall()

            if students:
                for student in students:
                    print("{:3}) {:10} {:10} {:10}".format(*student))
            else:
                print("no students with score higher than", score)

        elif option == "0":
            break
        else:
            input("invalid option. press enter to continue...")

print("goodbye")














