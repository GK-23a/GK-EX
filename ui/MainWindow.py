import json
import os

from PySide6.QtCore import (QRect, Qt, QSize)
from PySide6.QtGui import (QAction, QFont, QFontDatabase, QImage, QPixmap)
from PySide6.QtWidgets import (QMainWindow, QApplication, QScrollArea, QWidget, QLabel)

from ui.CreateCharacter import CreateWindow
from ui.EditCharacter import EditWindow
from cards.GKCard import GKCharacterCard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.installEventFilter(self)
        self.debug = 0
        self.setWindowTitle('实体卡牌编辑器 - GK23a/Genshin')
        self.setFixedSize(675, 600)

        if not os.path.exists('output'):
            os.makedirs('output')

        font_id = QFontDatabase.addApplicationFont(os.path.join('assets', 'font', 'MiSans-Demibold.ttf'))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font = QFont(font_family)
        self.font.setPointSize(10.5)
        self.font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(self.font)

        self.character_widgets = dict()
        self.edit_windows = dict()
        self.create_windows = list()
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
        # 数据加载
        with open(os.path.join('assets', 'card_data.json'), encoding='UTF-8') as data_file:
            gk_data = json.load(data_file)
        self.gk_character_data = gk_data.get('character_data')
        self.gk_versions = dict(character_data=gk_data.get('character_data_versions'))
        self.character_data = dict()
        self.data_list = dict()
        self.elt_title = dict()
        self.refresh_gk_data('character')

        title_en = QLabel(self)
        title_en.setGeometry(QRect(35, 25, 625, 75))
        title_en.setText('GK-23a / Genshin')
        title_zh = QLabel(self)
        title_zh.setGeometry(QRect(35, 75, 625, 75))
        title_zh.setText('原神杀 卡牌构建器')
        title_zh.setAlignment(Qt.AlignHCenter)
        version = QLabel(self)
        version.setGeometry(QRect(35, 100, 625, 75))
        version.setText(f'软件版本 Beta 2.0  |  数据版本  {self.gk_versions.get("character_data")}')
        version.setAlignment(Qt.AlignHCenter)

        # 选择框
        self.card_board = QWidget(self)
        self.card_board.setGeometry(QRect(0, 0, 0, 0))
        card_area = QScrollArea(self)
        card_area.setGeometry(QRect(25, 125, 625, 450))
        card_area.setWidget(self.card_board)
        self.refresh_character_board()

        # 菜单栏
        menu_bar = self.menuBar()

        menu_edit = menu_bar.addMenu('编辑')

        action_buildCard = QAction('卡面构建(未完成)', self)
        # action_buildCard.triggered.connect(self.create_character_action)
        menu_edit.addAction(action_buildCard)

        menu_edit.addSeparator()

        action_edit = QAction('新增角色', self)
        action_edit.triggered.connect(self.create_character_action)
        menu_edit.addAction(action_edit)
        action_restart = QAction('重启并刷新', self)
        action_restart.triggered.connect(lambda: self.restart_editor())
        menu_edit.addAction(action_restart)

        """
        menu_board_body = menu_edit.addMenu('选项板显示内容...')
        action_board_show_character = QAction('显示角色', self)
        action_board_show_character.triggered.connect(lambda: self.refresh_gk_data('character'))
        menu_board_body.addAction(action_board_show_character)
        action_board_show_game_card = QAction('显示卡牌', self)
        action_board_show_game_card.triggered.connect(lambda: self.refresh_gk_data('game_card'))
        menu_board_body.addAction(action_board_show_game_card)
        """"""
        menu_about = menu_bar.addMenu('关于')
        action_about = QAction('关于...', self)
        # action_about.triggered.connect(lambda: self.refresh_gk_data('character'))
        menu_about.addAction(action_about)
        """

    def refresh_gk_data(self, data_type):
        """刷新gk数据"""
        if data_type == 'character':
            for elt in self.elts:
                self.data_list[elt[0] + '_character'] = list()
            for cdata in self.gk_character_data:
                cid = cdata.get('id')
                self.character_data[cid] = GKCharacterCard(cid)
                self.character_data[cid].unpack(cdata)
                self.data_list[self.character_data[cid].element + '_character'].append(cid)
            for elt in self.elts:
                self.data_list[elt[0] + '_character'].sort()
        elif data_type == 'game_card':
            pass

    def refresh_character_board(self):
        """刷新ScrollArea选项板"""
        board_height = 15

        for widget in self.character_widgets:
            self.character_widgets[widget].setParent(None)
        self.character_widgets = {}
        for elt in self.elt_title:
            self.elt_title[elt].setParent(None)
        self.elt_title = dict()
        for elt in self.elts:
            self.elt_title[elt[0]] = QLabel(self.card_board)
            self.elt_title[elt[0]].setText(elt[1] + ' | ' + elt[0].title() + ' ' +
                                           f'({len(self.data_list.get(elt[0] + "_character"))})')
            self.elt_title[elt[0]].setGeometry(QRect(25, board_height, 450, 24))
            board_height += 10 + 24
            temp_var = 0
            for i, d in enumerate(self.data_list.get(elt[0] + '_character')):
                self.character_widgets[f'{d}_widget'] = QWidget(self.card_board)
                # self.character_widgets[f'{d}_widget'].data_id = d
                self.character_widgets[f'{d}_widget'].setGeometry(QRect(
                    10 * (i % 7 + 2) - 1 + 72 * (i % 7),
                    board_height + (10 + 96) * (i // 7),
                    72, 96))
                self.character_widgets[f'{d}_widget'].setStyleSheet('border: 1px solid #888888;')
                self.character_widgets[f'{d}_widget'].setCursor(Qt.PointingHandCursor)
                self.character_widgets[f'{d}_widget'].mousePressEvent = lambda event, cid=d: \
                    self.character_choice_clicked(event, cid)
                self.character_widgets[f'{d}_txt_label'] = QLabel(self.character_widgets[f'{d}_widget'])
                self.character_widgets[f'{d}_txt_label'].setGeometry(QRect(0, 72, 72, 24))
                self.character_widgets[f'{d}_txt_label'].setText(self.character_data.get(d).name)
                self.character_widgets[f'{d}_txt_label'].setAlignment(Qt.AlignCenter)
                self.character_widgets[f'{d}_img_widget'] = QWidget(self.character_widgets[f'{d}_widget'])
                self.character_widgets[f'{d}_img_widget'].setGeometry(QRect(0, 0, 72, 72))
                qss_code = 'border: 0;'
                if d in ['aloy']:
                    qss_code += 'background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #DA4F55, stop:1 #AF5155);'
                elif self.character_data.get(d).level == 5:
                    qss_code += 'background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #de9552, stop:1 #9a6d43);'
                elif self.character_data.get(d).level == 4:
                    qss_code += 'background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #917ab1, stop:1 #6c6192);'
                self.character_widgets[f'{d}_img_widget'].setStyleSheet(qss_code)
                self.character_widgets[f'{d}_img_label'] = QLabel(self.character_widgets[f'{d}_img_widget'])
                self.character_widgets[f'{d}_img_label'].setGeometry(QRect(0, 0, 72, 72))
                self.character_widgets[f'{d}_img_label'].setStyleSheet('border: 0;')
                if d[:8] == 'traveler':
                    dx = d[:8]
                else:
                    dx = d
                icon_path = os.path.join('assets', 'img', 'character_icon', dx + '.png')
                if os.path.exists(icon_path):
                    with open(icon_path, 'rb') as f:
                        img_data = f.read()
                    icon_img = QPixmap.fromImage(
                        QImage.fromData(img_data).scaled(QSize(72, 72), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    self.character_widgets[f'{d}_img_label'].setPixmap(icon_img)
                temp_var = i
            board_height += (10 + 96) * (temp_var // 7 + 1) + 5
        self.card_board.setGeometry(QRect(0, 0, 600, board_height))

    def character_choice_clicked(self, event, cid):
        event.accept()
        if cid in self.edit_windows:
            edit_window = self.edit_windows[cid]
            edit_window.activateWindow()
            edit_window.show()
        else:
            edit_window = EditWindow(cid)
            edit_window.show()
            self.edit_windows[cid] = edit_window

    def create_character_action(self):
        self.create_windows.append(CreateWindow())
        self.create_windows[len(self.create_windows) - 1].show()

    def restart_editor(self):
        # 重启
        self.close()

        app_ = QApplication.instance()
        window_ = MainWindow()
        window_.show()
        app_.exec_()
