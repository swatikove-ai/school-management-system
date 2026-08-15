import sqlite3
from database import connect_db


def main():

    conn = connect_db()
    cursor = conn.cursor()

    print("\nChecking marks table...\n")

   

    cursor.execute("PRAGMA table_info(marks)")
    columns = cursor.fetchall()

    if not columns:
        print("Marks table nahi mila.")
        conn.close()
        return

    print("Existing columns:")

    for column in columns:
        print(" -", column[1])

    existing = {
        str(column[1]).lower()
        for column in columns
    }

   
    required_columns = {
        "english": "REAL DEFAULT 0",
        "hindi": "REAL DEFAULT 0",
        "maths": "REAL DEFAULT 0",
        "science": "REAL DEFAULT 0",
        "computer": "REAL DEFAULT 0",
        "total": "REAL DEFAULT 0",
        "percentage": "REAL DEFAULT 0",
        "grade": "TEXT DEFAULT ''"
    }

   

    for column, datatype in required_columns.items():

        if column.lower() not in existing:

            print(
                f"Adding missing column: {column}"
            )

            cursor.execute(
                f"""
                ALTER TABLE marks
                ADD COLUMN {column} {datatype}
                """
            )

    conn.commit()


    cursor.execute("PRAGMA table_info(marks)")

    final_columns = cursor.fetchall()

    print("\nFinal marks table columns:")

    for column in final_columns:
        print(" -", column[1])

    conn.close()

    print("\n================================")
    print("MARKS DATABASE FIXED SUCCESSFULLY")
    print("================================")


if __name__ == "__main__":
    main()