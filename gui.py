import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)


class FinanceTrackerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Tracker")
        self.setGeometry(200, 200, 400, 300)

        self.title_label = QLabel("💰 Finance Tracker GUI")
        self.add_button = QPushButton("Új tranzakció hozzáadása")
        self.list_button = QPushButton("Tranzakciók listázása")
        self.summary_button = QPushButton("Összesítés")
        self.exit_button = QPushButton("Kilépés")

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.add_button)
        layout.addWidget(self.list_button)
        layout.addWidget(self.summary_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_transaction)
        self.list_button.clicked.connect(self.list_transactions)
        self.summary_button.clicked.connect(self.show_summary)
        self.exit_button.clicked.connect(self.close)

    def add_transaction(self):
        QMessageBox.information(self, "Info", "Itt lesz az új tranzakció hozzáadása.")

    def list_transactions(self):
        conn = sqlite3.connect("finance.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transactions")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            QMessageBox.information(self, "Tranzakciók", "Nincs még tranzakció.")
            return

        message = ""

        for row in rows:
            message += (
                f"ID: {row[0]} | "
                f"Összeg: {row[1]} | "
                f"Kategória: {row[2]} | "
                f"Típus: {row[3]} | "
                f"Dátum: {row[4]}\n"
            )

        QMessageBox.information(self, "Tranzakciók", message)

    def show_summary(self):
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

        conn.close()

        message = (
            f"Összes bevétel: {total_income}\n"
            f"Összes kiadás: {total_expense}\n"
            f"Egyenleg: {balance}"
        )

        QMessageBox.information(self, "Összesítés", message)


app = QApplication(sys.argv)
window = FinanceTrackerGUI()
window.show()
sys.exit(app.exec())