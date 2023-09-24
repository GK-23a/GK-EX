import json
import os

from PySide6.QtCore import QRect
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import (QWidget, QApplication, QScrollArea, QLabel, QCheckBox, QPushButton, QRadioButton,
                               QGroupBox)


class CustomCheckBox(QCheckBox):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.hidden_tag = None


class EditWindow(QWidget):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont(os.path.join('assets', 'font', 'MiSans-Demibold.ttf'))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font = QFont(font_family)
        self.font.setPointSize(10.5)
        self.font.setStyleStrategy(QFont.PreferAntialias)

        self.i_font = QFont(font_family)
        self.i_font.setPointSize(10.5)
        self.i_font.setStyleStrategy(QFont.PreferAntialias)
        self.i_font.setItalic(True)

        self.setFont(self.font)
        self.setFixedSize(650, 420)
        self.setWindowTitle('导出……')

        with open(os.path.join('assets', 'card_data.json'), encoding='UTF-8') as data_file:
            gk_data = json.load(data_file)
        self.gk_character_data = gk_data.get('character_data')

        self.character_board = QWidget(self)
        self.character_board.setGeometry(QRect(0, 0, 300, 370))
        board_area = QScrollArea(self)
        board_area.setGeometry(QRect(25, 25, 324, 380))
        board_area.setWidget(self.character_board)

        self.character_data = dict()
        self.character_widgets = dict()
        self.elt_title = dict()

        self.elts = [
            ['pyro', '火元素'],
            ['hydro', '水元素'],
            ['anemo', '风元素'],
            ['electro', '雷元素'],
            ['dendro', '草元素'],
            ['cryo', '冰元素'],
            ['geo', '岩元素'],
            ['others', '其他']
        ]

        self.data_list = {elt[0] + '_character': [] for elt in self.elts}
        for cdata in self.gk_character_data:
            self.data_list.setdefault(cdata['element'] + '_character', []).append(
                (cdata['id'], cdata['name'], cdata['design_state']))
        board_height = 5
        self.ndl = dict()
        self.cbc = list()
        state = [0, 0]
        for elt in self.elts:
            self.data_list[elt[0] + '_character'].sort()

            self.elt_title[elt[0]] = QLabel(self.character_board)
            self.elt_title[elt[0]].setText(elt[1] + ' | ' + elt[0].title() + ' ' +
                                           f'({len(self.data_list.get(elt[0] + "_character"))})')
            self.elt_title[elt[0]].setGeometry(QRect(5, board_height, 450, 20))
            board_height += 24
            h_not_plus = True
            for i, d in enumerate(self.data_list.get(elt[0] + '_character')):
                self.ndl[d[0]] = CustomCheckBox(self.character_board)
                show_name = d[1]
                if not d[2]:
                    show_name = '*' + show_name
                    self.ndl[d[0]].setFont(self.i_font)
                    self.ndl[d[0]].hidden_tag = True
                    self.ndl[d[0]].setToolTip(f'{d[1]}({d[0]})\n设计未完成')
                    state[1] += 1
                else:
                    self.ndl[d[0]].setToolTip(f'{d[1]}({d[0]})')
                    state[0] += 1
                self.ndl[d[0]].setText(show_name)
                self.ndl[d[0]].setGeometry(QRect(5 + (i % 3) * 100, board_height, 95, 22))
                self.ndl[d[0]].stateChanged.connect(self.update_count_label)
                self.cbc.append(self.ndl[d[0]].isChecked())
                if i % 3 == 2:
                    board_height += 24
                    h_not_plus = False
                else:
                    h_not_plus = True
            if h_not_plus:
                board_height += 24
            board_height += 12

        self.character_board.setGeometry(QRect(0, 0, 300, board_height))

        # 全选、全不选、选中设计完成的角色
        edit_id = QPushButton(self)
        edit_id.setGeometry(QRect(360, 25, 52, 22))
        edit_id.setText('全选')
        edit_id.clicked.connect(self.select_all)
        edit_id = QPushButton(self)
        edit_id.setGeometry(QRect(360+60, 25, 64, 22))
        edit_id.setText('全不选')
        edit_id.clicked.connect(self.deselect_all)
        edit_id = QPushButton(self)
        edit_id.setGeometry(QRect(360+132, 25, 140, 22))
        edit_id.setText('选中设计完成的角色')
        edit_id.clicked.connect(self.select_designed)

        # 数显区域
        show_all = QLabel(self)
        show_all.setText('共计含有')
        show_all.setGeometry(QRect(360, 75, 60, 16))
        data_all = QLabel(self)
        data_all.setGeometry(QRect(360+60, 75, 60, 16))
        show_designed = QLabel(self)
        show_designed.setText('设计完成')
        show_designed.setGeometry(QRect(360, 75+24, 60, 16))
        data_designed = QLabel(self)
        data_designed.setGeometry(QRect(360+60, 75+24, 60, 16))
        show_selected = QLabel(self)
        show_selected.setText('已选择')
        show_selected.setGeometry(QRect(360, 75+48, 60, 16))
        self.data_selected = QLabel(self)
        self.data_selected.setGeometry(QRect(360+60, 75+48, 60, 16))

        data_all.setText(str(state[0]+state[1]))
        data_designed.setText(str(state[0]))
        self.data_selected.setText('0')

        # 导出
        image_box = QGroupBox(self)
        image_box.setGeometry(QRect(360, 165, 120, 350))
        image_box.setTitle('导出')
        show_export_for = QLabel(self)
        show_export_for.setText('导出为：')
        show_export_for.setGeometry(QRect(360, 165, 60, 16))
        export_markdown = QRadioButton(self)
        export_markdown.setText('Markdown(*.md)')
        export_markdown.setGeometry(QRect(360+60, 165, 200, 16))
        export_plaintext = QRadioButton(self)
        export_plaintext.setText('纯文本(*.txt)')
        export_plaintext.setGeometry(QRect(360+60, 165+24, 200, 16))
        export_image = QRadioButton(self)
        export_image.setText('图片(*.png)')
        export_image.setGeometry(QRect(360+60, 165+48, 200, 16))

    def update_count_label(self):
        checked_count = sum([v.isChecked() for v in self.ndl.values()])
        self.data_selected.setText(str(checked_count))

    def select_all(self):
        for v in self.ndl.values():
            v.setChecked(True)
        self.update_count_label()

    def deselect_all(self):
        for v in self.ndl.values():
            v.setChecked(False)
        self.update_count_label()

    def select_designed(self):
        for v in self.ndl.values():
            if v.hidden_tag:
                v.setChecked(False)
            else:
                v.setChecked(True)
        self.update_count_label()


if __name__ == "__main__":
    app = QApplication([])
    window = EditWindow()
    window.show()
    app.exec()
