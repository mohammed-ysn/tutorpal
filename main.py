import os

from tutoring_system import TutoringSystem

# fresh start
if os.path.exists("tutoring.db"):
    os.remove("tutoring.db")
    print("File has been removed.")

# example usage
system = TutoringSystem("tutoring.db")

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
