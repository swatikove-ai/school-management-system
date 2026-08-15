import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database import connect_db


def attendance_management():

    window = tk.Toplevel()
    window.title("Attendance Management")
    window.geometry("1150x700")
    window.minsize(1000, 650)


    tk.Label(
        window,
        text="Attendance Management",
        font=("Arial", 24, "bold")
    ).pack(pady=15)


    search_frame = tk.Frame(window)
    search_frame.pack(
        fill="x",
        padx=25,
        pady=5
    )

    tk.Label(
        search_frame,
        text="Search Student:",
        font=("Arial", 11, "bold")
    ).pack(
        side=tk.LEFT,
        padx=5
    )

    search_entry = tk.Entry(
        search_frame,
        width=35,
        font=("Arial", 11)
    )

    search_entry.pack(
        side=tk.LEFT,
        padx=5
    )

    form = tk.LabelFrame(
        window,
        text="Attendance Details",
        font=("Arial", 12, "bold")
    )

    form.pack(
        fill="x",
        padx=25,
        pady=10
    )


    tk.Label(
        form,
        text="Roll No:"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    roll_entry = tk.Entry(
        form,
        width=25
    )

    roll_entry.grid(
        row=0,
        column=1,
        padx=10
    )

    tk.Label(
        form,
        text="Student Name:"
    ).grid(
        row=0,
        column=2,
        padx=10,
        pady=10
    )

    name_entry = tk.Entry(
        form,
        width=25,
        state="readonly"
    )

    name_entry.grid(
        row=0,
        column=3,
        padx=10
    )


    tk.Label(
        form,
        text="Date:"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )

    date_entry = tk.Entry(
        form,
        width=25
    )

    date_entry.grid(
        row=1,
        column=1,
        padx=10
    )

    date_entry.insert(
        0,
        date.today().strftime("%Y-%m-%d")
    )


    tk.Label(
        form,
        text="Status:"
    ).grid(
        row=1,
        column=2,
        padx=10,
        pady=10
    )

    status_combo = ttk.Combobox(
        form,
        values=[
            "Present",
            "Absent"
        ],
        state="readonly",
        width=22
    )

    status_combo.grid(
        row=1,
        column=3,
        padx=10
    )

    status_combo.current(0)


    def load_student_name():

        roll = roll_entry.get().strip()

        if roll == "":

            name_entry.config(
                state="normal"
            )

            name_entry.delete(
                0,
                tk.END
            )

            name_entry.config(
                state="readonly"
            )

            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM students
            WHERE roll_no = ?
        """, (roll,))

        result = cursor.fetchone()

        conn.close()

        name_entry.config(
            state="normal"
        )

        name_entry.delete(
            0,
            tk.END
        )

        if result:

            name_entry.insert(
                0,
                result[0]
            )

        name_entry.config(
            state="readonly"
        )

    roll_entry.bind(
        "<FocusOut>",
        lambda event: load_student_name()
    )


    def clear_fields():

        roll_entry.delete(
            0,
            tk.END
        )

        name_entry.config(
            state="normal"
        )

        name_entry.delete(
            0,
            tk.END
        )

        name_entry.config(
            state="readonly"
        )

        date_entry.delete(
            0,
            tk.END
        )

        date_entry.insert(
            0,
            date.today().strftime("%Y-%m-%d")
        )

        status_combo.current(0)


    def view_attendance():

        for item in table.get_children():

            table.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                roll_no,
                student_name,
                date,
                status
            FROM attendance
            ORDER BY CAST(roll_no AS INTEGER) ASC, date ASC
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            table.insert(
                "",
                tk.END,
                values=row
            )

    

    def search_attendance():

        search_value = search_entry.get().strip()

        for item in table.get_children():

            table.delete(item)

        clear_fields()

        if search_value == "":

            view_attendance()

            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                roll_no,
                student_name,
                date,
                status
            FROM attendance
            WHERE roll_no LIKE ?
               OR student_name LIKE ?
               OR date LIKE ?
               OR status LIKE ?
            ORDER BY CAST(roll_no AS INTEGER) ASC, date ASC
        """, (
            "%" + search_value + "%",
            "%" + search_value + "%",
            "%" + search_value + "%",
            "%" + search_value + "%"
        ))

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            table.insert(
                "",
                tk.END,
                values=row
            )

        if rows:

            first_item = table.get_children()[0]

            table.selection_set(
                first_item
            )

            table.focus(
                first_item
            )

            row = rows[0]

            roll_entry.insert(
                0,
                row[1]
            )

            name_entry.config(
                state="normal"
            )

            name_entry.insert(
                0,
                row[2]
            )

            name_entry.config(
                state="readonly"
            )

            date_entry.delete(
                0,
                tk.END
            )

            date_entry.insert(
                0,
                row[3]
            )

            status_combo.set(
                row[4]
            )

        else:

            messagebox.showinfo(
                "Search",
                "No attendance record found."
            )


    def add_attendance():

        roll = roll_entry.get().strip()
        attendance_date = date_entry.get().strip()
        status = status_combo.get()

        # Make sure student exists
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM students
            WHERE roll_no = ?
        """, (roll,))

        student = cursor.fetchone()

        conn.close()

        if roll == "":

            messagebox.showerror(
                "Error",
                "Please enter Roll No."
            )

            return

        if not student:

            messagebox.showerror(
                "Error",
                "Student with this Roll No does not exist."
            )

            return

        if attendance_date == "":

            messagebox.showerror(
                "Error",
                "Please enter Date."
            )

            return

        # Validate date
        try:

            date.fromisoformat(
                attendance_date
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Date must be in YYYY-MM-DD format."
            )

            return

        try:

            conn = connect_db()
            cursor = conn.cursor()

            # Prevent duplicate attendance
            cursor.execute("""
                SELECT id
                FROM attendance
                WHERE roll_no = ?
                  AND date = ?
            """, (
                roll,
                attendance_date
            ))

            existing = cursor.fetchone()

            if existing:

                conn.close()

                messagebox.showwarning(
                    "Already Exists",
                    "Attendance for this student on this date already exists."
                )

                return

            cursor.execute("""
                INSERT INTO attendance
                (
                    roll_no,
                    student_name,
                    date,
                    status
                )
                VALUES (?, ?, ?, ?)
            """, (
                roll,
                student[0],
                attendance_date,
                status
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Attendance added successfully!"
            )

            clear_fields()
            search_entry.delete(
                0,
                tk.END
            )

            view_attendance()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    def update_attendance():

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select an attendance record."
            )

            return

        row = table.item(
            selected[0]
        )["values"]

        attendance_id = row[0]

        roll = roll_entry.get().strip()
        attendance_date = date_entry.get().strip()
        status = status_combo.get()

        if roll == "":

            messagebox.showerror(
                "Error",
                "Roll No is required."
            )

            return

        try:

            date.fromisoformat(
                attendance_date
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Date must be in YYYY-MM-DD format."
            )

            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM students
            WHERE roll_no = ?
        """, (roll,))

        student = cursor.fetchone()

        if not student:

            conn.close()

            messagebox.showerror(
                "Error",
                "Student not found."
            )

            return

        cursor.execute("""
            UPDATE attendance
            SET
                roll_no = ?,
                student_name = ?,
                date = ?,
                status = ?
            WHERE id = ?
        """, (
            roll,
            student[0],
            attendance_date,
            status,
            attendance_id
        ))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        if rows_updated == 0:

            messagebox.showwarning(
                "Warning",
                "Attendance record not found."
            )

        else:

            messagebox.showinfo(
                "Success",
                "Attendance updated successfully!"
            )

            clear_fields()

            view_attendance()



    def delete_attendance():

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select an attendance record."
            )

            return

        row = table.item(
            selected[0]
        )["values"]

        attendance_id = row[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this attendance record?"
        )

        if not confirm:

            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM attendance WHERE id = ?",
            (attendance_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Attendance deleted successfully!"
        )

        clear_fields()

        view_attendance()



    def select_attendance(event):

        selected = table.selection()

        if not selected:

            return

        row = table.item(
            selected[0]
        )["values"]

        clear_fields()

        roll_entry.insert(
            0,
            row[1]
        )

        name_entry.config(
            state="normal"
        )

        name_entry.insert(
            0,
            row[2]
        )

        name_entry.config(
            state="readonly"
        )

        date_entry.delete(
            0,
            tk.END
        )

        date_entry.insert(
            0,
            row[3]
        )

        status_combo.set(
            row[4]
        )


    def attendance_report():

        roll = roll_entry.get().strip()

        if roll == "":

            messagebox.showerror(
                "Error",
                "Please enter or select Roll No."
            )

            return

        conn = connect_db()
        cursor = conn.cursor()

        # Student
        cursor.execute("""
            SELECT name
            FROM students
            WHERE roll_no = ?
        """, (roll,))

        student = cursor.fetchone()

        if not student:

            conn.close()

            messagebox.showerror(
                "Error",
                "Student not found."
            )

            return

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
                ),
                COALESCE(
                    SUM(
                        CASE
                            WHEN status = 'Absent'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                )
            FROM attendance
            WHERE roll_no = ?
        """, (roll,))

        summary = cursor.fetchone()

        conn.close()

        total_days = summary[0]
        present_days = summary[1]
        absent_days = summary[2]

        if total_days > 0:

            percentage = (
                present_days /
                total_days
            ) * 100

        else:

            percentage = 0


        report = tk.Toplevel(window)

        report.title(
            "Attendance Report"
        )

        report.geometry(
            "550x500"
        )

        tk.Label(
            report,
            text="ATTENDANCE REPORT",
            font=("Arial", 22, "bold")
        ).pack(
            pady=20
        )

        tk.Label(
            report,
            text=f"Student: {student[0]}",
            font=("Arial", 15, "bold")
        ).pack(
            pady=5
        )

        tk.Label(
            report,
            text=f"Roll No: {roll}",
            font=("Arial", 13)
        ).pack(
            pady=5
        )

        report_frame = tk.Frame(
            report,
            bd=2,
            relief="groove"
        )

        report_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=20
        )

        report_text = (
            f"Total Days     : {total_days}\n\n"
            f"Present Days   : {present_days}\n\n"
            f"Absent Days    : {absent_days}\n\n"
            f"Attendance     : {percentage:.2f}%"
        )

        tk.Label(
            report_frame,
            text=report_text,
            font=("Arial", 15),
            justify="left"
        ).pack(
            padx=30,
            pady=35
        )

        tk.Button(
            report,
            text="Close",
            width=15,
            command=report.destroy
        ).pack(
            pady=10
        )


    button_frame = tk.Frame(
        window
    )

    button_frame.pack(
        pady=10
    )

    tk.Button(
        button_frame,
        text="Search",
        width=14,
        command=search_attendance
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Add Attendance",
        width=15,
        command=add_attendance
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Update",
        width=14,
        command=update_attendance
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Delete",
        width=14,
        command=delete_attendance
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Attendance Report",
        width=17,
        command=attendance_report
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Clear",
        width=14,
        command=clear_fields
    ).grid(
        row=0,
        column=5,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Refresh",
        width=14,
        command=view_attendance
    ).grid(
        row=0,
        column=6,
        padx=5
    )


    table_frame = tk.Frame(
        window
    )

    table_frame.pack(
        fill=tk.BOTH,
        expand=True,
        padx=25,
        pady=10
    )

    columns = (
        "ID",
        "Roll No",
        "Student Name",
        "Date",
        "Status"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        table.heading(
            column,
            text=column
        )

        table.column(
            column,
            width=170
        )


    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(
        yscrollcommand=scrollbar.set
    )

    table.pack(
        side=tk.LEFT,
        fill=tk.BOTH,
        expand=True
    )

    scrollbar.pack(
        side=tk.RIGHT,
        fill=tk.Y
    )

    

    table.bind(
        "<ButtonRelease-1>",
        select_attendance
    )

    search_entry.bind(
        "<Return>",
        lambda event: search_attendance()
    )


    view_attendance()


if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    attendance_management()

    root.mainloop()