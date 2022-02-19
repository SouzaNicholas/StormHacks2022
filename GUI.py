from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Health Journal")
        self.setGeometry(0, 0, 600, 200)

        self.welcome = QLabel(self)
        self.welcome.setText("Hello, (Username)! Welcome back to your health journal!")
        self.welcome.resize(400, 50)
        self.welcome.move(100, 25)

        self.new_entry = QPushButton(self)
        self.new_entry.setText("New Entry")
        self.new_entry.resize(150, 50)
        self.new_entry.move(50, 120)

        self.check_logs = QPushButton(self)
        self.check_logs.setText("Check Logs")
        self.check_logs.resize(150, 50)
        self.check_logs.move(400, 120)

        self.show()
