import sqlite3


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_one(self):
        return self.cursor.fetchone()

    def fetch_all(self):
        return self.cursor.fetchall()

    def description(self):
        return self.cursor.description

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
