import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import subprocess
import sys


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


def open_dashboard(username, role):

    main_file = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "main.py"
    )

    if not os.path.exists(main_file):

        messagebox.showerror(
            "Error",
            "main.py file was not found."
        )

        return

    try:

        subprocess.Popen([
            sys.executable,
            main_file,
            username,
            role
        ])

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Unable to open dashboard:\n{e}"
        )



def login_window():

    root = tk.Tk()

    root.title(
        "School Management System - Login"
    )

    root.geometry(
        "500x420"
    )

    root.resizable(
        False,
        False
    )


    tk.Label(
        root,
        text="SCHOOL MANAGEMENT SYSTEM",
        font=("Arial", 20, "bold")
    ).pack(
        pady=(30, 5)
    )

    tk.Label(
        root,
        text="Login",
        font=("Arial", 17, "bold")
    ).pack(
        pady=10
    )


    login_frame = tk.Frame(
        root
    )

    login_frame.pack(
        pady=20
    )


    tk.Label(
        login_frame,
        text="Username:",
        font=("Arial", 11, "bold")
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=15,
        sticky="e"
    )

    username_entry = tk.Entry(
        login_frame,
        width=28,
        font=("Arial", 11)
    )

    username_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=15
    )

    tk.Label(
        login_frame,
        text="Password:",
        font=("Arial", 11, "bold")
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=15,
        sticky="e"
    )

    password_entry = tk.Entry(
        login_frame,
        width=28,
        show="*",
        font=("Arial", 11)
    )

    password_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=15
    )

    def login():

        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == "":

            messagebox.showerror(
                "Login Error",
                "Please enter username."
            )

            username_entry.focus()

            return

        if password == "":

            messagebox.showerror(
                "Login Error",
                "Please enter password."
            )

            password_entry.focus()

            return

        try:

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
                WHERE username = ?
                  AND password = ?
            """, (
                username,
                password
            ))

            user = cursor.fetchone()

            conn.close()

            if user:

                messagebox.showinfo(
                    "Login Successful",
                    f"Welcome {user[1]}!"
                )

                root.destroy()

                open_dashboard(
                    user[1],
                    user[2]
                )

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )

                password_entry.delete(
                    0,
                    tk.END
                )

                password_entry.focus()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        root,
        text="LOGIN",
        width=20,
        font=("Arial", 11, "bold"),
        command=login
    ).pack(
        pady=15
    )


    password_entry.bind(
        "<Return>",
        lambda event: login()
    )

    username_entry.bind(
        "<Return>",
        lambda event: password_entry.focus()
    )

    username_entry.focus()

    root.mainloop()


if __name__ == "__main__":

    create_users_table()

    login_window()