import PyQt5.QtCore
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit, \
    QInputDialog, QWidget, QFormLayout, QGridLayout
from PyQt5.QtGui import *
import DB
from os.path import exists
from datetime import date


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 600, 500)
        self.setFixedSize(600, 500)

        if not exists("name.txt"):
            self.change_name_win()

        self.username = open("name.txt", "r")
        self.name_string = self.username.readline()

        self.setWindowTitle(self.name_string + "\'s Health Journal")
        self.white = QLabel(self)
        self.pixwhite = QPixmap('white.png')

        # adding image to label
        self.white.setPixmap(self.pixwhite)

        # Optional, resize label to image size
        self.white.resize(self.pixwhite.width(),
                                   self.pixwhite.height())
        self.welcome = QLabel(self)
        self.welcome.setText("Hello, " + self.name_string + "! Welcome back!")
        self.welcome.resize(400, 50)
        self.welcome.move(15, 30)
        self.welcome.setFont(QFont('Helvetica', 15))
        self.Health_Journal = QLabel(self)
        # loading image
        self.pixmap = QPixmap('small.png')

        # adding image to label
        self.Health_Journal.setPixmap(self.pixmap)

        # Optional, resize label to image size
        self.Health_Journal.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.Health_Journal.move(-35, 0)
        self.blue = QLabel(self)
        # loading image
        self.pixmap2 = QPixmap('blue.png')

        # adding image to label
        self.blue.setPixmap(self.pixmap2)

        # Optional, resize label to image size
        self.blue.resize(self.pixmap2.width(),
                                   self.pixmap2.height())
        self.blue.move(0, 230)
        self.new_entry = QPushButton(self)
        self.new_entry.setText("New Entry")
        self.new_entry.resize(150, 50)
        self.new_entry.move(50, 400)
        self.new_entry.setFont(QFont('Times', 28))
        self.new_entry.setStyleSheet("background-color : pink")
        self.new_entry.clicked.connect(self.new_entry_win)

        self.check_logs = QPushButton(self)
        self.check_logs.setText("Check Logs")
        self.check_logs.resize(150, 50)
        self.check_logs.move(400, 400)
        self.check_logs.setFont(QFont('Times', 28))
        self.check_logs.setStyleSheet("background-color : pink")
        self.check_logs.clicked.connect(self.new_log_win)

        self.change_name = QPushButton(self)
        self.change_name.setText("Change Name")
        self.change_name.resize(150, 50)
        self.change_name.move(225, 400)
        self.change_name.setFont(QFont('Times', 24))
        self.change_name.setStyleSheet("background-color : pink")
        self.change_name.clicked.connect(self.change_name_win)

        self.show()

    def new_entry_win(self):
        self.popup = EntryWindow()
        self.popup.show()

    def new_log_win(self):
        self.popup = LogWindow()
        self.popup.show()

    def change_name_win(self):
        self.window = QInputDialog()
        name, ok = self.window.getText(self, "Change Name", "Enter your name")
        if ok and name:
            name_file = open("name.txt", "w+")
            name_file.write(name)
            name_file.close()



class EntryWindow(QMainWindow):

    # Mostly design work done in __init__, can generally be ignored
    # Window does not show itself, must be done when instance is created.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Log Entry")
        self.setGeometry(0, 0, 600, 500)
        self.setFixedSize(600, 500)

        self.blue = QLabel(self)
        # loading image
        self.pixmap2 = QPixmap('blue.png')

        # adding image to label
        self.blue.setPixmap(self.pixmap2)

        # Optional, resize label to image size
        self.blue.resize(self.pixmap2.width(),
                         self.pixmap2.height())
        self.blue.move(0, 50)

        self.blue2 = QLabel(self)
        # loading image

        # adding image to label
        self.blue2.setPixmap(self.pixmap2)

        # Optional, resize label to image size
        self.blue2.resize(self.pixmap2.width(),
                         self.pixmap2.height())
        self.blue2.move(0, -250)

        self.emotions = QComboBox(self)
        for i in self.fetch_emotions():
            self.emotions.addItem(i)
        self.emotions.move(50, 10)
        self.emotions.resize(150, 30)

        self.action_prompt = QLabel(self)
        self.action_prompt.setText("What did you do today?")
        self.action_prompt.setFont(QFont('Helvetica', 15))
        self.action_prompt.move(50, 55)
        self.action_prompt.resize(250, 30)

        self.action_field = QTextEdit(self)
        self.action_field.move(50, 80)
        self.action_field.resize(500, 150)

        self.cause_prompt = QLabel(self)
        self.cause_prompt.setText("Why do you think you feel that way?")
        self.cause_prompt.setFont(QFont('Helvetica', 15))
        self.cause_prompt.move(50, 255)
        self.cause_prompt.resize(250, 30)

        self.cause_field = QTextEdit(self)
        self.cause_field.move(50, 280)
        self.cause_field.resize(500, 150)

        self.submit_button = QPushButton(self)
        self.submit_button.move(100, 440)
        self.submit_button.resize(100, 50)
        self.submit_button.setText("Submit")
        self.submit_button.setFont(QFont('Times', 22))
        self.submit_button.setStyleSheet("background-color : pink")
        self.submit_button.clicked.connect(self.submit)

        self.cancel_button = QPushButton(self)
        self.cancel_button.move(400, 440)
        self.cancel_button.resize(100, 50)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setFont(QFont('Times', 22))
        self.cancel_button.setStyleSheet("background-color : pink")
        self.cancel_button.clicked.connect(self.exit)

    # Reads from file to avoid messy plaintext. File is short enough to not complicate time complexity
    def fetch_emotions(self):
        with open('emotions.txt', 'r') as e:
            raw = e.read()
        return raw.split(",")

    # Pushes log entry to database and clears fields
    def submit(self):
        entries: tuple = (date.today(), self.emotions.currentText(), self.action_field.toPlainText(),
                          self.cause_field.toPlainText())
        self.action_field.clear()
        self.cause_field.clear()
        DB.submit_entry(entries)

    # Closes window
    def exit(self):
        self.close()


