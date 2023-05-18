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
