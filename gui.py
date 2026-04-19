import sys
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox
)


class AddTransactionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Új tranzakció hozzáadása")
        self.setGeometry(300, 300, 300, 200)

        self.amount_input = QLineEdit()
        self.category_input = QLineEdit()
        self.type_input = QComboBox()
        self.type_input.addItems(["income", "expense"])

        self.save_button = QPushButton("Mentés")

        layout = QFormLayout()
        layout.addRow("Összeg:", self.amount_input)
        layout.addRow("Kategória:", self.category_input)
        layout.addRow("Típus:", self.type_input)
        layout.addRow(self.save_button)

        self.setLayout(layout)

        self.save_button.clicked.connect(self.save_transaction)

    def save_transaction(self):
        amount_text = self.amount_input.text().strip()
        category = self.category_input.text().strip().lower()
        type_ = self.type_input.currentText()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if amount_text == "":
            QMessageBox.warning(self, "Hiba", "Az összeg nem lehet üres.")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self, "Hiba", "Az összeg legyen 0-nál nagyobb.")
                return
        except ValueError:
            QMessageBox.warning(self, "Hiba", "Az összeg csak szám lehet.")
            return

        if category == "":
            QMessageBox.warning(self, "Hiba", "A kategória nem lehet üres.")
            return

        conn = sqlite3.connect("finance.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO transactions (amount, category, type, date)
        VALUES (?, ?, ?, ?)
        """, (amount, category, type_, date))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "Siker", "Tranzakció mentve.")
        self.accept()


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
        dialog = AddTransactionDialog()
        dialog.exec()

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