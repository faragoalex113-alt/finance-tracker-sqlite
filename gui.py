import sys
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
        QMessageBox.information(self, "Info", "Itt lesz a tranzakciók listázása.")

    def show_summary(self):
        QMessageBox.information(self, "Info", "Itt lesz az összesítés.")


app = QApplication(sys.argv)
window = FinanceTrackerGUI()
window.show()
sys.exit(app.exec())