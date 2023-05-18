import os

from tutoring_system import TutoringSystem

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CURRENT_DIR, "../tutoring.db")

# fresh start
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("File has been removed.")

# example usage
system = TutoringSystem(DB_PATH)

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
