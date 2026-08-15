import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os

from database import connect_db


# ============================================================
# REPORT MANAGEMENT SYSTEM
# ============================================================

def reports_management():

    window = tk.Toplevel()
    window.title("Report Management System")
    window.geometry("1450x850")
    window.minsize(1100, 700)

    # ========================================================
    # DATABASE HELPERS
    # ========================================================

    def get_columns(cursor, table_name):

        try:
            cursor.execute(
                f"PRAGMA table_info({table_name})"
            )

            rows = cursor.fetchall()

            return [str(row[1]) for row in rows]

        except Exception:
            return []

    def find_column(columns, names):

        lower_columns = {
            str(c).lower(): c
            for c in columns
        }

        for name in names:

            if name.lower() in lower_columns:
                return lower_columns[name.lower()]

        return None

    def quote_column(column):

        if not column:
            return None

        return '"' + str(column).replace('"', '""') + '"'

    # ========================================================
    # TITLE
    # ========================================================

    tk.Label(
        window,
        text="Report Management System",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    # ========================================================
    # TOP FRAME
    # ========================================================

    top_frame = tk.Frame(window)
    top_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(
        top_frame,
        text="Select Report:",
        font=("Arial", 11, "bold")
    ).pack(side="left")

    report_combo = ttk.Combobox(
        top_frame,
        width=28,
        state="readonly",
        values=[
            "Student Report",
            "Fees Report",
            "Attendance Report",
            "Marks Report",
            "Complete Student Report"
        ]
    )

    report_combo.pack(side="left", padx=10)
    report_combo.current(0)

    tk.Label(
        top_frame,
        text="Search:",
        font=("Arial", 11, "bold")
    ).pack(side="left", padx=(30, 5))

    search_entry = tk.Entry(
        top_frame,
        width=30,
        font=("Arial", 11)
    )

    search_entry.pack(side="left")

    # ========================================================
    # TABLE FRAME
    # ========================================================

    table_frame = tk.Frame(window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    table = None

    # ========================================================
    # CREATE TABLE
    # ========================================================

    def create_table(columns, widths=None):

        nonlocal table

        for widget in table_frame.winfo_children():
            widget.destroy()

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for i, column in enumerate(columns):

            table.heading(
                column,
                text=column
            )

            width = 120

            if widths and i < len(widths):
                width = widths[i]

            table.column(
                column,
                width=width,
                minwidth=70,
                anchor="center"
            )

        y_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=table.yview
        )

        x_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=table.xview
        )

        table.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        table.pack(
            side="left",
            fill="both",
            expand=True
        )

        y_scroll.pack(
            side="right",
            fill="y"
        )

        x_scroll.pack(
            side="bottom",
            fill="x"
        )

    # ========================================================
    # CLEAR TABLE
    # ========================================================

    def clear_table():

        if table:

            for item in table.get_children():
                table.delete(item)

    # ========================================================
    # STUDENT REPORT
    # ========================================================

    def student_report():

        clear_table()

        search = search_entry.get().strip()

        conn = connect_db()
        cursor = conn.cursor()

        try:

            columns = get_columns(
                cursor,
                "students"
            )

            id_col = find_column(
                columns,
                ["id"]
            )

            roll_col = find_column(
                columns,
                ["roll_no", "roll", "rollnumber"]
            )

            name_col = find_column(
                columns,
                ["name", "student_name"]
            )

            age_col = find_column(
                columns,
                ["age"]
            )

            gender_col = find_column(
                columns,
                ["gender"]
            )

            class_col = find_column(
                columns,
                [
                    "class_name",
                    "class",
                    "class_name_",
                    "standard",
                    "classroom"
                ]
            )

            phone_col = find_column(
                columns,
                ["phone", "mobile", "contact"]
            )

            email_col = find_column(
                columns,
                ["email", "email_id"]
            )

            if not roll_col or not name_col:

                messagebox.showerror(
                    "Error",
                    "Students table me Roll No ya Name column nahi mila."
                )

                return

            def select_col(col):

                if col:
                    return quote_column(col)

                return "''"

            query = f"""
                SELECT
                    {select_col(id_col)},
                    {select_col(roll_col)},
                    {select_col(name_col)},
                    {select_col(age_col)},
                    {select_col(gender_col)},
                    {select_col(class_col)},
                    {select_col(phone_col)},
                    {select_col(email_col)}
                FROM students
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            create_table(
                [
                    "ID",
                    "Roll No",
                    "Name",
                    "Age",
                    "Gender",
                    "Class",
                    "Phone",
                    "Email"
                ],
                [
                    60,
                    90,
                    150,
                    70,
                    90,
                    100,
                    150,
                    220
                ]
            )

            for row in rows:

                if search:

                    if (
                        search.lower() not in str(row[1]).lower()
                        and
                        search.lower() not in str(row[2]).lower()
                    ):
                        continue

                table.insert(
                    "",
                    "end",
                    values=row
                )

        except Exception as e:

            messagebox.showerror(
                "Student Report Error",
                str(e)
            )

        finally:

            conn.close()

    # ========================================================
    # FEES REPORT
    # ========================================================

    def fees_report():

        clear_table()

        search = search_entry.get().strip()

        conn = connect_db()
        cursor = conn.cursor()

        try:

            columns = get_columns(
                cursor,
                "fees"
            )

            id_col = find_column(
                columns,
                ["id"]
            )

            roll_col = find_column(
                columns,
                ["roll_no", "roll"]
            )

            name_col = find_column(
                columns,
                ["student_name", "name"]
            )

            total_col = find_column(
                columns,
                ["total_fees", "total_fee"]
            )

            paid_col = find_column(
                columns,
                ["paid_fees", "paid_fee"]
            )

            pending_col = find_column(
                columns,
                ["pending_fees", "pending_fee"]
            )

            if not roll_col:

                messagebox.showerror(
                    "Error",
                    "Fees table me Roll No column nahi mila."
                )

                return

            def col(c):

                if c:
                    return quote_column(c)

                return "0"

            cursor.execute(
                f"""
                SELECT
                    {col(id_col)},
                    {col(roll_col)},
                    {col(name_col)},
                    {col(total_col)},
                    {col(paid_col)},
                    {col(pending_col)}
                FROM fees
                """
            )

            rows = cursor.fetchall()

            create_table(
                [
                    "ID",
                    "Roll No",
                    "Student Name",
                    "Total Fees",
                    "Paid Fees",
                    "Pending Fees"
                ],
                [
                    60,
                    90,
                    180,
                    140,
                    140,
                    140
                ]
            )

            for row in rows:

                if search:

                    if search.lower() not in str(row[1]).lower():
                        continue

                table.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        f"₹{float(row[3] or 0):,.2f}",
                        f"₹{float(row[4] or 0):,.2f}",
                        f"₹{float(row[5] or 0):,.2f}"
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Fees Report Error",
                str(e)
            )

        finally:

            conn.close()

    # ========================================================
    # ATTENDANCE REPORT
    # ========================================================

    def attendance_report():

        clear_table()

        search = search_entry.get().strip()

        conn = connect_db()
        cursor = conn.cursor()

        try:

            columns = get_columns(
                cursor,
                "attendance"
            )

            roll_col = find_column(
                columns,
                ["roll_no", "roll"]
            )

            name_col = find_column(
                columns,
                ["student_name", "name"]
            )

            status_col = find_column(
                columns,
                ["status"]
            )

            if not roll_col or not status_col:

                messagebox.showerror(
                    "Error",
                    "Attendance table ka structure nahi mila."
                )

                return

            name_expression = (
                quote_column(name_col)
                if name_col
                else "''"
            )

            cursor.execute(
                f"""
                SELECT
                    {quote_column(roll_col)},
                    {name_expression},
                    COUNT(*),
                    SUM(
                        CASE
                            WHEN {quote_column(status_col)} = 'Present'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    SUM(
                        CASE
                            WHEN {quote_column(status_col)} = 'Absent'
                            THEN 1
                            ELSE 0
                        END
                    )
                FROM attendance
                GROUP BY
                    {quote_column(roll_col)},
                    {name_expression}
                ORDER BY
                    CAST({quote_column(roll_col)} AS INTEGER)
                """
            )

            rows = cursor.fetchall()

            create_table(
                [
                    "Roll No",
                    "Student Name",
                    "Total Days",
                    "Present",
                    "Absent",
                    "Attendance %"
                ],
                [
                    100,
                    180,
                    120,
                    100,
                    100,
                    130
                ]
            )

            for row in rows:

                if search:

                    if search.lower() not in str(row[0]).lower():
                        continue

                total_days = int(row[2] or 0)
                present = int(row[3] or 0)
                absent = int(row[4] or 0)

                percentage = 0

                if total_days:

                    percentage = (
                        present /
                        total_days
                    ) * 100

                table.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        total_days,
                        present,
                        absent,
                        f"{percentage:.2f}%"
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Attendance Report Error",
                str(e)
            )

        finally:

            conn.close()

    # ========================================================
    # MARKS REPORT
    # ========================================================

    def marks_report():

        clear_table()

        search = search_entry.get().strip()

        conn = connect_db()
        cursor = conn.cursor()

        try:

            columns = get_columns(
                cursor,
                "marks"
            )

            id_col = find_column(
                columns,
                ["id"]
            )

            roll_col = find_column(
                columns,
                ["roll_no", "roll"]
            )

            name_col = find_column(
                columns,
                ["student_name", "name"]
            )

            english_col = find_column(
                columns,
                ["english"]
            )

            hindi_col = find_column(
                columns,
                ["hindi"]
            )

            maths_col = find_column(
                columns,
                ["maths", "mathematics"]
            )

            science_col = find_column(
                columns,
                ["science"]
            )

            computer_col = find_column(
                columns,
                ["computer"]
            )

            total_col = find_column(
                columns,
                ["total"]
            )

            percentage_col = find_column(
                columns,
                ["percentage"]
            )

            grade_col = find_column(
                columns,
                ["grade"]
            )

            def c(column):

                if column:
                    return quote_column(column)

                return "0"

            cursor.execute(
                f"""
                SELECT
                    {c(id_col)},
                    {c(roll_col)},
                    {c(name_col)},
                    {c(english_col)},
                    {c(hindi_col)},
                    {c(maths_col)},
                    {c(science_col)},
                    {c(computer_col)},
                    {c(total_col)},
                    {c(percentage_col)},
                    {c(grade_col)}
                FROM marks
                ORDER BY
                    CAST({c(roll_col)} AS INTEGER)
                """
            )

            rows = cursor.fetchall()

            create_table(
                [
                    "ID",
                    "Roll No",
                    "Student Name",
                    "English",
                    "Hindi",
                    "Maths",
                    "Science",
                    "Computer",
                    "Total",
                    "Percentage",
                    "Grade"
                ],
                [
                    50,
                    80,
                    140,
                    90,
                    90,
                    90,
                    90,
                    90,
                    90,
                    100,
                    80
                ]
            )

            for row in rows:

                if search:

                    if (
                        search.lower() not in str(row[1]).lower()
                        and
                        search.lower() not in str(row[2]).lower()
                    ):
                        continue

                table.insert(
                    "",
                    "end",
                    values=row
                )

        except Exception as e:

            messagebox.showerror(
                "Marks Report Error",
                str(e)
            )

        finally:

            conn.close()

    # ========================================================
    # COMPLETE REPORT
    # ========================================================

    def complete_report():

        clear_table()

        search = search_entry.get().strip()

        conn = connect_db()
        cursor = conn.cursor()

        try:

            student_columns = get_columns(
                cursor,
                "students"
            )

            roll_col = find_column(
                student_columns,
                ["roll_no", "roll"]
            )

            name_col = find_column(
                student_columns,
                ["name", "student_name"]
            )

            class_col = find_column(
                student_columns,
                [
                    "class_name",
                    "class",
                    "standard",
                    "classroom"
                ]
            )

            if not roll_col or not name_col:

                messagebox.showerror(
                    "Error",
                    "Students table structure nahi mila."
                )

                return

            fees_columns = get_columns(
                cursor,
                "fees"
            )

            fees_roll = find_column(
                fees_columns,
                ["roll_no", "roll"]
            )

            total_fee_col = find_column(
                fees_columns,
                ["total_fees", "total_fee"]
            )

            paid_fee_col = find_column(
                fees_columns,
                ["paid_fees", "paid_fee"]
            )

            pending_fee_col = find_column(
                fees_columns,
                ["pending_fees", "pending_fee"]
            )

            attendance_columns = get_columns(
                cursor,
                "attendance"
            )

            attendance_roll = find_column(
                attendance_columns,
                ["roll_no", "roll"]
            )

            status_col = find_column(
                attendance_columns,
                ["status"]
            )

            # ------------------------------------------------
            # Get students
            # ------------------------------------------------

            def student_col(c):

                if c:
                    return quote_column(c)

                return "''"

            cursor.execute(
                f"""
                SELECT
                    {student_col(roll_col)},
                    {student_col(name_col)},
                    {student_col(class_col)}
                FROM students
                ORDER BY
                    CAST({student_col(roll_col)} AS INTEGER)
                """
            )

            students = cursor.fetchall()

            create_table(
                [
                    "Roll No",
                    "Student Name",
                    "Class",
                    "Total Fees",
                    "Paid Fees",
                    "Pending Fees",
                    "Attendance %"
                ],
                [
                    100,
                    180,
                    100,
                    130,
                    130,
                    130,
                    130
                ]
            )

            for student in students:

                roll = student[0]
                name = student[1]
                student_class = student[2]

                if search:

                    if (
                        search.lower() not in str(roll).lower()
                        and
                        search.lower() not in str(name).lower()
                    ):
                        continue

                total_fee = 0
                paid_fee = 0
                pending_fee = 0

                if fees_roll:

                    cursor.execute(
                        f"""
                        SELECT
                            {student_col(total_fee_col)},
                            {student_col(paid_fee_col)},
                            {student_col(pending_fee_col)}
                        FROM fees
                        WHERE {quote_column(fees_roll)} = ?
                        LIMIT 1
                        """,
                        (roll,)
                    )

                    fee = cursor.fetchone()

                    if fee:

                        total_fee = float(
                            fee[0] or 0
                        )

                        paid_fee = float(
                            fee[1] or 0
                        )

                        pending_fee = float(
                            fee[2] or 0
                        )

                attendance_percentage = 0

                if attendance_roll and status_col:

                    cursor.execute(
                        f"""
                        SELECT
                            COUNT(*),
                            SUM(
                                CASE
                                    WHEN {quote_column(status_col)} = 'Present'
                                    THEN 1
                                    ELSE 0
                                END
                            )
                        FROM attendance
                        WHERE {quote_column(attendance_roll)} = ?
                        """,
                        (roll,)
                    )

                    att = cursor.fetchone()

                    total_days = int(
                        att[0] or 0
                    )

                    present_days = int(
                        att[1] or 0
                    )

                    if total_days:

                        attendance_percentage = (
                            present_days /
                            total_days
                        ) * 100

                table.insert(
                    "",
                    "end",
                    values=(
                        roll,
                        name,
                        student_class,
                        f"₹{total_fee:,.2f}",
                        f"₹{paid_fee:,.2f}",
                        f"₹{pending_fee:,.2f}",
                        f"{attendance_percentage:.2f}%"
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Complete Report Error",
                str(e)
            )

        finally:

            conn.close()

    # ========================================================
    # GENERATE REPORT
    # ========================================================

    def generate_report():

        selected = report_combo.get()

        if selected == "Student Report":
            student_report()

        elif selected == "Fees Report":
            fees_report()

        elif selected == "Attendance Report":
            attendance_report()

        elif selected == "Marks Report":
            marks_report()

        elif selected == "Complete Student Report":
            complete_report()

    # ========================================================
    # GET TABLE DATA
    # ========================================================

    def get_table_data():

        if table is None:
            return [], []

        headers = [
            table.heading(c)["text"]
            for c in table["columns"]
        ]

        rows = [
            list(table.item(item)["values"])
            for item in table.get_children()
        ]

        return headers, rows

    # ========================================================
    # EXPORT CSV
    # ========================================================

    def export_csv():

        headers, rows = get_table_data()

        if not rows:

            messagebox.showwarning(
                "CSV",
                "Pehle Generate Report karo."
            )

            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile="school_report.csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )

        if not filename:
            return

        try:

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(headers)
                writer.writerows(rows)

            messagebox.showinfo(
                "Success",
                "CSV successfully exported."
            )

        except Exception as e:

            messagebox.showerror(
                "CSV Error",
                str(e)
            )

    # ========================================================
    # EXPORT PDF
    # ========================================================

    def export_pdf():

        try:

            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.units import mm
            from reportlab.platypus import (
                SimpleDocTemplate,
                Paragraph,
                Spacer,
                Table,
                TableStyle
            )
            from reportlab.lib.styles import getSampleStyleSheet

        except ImportError:

            messagebox.showerror(
                "PDF Error",
                "ReportLab installed nahi hai.\n\n"
                "CMD me run karo:\n\n"
                "python -m pip install reportlab"
            )

            return

        headers, rows = get_table_data()

        if not rows:

            messagebox.showwarning(
                "PDF",
                "Pehle Generate Report karo."
            )

            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile="school_report.pdf",
            filetypes=[
                ("PDF Files", "*.pdf")
            ]
        )

        if not filename:
            return

        try:

            document = SimpleDocTemplate(
                filename,
                pagesize=landscape(A4),
                rightMargin=8 * mm,
                leftMargin=8 * mm,
                topMargin=10 * mm,
                bottomMargin=10 * mm
            )

            styles = getSampleStyleSheet()

            elements = [
                Paragraph(
                    "SCHOOL MANAGEMENT SYSTEM",
                    styles["Title"]
                ),
                Spacer(1, 8),
                Paragraph(
                    report_combo.get(),
                    styles["Heading2"]
                ),
                Spacer(1, 10)
            ]

            data = [
                [str(x) for x in headers]
            ]

            for row in rows:
                data.append(
                    [str(x) for x in row]
                )

            pdf_table = Table(
                data,
                repeatRows=1
            )

            pdf_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.grey
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.black
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER"
                    )
                ])
            )

            elements.append(pdf_table)

            document.build(elements)

            messagebox.showinfo(
                "Success",
                "PDF successfully exported."
            )

        except Exception as e:

            messagebox.showerror(
                "PDF Error",
                str(e)
            )

    # ========================================================
    # STUDENT REPORT CARD
    # ========================================================

    def generate_report_card():

        # ----------------------------------------------------
        # First try search box
        # ----------------------------------------------------

        roll = search_entry.get().strip()

        # ----------------------------------------------------
        # If search empty, use selected row
        # ----------------------------------------------------

        if not roll and table:

            selected = table.selection()

            if selected:

                values = table.item(
                    selected[0]
                )["values"]

                if values:

                    roll = str(
                        values[1]
                        if report_combo.get() == "Student Report"
                        else values[0]
                    )

        if not roll:

            messagebox.showwarning(
                "Report Card",
                "Search box me Roll No enter karo.\n\n"
                "Example: 101\n\n"
                "Ya Student Report me student select karo."
            )

            return

        conn = connect_db()
        cursor = conn.cursor()

        try:

            # =================================================
            # STUDENT TABLE
            # =================================================

            student_columns = get_columns(
                cursor,
                "students"
            )

            roll_col = find_column(
                student_columns,
                ["roll_no", "roll", "rollnumber"]
            )

            name_col = find_column(
                student_columns,
                ["name", "student_name"]
            )

            age_col = find_column(
                student_columns,
                ["age"]
            )

            gender_col = find_column(
                student_columns,
                ["gender"]
            )

            # IMPORTANT:
            # class column automatically find hoga
            class_col = find_column(
                student_columns,
                [
                    "class_name",
                    "class",
                    "standard",
                    "classroom",
                    "class_std"
                ]
            )

            if not roll_col or not name_col:

                messagebox.showerror(
                    "Report Card",
                    "Student table ka Roll No/Name column nahi mila."
                )

                return

            def sc(c):

                if c:
                    return quote_column(c)

                return "''"

            cursor.execute(
                f"""
                SELECT
                    {sc(roll_col)},
                    {sc(name_col)},
                    {sc(age_col)},
                    {sc(gender_col)},
                    {sc(class_col)}
                FROM students
                WHERE {quote_column(roll_col)} = ?
                LIMIT 1
                """,
                (roll,)
            )

            student = cursor.fetchone()

            if not student:

                messagebox.showerror(
                    "Report Card",
                    f"Roll No {roll} ka student nahi mila."
                )

                return

            student_roll = student[0]
            student_name = student[1]
            student_age = student[2]
            student_gender = student[3]
            student_class = student[4]

            # =================================================
            # FEES
            # =================================================

            # The current fees.py uses exactly these columns:
            # roll_no, student_name, total_fees, paid_fees, pending_fees.
            # Use a direct query here so the report card reads the
            # same data that is shown in Fees Management.

            total_fee = 0.0
            paid_fee = 0.0
            pending_fee = 0.0

            # IMPORTANT:
            # Older versions of fees.py used:
            #   total_fee, paid_fee, pending_fee
            # Newer versions use:
            #   total_fees, paid_fees, pending_fees
            #
            # Some existing databases therefore contain BOTH sets of
            # columns. The old columns may contain the real values while
            # the new columns contain 0. This query supports BOTH schemas
            # and chooses the non-zero/current value safely.

            fee_columns = get_columns(cursor, "fees")

            fee_roll_col = find_column(
                fee_columns,
                ["roll_no", "roll"]
            )

            fee_name_col = find_column(
                fee_columns,
                ["student_name", "name"]
            )

            total_new_col = find_column(
                fee_columns,
                ["total_fees"]
            )

            total_old_col = find_column(
                fee_columns,
                ["total_fee"]
            )

            paid_new_col = find_column(
                fee_columns,
                ["paid_fees"]
            )

            paid_old_col = find_column(
                fee_columns,
                ["paid_fee"]
            )

            pending_new_col = find_column(
                fee_columns,
                ["pending_fees"]
            )

            pending_old_col = find_column(
                fee_columns,
                ["pending_fee"]
            )

            def fee_expr(new_col, old_col):
                new_q = quote_column(new_col) if new_col else "NULL"
                old_q = quote_column(old_col) if old_col else "NULL"

                return f"""
                    CASE
                        WHEN CAST(COALESCE({new_q}, 0) AS REAL) != 0
                            THEN CAST(COALESCE({new_q}, 0) AS REAL)
                        ELSE CAST(COALESCE({old_q}, 0) AS REAL)
                    END
                """

            if fee_roll_col:

                roll_q = quote_column(fee_roll_col)

                name_condition = ""

                if fee_name_col:
                    name_q = quote_column(fee_name_col)
                    name_condition = f"""
                        OR LOWER(TRIM(CAST({name_q} AS TEXT))) =
                           LOWER(TRIM(?))
                    """

                query = f"""
                    SELECT
                        {fee_expr(total_new_col, total_old_col)},
                        {fee_expr(paid_new_col, paid_old_col)},
                        {fee_expr(pending_new_col, pending_old_col)}
                    FROM fees
                    WHERE CAST({roll_q} AS TEXT) = ?
                    {name_condition}
                    LIMIT 1
                """

                params = [str(student_roll).strip()]

                if fee_name_col:
                    params.append(str(student_name).strip())

                cursor.execute(
                    query,
                    tuple(params)
                )

                fee_data = cursor.fetchone()

                if fee_data:

                    try:
                        total_fee = float(fee_data[0] or 0)
                    except (ValueError, TypeError):
                        total_fee = 0.0

                    try:
                        paid_fee = float(fee_data[1] or 0)
                    except (ValueError, TypeError):
                        paid_fee = 0.0

                    try:
                        stored_pending = float(
                            fee_data[2] or 0
                        )
                    except (ValueError, TypeError):
                        stored_pending = 0.0

                    # Total - Paid is the authoritative pending amount.
                    pending_fee = total_fee - paid_fee

                    if pending_fee < 0:
                        pending_fee = 0.0

                    # If total/paid are both zero, preserve a non-zero
                    # stored pending value rather than losing old data.
                    if total_fee == 0 and paid_fee == 0:
                        pending_fee = max(
                            stored_pending,
                            0.0
                        )

            # =================================================
            # ATTENDANCE
            # =================================================

            attendance_percentage = 0

            attendance_columns = get_columns(
                cursor,
                "attendance"
            )

            att_roll = find_column(
                attendance_columns,
                ["roll_no", "roll"]
            )

            att_status = find_column(
                attendance_columns,
                ["status"]
            )

            if att_roll and att_status:

                cursor.execute(
                    f"""
                    SELECT
                        COUNT(*),
                        SUM(
                            CASE
                                WHEN {quote_column(att_status)} = 'Present'
                                THEN 1
                                ELSE 0
                            END
                        )
                    FROM attendance
                    WHERE {quote_column(att_roll)} = ?
                    """,
                    (student_roll,)
                )

                att_data = cursor.fetchone()

                total_days = int(
                    att_data[0] or 0
                )

                present_days = int(
                    att_data[1] or 0
                )

                if total_days:

                    attendance_percentage = (
                        present_days /
                        total_days
                    ) * 100

            # =================================================
            # MARKS
            # =================================================

            english = 0
            hindi = 0
            maths = 0
            science = 0
            computer = 0

            marks_total = 0
            marks_percentage = 0
            marks_grade = ""

            marks_columns = get_columns(
                cursor,
                "marks"
            )

            marks_roll = find_column(
                marks_columns,
                ["roll_no", "roll"]
            )

            english_col = find_column(
                marks_columns,
                ["english"]
            )

            hindi_col = find_column(
                marks_columns,
                ["hindi"]
            )

            maths_col = find_column(
                marks_columns,
                ["maths", "mathematics"]
            )

            science_col = find_column(
                marks_columns,
                ["science"]
            )

            computer_col = find_column(
                marks_columns,
                ["computer"]
            )

            marks_total_col = find_column(
                marks_columns,
                ["total"]
            )

            percentage_col = find_column(
                marks_columns,
                ["percentage"]
            )

            grade_col = find_column(
                marks_columns,
                ["grade"]
            )

            if marks_roll:

                cursor.execute(
                    f"""
                    SELECT
                        {sc(english_col)},
                        {sc(hindi_col)},
                        {sc(maths_col)},
                        {sc(science_col)},
                        {sc(computer_col)},
                        {sc(marks_total_col)},
                        {sc(percentage_col)},
                        {sc(grade_col)}
                    FROM marks
                    WHERE {quote_column(marks_roll)} = ?
                    LIMIT 1
                    """,
                    (student_roll,)
                )

                marks_data = cursor.fetchone()

                if marks_data:

                    english = float(
                        marks_data[0] or 0
                    )

                    hindi = float(
                        marks_data[1] or 0
                    )

                    maths = float(
                        marks_data[2] or 0
                    )

                    science = float(
                        marks_data[3] or 0
                    )

                    computer = float(
                        marks_data[4] or 0
                    )

                    marks_total = float(
                        marks_data[5] or 0
                    )

                    marks_percentage = float(
                        marks_data[6] or 0
                    )

                    marks_grade = str(
                        marks_data[7] or ""
                    )

                    # If database total/percentage empty,
                    # calculate automatically.

                    calculated_total = (
                        english +
                        hindi +
                        maths +
                        science +
                        computer
                    )

                    if marks_total == 0:

                        marks_total = calculated_total

                    if marks_percentage == 0:

                        marks_percentage = (
                            marks_total /
                            500
                        ) * 100

                    if not marks_grade:

                        if marks_percentage >= 90:
                            marks_grade = "A+"

                        elif marks_percentage >= 80:
                            marks_grade = "A"

                        elif marks_percentage >= 70:
                            marks_grade = "B"

                        elif marks_percentage >= 60:
                            marks_grade = "C"

                        elif marks_percentage >= 50:
                            marks_grade = "D"

                        else:
                            marks_grade = "F"

            conn.close()

            # =================================================
            # REPORT CARD WINDOW
            # =================================================

            card = tk.Toplevel(window)

            card.title(
                "Student Report Card"
            )

            card.geometry(
                "1050x850"
            )

            card.minsize(
                900,
                700
            )

            # =================================================
            # HEADER
            # =================================================

            tk.Label(
                card,
                text="SCHOOL MANAGEMENT SYSTEM",
                font=("Arial", 22, "bold")
            ).pack(pady=(20, 5))

            tk.Label(
                card,
                text="STUDENT REPORT CARD",
                font=("Arial", 18, "bold")
            ).pack(pady=(0, 15))

            # =================================================
            # STUDENT INFO
            # =================================================

            info_frame = tk.LabelFrame(
                card,
                text="Student Information",
                font=("Arial", 11, "bold")
            )

            info_frame.pack(
                fill="x",
                padx=25,
                pady=10
            )

            information = [
                ("Roll No:", student_roll),
                ("Student Name:", student_name),
                ("Age:", student_age),
                ("Gender:", student_gender),
                ("Class:", student_class)
            ]

            for i, (label, value) in enumerate(information):

                row = i // 2
                col = (i % 2) * 2

                tk.Label(
                    info_frame,
                    text=label,
                    font=("Arial", 10, "bold")
                ).grid(
                    row=row,
                    column=col,
                    padx=20,
                    pady=10,
                    sticky="w"
                )

                tk.Label(
                    info_frame,
                    text=str(value),
                    font=("Arial", 10)
                ).grid(
                    row=row,
                    column=col + 1,
                    padx=20,
                    pady=10,
                    sticky="w"
                )

            # =================================================
            # MARKS
            # =================================================

            marks_frame = tk.LabelFrame(
                card,
                text="Marks",
                font=("Arial", 11, "bold")
            )

            marks_frame.pack(
                fill="both",
                expand=True,
                padx=25,
                pady=10
            )

            marks_table = ttk.Treeview(
                marks_frame,
                columns=(
                    "Subject",
                    "Marks",
                    "Total"
                ),
                show="headings"
            )

            marks_table.heading(
                "Subject",
                text="Subject"
            )

            marks_table.heading(
                "Marks",
                text="Marks"
            )

            marks_table.heading(
                "Total",
                text="Total"
            )

            marks_table.column(
                "Subject",
                width=300,
                anchor="center"
            )

            marks_table.column(
                "Marks",
                width=250,
                anchor="center"
            )

            marks_table.column(
                "Total",
                width=250,
                anchor="center"
            )

            marks_table.pack(
                fill="both",
                expand=True,
                padx=10,
                pady=10
            )

            # -------------------------------------------------
            # Insert subjects
            # -------------------------------------------------

            subjects = [
                ("English", english),
                ("Hindi", hindi),
                ("Maths", maths),
                ("Science", science),
                ("Computer", computer)
            ]

            for subject, marks in subjects:

                marks_table.insert(
                    "",
                    "end",
                    values=(
                        subject,
                        f"{marks:g}",
                        "100"
                    )
                )

            # =================================================
            # FEES + ATTENDANCE
            # =================================================

            summary_frame = tk.Frame(card)

            summary_frame.pack(
                fill="x",
                padx=25,
                pady=8
            )

            tk.Label(
                summary_frame,
                text=f"Total Fees: ₹{total_fee:,.2f}",
                font=("Arial", 10, "bold")
            ).pack(
                side="left",
                padx=12
            )

            tk.Label(
                summary_frame,
                text=f"Paid: ₹{paid_fee:,.2f}",
                font=("Arial", 10, "bold")
            ).pack(
                side="left",
                padx=12
            )

            tk.Label(
                summary_frame,
                text=f"Pending: ₹{pending_fee:,.2f}",
                font=("Arial", 10, "bold")
            ).pack(
                side="left",
                padx=12
            )

            tk.Label(
                summary_frame,
                text=f"Attendance: {attendance_percentage:.2f}%",
                font=("Arial", 10, "bold")
            ).pack(
                side="left",
                padx=12
            )

            # =================================================
            # RESULT
            # =================================================

            tk.Label(
                card,
                text=(
                    f"Marks: {marks_total:g} / 500    "
                    f"Percentage: {marks_percentage:.2f}%    "
                    f"Grade: {marks_grade}"
                ),
                font=("Arial", 13, "bold")
            ).pack(pady=8)

            # =================================================
            # CLOSE
            # =================================================

            tk.Button(
                card,
                text="Close",
                width=15,
                command=card.destroy
            ).pack(pady=10)

        except Exception as e:

            try:
                conn.close()
            except:
                pass

            messagebox.showerror(
                "Report Card Error",
                str(e)
            )

    # ========================================================
    # CLEAR
    # ========================================================

    def clear_report():

        search_entry.delete(
            0,
            "end"
        )

        generate_report()

    # ========================================================
    # BUTTONS
    # ========================================================

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Generate Report",
        width=18,
        command=generate_report
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Export CSV",
        width=15,
        command=export_csv
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Export PDF",
        width=15,
        command=export_pdf
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Print",
        width=15,
        command=lambda: export_pdf()
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    # ========================================================
    # THIS IS THE IMPORTANT BUTTON
    # ========================================================

    tk.Button(
        button_frame,
        text="Generate Report Card",
        width=22,
        command=generate_report_card
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Clear",
        width=12,
        command=clear_report
    ).grid(
        row=0,
        column=5,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Close",
        width=12,
        command=window.destroy
    ).grid(
        row=0,
        column=6,
        padx=5
    )

    # ========================================================
    # SEARCH ENTER
    # ========================================================

    search_entry.bind(
        "<Return>",
        lambda event: generate_report()
    )

    # ========================================================
    # DOUBLE CLICK STUDENT
    # ========================================================

    def double_click_student(event):

        if table is None:
            return

        selected = table.selection()

        if not selected:
            return

        values = table.item(
            selected[0]
        )["values"]

        if not values:
            return

        # Student Report table:
        # ID, Roll No, Name, ...

        if report_combo.get() == "Student Report":

            search_entry.delete(
                0,
                "end"
            )

            search_entry.insert(
                0,
                str(values[1])
            )

            generate_report_card()

    # Bind after table exists
    def bind_table_double_click():

        if table:

            table.bind(
                "<Double-1>",
                double_click_student
            )

    # ========================================================
    # COMBO CHANGE
    # ========================================================

    def report_changed(event):

        generate_report()

        bind_table_double_click()

    report_combo.bind(
        "<<ComboboxSelected>>",
        report_changed
    )

    # ========================================================
    # INITIAL REPORT
    # ========================================================

    generate_report()

    bind_table_double_click()


# ============================================================
# DIRECT RUN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    reports_management()

    root.mainloop()