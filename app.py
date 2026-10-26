
import os
import sqlite3
from pathlib import Path
from functools import wraps
from flask import Flask, request, redirect, url_for, session, render_template_string, flash

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SCHOOL_APP_SECRET", "replace-this-secret-before-deployment"
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "demo_database" / "school.db"
ADMIN_USERNAME = os.environ.get("SCHOOL_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("SCHOOL_ADMIN_PASSWORD", "ChangeMe123!")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper


CSS = """
*{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif;background:#f1f5f9;color:#172033}
header{background:#173b70;color:white;padding:22px 5%;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
header a{color:white;margin-left:12px;text-decoration:none}
.wrap{max-width:1150px;margin:25px auto;padding:0 18px}
nav{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}
nav a,.btn,button{background:#2458a6;color:white;border:0;border-radius:7px;padding:10px 14px;text-decoration:none;cursor:pointer;font-size:14px}
.btn.secondary{background:#64748b}
.card{background:white;padding:20px;border-radius:12px;box-shadow:0 3px 12px #0000000c;margin-bottom:18px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px}
.num{font-size:30px;font-weight:bold;color:#2563eb}
label{display:block;font-weight:bold;margin:10px 0 5px}
input,select{width:100%;padding:10px;border:1px solid #cbd5e1;border-radius:6px}
.formgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
table{width:100%;border-collapse:collapse;min-width:650px}
th,td{text-align:left;padding:11px;border-bottom:1px solid #e2e8f0}
th{background:#eaf1fb}
.tablewrap{overflow-x:auto}
.flash{padding:11px;margin:10px 0;border-radius:7px;background:#dcfce7;color:#166534}
.error{background:#fee2e2;color:#991b1b}
.small{font-size:13px;color:#64748b}
.login{max-width:430px;margin:50px auto}
"""

LAYOUT = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }} | School Management System</title>
<style>{{ css }}</style>
</head>
<body>
<header>
  <div>
    <strong>🏫 School Management System</strong>
    <div style="color:#dbeafe;font-size:13px">Recruiter demo</div>
  </div>
  <div>
    {% if is_admin %}
      <span>Admin mode</span>
      <a href="{{ url_for('logout') }}">Log out</a>
    {% else %}
      <a href="{{ url_for('login') }}">Admin login</a>
    {% endif %}
  </div>
</header>
<div class="wrap">
<nav>
  <a href="{{ url_for('home') }}">Dashboard</a>
  <a href="{{ url_for('students') }}">Students</a>
  <a href="{{ url_for('fees') }}">Fees</a>
  <a href="{{ url_for('attendance') }}">Attendance</a>
  <a href="{{ url_for('marks') }}">Marks</a>
  <a href="{{ url_for('reports') }}">Reports</a>
</nav>
{% for category,message in get_flashed_messages(with_categories=true) %}
  <div class="flash {{ 'error' if category=='error' else '' }}">{{ message }}</div>
{% endfor %}
{{ body|safe }}
</div>
</body>
</html>
"""


def page(title, body, **kwargs):
    return render_template_string(
        LAYOUT,
        title=title,
        body=render_template_string(body, **kwargs),
        css=CSS,
        is_admin=bool(session.get("admin"))
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form.get("username") == ADMIN_USERNAME
            and request.form.get("password") == ADMIN_PASSWORD
        ):
            session.clear()
            session["admin"] = True
            return redirect(request.args.get("next") or url_for("home"))
        flash("Username or password is incorrect.", "error")

    body = """
    <div class="card login">
      <h1>Admin login</h1>
      <form method="post">
        <label>Username</label>
        <input name="username" required autocomplete="username">
        <label>Password</label>
        <input type="password" name="password" required autocomplete="current-password">
        <p><button>Log in</button></p>
      </form>
      <p class="small">
        Local demo login: admin / ChangeMe123!
        Change credentials before deployment.
      </p>
    </div>
    """
    return page("Admin login", body)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/")
def home():
    with get_db() as db:
        student_count = db.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        fee_count = db.execute("SELECT COUNT(*) FROM fees").fetchone()[0]
        attendance_count = db.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
        marks_count = db.execute("SELECT COUNT(*) FROM marks").fetchone()[0]

    body = """
    <h1>Dashboard</h1>
    <p>Welcome to the School Management System demo.</p>
    <div class="cards">
      <div class="card"><h2>Students</h2><div class="num">{{ student_count }}</div><p>Student records</p></div>
      <div class="card"><h2>Fees</h2><div class="num">{{ fee_count }}</div><p>Fee records</p></div>
      <div class="card"><h2>Attendance</h2><div class="num">{{ attendance_count }}</div><p>Attendance records</p></div>
      <div class="card"><h2>Marks</h2><div class="num">{{ marks_count }}</div><p>Marks records</p></div>
    </div>
    <div class="card">
      <h2>Recruiter demo</h2>
      <p>Visitors can view records. Only admin can add or edit. Delete is disabled.</p>
    </div>
    """
    return page(
        "Dashboard", body,
        student_count=student_count,
        fee_count=fee_count,
        attendance_count=attendance_count,
        marks_count=marks_count
    )


STUDENT_PAGE = """
<h1>Student Management</h1>

