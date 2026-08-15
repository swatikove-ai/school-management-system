import tkinter as tk
from tkinter import ttk, messagebox

from database import connect_db


def fees_management():

    window = tk.Toplevel()
    window.title("Fees Management")
    window.geometry("1400x800")
    window.minsize(1100, 650)

    conn = connect_db()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE,
            student_name TEXT,
            total_fees REAL DEFAULT 0,
            paid_fees REAL DEFAULT 0,
            pending_fees REAL DEFAULT 0
        )
    """)

    conn.commit()

    # Add missing columns if an older fees table already exists.
    cursor.execute("PRAGMA table_info(fees)")
    existing_columns = {
        str(row[1]).lower()
        for row in cursor.fetchall()
    }

    required_columns = {
        "roll_no": "TEXT",
        "student_name": "TEXT",
        "total_fees": "REAL DEFAULT 0",
        "paid_fees": "REAL DEFAULT 0",
        "pending_fees": "REAL DEFAULT 0"
    }

    for column, datatype in required_columns.items():
        if column.lower() not in existing_columns:
            cursor.execute(
                f"ALTER TABLE fees ADD COLUMN {column} {datatype}"
            )

    conn.commit()


    search_var = tk.StringVar()

    roll_var = tk.StringVar()
    name_var = tk.StringVar()

    total_fees_var = tk.StringVar()
    paid_fees_var = tk.StringVar()
    pending_fees_var = tk.StringVar()



    def number(value):
        try:
            if value is None:
                return 0.0

            value = str(value).strip()

            if value == "":
                return 0.0

            return float(value)

        except (ValueError, TypeError):
            return 0.0


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

            for column in columns:

                lower = str(column).lower()

                if lower in (
                    "roll_no",
                    "roll",
                    "rollnumber"
                ):
                    roll_column = column

                if lower in (
                    "name",
                    "student_name"
                ):
                    name_column = column

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
            return ""

        return ""


    def calculate_pending(*args):

        total = number(
            total_fees_var.get()
        )

        paid = number(
            paid_fees_var.get()
        )

        pending = total - paid

        if pending < 0:
            pending = 0

        pending_fees_var.set(
            f"{pending:.2f}"
        )


    def clear_fields():

        search_var.set("")

        roll_var.set("")
        name_var.set("")

        total_fees_var.set("")
        paid_fees_var.set("")
        pending_fees_var.set("")

        if table.selection():
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
                    total_fees,
                    paid_fees,
                    pending_fees
                FROM fees
                ORDER BY id ASC
            """)

            rows = cursor.fetchall()

            search = (
                search_var.get()
                .strip()
                .lower()
            )

            display_id = 1

            for row in rows:

                if search:

                    if (
                        search not in str(row[1]).lower()
                        and
                        search not in str(row[2]).lower()
                    ):
                        continue

                total = number(row[3])
                paid = number(row[4])

                pending = total - paid

                if pending < 0:
                    pending = 0

                table.insert(
                    "",
                    "end",
                    values=(
                        display_id,
                        row[1],
                        row[2],
                        f"{total:.2f}",
                        f"{paid:.2f}",
                        f"{pending:.2f}"
                    )
                )

                display_id += 1

        except Exception as e:

            messagebox.showerror(
                "Fees Error",
                str(e)
            )


    def search_fees():
        load_data()


    def add_fees():

        roll = roll_var.get().strip()

        if not roll:
            messagebox.showwarning(
                "Warning",
                "Roll No enter karo."
            )
            return

        name = name_var.get().strip()

        if not name:
            name = get_student_name(roll)

            if name:
                name_var.set(name)

        if not name:
            messagebox.showwarning(
                "Warning",
                "Student Name enter karo."
            )
            return

        total = number(
            total_fees_var.get()
        )

        paid = number(
            paid_fees_var.get()
        )

        if total < 0 or paid < 0:
            messagebox.showwarning(
                "Warning",
                "Fees negative nahi ho sakti."
            )
            return

        if paid > total:
            messagebox.showwarning(
                "Warning",
                "Paid Fees, Total Fees se zyada nahi ho sakti."
            )
            return

        pending = total - paid

        try:

            cursor.execute(
                """
                SELECT id
                FROM fees
                WHERE roll_no = ?
                """,
                (roll,)
            )

            existing = cursor.fetchone()

            if existing:

                messagebox.showwarning(
                    "Already Exists",
                    f"Roll No {roll} ke fees record already hain.\n"
                    "Update button use karo."
                )
                return

            cursor.execute(
                """
                INSERT INTO fees (
                    roll_no,
                    student_name,
                    total_fees,
                    paid_fees,
                    pending_fees
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    roll,
                    name,
                    total,
                    paid,
                    pending
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Fees successfully added."
            )

            load_data()

        except Exception as e:

            messagebox.showerror(
                "Add Fees Error",
                str(e)
            )


    def update_fees():

        roll = roll_var.get().strip()

        if not roll:
            messagebox.showwarning(
                "Warning",
                "Pehle student select karo."
            )
            return

        name = name_var.get().strip()

        if not name:
            name = get_student_name(roll)

        total = number(
            total_fees_var.get()
        )

        paid = number(
            paid_fees_var.get()
        )

        if total < 0 or paid < 0:
            messagebox.showwarning(
                "Warning",
                "Fees negative nahi ho sakti."
            )
            return

        if paid > total:
            messagebox.showwarning(
                "Warning",
                "Paid Fees, Total Fees se zyada nahi ho sakti."
            )
            return

        pending = total - paid

        try:

            cursor.execute(
                """
                UPDATE fees
                SET
                    student_name = ?,
                    total_fees = ?,
                    paid_fees = ?,
                    pending_fees = ?
                WHERE roll_no = ?
                """,
                (
                    name,
                    total,
                    paid,
                    pending,
                    roll
                )
            )

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Not Found",
                    f"Roll No {roll} ka fees record nahi mila."
                )
                return

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Fees successfully updated."
            )

            load_data()

        except Exception as e:

            messagebox.showerror(
                "Update Fees Error",
                str(e)
            )


    def delete_fees():

        roll = roll_var.get().strip()

        if not roll:
            messagebox.showwarning(
                "Warning",
                "Pehle student select karo."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Roll No {roll} ka fees record delete karna hai?"
        )

        if not confirm:
            return

        try:

            cursor.execute(
                """
                DELETE FROM fees
                WHERE roll_no = ?
                """,
                (roll,)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Fees record successfully deleted."
            )

            clear_fields()
            load_data()

        except Exception as e:

            messagebox.showerror(
                "Delete Fees Error",
                str(e)
            )


    def select_fees(event=None):

        selected = table.selection()

        if not selected:
            return

        item = table.item(
            selected[0]
        )

        row = item["values"]

        if len(row) < 6:
            return

        roll_var.set(
            str(row[1])
        )

        name_var.set(
            str(row[2])
        )

        total_fees_var.set(
            f"{number(row[3]):.2f}"
        )

        paid_fees_var.set(
            f"{number(row[4]):.2f}"
        )

        pending_fees_var.set(
            f"{number(row[5]):.2f}"
        )


    def fee_receipt():

        roll = roll_var.get().strip()

        if not roll:
            messagebox.showwarning(
                "Fee Receipt",
                "Pehle student select karo."
            )
            return

        name = name_var.get().strip()

        total = number(
            total_fees_var.get()
        )

        paid = number(
            paid_fees_var.get()
        )

        pending = total - paid

        if pending < 0:
            pending = 0

        receipt = tk.Toplevel(window)

        receipt.title(
            "Fee Receipt"
        )

        receipt.geometry(
            "600x600"
        )

        receipt.resizable(
            False,
            False
        )

        tk.Label(
            receipt,
            text="SCHOOL MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold")
        ).pack(pady=(25, 5))

        tk.Label(
            receipt,
            text="FEE RECEIPT",
            font=("Arial", 16, "bold")
        ).pack(pady=5)

        frame = tk.LabelFrame(
            receipt,
            text="Student & Fee Details",
            font=("Arial", 11, "bold")
        )

        frame.pack(
            fill="x",
            padx=30,
            pady=25
        )

        details = [
            ("Roll No:", roll),
            ("Student Name:", name),
            ("Total Fees:", f"₹{total:,.2f}"),
            ("Paid Fees:", f"₹{paid:,.2f}"),
            ("Pending Fees:", f"₹{pending:,.2f}")
        ]

        for i, (label, value) in enumerate(details):

            tk.Label(
                frame,
                text=label,
                font=("Arial", 11, "bold")
            ).grid(
                row=i,
                column=0,
                sticky="w",
                padx=20,
                pady=12
            )

            tk.Label(
                frame,
                text=value,
                font=("Arial", 11)
            ).grid(
                row=i,
                column=1,
                sticky="w",
                padx=20,
                pady=12
            )

        tk.Label(
            receipt,
            text="Thank you",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        tk.Button(
            receipt,
            text="Close",
            width=15,
            command=receipt.destroy
        ).pack(pady=15)


    def close_window():

        try:
            conn.close()
        except Exception:
            pass

        window.destroy()

    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )

   

    tk.Label(
        window,
        text="Fees Management",
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

    tk.Entry(
        search_frame,
        textvariable=search_var,
        width=35,
        font=("Arial", 11)
    ).pack(
        side="left",
        padx=10
    )

    tk.Button(
        search_frame,
        text="Search",
        width=12,
        command=search_fees
    ).pack(
        side="left",
        padx=5
    )


    details = tk.LabelFrame(
        window,
        text="Fees Details",
        font=("Arial", 11, "bold")
    )

    details.pack(
        fill="x",
        padx=20,
        pady=10
    )

    # Roll No
    tk.Label(
        details,
        text="Roll No:"
    ).grid(
        row=0,
        column=0,
        padx=20,
        pady=12,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=roll_var,
        width=25
    ).grid(
        row=0,
        column=1,
        padx=10
    )

    # Student Name
    tk.Label(
        details,
        text="Student Name:"
    ).grid(
        row=0,
        column=2,
        padx=20,
        pady=12,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=name_var,
        width=25
    ).grid(
        row=0,
        column=3,
        padx=10
    )

    # Total Fees
    tk.Label(
        details,
        text="Total Fees:"
    ).grid(
        row=1,
        column=0,
        padx=20,
        pady=12,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=total_fees_var,
        width=25
    ).grid(
        row=1,
        column=1,
        padx=10
    )

    # Paid Fees
    tk.Label(
        details,
        text="Paid Fees:"
    ).grid(
        row=1,
        column=2,
        padx=20,
        pady=12,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=paid_fees_var,
        width=25
    ).grid(
        row=1,
        column=3,
        padx=10
    )

    # Pending Fees
    tk.Label(
        details,
        text="Pending Fees:"
    ).grid(
        row=2,
        column=0,
        padx=20,
        pady=12,
        sticky="w"
    )

    tk.Entry(
        details,
        textvariable=pending_fees_var,
        width=25,
        state="readonly"
    ).grid(
        row=2,
        column=1,
        padx=10
    )


    button_frame = tk.Frame(window)

    button_frame.pack(pady=10)

    buttons = [
        ("Search", search_fees),
        ("Add Fees", add_fees),
        ("Update", update_fees),
        ("Delete", delete_fees),
        ("Fee Receipt", fee_receipt),
        ("Clear", clear_fields),
        ("Refresh", load_data)
    ]

    for index, (text, command) in enumerate(buttons):

        tk.Button(
            button_frame,
            text=text,
            width=14,
            command=command
        ).grid(
            row=0,
            column=index,
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
        "Total Fees",
        "Paid Fees",
        "Pending Fees"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    widths = {
        "ID": 70,
        "Roll No": 120,
        "Student Name": 220,
        "Total Fees": 180,
        "Paid Fees": 180,
        "Pending Fees": 180
    }

    for column in columns:

        table.heading(
            column,
            text=column
        )

        table.column(
            column,
            width=widths[column],
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
        select_fees
    )

   

    total_fees_var.trace_add(
        "write",
        calculate_pending
    )

    paid_fees_var.trace_add(
        "write",
        calculate_pending
    )


    load_data()


if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    fees_management()

    root.mainloop()