import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import sys

from database import connect_db

if len(sys.argv) >= 3:
    logged_username = sys.argv[1]
    logged_role = sys.argv[2]
else:
    logged_username = "admin"
    logged_role = "Admin"


def open_students():

    try:
        import students

        students.student_management()

        update_dashboard()

    except Exception as e:

        messagebox.showerror(
            "Student Management Error",
            str(e)
        )


def open_fees():

    try:
        import fees

        fees.fees_management()

        update_dashboard()

    except Exception as e:

        messagebox.showerror(
            "Fees Management Error",
            str(e)
        )


def open_attendance():

    try:
        import attendance

        attendance.attendance_management()

        update_dashboard()

    except Exception as e:

        messagebox.showerror(
            "Attendance Management Error",
            str(e)
        )


def open_marks():

    try:
        import marks

        marks.marks_management()

        update_dashboard()

    except Exception as e:

        messagebox.showerror(
            "Marks Management Error",
            str(e)
        )


def open_users():

    if logged_role.lower() != "admin":

        messagebox.showwarning(
            "Access Denied",
            "Only Admin can access User Management."
        )

        return

    try:

        import users

        users.user_management()

    except Exception as e:

        messagebox.showerror(
            "User Management Error",
            str(e)
        )


def open_reports():

    try:

        import reports

        reports.reports_management()

    except Exception as e:

        messagebox.showerror(
            "Report Management Error",
            str(e)
        )


def get_total_students():

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM students
        """)

        result = cursor.fetchone()

        conn.close()

        if result:
            return int(result[0])

        return 0

    except Exception as e:

        print(
            "Student Dashboard Error:",
            e
        )

        return 0


def get_fees_data():

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COALESCE(SUM(paid_fee), 0),
                COALESCE(SUM(pending_fee), 0)
            FROM fees
        """)

        result = cursor.fetchone()

        conn.close()

        if result:

            paid = float(
                result[0] or 0
            )

            pending = float(
                result[1] or 0
            )

            return paid, pending

        return 0, 0

    except Exception as e:

        print(
            "Fees Dashboard Error:",
            e
        )

        return 0, 0


def get_attendance_percentage():

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(
                    SUM(
                        CASE
                            WHEN status = 'Present'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                )
            FROM attendance
        """)

        result = cursor.fetchone()

        conn.close()

        if not result:
            return 0

        total = int(
            result[0] or 0
        )

        present = int(
            result[1] or 0
        )

        if total == 0:
            return 0

        return (
            present / total
        ) * 100

    except Exception as e:

        print(
            "Attendance Dashboard Error:",
            e
        )

        return 0


def update_dashboard():

    total_students = get_total_students()

    paid_fees, pending_fees = get_fees_data()

    attendance = get_attendance_percentage()

    if "students_value" in globals():

        students_value.config(
            text=str(total_students)
        )

    if "fees_value" in globals():

        fees_value.config(
            text=f"₹{paid_fees:,.2f}"
        )

    if "pending_value" in globals():

        pending_value.config(
            text=f"₹{pending_fees:,.2f}"
        )

    if "attendance_value" in globals():

        attendance_value.config(
            text=f"{attendance:.2f}%"
        )




def change_password():

    window = tk.Toplevel(root)

    window.title(
        "Change Password"
    )

    window.geometry(
        "500x420"
    )

    window.resizable(
        False,
        False
    )

    tk.Label(
        window,
        text="Change Password",
        font=("Arial", 22, "bold")
    ).pack(
        pady=25
    )

   

    tk.Label(
        window,
        text="Current Password:",
        font=("Arial", 11, "bold")
    ).pack(
        pady=(10, 5)
    )

    current_entry = tk.Entry(
        window,
        width=30,
        show="*",
        font=("Arial", 11)
    )

    current_entry.pack(
        pady=5
    )


    tk.Label(
        window,
        text="New Password:",
        font=("Arial", 11, "bold")
    ).pack(
        pady=(15, 5)
    )

    new_entry = tk.Entry(
        window,
        width=30,
        show="*",
        font=("Arial", 11)
    )

    new_entry.pack(
        pady=5
    )

    tk.Label(
        window,
        text="Confirm New Password:",
        font=("Arial", 11, "bold")
    ).pack(
        pady=(15, 5)
    )

    confirm_entry = tk.Entry(
        window,
        width=30,
        show="*",
        font=("Arial", 11)
    )

    confirm_entry.pack(
        pady=5
    )

    def update_password():

        current = current_entry.get().strip()

        new_password = new_entry.get().strip()

        confirm = confirm_entry.get().strip()

        if current == "":

            messagebox.showerror(
                "Error",
                "Please enter current password."
            )

            return

        if new_password == "":

            messagebox.showerror(
                "Error",
                "Please enter new password."
            )

            return

        if len(new_password) < 4:

            messagebox.showerror(
                "Error",
                "New password must contain at least 4 characters."
            )

            return

        if confirm == "":

            messagebox.showerror(
                "Error",
                "Please confirm new password."
            )

            return

        if new_password != confirm:

            messagebox.showerror(
                "Error",
                "New passwords do not match."
            )

            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id
                FROM users
                WHERE username = ?
                  AND password = ?
            """, (
                logged_username,
                current
            ))

            user = cursor.fetchone()

            if not user:

                conn.close()

                messagebox.showerror(
                    "Error",
                    "Current password is incorrect."
                )

                return

            cursor.execute("""
                UPDATE users
                SET password = ?
                WHERE username = ?
            """, (
                new_password,
                logged_username
            ))

            conn.commit()

            conn.close()

            messagebox.showinfo(
                "Success",
                "Password changed successfully!"
            )

            window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    tk.Button(
        window,
        text="Change Password",
        width=20,
        font=("Arial", 11, "bold"),
        command=update_password
    ).pack(
        pady=20
    )


