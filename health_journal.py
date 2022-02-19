import sys
import GUI


def main():
    app = GUI.QApplication(sys.argv)
    m = GUI.MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
