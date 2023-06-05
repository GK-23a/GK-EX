from PySide6.QtCore import (QRect)
from PySide6.QtGui import (QPalette)
from PySide6.QtWidgets import (QApplication, QMainWindow, QScrollArea, QVBoxLayout, QWidget, QGridLayout, QLabel)
from sys import argv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GK-23a 实体卡牌编辑器')
        self.resize(800, 600)

        self.init_character_board()

    def init_character_board(self):
        character_board = QWidget(self)
        character_board.setGeometry(QRect(0, 0, 580, 700))
        cboard_layout = QVBoxLayout(character_board)
        cboard_layout.setGeometry(QRect(0, 0, 580, 700))
        character_area = QScrollArea(self)
        character_area.setGeometry(QRect(25, 125, 600, 450))
        character_area.setWidget(character_board)
        character_area.setBackgroundRole(QPalette.Dark)
    #     self.refresh_board()

    # def refresh_board(self):
        for _ in ['pyro', 'hydro', 'anemo', 'electro', 'dendro', 'cryo', 'geo']:
            element_widget = QWidget()
            element_layout = QGridLayout(element_widget)
            for i in range(8):
                element_layout.setColumnStretch(i, 120)

            label1 = QLabel("Label 1")
            element_layout.addWidget(label1, 0, 0)

            cboard_layout.addWidget(element_widget)


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()
