from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QComboBox, QLineEdit


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
        self.new_entry.clicked.connect(self.new_entry_win)

        self.check_logs = QPushButton(self)
        self.check_logs.setText("Check Logs")
        self.check_logs.resize(150, 50)
        self.check_logs.move(400, 120)

        self.show()

    def new_entry_win(self):
        self.entry = EntryWindow()
        self.entry.show()

    def new_log_win(self):
        self.log = LogWindow()
        self.log.show()


class EntryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Log Entry")
        self.setGeometry(0, 0, 600, 500)

        self.emotions = QComboBox(self)
        for i in self.fetch_emotions().split(", "):
            self.emotions.addItem(i)
        self.emotions.move(50, 10)
        self.emotions.resize(150, 30)

        self.action_prompt = QLabel(self)
        self.action_prompt.setText("What did you do today?")
        self.action_prompt.move(50, 70)
        self.action_prompt.resize(200, 30)

        self.action_field = QLineEdit(self)
        self.action_field.move(50, 100)
        self.action_field.resize(500, 150)

        self.cause_prompt = QLabel(self)
        self.cause_prompt.setText("Why do you think you feel that way?")
        self.cause_prompt.move(50, 270)
        self.cause_prompt.resize(200, 30)

        self.cause_field = QLineEdit(self)
        self.cause_field.move(50, 300)
        self.cause_field.resize(500, 150)

    def fetch_emotions(self):
        with open('emotions.txt', 'r') as e:
            return e.read()


class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()

