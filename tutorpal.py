import os
import sqlite3
import uuid


class Student:
    def __init__(self, name, hourly_price, discount=0):
        self.id = str(uuid.uuid4())
        self.name = name
        self.hourly_price = hourly_price
        self.discount = discount


class Tutor:
    def __init__(self, name, hourly_rate):
        self.id = str(uuid.uuid4())
        self.name = name
        self.hourly_rate = hourly_rate


class Lesson:
    def __init__(self, student_id, tutor_id, date, time, duration):
        self.id = str(uuid.uuid4())
        self.student_id = student_id
        self.tutor_id = tutor_id
        self.date = date
        self.time = time
        self.duration = duration


class TutoringSystem:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT, hourly_price REAL, discount REAL)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tutors (id TEXT PRIMARY KEY, name TEXT, hourly_rate REAL)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS lessons (id TEXT PRIMARY KEY, student_id TEXT, tutor_id TEXT, date TEXT, time TEXT, duration INTEGER)"
        )

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def add_tutor(self, name, hourly_rate):
        tutor = Tutor(name, hourly_rate)
        self.cursor.execute(
            "INSERT INTO tutors VALUES (?, ?, ?)",
            (tutor.id, tutor.name, tutor.hourly_rate),
        )
        self.connection.commit()
        print(f"Tutor '{name}' has been added to the database with id '{tutor.id}'.")
        return tutor.id

    def add_student(self, name, hourly_price, discount=0):
        student = Student(name, hourly_price, discount)
        self.cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?)",
            (student.id, student.name, student.hourly_price, student.discount),
        )
        self.connection.commit()
        print(
            f"Student '{name}' has been added to the database with id '{student.id}'."
        )
        return student.id

    def schedule_lesson(self, student_id, tutor_id, date, time, duration):
        self.cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student_row = self.cursor.fetchone()

        self.cursor.execute("SELECT * FROM tutors WHERE id = ?", (tutor_id,))
        tutor_row = self.cursor.fetchone()

        if student_row is None or tutor_row is None:
            print("Student or tutor not found in the database.")
            return None

        lesson = Lesson(student_id, tutor_id, date, time, duration)
        self.cursor.execute(
            "INSERT INTO lessons VALUES (?, ?, ?, ?, ?, ?)",
            (
                lesson.id,
                lesson.student_id,
                lesson.tutor_id,
                lesson.date,
                lesson.time,
                lesson.duration,
            ),
        )
        self.connection.commit()
        print(
            f"Lesson scheduled for student with id '{student_id}' with tutor with id '{tutor_id}' on {date} at {time} for {duration} hour(s)."
        )
        return lesson.id

    def update_student(self, id, hourly_price=None, discount=None):
        if hourly_price is not None:
            self.cursor.execute(
                "UPDATE students SET hourly_price = ? WHERE id = ?",
                (hourly_price, id),
            )
        if discount is not None:
            self.cursor.execute(
                "UPDATE students SET discount = ? WHERE id = ?", (discount, id)
            )
        self.connection.commit()
        if self.cursor.rowcount > 0:
            print(f"Student with id '{id}' has been updated.")
        else:
            print(f"Student with id '{id}' not found in the database.")

    def display_tutors(self):
        self.cursor.execute("SELECT * FROM tutors")
        rows = self.cursor.fetchall()

        print("Tutor Database:")
        for row in rows:
            id, name, hourly_rate = row
            print(f"ID: {id}")
            print(f"Name: {name}")
            print(f"Hourly Rate: £{hourly_rate}")
            print("-----------------------")

    def display_students(self):
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()

        print("Student Database:")
        for row in rows:
            id, name, hourly_price, discount = row
            print(f"ID: {id}")
            print(f"Name: {name}")
            print(f"Hourly Price: £{hourly_price}")
            print(f"Discount: {discount * 100}%")
            print("-----------------------")

    def calculate_payment(self, student_id, hours):
        self.cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = self.cursor.fetchone()

        if row is not None:
            id, name, hourly_price, discount = row
            student = Student(name, hourly_price, discount)
            payment = student.hourly_price * hours * (1 - student.discount)
            print(f"Payment for student with id '{student_id}': £{payment}")
        else:
            print(f"Student with id '{student_id}' not found in the database.")


# fresh start
if os.path.exists("tutoring.db"):
    os.remove("tutoring.db")
    print("File has been removed.")

# example usage
system = TutoringSystem("tutoring.db")
system.connect()

# add students
s1 = system.add_student("Alice", 20, 0.1)
s2 = system.add_student("Bob", 25)

# add tutors
t1 = system.add_tutor("John", 30)
t2 = system.add_tutor("Sarah", 35)

# update student
system.update_student(s1, hourly_price=22, discount=0.2)

# display student and tutor databases
system.display_students()
system.display_tutors()

# calculate payment
system.calculate_payment(s1, 5)
system.calculate_payment(s2, 3)
system.calculate_payment("Not an ID", 4)

# schedule lesson
system.schedule_lesson(s1, t1, "2023-05-20", "15:00", 2)
system.schedule_lesson(s2, t2, "2023-05-21", "14:30", 1)

system.disconnect()