{% if is_admin %}
<div class="card">
  <h2>{{ 'Update student' if student else 'Add student' }}</h2>
  <form method="post" action="{{ url_for('save_student') }}">
    <input type="hidden" name="id" value="{{ student['id'] if student else '' }}">
    <div class="formgrid">
      <div>
        <label>Roll number *</label>
        <input name="roll_no" required value="{{ student['roll_no'] if student else '' }}"
          {{ 'readonly' if student else '' }}>
      </div>
      <div>
        <label>Name *</label>
        <input name="name" required value="{{ student['name'] if student else '' }}">
      </div>
      <div>
        <label>Age</label>
        <input type="number" min="1" max="120" name="age"
          value="{{ student['age'] if student and student['age'] is not none else '' }}">
      </div>
      <div>
        <label>Gender</label>
        <select name="gender">
          <option value="">Select</option>
          {% for g in ['Female','Male','Other'] %}
          <option value="{{ g }}" {{ 'selected' if student and student['gender']==g else '' }}>{{ g }}</option>
          {% endfor %}
        </select>
      </div>
      <div>
        <label>Class</label>
        <input name="class_name" value="{{ student['class_name'] if student else '' }}">
      </div>
      <div>
        <label>Phone</label>
        <input name="phone" value="{{ student['phone'] if student else '' }}">
      </div>
      <div>
        <label>Email</label>
        <input type="email" name="email" value="{{ student['email'] if student else '' }}">
      </div>
    </div>
    <p>
      <button>{{ 'Save changes' if student else 'Add student' }}</button>
      {% if student %}
      <a class="btn secondary" href="{{ url_for('students') }}">Cancel</a>
      {% endif %}
    </p>
  </form>
</div>
{% else %}
<div class="card">
  <strong>Read-only demo.</strong>
  Admin login is required to add or edit. Delete is disabled.
</div>
{% endif %}

<div class="card">
  <h2>Student records ({{ rows|length }})</h2>
  <form method="get">
    <div class="formgrid">
      <div>
        <label>Search name, roll no, class or phone</label>
        <input name="search" value="{{ search }}" placeholder="Type to search">
      </div>
    </div>
    <p>
      <button>Search</button>
      <a class="btn secondary" href="{{ url_for('students') }}">Show all</a>
    </p>
  </form>

  <div class="tablewrap">
    <table>
      <tr>
        <th>Roll No</th><th>Name</th><th>Age</th><th>Gender</th>
        <th>Class</th><th>Phone</th><th>Email</th>
        {% if is_admin %}<th>Action</th>{% endif %}
      </tr>

      {% for s in rows %}
      <tr>
        <td>{{ s['roll_no'] }}</td>
        <td>{{ s['name'] }}</td>
        <td>{{ s['age'] if s['age'] is not none else '-' }}</td>
        <td>{{ s['gender'] or '-' }}</td>
        <td>{{ s['class_name'] or '-' }}</td>

        <td>
          {% if s['phone'] %}
            {{ 'X' * ([s['phone']|string|length - 3, 0]|max) }}{{ (s['phone']|string)[-3:] }}
          {% else %}
            -
          {% endif %}
        </td>
        <td>{{ 'XXXXX' if s['email'] else '-' }}</td>

        {% if is_admin %}
        <td><a class="btn secondary" href="{{ url_for('students', edit=s['id']) }}">Edit</a></td>
        {% endif %}
      </tr>
      {% else %}
      <tr><td colspan="8">No matching records.</td></tr>
      {% endfor %}
    </table>
  </div>
