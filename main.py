import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

def expense_chart():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, SUM(amount)
    FROM transactions
    WHERE type = 'expense'
    GROUP BY category
    """)

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("Nincs kiadás adat.")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.bar(categories, amounts)
    plt.title("Kiadások kategória szerint")
    plt.xlabel("Kategória")
    plt.ylabel("Összeg")
    plt.show()

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


def get_valid_amount():
    while True:
        user_input = input("Összeg: ")

        try:
            amount = float(user_input)

            if amount <= 0:
                print("Az összeg legyen 0-nál nagyobb.")
            else:
                return amount

        except ValueError:
            print("Hiba: csak számot adhatsz meg.")


def get_valid_type():
    while True:
        type_ = input("Típus (income/expense): ").lower().strip()

        if type_ == "income" or type_ == "expense":
            return type_
        else:
            print("Hiba: csak 'income' vagy 'expense' lehet.")


def get_valid_id():
    while True:
        user_input = input("Add meg a tranzakció ID-ját: ")

        try:
            transaction_id = int(user_input)

            if transaction_id <= 0:
                print("Az ID legyen 1 vagy nagyobb.")
            else:
                return transaction_id

        except ValueError:
            print("Hiba: az ID csak egész szám lehet.")


def add_transaction():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    amount = get_valid_amount()
    category = get_valid_category()
    type_ = get_valid_type()
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
        print("\n--- ÖSSZES TRANZAKCIÓ ---")
        for row in rows:
            print(f"ID: {row[0]} | Összeg: {row[1]} | Kategória: {row[2]} | Típus: {row[3]} | Dátum: {row[4]}")

    conn.close()


def list_transactions_by_type(transaction_type):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE type = ?", (transaction_type,))
    rows = cursor.fetchall()

    if not rows:
        print(f"Nincs {transaction_type} típusú tranzakció.")
    else:
        print(f"\n--- {transaction_type.upper()} TRANZAKCIÓK ---")
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


def delete_transaction():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    transaction_id = get_valid_id()

    cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
    transaction = cursor.fetchone()

    if transaction is None:
        print("Nincs ilyen ID-jú tranzakció.")
        conn.close()
        return

    print("\nTörlésre kijelölt tranzakció:")
    print(f"ID: {transaction[0]} | Összeg: {transaction[1]} | Kategória: {transaction[2]} | Típus: {transaction[3]} | Dátum: {transaction[4]}")

    confirm = input("Biztos törlöd? (i/n): ").lower().strip()

    if confirm == "i":
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        print("Tranzakció törölve.")
    else:
        print("Törlés megszakítva.")

    conn.close()


def main():
    create_table()

    while True:
        print("\n===== FINANCE TRACKER =====")
        print("1 - Új tranzakció hozzáadása")
        print("2 - Összes tranzakció listázása")
        print("3 - Összesítés")
        print("4 - Tranzakció törlése")
        print("5 - Csak bevételek listázása")
        print("6 - Csak kiadások listázása")
        print("7 - Keresés kategória alapján")
        print("8 - Havi összesítés")
        print("9 - Kiadások diagram")
        print("10 - Bevétel vs kiadás diagram")
        print("11 - Kilépés")

        choice = input("Válassz egy opciót: ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            list_transactions()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            list_transactions_by_type("income")
        elif choice == "6":
            list_transactions_by_type("expense")
        elif choice == "7":
            search_by_category()
        elif choice == "8":
            monthly_summary()
        elif choice == "9":
            expense_chart()
        elif choice == "10":
            income_expense_chart()
        elif choice == "11":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás, próbáld újra.")

def search_by_category():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    category = input("Add meg a kategóriát: ").strip().lower()

    cursor.execute("SELECT * FROM transactions WHERE category = ?", (category,))
    rows = cursor.fetchall()

    if not rows:
        print("Nincs ilyen kategóriájú tranzakció.")
    else:
        print(f"\n--- '{category}' KATEGÓRIA ---")
        for row in rows:
            print(f"ID: {row[0]} | Összeg: {row[1]} | Kategória: {row[2]} | Típus: {row[3]} | Dátum: {row[4]}")

    conn.close()

def get_valid_category():
    while True:
        category = input("Kategória: ").strip().lower()

        if category == "":
            print("A kategória nem lehet üres.")
        else:
            return category


def income_expense_chart():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT type, SUM(amount)
    FROM transactions
    GROUP BY type
    """)

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("Nincs adat a diagramhoz.")
        return

    labels = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.bar(labels, amounts)
    plt.title("Bevétel vs kiadás")
    plt.xlabel("Típus")
    plt.ylabel("Összeg")
    plt.show()

def monthly_summary():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    month = input("Add meg a hónapot (pl: 2026-03): ").strip()

    cursor.execute("SELECT * FROM transactions WHERE date LIKE ?", (f"{month}%",))
    rows = cursor.fetchall()

    if not rows:
        print("Nincs adat erre a hónapra.")
        conn.close()
        return

    total_income = 0
    total_expense = 0

    for row in rows:
        if row[3] == "income":
            total_income += row[1]
        elif row[3] == "expense":
            total_expense += row[1]

    balance = total_income - total_expense

    print(f"\n--- {month} ÖSSZESÍTÉS ---")
    print(f"Bevétel: {total_income}")
    print(f"Kiadás: {total_expense}")
    print(f"Egyenleg: {balance}")

    conn.close()

main()