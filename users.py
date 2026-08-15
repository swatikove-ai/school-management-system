import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os


DB_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "school.db"
)



def create_users_table():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Default admin
    cursor.execute("""
        SELECT id
        FROM users
        WHERE username = ?
    """, ("admin",))

    existing = cursor.fetchone()

    if existing is None:

        cursor.execute("""
            INSERT INTO users
            (
                username,
                password,
                role
            )
            VALUES (?, ?, ?)
        """, (
            "admin",
            "admin123",
            "Admin"
        ))

    conn.commit()
    conn.close()



def user_management():

    create_users_table()

    window = tk.Toplevel()

    window.title(
        "User Management"
    )

    window.geometry(
        "950x650"
    )

    window.minsize(
        850,
        600
    )


    tk.Label(
        window,
        text="User Management",
        font=("Arial", 24, "bold")
    ).pack(
        pady=20
    )

  

    search_frame = tk.Frame(
        window
    )

    search_frame.pack(
        fill="x",
        padx=30,
        pady=5
    )

    tk.Label(
        search_frame,
        text="Search User:",
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
        text="User Details",
        font=("Arial", 12, "bold")
    )

    form.pack(
        fill="x",
        padx=30,
        pady=15
    )

   
    tk.Label(
        form,
        text="Username:"
    ).grid(
        row=0,
        column=0,
        padx=15,
        pady=15
    )

    username_entry = tk.Entry(
        form,
        width=30
    )

    username_entry.grid(
        row=0,
        column=1,
        padx=15
    )

  
    tk.Label(
        form,
        text="Password:"
    ).grid(
        row=0,
        column=2,
        padx=15,
        pady=15
    )

    password_entry = tk.Entry(
        form,
        width=30,
        show="*"
    )

    password_entry.grid(
        row=0,
        column=3,
        padx=15
    )

  

    tk.Label(
        form,
        text="Role:"
    ).grid(
        row=1,
        column=0,
        padx=15,
        pady=15
    )

    role_combo = ttk.Combobox(
        form,
        values=[
            "Admin",
            "Teacher"
        ],
        state="readonly",
        width=27
    )

    role_combo.grid(
        row=1,
        column=1,
        padx=15
    )

    role_combo.current(1)

   

    def clear_fields():

        username_entry.delete(
            0,
            tk.END
        )

        password_entry.delete(
            0,
            tk.END
        )

        role_combo.current(1)

        table.selection_remove(
            table.selection()
        )

 
    def view_users():

        for item in table.get_children():

            table.delete(item)

        conn = sqlite3.connect(
            DB_FILE
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                username,
                role
            FROM users
            ORDER BY id ASC
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            table.insert(
                "",
                tk.END,
                values=row
            )

  
    def search_user():

        value = search_entry.get().strip()

        for item in table.get_children():

            table.delete(item)

        if value == "":

            view_users()

            return

        conn = sqlite3.connect(
            DB_FILE
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                username,
                role
            FROM users
            WHERE username LIKE ?
               OR role LIKE ?
            ORDER BY id ASC
        """, (
            "%" + value + "%",
            "%" + value + "%"
        ))

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            table.insert(
                "",
                tk.END,
                values=row
            )

        if not rows:

            messagebox.showinfo(
                "Search",
                "No user found."
            )

   
    def add_user():

        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role = role_combo.get()

        if username == "":

            messagebox.showerror(
                "Error",
                "Please enter username."
            )

            return

        if password == "":

            messagebox.showerror(
                "Error",
                "Please enter password."
            )

            return

        if len(password) < 4:

            messagebox.showerror(
                "Error",
                "Password must contain at least 4 characters."
            )

            return

        if role == "":

            messagebox.showerror(
                "Error",
                "Please select a role."
            )

            return

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users
                (
                    username,
                    password,
                    role
                )
                VALUES (?, ?, ?)
            """, (
                username,
                password,
                role
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "User added successfully!"
            )

            clear_fields()
            view_users()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Username already exists."
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

   

    def update_user():

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a user."
            )

            return

        row = table.item(
            selected[0]
        )["values"]

        user_id = row[0]

        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role = role_combo.get()

        if username == "":

            messagebox.showerror(
                "Error",
                "Username is required."
            )

            return

        if role == "":

            messagebox.showerror(
                "Error",
                "Please select a role."
            )

            return

        conn = sqlite3.connect(
            DB_FILE
        )

        cursor = conn.cursor()

        try:

         
            if password == "":

                cursor.execute("""
                    UPDATE users
                    SET
                        username = ?,
                        role = ?
                    WHERE id = ?
                """, (
                    username,
                    role,
                    user_id
                ))

            else:

                if len(password) < 4:

                    conn.close()

                    messagebox.showerror(
                        "Error",
                        "Password must contain at least 4 characters."
                    )

                    return

                cursor.execute("""
                    UPDATE users
                    SET
                        username = ?,
                        password = ?,
                        role = ?
                    WHERE id = ?
                """, (
                    username,
                    password,
                    role,
                    user_id
                ))

            conn.commit()

            conn.close()

            messagebox.showinfo(
                "Success",
                "User updated successfully!"
            )

            clear_fields()
            view_users()

        except sqlite3.IntegrityError:

            conn.close()

            messagebox.showerror(
                "Error",
                "Username already exists."
            )

        except Exception as e:

            conn.close()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

   

    def delete_user():

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a user."
            )

            return

        row = table.item(
            selected[0]
        )["values"]

        user_id = row[0]
        username = row[1]
        role = row[2]

       
        if username == "admin":

            messagebox.showerror(
                "Not Allowed",
                "The main admin account cannot be deleted."
            )

            return

        # Don't delete last admin
        if role == "Admin":

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM users
                WHERE role = 'Admin'
            """)

            admin_count = cursor.fetchone()[0]

            conn.close()

            if admin_count <= 1:

                messagebox.showerror(
                    "Not Allowed",
                    "At least one Admin account must remain."
                )

                return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete user '{username}'?"
        )

        if not confirm:

            return

        conn = sqlite3.connect(
            DB_FILE
        )

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "User deleted successfully!"
        )

        clear_fields()
        view_users()

   
    def select_user(event):

        selected = table.selection()

        if not selected:

            return

        row = table.item(
            selected[0]
        )["values"]

        username_entry.delete(
            0,
            tk.END
        )

        username_entry.insert(
            0,
            row[1]
        )

        password_entry.delete(
            0,
            tk.END
        )

        role_combo.set(
            row[2]
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
        command=search_user
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Add User",
        width=14,
        command=add_user
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Update",
        width=14,
        command=update_user
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Delete",
        width=14,
        command=delete_user
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Clear",
        width=14,
        command=clear_fields
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Refresh",
        width=14,
        command=view_users
    ).grid(
        row=0,
        column=5,
        padx=5
    )

    
    table_frame = tk.Frame(
        window
    )

    table_frame.pack(
        fill=tk.BOTH,
        expand=True,
        padx=30,
        pady=15
    )

    columns = (
        "ID",
        "Username",
        "Role"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    table.heading(
        "ID",
        text="ID"
    )

    table.heading(
        "Username",
        text="Username"
    )

    table.heading(
        "Role",
        text="Role"
    )

    table.column(
        "ID",
        width=100
    )

    table.column(
        "Username",
        width=300
    )

    table.column(
        "Role",
        width=250
    )

    table.pack(
        side=tk.LEFT,
        fill=tk.BOTH,
        expand=True
    )

  

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side=tk.RIGHT,
        fill=tk.Y
    )

    
    table.bind(
        "<ButtonRelease-1>",
        select_user
    )

    search_entry.bind(
        "<Return>",
        lambda event: search_user()
    )

   
    view_users()




if __name__ == "__main__":

    create_users_table()

    root = tk.Tk()

    root.withdraw()

    user_management()

    root.mainloop()