    
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEMO_DIR = BASE_DIR / "demo_database"
DEMO_DIR.mkdir(exist_ok=True)

DB_PATH = DEMO_DIR / "school.db"

if DB_PATH.exists():
    print("Demo database already exists.")
    print("Existing file was NOT overwritten:", DB_PATH)
    raise SystemExit(0)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE students (
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

cur.execute("""
CREATE TABLE fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT,
    total_fee REAL DEFAULT 0,
    paid_fee REAL DEFAULT 0,
    pending_fee REAL DEFAULT 0
)
""")

cur.execute("""
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT,
    student_name TEXT,
    date TEXT,
    status TEXT
)
""")

cur.execute("""
CREATE TABLE marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT,
    student_name TEXT,
    subject TEXT,
    marks REAL,
    total_marks REAL
)
""")

students = [
    ("D101", "Aarav Sharma", 16, "Male", "10th", "XXXXXXX101", "XXXXX"),
    ("D102", "Anaya Verma", 15, "Female", "10th", "XXXXXXX102", "XXXXX"),
    ("D103", "Rohan Patel", 16, "Male", "10th", "XXXXXXX103", "XXXXX"),
    ("D104", "Meera Singh", 15, "Female", "10th", "XXXXXXX104", "XXXXX"),
    ("D105", "Kabir Joshi", 16, "Male", "10th", "XXXXXXX105", "XXXXX"),
    ("D106", "Ira Deshmukh", 15, "Female", "10th", "XXXXXXX106", "XXXXX"),
    ("D107", "Vivaan Rao", 16, "Male", "10th", "XXXXXXX107", "XXXXX"),
]

cur.executemany("""
INSERT INTO students
(roll_no, name, age, gender, class_name, phone, email)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", students)

cur.executemany("""
INSERT INTO fees (roll_no, total_fee, paid_fee, pending_fee)
VALUES (?, ?, ?, ?)
""", [
    ("D101", 20000, 15000, 5000),
    ("D102", 20000, 20000, 0),
    ("D103", 20000, 12000, 8000),
])

cur.executemany("""
INSERT INTO attendance (roll_no, student_name, date, status)
VALUES (?, ?, ?, ?)
""", [
    ("D101", "Aarav Sharma", "2026-10-20", "Present"),
    ("D102", "Anaya Verma", "2026-10-20", "Present"),
    ("D103", "Rohan Patel", "2026-10-20", "Absent"),
])

cur.executemany("""
INSERT INTO marks (roll_no, student_name, subject, marks, total_marks)
VALUES (?, ?, ?, ?, ?)
""", [
    ("D101", "Aarav Sharma", "Mathematics", 85, 100),
    ("D102", "Anaya Verma", "Science", 91, 100),
    ("D103", "Rohan Patel", "English", 78, 100),
])

conn.commit()
conn.close()

print("Demo database created successfully!")
print("Location:", DB_PATH)
print("Original database was not changed.")
