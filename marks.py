import tkinter as tk
from tkinter import ttk, messagebox

from database import connect_db


def marks_management():

    window = tk.Toplevel()
    window.title("Marks Management")
    window.geometry("1450x850")
    window.minsize(1100, 700)


    conn = connect_db()
    cursor = conn.cursor()

   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE,
            student_name TEXT,
            english REAL DEFAULT 0,
            hindi REAL DEFAULT 0,
            maths REAL DEFAULT 0,
            science REAL DEFAULT 0,
            computer REAL DEFAULT 0,
            total REAL DEFAULT 0,
            percentage REAL DEFAULT 0,
            grade TEXT DEFAULT ''
        )
    """)

    conn.commit()

   

    search_var = tk.StringVar()

    roll_var = tk.StringVar()
    name_var = tk.StringVar()

    english_var = tk.StringVar()
    hindi_var = tk.StringVar()
    maths_var = tk.StringVar()
    science_var = tk.StringVar()
    computer_var = tk.StringVar()

    total_var = tk.StringVar()
    percentage_var = tk.StringVar()
    grade_var = tk.StringVar()

   

    def number(value):

        try:

            if value is None:
                return 0.0

            value = str(value).strip()

            if value == "":
                return 0.0

            return float(value)

        except:

            return 0.0

   

    def calculate_grade(percentage):

        percentage = number(percentage)

        if percentage >= 90:
            return "A+"

        elif percentage >= 80:
            return "A"

        elif percentage >= 70:
            return "B"

        elif percentage >= 60:
            return "C"

        elif percentage >= 50:
            return "D"

        elif percentage >= 33:
            return "E"

        else:
            return "F"

    

    def calculate_marks(*args):

        english = number(
            english_var.get()
        )

        hindi = number(
            hindi_var.get()
        )

        maths = number(
            maths_var.get()
        )

        science = number(
            science_var.get()
        )

        computer = number(
            computer_var.get()
        )

        total = (
            english +
            hindi +
            maths +
            science +
            computer
        )

        percentage = (
            total / 500
        ) * 100

        grade = calculate_grade(
            percentage
        )

        total_var.set(
            f"{total:.2f}"
        )

        percentage_var.set(
            f"{percentage:.2f}"
        )

        grade_var.set(
            grade
        )

    
    def get_student_name(roll):

        if not roll:
            return ""

        try:

            student_cursor = conn.cursor()

            student_cursor.execute(
                "PRAGMA table_info(students)"
            )

            columns = [
                row[1]
                for row in student_cursor.fetchall()
            ]

            roll_column = None
            name_column = None

            for col in columns:

                lower = str(col).lower()

                if lower in [
                    "roll_no",
                    "roll",
                    "rollnumber"
                ]:
                    roll_column = col

                if lower in [
                    "name",
                    "student_name"
                ]:
                    name_column = col

            if not roll_column or not name_column:
                return ""

            query = f"""
                SELECT "{name_column}"
                FROM students
                WHERE "{roll_column}" = ?
                LIMIT 1
            """

            student_cursor.execute(
                query,
                (str(roll),)
            )

            result = student_cursor.fetchone()

            if result:
                return str(result[0])

        except Exception:
            pass

        return ""

   
    def clear_fields():

        search_var.set("")

        roll_var.set("")
        name_var.set("")

        english_var.set("")
        hindi_var.set("")
        maths_var.set("")
        science_var.set("")
        computer_var.set("")

        total_var.set("")
        percentage_var.set("")
        grade_var.set("")

        table.selection_remove(
            table.selection()
        )

   

    def load_data():

        for item in table.get_children():

            table.delete(item)

        try:

            cursor.execute("""
                SELECT
                    id,
                    roll_no,
                    student_name,
                    english,
                    hindi,
                    maths,
                    science,
                    computer,
                    total,
                    percentage,
                    grade
                FROM marks
                ORDER BY id ASC
            """)

            rows = cursor.fetchall()

            search = search_var.get().strip().lower()

            
            display_id = 1

            for row in rows:

                if search:

                    if (
                        search not in str(row[1]).lower()
                        and
                        search not in str(row[2]).lower()
                    ):
                        continue

                table.insert(
                    "",
                    "end",
                    values=(
                        display_id,
                        row[1],
                        row[2],
                        number(row[3]),
                        number(row[4]),
                        number(row[5]),
                        number(row[6]),
                        number(row[7]),
                        number(row[8]),
                        number(row[9]),
                        row[10]
                    )
                )

                display_id += 1

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )



    def search_student():

        load_data()


    def add_marks():

        roll = roll_var.get().strip()

        if not roll:

            messagebox.showwarning(
                "Warning",
                "Roll No enter karo."
            )

            return

        # Automatically get name if empty
        name = name_var.get().strip()

        if not name:

            name = get_student_name(
                roll
            )

            if name:

                name_var.set(name)

        if not name:

            messagebox.showwarning(
                "Warning",
                "Student Name enter karo."
            )

            return

        # Calculate
        calculate_marks()

        english = number(
            english_var.get()
        )

        hindi = number(
            hindi_var.get()
        )

        maths = number(
            maths_var.get()
        )

        science = number(
            science_var.get()
        )

        computer = number(
            computer_var.get()
        )

        total = number(
            total_var.get()
        )

        percentage = number(
            percentage_var.get()
        )

        grade = grade_var.get()

        try:

            # Check existing roll
            cursor.execute(
                """
                SELECT id
                FROM marks
                WHERE roll_no = ?
                """,
                (roll,)
            )

            existing = cursor.fetchone()

            if existing:

                messagebox.showwarning(
                    "Already Exists",
                    f"Roll No {roll} ke marks already exist hain.\n"
                    f"Update button use karo."
                )

                return

            cursor.execute(
                """
                INSERT INTO marks (
                    roll_no,
                    student_name,
                    english,
                    hindi,
                    maths,
                    science,
                    computer,
                    total,
                    percentage,
                    grade
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    roll,
                    name,
                    english,
                    hindi,
                    maths,
                    science,
                    computer,
                    total,
                    percentage,
                    grade
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Marks successfully added."
            )

            load_data()

        except Exception as e:

            messagebox.showerror(
                "Add Marks Error",
                str(e)
            )

   

    def update_marks():

        roll = roll_var.get().strip()

        if not roll:

            messagebox.showwarning(
                "Warning",
                "Roll No enter karo."
            )

            return

        name = name_var.get().strip()

        if not name:

            name = get_student_name(
                roll
            )

        calculate_marks()

        english = number(
            english_var.get()
        )

        hindi = number(
            hindi_var.get()
        )

        maths = number(
            maths_var.get()
        )

        science = number(
            science_var.get()
        )

        computer = number(
            computer_var.get()
        )

        total = number(
            total_var.get()
        )

        percentage = number(
            percentage_var.get()
        )

        grade = grade_var.get()

        try:

            cursor.execute(
                """
                UPDATE marks
                SET
                    student_name = ?,
                    english = ?,
                    hindi = ?,
                    maths = ?,
                    science = ?,
                    computer = ?,
                    total = ?,
                    percentage = ?,
                    grade = ?
                WHERE roll_no = ?
                """,
                (
                    name,
                    english,
                    hindi,
                    maths,
                    science,
                    computer,
                    total,
                    percentage,
                    grade,
                    roll
                )
            )

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Not Found",
                    f"Roll No {roll} ke marks nahi mile."
                )

                return

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Marks successfully updated."
            )

            load_data()

        except Exception as e:

            messagebox.showerror(
                "Update Error",
                str(e)
            )

  
    def delete_marks():

        roll = roll_var.get().strip()

        if not roll:

            messagebox.showwarning(
                "Warning",
                "Pehle student select karo."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Roll No {roll} ke marks delete karna hai?"
        )

        if not confirm:
            return

        try:

            cursor.execute(
                """
                DELETE FROM marks
                WHERE roll_no = ?
                """,
                (roll,)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Marks successfully deleted."
            )

            clear_fields()
            load_data()

        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                str(e)
            )

   
    def select_marks(event=None):

        selected = table.selection()

        if not selected:
            return

        item = table.item(
            selected[0]
        )

        row = item["values"]

        if len(row) < 11:
            return


        roll_var.set(
            str(row[1])
        )

        name_var.set(
            str(row[2])
        )

        english_var.set(
            f"{number(row[3]):.2f}"
        )

        hindi_var.set(
            f"{number(row[4]):.2f}"
        )

        maths_var.set(
            f"{number(row[5]):.2f}"
        )

        science_var.set(
            f"{number(row[6]):.2f}"
        )

        computer_var.set(
            f"{number(row[7]):.2f}"
        )

        total_var.set(
            f"{number(row[8]):.2f}"
        )

        percentage_var.set(
            f"{number(row[9]):.2f}"
        )

        grade_var.set(
            str(row[10] or "")
        )

   
    def result_card():

        roll = roll_var.get().strip()

        if not roll:

            messagebox.showwarning(
                "Result Card",
                "Pehle student select karo."
            )

            return

        name = name_var.get().strip()

        if not name:

            name = get_student_name(
                roll
            )

        calculate_marks()

        english = number(
            english_var.get()
        )

        hindi = number(
            hindi_var.get()
        )

        maths = number(
            maths_var.get()
        )

        science = number(
            science_var.get()
        )

        computer = number(
            computer_var.get()
        )

        total = number(
            total_var.get()
        )

        percentage = number(
            percentage_var.get()
        )

        grade = grade_var.get()

        card = tk.Toplevel(window)

        card.title(
            "Student Result Card"
        )

        card.geometry(
            "850x700"
        )

    
        tk.Label(
            card,
            text="SCHOOL MANAGEMENT SYSTEM",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            card,
            text="STUDENT RESULT CARD",
            font=("Arial", 18, "bold")
        ).pack(pady=5)

       
        info = tk.LabelFrame(
            card,
            text="Student Information",
            font=("Arial", 11, "bold")
        )

        info.pack(
            fill="x",
            padx=30,
            pady=15
        )

        tk.Label(
            info,
            text="Roll No:",
            font=("Arial", 11, "bold")
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=10
        )

        tk.Label(
            info,
            text=roll
        ).grid(
            row=0,
            column=1,
            padx=20
        )

        tk.Label(
            info,
            text="Student Name:",
            font=("Arial", 11, "bold")
        ).grid(
            row=0,
            column=2,
            padx=20
        )

        tk.Label(
            info,
            text=name
        ).grid(
            row=0,
            column=3,
            padx=20
        )


        marks_frame = tk.LabelFrame(
            card,
            text="Marks",
            font=("Arial", 11, "bold")
        )

        marks_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        result_table = ttk.Treeview(
            marks_frame,
            columns=(
                "Subject",
                "Marks",
                "Total"
            ),
            show="headings"
        )

        result_table.heading(
            "Subject",
            text="Subject"
        )

        result_table.heading(
            "Marks",
            text="Marks"
        )

        result_table.heading(
            "Total",
            text="Total"
        )

        result_table.column(
            "Subject",
            width=300,
            anchor="center"
        )

        result_table.column(
            "Marks",
            width=200,
            anchor="center"
        )

        result_table.column(
            "Total",
            width=200,
            anchor="center"
        )

        result_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        subjects = [
            ("English", english),
            ("Hindi", hindi),
            ("Maths", maths),
            ("Science", science),
            ("Computer", computer)
        ]

        for subject, marks in subjects:

            result_table.insert(
                "",
                "end",
                values=(
                    subject,
                    f"{marks:.2f}",
                    "100"
                )
            )


        tk.Label(
            card,
            text=(
                f"Total Marks: {total:.2f} / 500"
            ),
            font=("Arial", 13, "bold")
        ).pack(pady=5)

        tk.Label(
            card,
            text=(
                f"Percentage: {percentage:.2f}%"
            ),
            font=("Arial", 13, "bold")
        ).pack(pady=5)

        tk.Label(
            card,
            text=(
                f"Grade: {grade}"
            ),
            font=("Arial", 13, "bold")
        ).pack(pady=5)

        tk.Button(
            card,
            text="Close",
            width=15,
            command=card.destroy
        ).pack(pady=15)


    def close_window():

        try:
            conn.close()
        except:
            pass

        window.destroy()

    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )


    tk.Label(
        window,
        text="Marks Management",
        font=("Arial", 25, "bold")
    ).pack(pady=15)


    search_frame = tk.Frame(window)

    search_frame.pack(
        fill="x",
        padx=30,
        pady=5
    )

    tk.Label(
        search_frame,
        text="Search Student:",
        font=("Arial", 11, "bold")
    ).pack(
        side="left"
    )

    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        width=35,
        font=("Arial", 11)
    )

    search_entry.pack(
        side="left",
        padx=10
    )

    tk.Button(
        search_frame,
        text="Search",
        width=12,
        command=search_student
    ).pack(
        side="left",
        padx=5
    )


    details = tk.LabelFrame(
        window,
        text="Student Marks",
        font=("Arial", 11, "bold")
    )

    details.pack(
        fill="x",
        padx=20,
        pady=10
    )


    tk.Label(
        details,
        text="Roll No:"
    ).grid(
        row=0,
        column=0,
        padx=20,
        pady=10,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=roll_var,
        width=22
    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    tk.Label(
        details,
        text="Student Name:"
    ).grid(
        row=0,
        column=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=name_var,
        width=22
    ).grid(
        row=0,
        column=3,
        padx=10,
        pady=10
    )


    tk.Label(
        details,
        text="English:"
    ).grid(
        row=1,
        column=0,
        padx=20,
        pady=10,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=english_var,
        width=22
    ).grid(
        row=1,
        column=1,
        padx=10
    )

    tk.Label(
        details,
        text="Hindi:"
    ).grid(
        row=1,
        column=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=hindi_var,
        width=22
    ).grid(
        row=1,
        column=3,
        padx=10
    )


    tk.Label(
        details,
        text="Maths:"
    ).grid(
        row=2,
        column=0,
        padx=20,
        pady=10,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=maths_var,
        width=22
    ).grid(
        row=2,
        column=1,
        padx=10
    )

    tk.Label(
        details,
        text="Science:"
    ).grid(
        row=2,
        column=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=science_var,
        width=22
    ).grid(
        row=2,
        column=3,
        padx=10
    )

    tk.Label(
        details,
        text="Computer:"
    ).grid(
        row=3,
        column=0,
        padx=20,
        pady=10,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=computer_var,
        width=22
    ).grid(
        row=3,
        column=1,
        padx=10
    )

    tk.Label(
        details,
        text="Total:"
    ).grid(
        row=3,
        column=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=total_var,
        width=22,
        state="readonly"
    ).grid(
        row=3,
        column=3,
        padx=10
    )

    tk.Label(
        details,
        text="Percentage:"
    ).grid(
        row=4,
        column=0,
        padx=20,
        pady=10,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=percentage_var,
        width=22,
        state="readonly"
    ).grid(
        row=4,
        column=1,
        padx=10
    )


    tk.Label(
        details,
        text="Grade:"
    ).grid(
        row=4,
        column=2,
        padx=20,
        pady=10,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=grade_var,
        width=22,
        state="readonly"
    ).grid(
        row=4,
        column=3,
        padx=10
    )


    button_frame = tk.Frame(window)

    button_frame.pack(
        pady=10
    )

    tk.Button(
        button_frame,
        text="Search",
        width=14,
        command=search_student
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Add Marks",
        width=14,
        command=add_marks
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Update",
        width=14,
        command=update_marks
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Delete",
        width=14,
        command=delete_marks
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Result Card",
        width=14,
        command=result_card
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
        command=load_data
    ).grid(
        row=0,
        column=6,
        padx=5
    )


    table_frame = tk.Frame(window)

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    columns = (
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
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    widths = [
        60,
        90,
        160,
        90,
        90,
        90,
        90,
        100,
        100,
        110,
        80
    ]

    for column, width in zip(
        columns,
        widths
    ):

        table.heading(
            column,
            text=column
        )

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

    table.bind(
        "<ButtonRelease-1>",
        select_marks
    )



    english_var.trace_add(
        "write",
        calculate_marks
    )

    hindi_var.trace_add(
        "write",
        calculate_marks
    )

    maths_var.trace_add(
        "write",
        calculate_marks
    )

    science_var.trace_add(
        "write",
        calculate_marks
    )

    computer_var.trace_add(
        "write",
        calculate_marks
    )


    load_data()


if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    marks_management()

    root.mainloop()