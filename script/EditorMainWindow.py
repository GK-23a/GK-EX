import json
import os

from PySide6.QtCore import (QRect)
from PySide6.QtWidgets import (QMainWindow, QScrollArea, QWidget, QLabel)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GK-23a 实体卡牌编辑器')
        self.resize(800, 600)

        # 数据加载
        with open(os.path.join('data', 'data.json')) as data_file:
            gk_data = json.load(data_file)
        self.gk_character_data = gk_data.get('character_data')
        self.gk_versions = dict(character_data=gk_data.get('character_data_versions'))
        self.character_data = []
        self.refresh_gk_data('character')

        # 角色选择框
        self.character_board = QWidget(self)
        self.character_board.setGeometry(QRect(0, 0, 610, 700))
        character_area = QScrollArea(self)
        character_area.setGeometry(QRect(25, 125, 620, 450))
        character_area.setWidget(self.character_board)
        self.refresh_board()

    def refresh_gk_data(self, data_type):
        if data_type == 'character':
            for cdata in self.gk_character_data:
                print(cdata)
                pass
            pass
        pass

    def refresh_board(self):
        board_height = 25
        elt_title = dict()
        elts = [
            ['pyro', '火元素'],
            ['hydro', '水元素'],
            ['anemo', '风元素'],
            ['electro', '雷元素'],
            ['dendro', '草元素'],
            ['cryo', '冰元素'],
            ['geo', '岩元素'],
        ]
        for elt in elts:
            elt_title[elt[0]] = QLabel(self.character_board)
            elt_title[elt[0]].setText(elt[1] + ' | ' + elt[0].title())
            elt_title[elt[0]].setGeometry(QRect(25, board_height, 450, 24))
            board_height += 10 + 24