</div>
"""


@app.route("/students")
def students():
    search = request.args.get("search", "").strip()
    edit_id = request.args.get("edit", type=int)

    with get_db() as db:
        if search:
            term = f"%{search}%"
            rows = db.execute(
                """SELECT * FROM students
                   WHERE roll_no LIKE ? OR name LIKE ?
                   OR class_name LIKE ? OR phone LIKE ?
                   ORDER BY name""",
                (term, term, term, term)
            ).fetchall()
        else:
            rows = db.execute("SELECT * FROM students ORDER BY name").fetchall()

        student = (
            db.execute("SELECT * FROM students WHERE id=?", (edit_id,)).fetchone()
            if edit_id and session.get("admin") else None
        )

    return page(
        "Students", STUDENT_PAGE, rows=rows, student=student,
        search=search, is_admin=bool(session.get("admin"))
    )


@app.route("/students/save", methods=["POST"])
@admin_required
def save_student():
    form = request.form
    roll = form.get("roll_no", "").strip()
    name = form.get("name", "").strip()

    if not roll or not name:
        flash("Roll number and name are required.", "error")
        return redirect(url_for("students"))

    try:
        age_text = form.get("age", "").strip()
        age = int(age_text) if age_text else None
        if age is not None and not 1 <= age <= 120:
            raise ValueError
    except ValueError:
        flash("Age must be a number from 1 to 120.", "error")
        return redirect(url_for("students"))

    fields = (
        name, age, form.get("gender", "").strip(),
        form.get("class_name", "").strip(),
        form.get("phone", "").strip(), form.get("email", "").strip()
    )

    try:
        with get_db() as db:
            student_id = form.get("id", "").strip()
            if student_id:
                db.execute(
                    """UPDATE students
                       SET name=?,age=?,gender=?,class_name=?,phone=?,email=?
                       WHERE id=?""",
                    fields + (int(student_id),)
                )
                flash("Student updated.")
            else:
                db.execute(
                    """INSERT INTO students
                       (roll_no,name,age,gender,class_name,phone,email)
                       VALUES (?,?,?,?,?,?,?)""",
                    (roll,) + fields
                )
                flash("Student added.")
    except sqlite3.IntegrityError:
        flash("That roll number already exists. Use a unique roll number.", "error")

    return redirect(url_for("students"))


FEES_PAGE = """
<h1>Fees</h1>
{% if is_admin %}
<div class="card">
  <h2>Add fee record</h2>
  <form method="post" action="{{ url_for('add_fee') }}">
    <div class="formgrid">
      <div>
        <label>Student *</label>
        <select name="roll_no" required>
          <option value="">Choose</option>
          {% for s in students %}
          <option value="{{ s['roll_no'] }}">{{ s['roll_no'] }} — {{ s['name'] }}</option>
          {% endfor %}
        </select>
      </div>
      <div><label>Total fee</label><input type="number" min="0" step=".01" name="total_fee" required></div>
      <div><label>Paid fee</label><input type="number" min="0" step=".01" name="paid_fee" required></div>
    </div>
    <p><button>Add fee record</button></p>
  </form>
</div>
{% endif %}
<div class="card">
  <h2>Fee records</h2>
  <div class="tablewrap">
    <table>
      <tr><th>Roll No</th><th>Total</th><th>Paid</th><th>Pending</th></tr>
      {% for f in records %}
      <tr>
        <td>{{ f['roll_no'] }}</td>
        <td>₹{{ '%.2f'|format(f['total_fee']) }}</td>
        <td>₹{{ '%.2f'|format(f['paid_fee']) }}</td>
        <td>₹{{ '%.2f'|format(f['pending_fee']) }}</td>
      </tr>
      {% else %}
      <tr><td colspan="4">No fee records.</td></tr>
      {% endfor %}
    </table>
  </div>
