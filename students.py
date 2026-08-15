import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox

from database import connect_db



def student_management():

    window = tk.Toplevel()
    window.title("Student Management")
    window.geometry("1150x700")
    window.minsize(1000, 650)


    title_label = tk.Label(
        window,
        text="Student Management",
        font=("Arial", 24, "bold")
    )

    title_label.pack(pady=15)

   
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
        text="Student Details",
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
        width=25
    )

    name_entry.grid(
        row=0,
        column=3,
        padx=10
    )

    

    tk.Label(
        form,
        text="Age:"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )

    age_entry = tk.Entry(
        form,
        width=25
    )

    age_entry.grid(
        row=1,
        column=1,
        padx=10
    )

   
    tk.Label(
        form,
        text="Gender:"
    ).grid(
        row=1,
        column=2,
        padx=10,
        pady=10
    )

    gender_combo = ttk.Combobox(
        form,
        values=[
            "Male",
            "Female",
            "Other"
        ],
        state="readonly",
        width=22
    )

    gender_combo.grid(
        row=1,
        column=3,
        padx=10
    )

    gender_combo.current(0)

   

    tk.Label(
        form,
        text="Class:"
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=10
    )

    class_entry = tk.Entry(
        form,
        width=25
    )

    class_entry.grid(
        row=2,
        column=1,
        padx=10
    )

   

    tk.Label(
        form,
        text="Phone:"
    ).grid(
        row=2,
        column=2,
        padx=10,
        pady=10
    )

    phone_entry = tk.Entry(
        form,
        width=25
    )

    phone_entry.grid(
        row=2,
        column=3,
        padx=10
    )

   

    tk.Label(
        form,
        text="Email:"
    ).grid(
        row=3,
        column=0,
        padx=10,
        pady=10
    )

    email_entry = tk.Entry(
        form,
        width=25
    )

    email_entry.grid(
        row=3,
        column=1,
        padx=10
    )

   

    def clear_fields():

        roll_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        class_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

        gender_combo.current(0)

   

    def view_students():

        # Clear table
        for item in table.get_children():
            table.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                roll_no,
                name,
                age,
                gender,
                class_name,
                phone,
                email
            FROM students
            ORDER BY CAST(roll_no AS INTEGER) ASC
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            table.insert(
                "",
                tk.END,
                values=row
            )

   

    def search_student():

        search_value = search_entry.get().strip()

        # Clear table
        for item in table.get_children():
            table.delete(item)

        # Clear old fields
        clear_fields()

      
        if search_value == "":
            view_students()
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                roll_no,
                name,
                age,
                gender,
                class_name,
                phone,
                email
            FROM students
            WHERE roll_no LIKE ?
               OR name LIKE ?
               OR class_name LIKE ?
               OR phone LIKE ?
               OR email LIKE ?
            ORDER BY CAST(roll_no AS INTEGER) ASC
        """, (
            "%" + search_value + "%",
            "%" + search_value + "%",
            "%" + search_value + "%",
            "%" + search_value + "%",
            "%" + search_value + "%"
        ))

        rows = cursor.fetchall()

        conn.close()

        # Insert results
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

            name_entry.insert(
                0,
                row[2]
            )

            if row[3] is not None:

                age_entry.insert(
                    0,
                    row[3]
                )

            gender_combo.set(
                row[4]
            )

            if row[5] is not None:

                class_entry.insert(
                    0,
                    row[5]
                )

            if row[6] is not None:

                phone_entry.insert(
                    0,
                    row[6]
                )

            if row[7] is not None:

                email_entry.insert(
                    0,
                    row[7]
                )

        else:

            messagebox.showinfo(
                "Search",
                "No student found."
            )



    def add_student():

        roll = roll_entry.get().strip()
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_combo.get()
        class_name = class_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()

        # Validation
        if roll == "":

            messagebox.showerror(
                "Error",
                "Please enter Roll No."
            )

            return

        if name == "":

            messagebox.showerror(
                "Error",
                "Please enter Student Name."
            )

            return

        try:

            if age == "":
                age_value = None
            else:
                age_value = int(age)

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO students
                (
                    roll_no,
                    name,
                    age,
                    gender,
                    class_name,
                    phone,
                    email
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                roll,
                name,
                age_value,
                gender,
                class_name,
                phone,
                email
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Student added successfully!"
            )

            clear_fields()

            search_entry.delete(
                0,
                tk.END
            )

            view_students()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "This Roll No already exists!"
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Age must be a number."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

   

    def update_student():

        roll = roll_entry.get().strip()

        if roll == "":

            messagebox.showerror(
                "Error",
                "Please select a student first."
            )

            return

        name = name_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_combo.get()
        class_name = class_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()

        if name == "":

            messagebox.showerror(
                "Error",
                "Student Name is required."
            )

            return

        try:

            if age == "":
                age_value = None
            else:
                age_value = int(age)

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE students
                SET
                    name = ?,
                    age = ?,
                    gender = ?,
                    class_name = ?,
                    phone = ?,
                    email = ?
                WHERE roll_no = ?
            """, (
                name,
                age_value,
                gender,
                class_name,
                phone,
                email,
                roll
            ))

            conn.commit()

            rows_updated = cursor.rowcount

            conn.close()

            if rows_updated == 0:

                messagebox.showwarning(
                    "Not Found",
                    "Student not found."
                )

            else:

                messagebox.showinfo(
                    "Success",
                    "Student updated successfully!"
                )

                clear_fields()

                search_entry.delete(
                    0,
                    tk.END
                )

                view_students()

        except ValueError:

            messagebox.showerror(
                "Error",
                "Age must be a number."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

   
    def delete_student():

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a student."
            )

            return

        row = table.item(
            selected[0]
        )["values"]

        student_id = row[0]
        student_name = row[2]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{student_name}'?"
        )

        if not confirm:
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully!"
        )

        clear_fields()

        view_students()

   

    def select_student(event):

        selected = table.selection()

        if not selected:
            return

        row = table.item(
            selected[0]
        )["values"]

        clear_fields()

        # Roll
        roll_entry.insert(
            0,
            row[1]
        )

        # Name
        name_entry.insert(
            0,
            row[2]
        )

        # Age
        if row[3] is not None:

            age_entry.insert(
                0,
                row[3]
            )

        # Gender
        if row[4] is not None:

            gender_combo.set(
                row[4]
            )

        # Class
        if row[5] is not None:

            class_entry.insert(
                0,
                row[5]
            )

        # Phone
        if row[6] is not None:

            phone_entry.insert(
                0,
                row[6]
            )

        # Email
        if row[7] is not None:

            email_entry.insert(
                0,
                row[7]
            )


    def view_profile():

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a student."
            )

            return

        row = table.item(
            selected[0]
        )["values"]

        roll = str(row[1])
        name = str(row[2])
        age = row[3]
        gender = row[4]
        class_name = row[5]
        phone = row[6]
        email = row[7]


        profile = tk.Toplevel(window)

        profile.title(
            "Student Profile"
        )

        profile.geometry(
            "900x700"
        )

       

        tk.Label(
            profile,
            text="STUDENT PROFILE",
            font=("Arial", 24, "bold")
        ).pack(
            pady=15
        )

        tk.Label(
            profile,
            text=name,
            font=("Arial", 20, "bold")
        ).pack()

      

        info_frame = tk.LabelFrame(
            profile,
            text="Personal Information",
            font=("Arial", 12, "bold")
        )

        info_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        info_text = (
            f"Roll No: {roll}     "
            f"Name: {name}     "
            f"Age: {age if age else '-'}     "
            f"Gender: {gender if gender else '-'}\n\n"
            f"Class: {class_name if class_name else '-'}     "
            f"Phone: {phone if phone else '-'}     "
            f"Email: {email if email else '-'}"
        )

        tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 11),
            justify="left"
        ).pack(
            padx=20,
            pady=15
        )

      
        summary_frame = tk.Frame(
            profile
        )

        summary_frame.pack(
            fill="x",
            padx=25
        )

      
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COALESCE(SUM(total_fee), 0),
                COALESCE(SUM(paid_fee), 0),
                COALESCE(SUM(pending_fee), 0)
            FROM fees
            WHERE roll_no = ?
        """, (roll,))

        fees_data = cursor.fetchone()

       
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
            WHERE roll_no = ?
        """, (roll,))

        attendance_data = cursor.fetchone()

        conn.close()

        total_fee = fees_data[0]
        paid_fee = fees_data[1]
        pending_fee = fees_data[2]

        total_attendance = attendance_data[0]
        present = attendance_data[1]
        absent = total_attendance - present

        if total_attendance > 0:

            attendance_percentage = (
                present / total_attendance
            ) * 100

        else:

            attendance_percentage = 0


        fees_frame = tk.LabelFrame(
            summary_frame,
            text="Fees",
            font=("Arial", 12, "bold")
        )

        fees_frame.pack(
            side=tk.LEFT,
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            fees_frame,
            text=(
                f"Total: ₹{total_fee:,.2f}\n"
                f"Paid: ₹{paid_fee:,.2f}\n"
                f"Pending: ₹{pending_fee:,.2f}"
            ),
            font=("Arial", 11),
            justify="left"
        ).pack(
            padx=20,
            pady=15
        )

        attendance_frame = tk.LabelFrame(
            summary_frame,
            text="Attendance",
            font=("Arial", 12, "bold")
        )

        attendance_frame.pack(
            side=tk.LEFT,
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            attendance_frame,
            text=(
                f"Present: {present}\n"
                f"Absent: {absent}\n"
                f"Attendance: {attendance_percentage:.2f}%"
            ),
            font=("Arial", 11),
            justify="left"
        ).pack(
            padx=20,
            pady=15
        )


        marks_frame = tk.LabelFrame(
            profile,
            text="Academic Result",
            font=("Arial", 12, "bold")
        )

        marks_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                english,
                hindi,
                maths,
                science,
                computer,
                total,
                percentage,
                grade
            FROM student_marks
            WHERE roll_no = ?
        """, (roll,))

        marks_data = cursor.fetchone()

        conn.close()

        if marks_data:

            columns = (
                "English",
                "Hindi",
                "Maths",
                "Science",
                "Computer",
                "Total",
                "Percentage",
                "Grade"
            )

            values = (
                marks_data[0],
                marks_data[1],
                marks_data[2],
                marks_data[3],
                marks_data[4],
                marks_data[5],
                f"{marks_data[6]:.2f}%",
                marks_data[7]
            )

            marks_table = ttk.Treeview(
                marks_frame,
                columns=columns,
                show="headings",
                height=2
            )

            for column in columns:

                marks_table.heading(
                    column,
                    text=column
                )

                marks_table.column(
                    column,
                    width=100
                )

            marks_table.pack(
                fill="x",
                padx=10,
                pady=20
            )

            marks_table.insert(
                "",
                tk.END,
                values=values
            )

        else:

            tk.Label(
                marks_frame,
                text="No marks record found.",
                font=("Arial", 12),
                fg="gray"
            ).pack(
                pady=30
            )


        tk.Button(
            profile,
            text="Close",
            width=15,
            command=profile.destroy
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
        command=search_student
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Add Student",
        width=14,
        command=add_student
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Update",
        width=14,
        command=update_student
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Delete",
        width=14,
        command=delete_student
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    tk.Button(
        button_frame,
        text="View Profile",
        width=14,
        command=view_profile
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
        command=view_students
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
        "Name",
        "Age",
        "Gender",
        "Class",
        "Phone",
        "Email"
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
            width=120
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
        select_student
    )

    search_entry.bind(
        "<Return>",
        lambda event: search_student()
    )

   
    view_students()



if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    student_management()

    root.mainloop()