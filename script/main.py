from PySide6.QtCore import QRect
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (QApplication, QMainWindow, QScrollArea, QLabel)
from sys import argv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GK-23a 实体卡牌编辑器')
        self.resize(800, 600)

        self.init_character_board()

    def init_character_board(self):
        character_board = QLabel(self)
        character_area = QScrollArea(self)
        character_area.setGeometry(QRect(25, 125, 600, 450))
        character_area.setWidget(character_board)
        character_area.setBackgroundRole(QPalette.Dark)


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()