class LogWindow(QMainWindow):

    # Mostly design work done in __init__, can generally be ignored.
    # Window does not show itself, must be done when instance is created.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log Search")
        self.setGeometry(0, 0, 600, 500)
        self.setFixedSize(600, 500)

        self.blue = QLabel(self)
        # loading image
        self.pixmap2 = QPixmap('blue.png')

        # adding image to label
        self.blue.setPixmap(self.pixmap2)

        # Optional, resize label to image size
        self.blue.resize(self.pixmap2.width(),
                         self.pixmap2.height())
        self.blue.move(0, 50)

        self.blue2 = QLabel(self)
        # loading image

        # adding image to label
        self.blue2.setPixmap(self.pixmap2)

        # Optional, resize label to image size
        self.blue2.resize(self.pixmap2.width(),
                          self.pixmap2.height())
        self.blue2.move(0, -250)

        self.date_label = QLabel(self)
        self.date_label.move(50, 20)
        self.date_label.resize(100, 35)
        self.date_label.setText("Date")
        self.date_label.setFont(QFont('Helvetica', 20))

        self.date_field = QLineEdit(self)
        self.date_field.move(50, 50)
        self.date_field.resize(500, 30)

        self.emotion_label = QLabel(self)
        self.emotion_label.move(50, 125)
        self.emotion_label.resize(100, 30)
        self.emotion_label.setText("Emotion")
        self.emotion_label.setFont(QFont('Helvetica', 20))

        self.emotion_field = QLineEdit(self)
        self.emotion_field.move(50, 150)
        self.emotion_field.resize(500, 30)

        self.action_label = QLabel(self)
        self.action_label.move(50, 225)
        self.action_label.resize(100, 30)
        self.action_label.setText("Action")
        self.action_label.setFont(QFont('Helvetica', 20))

        self.action_field = QLineEdit(self)
        self.action_field.move(50, 250)
        self.action_field.resize(500, 30)

        self.cause_label = QLabel(self)
        self.cause_label.move(50, 320)
        self.cause_label.resize(100, 35)
        self.cause_label.setText("Cause")
        self.cause_label.setFont(QFont('Helvetica', 20))

        self.cause_field = QLineEdit(self)
        self.cause_field.move(50, 350)
        self.cause_field.resize(500, 30)

        self.submit_button = QPushButton(self)
        self.submit_button.move(100, 400)
        self.submit_button.resize(100, 50)
        self.submit_button.setText("Submit")
        self.submit_button.clicked.connect(self.submit)

        self.cancel_button = QPushButton(self)
        self.cancel_button.move(400, 400)
        self.cancel_button.resize(100, 50)
        self.cancel_button.setText("Cancel")
        self.cancel_button.clicked.connect(self.exit)

    # Will open new window to show records
    def submit(self):
        self.popup = ResultWindow(self.package_terms())
        self.popup.show()

        # Empties the fields once the data is used.
        self.date_field.clear()
        self.emotion_field.clear()
        self.action_field.clear()
        self.cause_field.clear()

    # Closes window
    def exit(self):
        self.close()

    # Grabs user input from text fields and packs them into a dict
    def package_terms(self) -> dict:
        terms = {
            "Date": self.date_field.text(),
            "Emotion": self.emotion_field.text(),
            "Action": self.action_field.text(),
            "Cause": self.cause_field.text()
        }
        return terms


class ResultWindow(QWidget):
    # Window needs to dynamically populate with entries from SQL database
    def __init__(self, terms: dict):
        super().__init__()
        self.setWindowTitle("Results")
        self.setGeometry(0, 0, 600, 500)
        self.records = DB.query_db(terms)
        self.layout = QFormLayout()
        self.blue = QLabel(self)
        # loading image
        self.pixmap2 = QPixmap('blue.png')

        # adding image to label
        self.blue.setPixmap(self.pixmap2)

        # Optional, resize label to image size
        self.blue.resize(self.pixmap2.width(),
                         self.pixmap2.height())
        self.blue.move(0, 50)

        self.blue2 = QLabel(self)
        # loading image

        # adding image to label
        self.blue2.setPixmap(self.pixmap2)

        # Optional, resize label to image size
        self.blue2.resize(self.pixmap2.width(),
                          self.pixmap2.height())
        self.blue2.move(0, -250)

        for row in self.records:
            self.date = QLabel(self)
            self.emotion = QLabel(self)
            self.cause = QLabel(self)
            self.action = QLabel(self)

            self.date.setText('Date: '+ row[0])
            self.date.setFont(QFont('Helvetica', 14))
            self.emotion.setText('Emotion: '+row[1])
            self.emotion.setFont(QFont('Helvetica', 14))
            self.cause.setText('Cause: '+row[2])
            self.cause.setFont(QFont('Helvetica', 12))
            self.action.setText('Action: '+row[3])
            self.action.setFont(QFont('Helvetica', 12))

            self.layout.addRow(self.date, self.emotion)
            self.layout.addRow(self.cause)
            self.layout.addRow(self.action)

        # necessary to apply the layout to the window
        self.setLayout(self.layout)
