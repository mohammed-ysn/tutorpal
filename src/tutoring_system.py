from database import Database
from models import Lesson, Student, Tutor
from str_utils import print_table, truncate_str


class TutoringSystem:
    def __init__(self, db_file):
        self.db = Database(db_file)
        self.create_tables()

    def create_tables(self):
        with self.db:
            self.db.execute_query(
                "CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT, hourly_price REAL, discount REAL)"
            )
            self.db.execute_query(
                "CREATE TABLE IF NOT EXISTS tutors (id TEXT PRIMARY KEY, name TEXT, hourly_rate REAL)"
            )
            self.db.execute_query(
                "CREATE TABLE IF NOT EXISTS lessons (id TEXT PRIMARY KEY, student_id TEXT, tutor_id TEXT, date TEXT, time TEXT, duration INTEGER)"
            )

    def add_tutor(self, name, hourly_rate):
        tutor = Tutor(name, hourly_rate)
        with self.db:
            self.db.execute_query(
                "INSERT INTO tutors VALUES (?, ?, ?)",
                (tutor.id, tutor.name, tutor.hourly_rate),
            )
        print(f"Tutor {name} added [{truncate_str(tutor.id)}].")
        return tutor.id

    def add_student(self, name, hourly_price, discount=0):
        student = Student(name, hourly_price, discount)
        with self.db:
            self.db.execute_query(
                "INSERT INTO students VALUES (?, ?, ?, ?)",
                (student.id, student.name, student.hourly_price, student.discount),
            )
        print(f"Student {name} added [{truncate_str(student.id)}].")
        return student.id

    def schedule_lesson(self, student_id, tutor_id, date, time, duration):
        with self.db:
            self.db.execute_query("SELECT * FROM students WHERE id = ?", (student_id,))
            student_row = self.db.fetch_one()

            self.db.execute_query("SELECT * FROM tutors WHERE id = ?", (tutor_id,))
            tutor_row = self.db.fetch_one()

            if student_row is None or tutor_row is None:
                print("Student or tutor not found in the database.")
                return None

            lesson = Lesson(student_id, tutor_id, date, time, duration)
            self.db.execute_query(
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
        print(f"Lesson scheduled for {date} at {time} for {duration} hour(s).")
        print(f"\tStudent: {student_row[1]} [{truncate_str(student_id)}]")
        print(f"\tTutor: {tutor_row[1]} [{truncate_str(tutor_id)}]")
        return lesson.id

    def update_student(self, id, hourly_price=None, discount=None):
        query = "UPDATE students SET "
        params = []

        if hourly_price is not None:
            query += "hourly_price = ?, "
            params.append(hourly_price)
        if discount is not None:
            query += "discount = ?, "
            params.append(discount)

        # remove the trailing comma and space
        query = query[:-2]
        query += " WHERE id = ?"
        params.append(id)

        with self.db:
            self.db.execute_query(query, tuple(params))

        if self.db.cursor.rowcount > 0:
            print(f"Student with id [{truncate_str(id)}] has been updated.")
        else:
            print(f"Student with id [{truncate_str(id)}] not found in the database.")

    def display_tutors(self):
        print("Tutor Database:")
        with self.db:
            self.db.execute_query("SELECT * FROM tutors")
            headers = [desc[0] for desc in self.db.description()]
            print_table(rows=self.db.fetch_all(), headers=headers)

    def display_students(self):
        print("Student Database:")
        with self.db:
            self.db.execute_query("SELECT * FROM students")
            headers = [desc[0] for desc in self.db.description()]
            print_table(rows=self.db.fetch_all(), headers=headers)

    def calculate_payment(self, student_id, hours):
        with self.db:
            self.db.execute_query("SELECT * FROM students WHERE id = ?", (student_id,))
            row = self.db.fetch_one()

        if row is not None:
            id, name, hourly_price, discount = row
            student = Student(name, hourly_price, discount)
            payment = student.hourly_price * hours * (1 - student.discount)
            print(
                f"Payment for student with id [{truncate_str(student_id)}]: £{payment}"
            )
        else:
            print(
                f"Student with id [{truncate_str(student_id)}] not found in the database."
            )
