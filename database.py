import sqlite3
import os

DATABASE = "database/school.db"


def connect_db():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DATABASE)


def add_column_if_missing(cursor, table, column, column_definition):

    cursor.execute(f"PRAGMA table_info({table})")

    columns = [row[1] for row in cursor.fetchall()]

    if column not in columns:
        cursor.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {column_definition}"
        )


def create_tables():

    conn = connect_db()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            class_name TEXT,
            phone TEXT,
            email TEXT
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL,
            total_fee REAL NOT NULL,
            paid_fee REAL NOT NULL,
            pending_fee REAL NOT NULL
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL,
            student_name TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL,
            student_name TEXT,
            subject TEXT NOT NULL,
            marks REAL NOT NULL,
            total_marks REAL NOT NULL
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            student_name TEXT NOT NULL,
            english REAL NOT NULL,
            hindi REAL NOT NULL,
            maths REAL NOT NULL,
            science REAL NOT NULL,
            computer REAL NOT NULL,
            total REAL NOT NULL,
            percentage REAL NOT NULL,
            grade TEXT NOT NULL
        )
    """)


    add_column_if_missing(
        cursor,
        "marks",
        "student_name",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "marks",
        "total_marks",
        "REAL"
    )

    add_column_if_missing(
        cursor,
        "attendance",
        "student_name",
        "TEXT"
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_tables()

    print("Database and tables created/updated successfully!")