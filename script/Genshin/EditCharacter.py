import json
import os
from time import asctime, localtime, time

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QFontDatabase, QFont, QImage, QPixmap
from PySide6.QtWidgets import (QLabel, QLineEdit, QCheckBox, QComboBox, QWidget, QPushButton, QSpinBox, QProgressBar,
                               QGroupBox, QPlainTextEdit, QTabWidget, QMessageBox, QDialogButtonBox, QDialog)

from script.NWidgets import TabWidget as NTabWidget
from script.Genshin.GKCard import GKCharacterCard


def get_time(left=0, right=0):
    return asctime(localtime(time()))[4 + left:19 + right]


class EditWindow(QWidget):
    def __init__(self, cid: str | int):
        super().__init__()
        self.setFixedSize(650, 420)

        font_id = QFontDatabase.addApplicationFont(os.path.join('font', 'MiSans-Demibold.ttf'))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font = QFont(font_family)
        self.font.setPointSize(10.5)
        self.font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(self.font)

        #     id
        show_id = QLabel(self)
        show_id.setText('ID')
        show_id.setGeometry(QRect(25, 30, 38, 16))
        self.data_id = QLabel(self)
        self.data_id.setGeometry(QRect(63, 30, 176, 16))
        #    title
        show_title = QLabel(self)
        show_title.setText('称号')
        show_title.setGeometry(QRect(25, 60, 38, 16))
        self.data_title = QLineEdit(self)
        self.data_title.setGeometry(QRect(60, 58, 120, 20))
        #    name
        show_name = QLabel(self)
        show_name.setText('名字')
        show_name.setGeometry(QRect(25, 90, 38, 16))
        self.data_name = QLineEdit(self)
        self.data_name.setGeometry(QRect(60, 88, 120, 20))
        #    designer
        show_designer = QLabel(self)
        show_designer.setText('设计')
        show_designer.setGeometry(QRect(25, 120, 38, 16))
        self.data_designer = QLineEdit(self)
        self.data_designer.setGeometry(QRect(60, 118, 120, 20))
        #    design_state
        show_design_state = QLabel(self)
        show_design_state.setText('状态')
        show_design_state.setGeometry(QRect(25, 150, 38, 16))
        self.data_design_state = QCheckBox(self)
        self.data_design_state.setText('设计完成（未勾选状态下，不会生成此角色卡图片）')
        self.data_design_state.setGeometry(QRect(60, 150, 340, 16))
        #    sex
        show_sex = QLabel(self)
        show_sex.setText('性别')
        show_sex.setGeometry(QRect(190, 60, 35, 16))
        self.data_sex = QComboBox(self)
        self.data_sex.addItem('男')
        self.data_sex.addItem('女')
        self.data_sex.addItem('其他')
        self.data_sex.setGeometry(QRect(225, 58, 65, 20))
        #    level
        show_level = QLabel(self)
        show_level.setText('星级')
        show_level.setGeometry(QRect(190, 90, 35, 16))
        self.data_level = QSpinBox(self)
        self.data_level.setGeometry(QRect(225, 88, 65, 20))
        #    country
        show_country = QLabel(self)
        show_country.setText('所属')
        show_country.setGeometry(QRect(305, 60, 35, 16))
        self.data_country = QComboBox(self)
        self.data_country.addItem('蒙德')
        self.data_country.addItem('璃月')
        self.data_country.addItem('稻妻')
        self.data_country.addItem('须弥')
        self.data_country.addItem('枫丹')
        self.data_country.addItem('纳塔')
        self.data_country.addItem('至冬')
        self.data_country.addItem('坎瑞亚')
        self.data_country.addItem('其他')
        self.data_country.setGeometry(QRect(340, 58, 65, 20))
        #    element
        show_element = QLabel(self)
        show_element.setText('元素')
        show_element.setGeometry(QRect(305, 90, 35, 16))
        self.data_element = QComboBox(self)
        self.data_element.addItem('火元素')
        self.data_element.addItem('水元素')
        self.data_element.addItem('风元素')
        self.data_element.addItem('雷元素')
        self.data_element.addItem('草元素')
        self.data_element.addItem('冰元素')
        self.data_element.addItem('岩元素')
        self.data_element.addItem('其他')
        self.data_element.setGeometry(QRect(340, 88, 65, 20))
        #    health
        show_health = QLabel(self)
        show_health.setText('体力')
        show_health.setGeometry(QRect(190, 120, 60, 16))
        self.data_health_def = QSpinBox(self)
        self.data_health_def.setGeometry(QRect(220, 118, 40, 20))
        show_health_fgf = QLabel(self)
        show_health_fgf.setText('/')
        show_health_fgf.setGeometry(QRect(263, 120, 60, 16))
        self.data_health_max = QSpinBox(self)
        self.data_health_max.setGeometry(QRect(270, 118, 40, 20))
        #    armor
        show_armor = QLabel(self)
        show_armor.setText('护甲值')
        show_armor.setGeometry(QRect(320, 120, 60, 16))
        self.data_armor = QSpinBox(self)
        self.data_armor.setGeometry(QRect(365, 118, 40, 20))

        # 进度条
        pg_bar = QProgressBar(self)
        pg_bar.setGeometry(QRect(510, 30, 160, 18))
        pg_bar.setFormat('')
        # 图片
        image_box = QGroupBox(self)
        image_box.setGeometry(QRect(415, 60, 214, 350))
        image_box.setTitle('角色立绘/卡面')
        self.show_image = QLabel(self)
        self.show_image.setGeometry(QRect(422, 82, 200, 320))
        self.card_image = None
        # 技能
        self.data_skill = NTabWidget(self)
        self.data_skill.setGeometry(QRect(25, 200, 380, 210))
        # noinspection PyUnresolvedReferences
        self.data_skill.setTabPosition(QTabWidget.West)
        self.data_skill.setStyleSheet('QTabBar::tab{ height:50px;width:30px; }')

        # 数据加载与显示
        with open(os.path.join('json', 'genshin-impact.json'), encoding='UTF-8') as self.data_file:
            self.gk_data = json.load(self.data_file)
            gk_character_data = self.gk_data.get('character_data')
            gk_versions = dict(character_data=self.gk_data.get('character_self.data_versions'))
        self.sdata = dict()
        if isinstance(cid, int):
            d = gk_character_data[cid]
            self.ch_card = GKCharacterCard(d.get('id'))
            self.ch_card.unpack(d)
            self.sdata = d
        elif isinstance(cid, str):
            self.ch_card = GKCharacterCard(cid)
            for d in gk_character_data:
                if d.get('id') == cid:
                    self.ch_card.unpack(d)
                    self.sdata = d
                    break
            raise
        else:
            raise

        self.refresh_data()

        # 修改id
        edit_id = QPushButton(self)
        edit_id.setGeometry(QRect(267, 28, 50, 22))
        edit_id.setText('修改ID')
        edit_id.clicked.connect(lambda: self.edit_id(self.ch_card.id))
        # 保存并刷新
        save_and_refresh = QPushButton(self)
        save_and_refresh.setGeometry(QRect(325, 28, 80, 22))
        save_and_refresh.setText('保存并刷新')
        save_and_refresh.setEnabled(False)
        save_and_refresh.clicked.connect(lambda: self.save_data(True))
        # 生成角色图片
        build_image = QPushButton(self)
        build_image.setGeometry(QRect(415, 28, 90, 22))
        build_image.setText('生成角色图片')
        build_image.setEnabled(False)

    def refresh_data(self):
        self.setWindowTitle(f'编辑角色 {self.ch_card.name} - GK-23a/Genshin')
        self.data_id.setText(self.ch_card.id)
        self.data_name.setText(self.ch_card.name)
        self.data_title.setText(self.ch_card.title)
        self.data_designer.setText(self.ch_card.designer)
        self.data_design_state.setChecked(bool(self.ch_card.design_state))
        self.data_sex.setCurrentIndex(self.ch_card.to_number('sex'))
        self.data_level.setValue(self.ch_card.level)
        self.data_country.setCurrentIndex(self.ch_card.to_number('country'))
        self.data_element.setCurrentIndex(self.ch_card.to_number('element'))
        self.data_health_def.setValue(self.ch_card.health_point)
        self.data_health_max.setValue(self.ch_card.max_health_point)
        self.data_armor.setValue(self.ch_card.armor_point)
        image_path = os.path.join('img', 'character', self.ch_card.id + '.png')
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img_data = f.read()
            image = QImage.fromData(img_data)
            image_scaled = image.scaled(QSize(200, 320), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap = QPixmap.fromImage(image_scaled)
            self.show_image.setPixmap(pixmap)
            self.show_image.setText('')
        else:
            self.show_image.setText('No Image.')
        # 技能显示
        for i in range(1, self.ch_card.skill_num + 1):
            sw = f"show_skill{i}_Widget"
            sn = f"show_skill{i}_Name"
            dn = f"self.data_skill{i}_Name"
            sd = f"show_skill{i}_Description"
            dd = f"self.data_skill{i}_Description"
            dv = f"self.data_skill{i}_Visible"
            self.add_skill(getattr(self.ch_card, f'skill{i}'), sw, sn, dn, sd, dd, dv)

            getattr(self, dn).setText(getattr(self.ch_card, f'skill{i}').get('name'))
            getattr(self, dd).setPlainText(getattr(self.ch_card, f'skill{i}').get('description'))
            getattr(self, dv).setChecked(getattr(self.ch_card, f'skill{i}').get('visible'))

    def add_skill(self, data, sw, sn, dn, sd, dd, dv):
        setattr(self, sw, QWidget())
        getattr(self, sw).setFont(self.font)
        setattr(self, sn, QLabel(getattr(self, sw)))
        getattr(self, sn).setGeometry(QRect(10, 10, 56, 16))
        getattr(self, sn).setText('技能名字')
        setattr(self, dn, QLineEdit(getattr(self, sw)))
        getattr(self, dn).setGeometry(QRect(70, 8, 120, 20))
        setattr(self, sd, QLabel(getattr(self, sw)))
        getattr(self, sd).setGeometry(QRect(10, 40, 56, 16))
        getattr(self, sd).setText('技能描述')
        setattr(self, dd, QPlainTextEdit(getattr(self, sw)))
        getattr(self, dd).setGeometry(QRect(70, 40, 240, 150))
        setattr(self, dv, QCheckBox(getattr(self, sw)))
        getattr(self, dv).setGeometry(QRect(240, 10, 70, 20))
        getattr(self, dv).setText('初始拥有')

        self.data_skill.addTab(getattr(self, sw), data.get('name'))

    def save_data(self, refresh):
        saved_data = self.ch_card.pack()
        if saved_data != self.sdata:
            # 保存准备
            save_info = list()
            if saved_data['id'] != self.sdata['id']:
                save_info.append(
                    [get_time(), 'CI', self.sdata['id'], 'id', saved_data['id']]
                )
            for key in saved_data:
                if key == 'id':
                    pass
                elif key == 'skill':
                    before_list = [n['name'] for n in self.sdata['skill']]
                    after_list = [n['name'] for n in saved_data['skill']]
                    d_skill_list = [n for n in self.sdata['skill'] if n['name'] not in after_list]
                    c_skill_list = list()
                    for n_saved in saved_data['skill']:
                        for n_self in self.sdata['skill']:
                            if n_saved['name'] == n_self['name'] and n_saved['name'] in after_list:
                                c_skill_list.append((n_saved, n_self))
                    a_skill_list = [n for n in saved_data['skill'] if n['name'] not in before_list]
                    for skill in d_skill_list:
                        save_info.append(
                            [get_time(), 'D', saved_data['id'], 'skill', skill['name']]
                        )
                    for skills in c_skill_list:
                        for k in ['description', 'visible']:
                            if skills[0][k] != skills[1][k]:
                                save_info.append(
                                    [get_time(), 'C', saved_data['id'], 'skill', skills[0]['name'],
                                     k, skills[1][k], skills[0][k]]
                                )
                    for skill in a_skill_list:
                        save_info.append(
                            [get_time(), 'A', saved_data['id'], 'skill', skill['name'],
                             skill['description'], skill['visible']]
                        )
                else:
                    if saved_data[key] != self.sdata[key]:
                        save_info.append(
                            [get_time(), 'C', saved_data['id'], key, self.sdata[key], saved_data[key]]
                        )
            # 保存内容
            with open(os.path.join('script', 'genshin-impact.json'), 'w', encoding='UTF-8') as jsonfile:
                for i, char_dict in enumerate(self.gk_data['character_data']):
                    if char_dict['name'] == saved_data['name']:
                        self.gk_data['character_data'][i] = saved_data
                json.dump(self.gk_data, jsonfile, ensure_ascii=False)
            with open('output/change_log.gkcl', 'a', encoding='UTF-8') as gkcl:
                for log in save_info:
                    gkcl.write(str(log) + '\n')
        if refresh:
            self.ch_card = GKCharacterCard('')
            self.ch_card.unpack(saved_data)
            self.refresh_data()
            pass

    def edit_id(self, origin_id):
        id_editor = QDialog()
        id_editor.setFixedSize(200, 100)
        id_editor.setFont(self.font)
        id_editor.setWindowTitle('修改ID')
        ide_console = dict()
        ide_console['show_origin_id'] = QLabel(id_editor)
        ide_console['show_origin_id'].setGeometry(QRect(10, 10, 180, 20))
        ide_console['show_origin_id'].setText(f'原ID：{origin_id}')
        ide_console['show_new_id'] = QLabel(id_editor)
        ide_console['show_new_id'].setGeometry(QRect(10, 40, 180, 20))
        ide_console['show_new_id'].setText('新ID：')
        ide_console['edit_new_id'] = QLineEdit(id_editor)
        ide_console['edit_new_id'].setGeometry(QRect(50, 38, 140, 20))
        ide_console['button'] = QDialogButtonBox(id_editor)
        ide_console['button'].setGeometry(QRect(10, 70, 181, 24))
        # noinspection PyUnresolvedReferences
        ide_console['button'].setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        ide_console['button'].setCenterButtons(True)
        ide_console['button'].accepted.connect(
            lambda: self.on_id_edit_accepted(ide_console['edit_new_id'].text(), id_editor))
        ide_console['button'].rejected.connect(id_editor.reject)
        id_editor.exec()

    def on_id_edit_accepted(self, new_id, window):
        window.accept()
        self.data_id.setText(new_id)

    def closeEvent(self, event):
        saved_data = self.ch_card.pack()

        if saved_data != self.sdata:
            exit_tip = QMessageBox()
            exit_tip.setWindowTitle('提示')
            exit_tip.setFont(self.font)
            exit_tip.setText('有未保存的更改。真的要直接关闭吗？')
            exit_tip.setInformativeText('    Save:保存并退出\nDiscard:直接退出\n Cancel:取消')
            # noinspection PyUnresolvedReferences
            exit_tip.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            # noinspection PyUnresolvedReferences
            exit_tip.setDefaultButton(QMessageBox.Cancel)
            reply = exit_tip.exec()

            # noinspection PyUnresolvedReferences
            if reply == QMessageBox.Discard:
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
            else:
                self.save_data(False)
                event.accept()
        else:
            event.accept()