</div>
"""


@app.route("/fees")
def fees():
    with get_db() as db:
        students = db.execute("SELECT roll_no,name FROM students ORDER BY name").fetchall()
        records = db.execute("SELECT * FROM fees ORDER BY id DESC").fetchall()
    return page("Fees", FEES_PAGE, students=students, records=records,
                is_admin=bool(session.get("admin")))


@app.route("/fees/add", methods=["POST"])
@admin_required
def add_fee():
    try:
        roll = request.form["roll_no"]
        total = float(request.form["total_fee"])
        paid = float(request.form["paid_fee"])
        if total < 0 or paid < 0 or paid > total:
            raise ValueError

        with get_db() as db:
            if not db.execute("SELECT 1 FROM students WHERE roll_no=?", (roll,)).fetchone():
                flash("Choose an existing student.", "error")
            else:
                db.execute(
                    "INSERT INTO fees (roll_no,total_fee,paid_fee,pending_fee) VALUES (?,?,?,?)",
                    (roll, total, paid, total - paid)
                )
                flash("Fee record added.")
    except (ValueError, KeyError):
        flash("Invalid amounts. Paid fee cannot exceed total fee.", "error")

    return redirect(url_for("fees"))


ATTENDANCE_PAGE = """
<h1>Attendance</h1>
{% if is_admin %}
<div class="card">
  <h2>Mark attendance</h2>
  <form method="post" action="{{ url_for('add_attendance') }}">
    <div class="formgrid">
      <div>
        <label>Student</label>
        <select name="roll_no" required>
          <option value="">Choose</option>
          {% for s in students %}
          <option value="{{ s['roll_no'] }}">{{ s['roll_no'] }} — {{ s['name'] }}</option>
          {% endfor %}
        </select>
      </div>
      <div><label>Date</label><input type="date" name="date" value="{{ today }}" required></div>
      <div>
        <label>Status</label>
        <select name="status"><option>Present</option><option>Absent</option><option>Late</option></select>
      </div>
    </div>
    <p><button>Save attendance</button></p>
  </form>
</div>
{% endif %}
<div class="card">
  <h2>Attendance records</h2>
  <div class="tablewrap">
    <table>
      <tr><th>Date</th><th>Roll No</th><th>Student</th><th>Status</th></tr>
      {% for a in records %}
      <tr><td>{{ a['date'] }}</td><td>{{ a['roll_no'] }}</td><td>{{ a['student_name'] }}</td><td>{{ a['status'] }}</td></tr>
      {% else %}
      <tr><td colspan="4">No attendance records.</td></tr>
      {% endfor %}
    </table>
  </div>
</div>
"""


@app.route("/attendance")
def attendance():
    from datetime import date
    with get_db() as db:
        students = db.execute("SELECT roll_no,name FROM students ORDER BY name").fetchall()
        records = db.execute(
            "SELECT * FROM attendance ORDER BY date DESC,id DESC LIMIT 500"
        ).fetchall()
    return page(
        "Attendance", ATTENDANCE_PAGE, students=students, records=records,
        today=date.today().isoformat(), is_admin=bool(session.get("admin"))
    )


@app.route("/attendance/add", methods=["POST"])
@admin_required
def add_attendance():
    roll = request.form.get("roll_no", "")
    day = request.form.get("date", "")
    status = request.form.get("status", "")

    if status not in ("Present", "Absent", "Late") or not day:
        flash("Enter a valid date and status.", "error")
        return redirect(url_for("attendance"))

    with get_db() as db:
        student = db.execute(
            "SELECT name FROM students WHERE roll_no=?", (roll,)
        ).fetchone()
        if student:
            db.execute(
                "INSERT INTO attendance (roll_no,student_name,date,status) VALUES (?,?,?,?)",
                (roll, student["name"], day, status)
            )
            flash("Attendance saved.")
        else:
            flash("Choose an existing student.", "error")

    return redirect(url_for("attendance"))


MARKS_PAGE = """
<h1>Marks</h1>
{% if is_admin %}
<div class="card">
  <h2>Add subject marks</h2>
  <form method="post" action="{{ url_for('add_mark') }}">
    <div class="formgrid">
      <div>
        <label>Student</label>
        <select name="roll_no" required>
          <option value="">Choose</option>
          {% for s in students %}
          <option value="{{ s['roll_no'] }}">{{ s['roll_no'] }} — {{ s['name'] }}</option>
          {% endfor %}
        </select>
      </div>
      <div><label>Subject</label><input name="subject" required></div>
      <div><label>Marks scored</label><input type="number" min="0" step=".01" name="marks" required></div>
      <div><label>Total marks</label><input type="number" min=".01" step=".01" name="total_marks" required></div>
    </div>
    <p><button>Save marks</button></p>
  </form>
