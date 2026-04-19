import sys
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

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
    QComboBox,
    QTableWidget,
    QTableWidgetItem
)


# =========================
# ÚJ TRANZAKCIÓ ABLAK
# =========================
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


# =========================
# TÁBLÁZAT + TÖRLÉS
# =========================
class TransactionListDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tranzakciók listája")
        self.setGeometry(250, 250, 800, 400)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Összeg", "Kategória", "Típus", "Dátum"])

        # 🔥 FONTOS FIX
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.delete_button = QPushButton("Kijelölt tranzakció törlése")

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)

        self.delete_button.clicked.connect(self.delete_selected_transaction)

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("finance.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transactions")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)
        self.table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        self.table.resizeColumnsToContents()

    def delete_selected_transaction(self):
        selected_items = self.table.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Hiba", "Először jelölj ki egy tranzakciót.")
            return

        selected_row = selected_items[0].row()
        transaction_id_item = self.table.item(selected_row, 0)

        if transaction_id_item is None:
            QMessageBox.warning(self, "Hiba", "Nem sikerült kiolvasni az ID-t.")
            return

        transaction_id = int(transaction_id_item.text())

        reply = QMessageBox.question(
            self,
            "Megerősítés",
            "Biztos törlöd a kijelölt tranzakciót?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect("finance.db")
            cursor = conn.cursor()

            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Siker", "Tranzakció törölve.")
            self.load_data()


# =========================
# FŐ ABLAK
# =========================
class FinanceTrackerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Tracker")
        self.setGeometry(200, 200, 450, 350)

        self.title_label = QLabel("💰 Finance Tracker GUI")

        self.add_button = QPushButton("Új tranzakció hozzáadása")
        self.list_button = QPushButton("Tranzakciók listázása")
        self.summary_button = QPushButton("Összesítés")
        self.chart_button = QPushButton("Kiadások diagram")
        self.exit_button = QPushButton("Kilépés")

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.add_button)
        layout.addWidget(self.list_button)
        layout.addWidget(self.summary_button)
        layout.addWidget(self.chart_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_transaction)
        self.list_button.clicked.connect(self.list_transactions)
        self.summary_button.clicked.connect(self.show_summary)
        self.chart_button.clicked.connect(self.show_expense_chart)
        self.exit_button.clicked.connect(self.close)

    def add_transaction(self):
        dialog = AddTransactionDialog()
        dialog.exec()

    def list_transactions(self):
        dialog = TransactionListDialog()
        dialog.exec()

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

    def show_expense_chart(self):
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
            QMessageBox.information(self, "Diagram", "Nincs kiadás adat.")
            return

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.bar(categories, amounts)
        plt.title("Kiadások kategória szerint")
        plt.xlabel("Kategória")
        plt.ylabel("Összeg")
        plt.show()


# =========================
# APP INDÍTÁS
# =========================
app = QApplication(sys.argv)
window = FinanceTrackerGUI()
window.show()
sys.exit(app.exec())

