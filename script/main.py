from PySide6.QtWidgets import QApplication
from sys import argv
from EditorMainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()
