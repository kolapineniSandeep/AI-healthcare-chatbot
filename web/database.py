import sqlite3
from sqlite3 import Error


class database(object):

    def __init__(self):
        self.conn = None

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(r"database/app.db")


        except Error as e:
            print(e)

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS  appointments (
                    name TEXT,
                    email TEXT,
                    appointment_date TEXT,
                    doctor TEXT,
                    department TEXT,
                    severity TEXT,
                    UNIQUE (appointment_date, doctor) ON CONFLICT REPLACE
                );
            """)



    def get_all_appointments(self):
        sql_query = """SELECT * FROM appointments ;"""
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        return rows;

    def add_appointment(self, name, email, appointment_date, doctor, department, severity):

        cur = self.conn.cursor()

        cur.execute(
            'INSERT INTO appointments (name, email, appointment_date, doctor, department, severity) VALUES (?, ?,?,?,?,?)',
            (name, email, appointment_date, doctor, department, severity))
        self.conn.commit()
        return cur.lastrowid

    def remove_appointment(self, email):
        sql = 'DELETE FROM appointments WHERE email=?'
        cur = self.conn.cursor()
        cur.execute(sql, (email,))
        self.conn.commit()

    def get_appointment(self, email):
        sql = f"SELECT * FROM appointments WHERE email='{email}'"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return rows

    def remove_all(self):
        sql = 'DELETE FROM appointments '
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