</div>
{% endif %}
<div class="card">
  <h2>Marks records</h2>
  <div class="tablewrap">
    <table>
      <tr><th>Roll No</th><th>Student</th><th>Subject</th><th>Marks</th><th>Total</th><th>Percent</th></tr>
      {% for m in records %}
      <tr>
        <td>{{ m['roll_no'] }}</td><td>{{ m['student_name'] or '-' }}</td>
        <td>{{ m['subject'] }}</td><td>{{ m['marks'] }}</td><td>{{ m['total_marks'] }}</td>
        <td>{{ '%.1f'|format(m['marks']*100/m['total_marks']) if m['total_marks'] else '-' }}%</td>
      </tr>
      {% else %}
      <tr><td colspan="6">No marks records.</td></tr>
      {% endfor %}
    </table>
  </div>
</div>
"""


@app.route("/marks")
def marks():
    with get_db() as db:
        students = db.execute("SELECT roll_no,name FROM students ORDER BY name").fetchall()
        records = db.execute("SELECT * FROM marks ORDER BY id DESC LIMIT 500").fetchall()
    return page("Marks", MARKS_PAGE, students=students, records=records,
                is_admin=bool(session.get("admin")))


@app.route("/marks/add", methods=["POST"])
@admin_required
def add_mark():
    roll = request.form.get("roll_no", "")
    subject = request.form.get("subject", "").strip()

    try:
        mark = float(request.form["marks"])
        total = float(request.form["total_marks"])
        if not subject or total <= 0 or mark < 0 or mark > total:
            raise ValueError

        with get_db() as db:
            student = db.execute(
                "SELECT name FROM students WHERE roll_no=?", (roll,)
            ).fetchone()
            if student:
                db.execute(
                    "INSERT INTO marks (roll_no,student_name,subject,marks,total_marks) VALUES (?,?,?,?,?)",
                    (roll, student["name"], subject, mark, total)
                )
                flash("Marks saved.")
            else:
                flash("Choose an existing student.", "error")
    except (ValueError, KeyError):
        flash("Enter valid marks; scored marks cannot exceed total marks.", "error")

    return redirect(url_for("marks"))


@app.route("/reports")
def reports():
    with get_db() as db:
        students = db.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        total, paid, pending = db.execute(
            "SELECT COALESCE(SUM(total_fee),0),COALESCE(SUM(paid_fee),0),COALESCE(SUM(pending_fee),0) FROM fees"
        ).fetchone()
        present = db.execute(
            "SELECT COUNT(*) FROM attendance WHERE status='Present'"
        ).fetchone()[0]
        absent = db.execute(
            "SELECT COUNT(*) FROM attendance WHERE status='Absent'"
        ).fetchone()[0]

    body = """
    <h1>Reports</h1>
    <div class="cards">
      <div class="card"><h2>Students</h2><div class="num">{{ students }}</div></div>
      <div class="card"><h2>Total fees</h2><div class="num">₹{{ '%.2f'|format(total) }}</div></div>
      <div class="card"><h2>Paid fees</h2><div class="num">₹{{ '%.2f'|format(paid) }}</div></div>
      <div class="card"><h2>Pending fees</h2><div class="num">₹{{ '%.2f'|format(pending) }}</div></div>
    </div>
    <div class="card">
      <h2>Attendance summary</h2>
      <p>Present: {{ present }}</p>
      <p>Absent: {{ absent }}</p>
    </div>
    """
    return page(
        "Reports", body, students=students, total=total, paid=paid,
        pending=pending, present=present, absent=absent
    )


if __name__ == "__main__":
    if not DATABASE.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE}. Keep app.py beside the database folder."
        )
    app.run(debug=True)
