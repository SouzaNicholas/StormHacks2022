import sys
import sqlite3 as sql
import GUI


def main():
    app = GUI.QApplication(sys.argv)
    m = GUI.MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
