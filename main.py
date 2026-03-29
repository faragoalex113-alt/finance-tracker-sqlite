import sqlite3
from datetime import datetime


def create_table():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        type TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_transaction():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    amount = float(input("Összeg: "))
    category = input("Kategória: ")
    type_ = input("Típus (income/expense): ").lower()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO transactions (amount, category, type, date)
    VALUES (?, ?, ?, ?)
    """, (amount, category, type_, date))

    conn.commit()
    conn.close()

    print("Tranzakció mentve.")


def list_transactions():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    if not rows:
        print("Nincs még tranzakció.")
    else:
        print("\n--- TRANZAKCIÓK ---")
        for row in rows:
            print(f"ID: {row[0]} | Összeg: {row[1]} | Kategória: {row[2]} | Típus: {row[3]} | Dátum: {row[4]}")

    conn.close()


def show_summary():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    total_income = 0
    total_expense = 0

    for row in rows:
        if row[3] == "income":
            total_income += row[1]
        elif row[3] == "expense":
            total_expense += row[1]

    balance = total_income - total_expense

    print("\n--- ÖSSZESÍTÉS ---")
    print(f"Összes bevétel: {total_income}")
    print(f"Összes kiadás: {total_expense}")
    print(f"Egyenleg: {balance}")

    conn.close()


def main():
    create_table()

    while True:
        print("\n===== FINANCE TRACKER =====")
        print("1 - Új tranzakció hozzáadása")
        print("2 - Tranzakciók listázása")
        print("3 - Összesítés")
        print("4 - Kilépés")

        choice = input("Válassz egy opciót: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            list_transactions()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás, próbáld újra.")


main()