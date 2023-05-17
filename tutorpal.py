import os
import sqlite3


class Student:
    def __init__(self, name, hourly_price, discount=0):
        self.name = name
        self.hourly_price = hourly_price
        self.discount = discount


class Tutor:
    def __init__(self, name, hourly_rate):
        self.name = name
        self.hourly_rate = hourly_rate


class Lesson:
    def __init__(self, student_name, tutor_name, date, time, hours):
        self.student_name = student_name
        self.tutor_name = tutor_name
        self.date = date
        self.time = time
        self.hours = hours


class TutoringSystem:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS students (name TEXT, hourly_price REAL, discount REAL)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tutors (name TEXT, hourly_rate REAL)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS lessons (student_name TEXT, tutor_name TEXT, date TEXT, time TEXT, hours INTEGER)"
        )

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def add_tutor(self, name, hourly_rate):
        self.cursor.execute("INSERT INTO tutors VALUES (?, ?)", (name, hourly_rate))
        self.connection.commit()
        print(f"Tutor '{name}' has been added to the database.")

    def add_student(self, name, hourly_price, discount=0):
        self.cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?)", (name, hourly_price, discount)
        )
        self.connection.commit()
        print(f"Student '{name}' has been added to the database.")

    def schedule_lesson(self, student_name, tutor_name, date, time, hours):
        self.cursor.execute("SELECT * FROM students WHERE name = ?", (student_name,))
        student_row = self.cursor.fetchone()

        self.cursor.execute("SELECT * FROM tutors WHERE name = ?", (tutor_name,))
        tutor_row = self.cursor.fetchone()

        if student_row is not None and tutor_row is not None:
            lesson = Lesson(student_name, tutor_name, date, time, hours)
            self.cursor.execute(
                "INSERT INTO lessons VALUES (?, ?, ?, ?, ?)",
                (
                    lesson.student_name,
                    lesson.tutor_name,
                    lesson.date,
                    lesson.time,
                    lesson.hours,
                ),
            )
            self.connection.commit()
            print(
                f"Lesson scheduled for '{student_name}' with tutor '{tutor_name}' on {date} at {time} for {hours} hour(s)."
            )
        else:
            print("Student or tutor not found in the database.")

    def update_student(self, name, hourly_price=None, discount=None):
        if hourly_price is not None:
            self.cursor.execute(
                "UPDATE students SET hourly_price = ? WHERE name = ?",
                (hourly_price, name),
            )
        if discount is not None:
            self.cursor.execute(
                "UPDATE students SET discount = ? WHERE name = ?", (discount, name)
            )
        self.connection.commit()
        if self.cursor.rowcount > 0:
            print(f"Student '{name}' has been updated.")
        else:
            print(f"Student '{name}' not found in the database.")

    def display_tutors(self):
        self.cursor.execute("SELECT * FROM tutors")
        rows = self.cursor.fetchall()

        print("Tutor Database:")
        for row in rows:
            name, hourly_rate = row
            print(f"Name: {name}")
            print(f"Hourly Rate: £{hourly_rate}")
            print("-----------------------")

    def display_students(self):
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()

        print("Student Database:")
        for row in rows:
            name, hourly_price, discount = row
            print(f"Name: {name}")
            print(f"Hourly Price: £{hourly_price}")
            print(f"Discount: {discount * 100}%")
            print("-----------------------")

    def calculate_payment(self, name, hours):
        self.cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        row = self.cursor.fetchone()

        if row is not None:
            name, hourly_price, discount = row
            student = Student(name, hourly_price, discount)
            payment = student.hourly_price * hours * (1 - student.discount)
            print(f"Payment for '{name}': £{payment}")
        else:
            print(f"Student '{name}' not found in the database.")


# fresh start
if os.path.exists("tutoring.db"):
    os.remove("tutoring.db")
    print("File has been removed.")

# example usage
system = TutoringSystem("tutoring.db")
system.connect()

# add students
system.add_student("Alice", 20, 0.1)
system.add_student("Bob", 25)

# add tutors
system.add_tutor("John", 30)
system.add_tutor("Sarah", 35)

# update student
system.update_student("Alice", hourly_price=22, discount=0.2)

# display student and tutor databases
system.display_students()
system.display_tutors()

# calculate payment
system.calculate_payment("Alice", 5)
system.calculate_payment("Bob", 3)
system.calculate_payment("Charlie", 4)

# schedule lesson
system.schedule_lesson("Alice", "John", "2023-05-20", "15:00", 2)
system.schedule_lesson("Bob", "Sarah", "2023-05-21", "14:30", 1)

system.disconnect()