def logout():

    answer = messagebox.askyesno(
        "Logout",
        f"Are you sure you want to logout, {logged_username}?"
    )

    if not answer:
        return

    try:

        root.destroy()

        login_file = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "login.py"
        )

        os.spawnv(
            os.P_NOWAIT,
            sys.executable,
            [
                sys.executable,
                login_file
            ]
        )

    except Exception as e:

        messagebox.showerror(
            "Logout Error",
            str(e)
        )


def exit_program():

    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if answer:

        root.destroy()



def create_card(
    parent,
    title,
    value,
    column
):

    card = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid"
    )

    card.grid(
        row=0,
        column=column,
        padx=7,
        pady=8,
        sticky="nsew"
    )

    tk.Label(
        card,
        text=title,
        font=("Arial", 11),
        bg="white",
        fg="#666666"
    ).pack(
        pady=(18, 5)
    )

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 22, "bold"),
        bg="white",
        fg="black"
    )

    value_label.pack(
        pady=(5, 18)
    )

    return value_label


root = tk.Tk()

root.title(
    "School Management System"
)

root.geometry(
    "1200x700"
)

root.minsize(
    1000,
    600
)

root.configure(
    bg="#f2f4f7"
)

try:

    root.state("zoomed")

except Exception:

    pass


sidebar = tk.Frame(
    root,
    bg="#202b3c",
    width=230
)

sidebar.pack(
    side=tk.LEFT,
    fill=tk.Y
)

sidebar.pack_propagate(False)


tk.Label(
    sidebar,
    text="SCHOOL",
    font=("Arial", 27, "bold"),
    fg="white",
    bg="#202b3c"
).pack(
    pady=(28, 0)
)

tk.Label(
    sidebar,
    text="MANAGEMENT",
    font=("Arial", 15),
    fg="#b9c2cf",
    bg="#202b3c"
).pack(
    pady=(0, 20)
)


tk.Label(
    sidebar,
    text=f"User: {logged_username}",
    font=("Arial", 10, "bold"),
    fg="white",
    bg="#202b3c"
).pack(
    pady=3
)

tk.Label(
    sidebar,
    text=f"Role: {logged_role}",
    font=("Arial", 9),
    fg="#b9c2cf",
    bg="#202b3c"
).pack(
    pady=(0, 20)
)


def sidebar_button(
    text,
    command
):

    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        font=("Arial", 11),
        anchor="w",
        padx=22,
        bg="#202b3c",
        fg="white",
        activebackground="#34445c",
        activeforeground="white",
        bd=0,
        relief="flat",
        height=2,
        cursor="hand2"
    )

    button.pack(
        fill=tk.X,
        padx=5,
        pady=1
    )

    return button


sidebar_button(
    "  Dashboard",
    update_dashboard
)

sidebar_button(
    "  Students",
    open_students
)

sidebar_button(
    "  Fees",
    open_fees
)

