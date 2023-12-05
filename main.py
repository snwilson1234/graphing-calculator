from PySide6.QtWidgets import QApplication
import sys

from graph_app import MyApp

def main ():
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()