sidebar_button(
    "  Attendance",
    open_attendance
)

sidebar_button(
    "  Marks",
    open_marks
)

sidebar_button(
    "  User Management",
    open_users
)

sidebar_button(
    "  Reports",
    open_reports
)

sidebar_button(
    "  Change Password",
    change_password
)


tk.Button(
    sidebar,
    text="  Exit",
    command=exit_program,
    font=("Arial", 11),
    anchor="w",
    padx=22,
    bg="#202b3c",
    fg="white",
    activebackground="#34445c",
    activeforeground="white",
    bd=0,
    relief="flat",
    height=2,
    cursor="hand2"
).pack(
    side=tk.BOTTOM,
    fill=tk.X,
    padx=5,
    pady=1
)


tk.Button(
    sidebar,
    text="  Logout",
    command=logout,
    font=("Arial", 11),
    anchor="w",
    padx=22,
    bg="#202b3c",
    fg="white",
    activebackground="#34445c",
    activeforeground="white",
    bd=0,
    relief="flat",
    height=2,
    cursor="hand2"
).pack(
    side=tk.BOTTOM,
    fill=tk.X,
    padx=5,
    pady=1
)


content = tk.Frame(
    root,
    bg="#f2f4f7"
)

content.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)


header = tk.Frame(
    content,
    bg="white",
    height=80
)

header.pack(
    fill=tk.X
)

header.pack_propagate(False)


tk.Label(
    header,
    text="Dashboard",
    font=("Arial", 27, "bold"),
    bg="white"
).pack(
    side=tk.LEFT,
    padx=30
)


tk.Label(
    header,
    text=f"Welcome, {logged_username}",
    font=("Arial", 11),
    bg="white",
    fg="#777777"
).pack(
    side=tk.RIGHT,
    padx=30
)



dashboard = tk.Frame(
    content,
    bg="#f2f4f7"
)

dashboard.pack(
    fill=tk.BOTH,
    expand=True,
    padx=22,
    pady=20
)



stats_frame = tk.Frame(
    dashboard,
    bg="#f2f4f7"
)

stats_frame.pack(
    fill=tk.X
)


for i in range(4):

    stats_frame.columnconfigure(
        i,
        weight=1
    )



students_value = create_card(
    stats_frame,
    "Total Students",
    "0",
    0
)

fees_value = create_card(
    stats_frame,
    "Fees Collected",
    "₹0.00",
    1
)

pending_value = create_card(
    stats_frame,
    "Pending Fees",
    "₹0.00",
    2
)

attendance_value = create_card(
    stats_frame,
    "Attendance",
    "0.00%",
    3
)



tk.Label(
    dashboard,
    text="Quick Actions",
    font=("Arial", 21, "bold"),
    bg="#f2f4f7"
).pack(
    anchor="w",
    pady=(20, 8)
)


quick_frame = tk.Frame(
    dashboard,
    bg="#f2f4f7"
)

quick_frame.pack(
    fill=tk.X
)


def quick_button(
    text,
    command,
    column
):

    button = tk.Button(
        quick_frame,
        text=text,
        command=command,
        font=("Arial", 10),
        height=2,
        cursor="hand2"
    )

    button.grid(
        row=0,
        column=column,
        padx=4,
        sticky="ew"
    )

    quick_frame.columnconfigure(
        column,
        weight=1
    )


quick_button(
    "Students",
    open_students,
    0
)

quick_button(
    "Fees",
    open_fees,
    1
)

quick_button(
    "Attendance",
    open_attendance,
    2
)

quick_button(
    "Marks",
    open_marks,
    3
)

quick_button(
    "Users",
    open_users,
    4
)

quick_button(
    "Reports",
    open_reports,
    5
)




welcome_frame = tk.Frame(
    dashboard,
    bg="white",
    bd=1,
    relief="solid"
)

welcome_frame.pack(
    fill=tk.BOTH,
    expand=True,
    pady=25
)


tk.Label(
    welcome_frame,
    text="Welcome to School Management System",
    font=("Arial", 23, "bold"),
    bg="white"
).pack(
    pady=(55, 12)
)


tk.Label(
    welcome_frame,
    text=(
        "Manage students, fees, attendance, "
        "marks, users and reports from one place."
    ),
    font=("Arial", 12),
    fg="#777777",
    bg="white"
).pack()



update_dashboard()


root.mainloop()