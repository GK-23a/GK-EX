import os
import json
from copy import deepcopy
from time import asctime, localtime, time

from PIL.ImageQt import ImageQt
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QFontDatabase, QFont, QImage, QPixmap
from PySide6.QtWidgets import (QLabel, QLineEdit, QCheckBox, QComboBox, QWidget, QPushButton, QSpinBox, QProgressBar,
                               QGroupBox, QPlainTextEdit, QTabWidget, QMessageBox, QDialogButtonBox, QDialog,
                               QApplication)

from cards.CardBuild import character_card_build
from cards.GKCard import GKCharacterCard
from ui.NWidgets import TabWidget as NTabWidget


def get_time(left=0, right=0):
    return asctime(localtime(time()))[4 + left:19 + right]


def copy_text_to_clipboard(text):
    text_to_copy = text
    clipboard = QApplication.clipboard()
    clipboard.setText(text_to_copy)
    msg_box = QMessageBox()
    msg_box.setText(f'{text}已复制到剪贴板')
    msg_box.exec()


class EditWindow(QWidget):
    def __init__(self, cid: str | int):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont(os.path.join('assets', 'font', 'MiSans-Demibold.ttf'))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font = QFont(font_family)
        self.font.setPointSize(10.5)
        self.font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(self.font)

        self.cimg = None

        #     id
        show_id = QLabel(self)
        show_id.setText('ID')
        show_id.setGeometry(QRect(25+224, 30, 38, 16))
        self.data_id = QLabel(self)
        self.data_id.setGeometry(QRect(63+224, 30, 176, 16))
        #    title
        show_title = QLabel(self)
        show_title.setText('称号')
        show_title.setGeometry(QRect(25+224, 60, 38, 16))
        self.data_title = QLineEdit(self)
        self.data_title.setGeometry(QRect(60+224, 58, 120, 20))
        #    name
        show_name = QLabel(self)
        show_name.setText('名字')
        show_name.setGeometry(QRect(25+224, 90, 38, 16))
        self.data_name = QLineEdit(self)
        self.data_name.setGeometry(QRect(60+224, 88, 120, 20))
        #    designer
        show_designer = QLabel(self)
        show_designer.setText('设计')
        show_designer.setGeometry(QRect(25+224, 120, 38, 16))
        self.data_designer = QLineEdit(self)
        self.data_designer.setGeometry(QRect(60+224, 118, 120, 20))
        #    design_state
        show_design_state = QLabel(self)
        show_design_state.setText('状态')
        show_design_state.setGeometry(QRect(25+224, 150, 38, 16))
        self.data_design_state = QCheckBox(self)
        self.data_design_state.setText('设计完成（未勾选状态下，不会生成此角色卡图片）')
        self.data_design_state.setGeometry(QRect(60+224, 150, 340, 16))
        #    sex
        show_sex = QLabel(self)
        show_sex.setText('性别')
        show_sex.setGeometry(QRect(190+224, 60, 35, 16))
        self.data_sex = QComboBox(self)
        self.data_sex.addItem('男')
        self.data_sex.addItem('女')
        self.data_sex.addItem('其他')
        self.data_sex.setGeometry(QRect(225+224, 58, 55, 20))
        #    level
        show_level = QLabel(self)
        show_level.setText('星级')
        show_level.setGeometry(QRect(190+224, 90, 35, 16))
        self.data_level = QSpinBox(self)
        self.data_level.setGeometry(QRect(225+224, 88, 55, 20))
        #    country
        show_country = QLabel(self)
        show_country.setText('所属')
        show_country.setGeometry(QRect(290+224, 60, 35, 16))
        self.data_country = QComboBox(self)
        self.data_country.addItem('蒙德')
        self.data_country.addItem('璃月')
        self.data_country.addItem('稻妻')
        self.data_country.addItem('须弥')
        self.data_country.addItem('枫丹(荒)')
        self.data_country.addItem('枫丹(芒)')
        self.data_country.addItem('纳塔')
        self.data_country.addItem('至冬')
        self.data_country.addItem('坎瑞亚')
        self.data_country.addItem('其他')
        self.data_country.setGeometry(QRect(325+224, 58, 80, 20))
        #    element
        show_element = QLabel(self)
        show_element.setText('元素')
        show_element.setGeometry(QRect(290+224, 90, 35, 16))
        self.data_element = QComboBox(self)
        self.data_element.addItem('火元素')
        self.data_element.addItem('水元素')
        self.data_element.addItem('风元素')
        self.data_element.addItem('雷元素')
        self.data_element.addItem('草元素')
        self.data_element.addItem('冰元素')
        self.data_element.addItem('岩元素')
        self.data_element.addItem('其他')
        self.data_element.setGeometry(QRect(325+224, 88, 80, 20))
        #    health
        show_health = QLabel(self)
        show_health.setText('体力')
        show_health.setGeometry(QRect(190+224, 120, 60, 16))
        self.data_health_def = QSpinBox(self)
        self.data_health_def.setGeometry(QRect(220+224, 118, 40, 20))
        show_health_fgf = QLabel(self)
        show_health_fgf.setText('/')
        show_health_fgf.setGeometry(QRect(263+224, 120, 60, 16))
        self.data_health_max = QSpinBox(self)
        self.data_health_max.setGeometry(QRect(270+224, 118, 40, 20))
        #    armor
        show_armor = QLabel(self)
        show_armor.setText('护甲值')
        show_armor.setGeometry(QRect(320+224, 120, 60, 16))
        self.data_armor = QSpinBox(self)
        self.data_armor.setGeometry(QRect(365+224, 118, 40, 20))
        #    dlc
        show_dlc = QLabel(self)
        show_dlc.setText('DLC')
        show_dlc.setGeometry(QRect(25+224, 180, 35, 16))
        self.data_dlc = QComboBox(self)
        self.data_dlc.addItem('标准包')
        self.data_dlc.addItem('诸神包')
        self.data_dlc.addItem('创者包')
        self.data_dlc.setGeometry(QRect(58+224, 178, 65, 20))
        #    tip
        tip_box = QGroupBox(self)
        tip_box.setGeometry(QRect(648, 60, 214, 350))
        tip_box.setTitle('角色注释')
        # show_tip = QLabel(self)
        # show_tip.setGeometry(QRect(10, 40, 56, 16))
        # show_tip.setText('描述')
        self.data_tip = QPlainTextEdit(self)
        self.data_tip.setGeometry(QRect(658, 84, 200, 314))

        # 进度条
        self.pg_bar = QProgressBar(self)
        self.pg_bar.setGeometry(QRect(510-390, 30, 160, 18))
        self.pg_bar.setFormat('')
        # 图片
        image_box = QGroupBox(self)
        image_box.setGeometry(QRect(415-390, 60, 214, 350))
        image_box.setTitle('角色立绘/卡面')
        self.show_image = QLabel(self)
        self.show_image.setGeometry(QRect(422-390, 82, 200, 320))
        self.card_image = None
        # 技能
        self.data_skill = NTabWidget(self)
        self.data_skill.setGeometry(QRect(25+224, 210, 380, 200))
        # noinspection PyUnresolvedReferences
        self.data_skill.setTabPosition(QTabWidget.West)
        self.data_skill.setStyleSheet('QTabBar::tab{ height:50px;width:30px; }')

        # 复制id
        edit_id = QPushButton(self)
        edit_id.setGeometry(QRect(214+224, 28, 50, 22))
        edit_id.setText('复制ID')
        edit_id.clicked.connect(lambda: copy_text_to_clipboard(self.ch_card.id))
        # 修改id
        edit_id = QPushButton(self)
        edit_id.setGeometry(QRect(270+224, 28, 50, 22))
        edit_id.setText('修改ID')
        edit_id.clicked.connect(lambda: self.edit_id(self.ch_card.id))
        # 保存并刷新
        save_and_refresh = QPushButton(self)
        save_and_refresh.setGeometry(QRect(326+224, 28, 80, 22))
        save_and_refresh.setText('保存并刷新')
        save_and_refresh.clicked.connect(lambda: self.save_data(True))
        # 生成角色图片
        build_image = QPushButton(self)
        build_image.setGeometry(QRect(415-390, 28, 90, 22))
        build_image.setText('生成角色图片')
        build_image.clicked.connect(self.build_image)

        # 新增技能
        skill_add = QPushButton(self)
        skill_add.setGeometry(QRect(156+224, 178, 70, 22))
        skill_add.setText('新增技能')
        skill_add.clicked.connect(self.skill_change_add)
        # 删除技能
        skill_del = QPushButton(self)
        skill_del.setGeometry(QRect(231+224, 178, 70, 22))
        skill_del.setText('删除技能')
        skill_del.clicked.connect(self.skill_change_del)

        # 显示注释
        save_and_refresh = QPushButton(self)
        save_and_refresh.setGeometry(QRect(306+224, 178, 100, 22))
        save_and_refresh.setText('显示/隐藏注释')
        save_and_refresh.clicked.connect(lambda: self.show_or_hide_tip())

        # 数据加载与显示
        with open(os.path.join('assets', 'card_data.json'), encoding='UTF-8') as self.data_file:
            self.gk_data = json.load(self.data_file)
            gk_character_data = self.gk_data.get('character_data')
            self.gk_versions = dict(character_data=self.gk_data.get('character_data_versions'))
        self.sdata = 0
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
            if self.sdata == 0:
                raise
        else:
            raise

        if self.ch_card.tip:
            self.show_tip_now = True
            self.setFixedSize(650 + 224, 420)
        else:
            self.show_tip_now = False
            self.setFixedSize(650, 420)

        self.refresh_data()

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
        self.data_dlc.setCurrentIndex(self.ch_card.to_number('dlc'))
        self.data_tip.setPlainText(self.ch_card.tip)
        image_path = os.path.join('assets', 'img', 'character', self.ch_card.id + '.png')
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
        self.refresh_skill()

    def refresh_skill(self):
        # 技能显示
        self.data_skill.clear()
        for i in range(1, self.ch_card.skill_num + 1):
            sw = f'show_skill{i}_widget'
            sn = f'show_skill{i}_name'
            dn = f'self.data_skill{i}_name'
            sd = f'show_skill{i}_description'
            dd = f'self.data_skill{i}_description'
            dv = f'self.data_skill{i}_visible'
            self.add_skill(getattr(self.ch_card, f'skill{i}'), sw, sn, dn, sd, dd, dv)

            getattr(self, dn).setText(getattr(self.ch_card, f'skill{i}').get('name'))
            getattr(self, dd).setPlainText(getattr(self.ch_card, f'skill{i}').get('description'))
            getattr(self, dv).setChecked(getattr(self.ch_card, f'skill{i}').get('visible'))

    def add_skill(self, data, sw, sn, dn, sd, dd, dv):
        setattr(self, sw, QWidget())
        getattr(self, sw).setFont(self.font)
        setattr(self, dv, QCheckBox(getattr(self, sw)))
        getattr(self, dv).setGeometry(QRect(240, 10, 70, 20))
        getattr(self, dv).setText('初始拥有')

        setattr(self, sn, QLabel(getattr(self, sw)))
        getattr(self, sn).setGeometry(QRect(10, 10, 56, 16))
        getattr(self, sn).setText('名字')
        setattr(self, dn, QLineEdit(getattr(self, sw)))
        getattr(self, dn).setGeometry(QRect(70-24, 8, 120+24, 20))

        setattr(self, sd, QLabel(getattr(self, sw)))
        getattr(self, sd).setGeometry(QRect(10, 40, 56, 16))
        getattr(self, sd).setText('描述')
        setattr(self, dd, QPlainTextEdit(getattr(self, sw)))
        getattr(self, dd).setGeometry(QRect(70-24, 40, 240+24, 150))

        self.data_skill.addTab(getattr(self, sw), data.get('name'))

    def build_image(self):
        self.ch_card.id = self.data_id.text()
        self.ch_card.name = self.data_name.text()
        self.ch_card.title = self.data_title.text()
        self.ch_card.designer = self.data_designer.text()
        self.ch_card.design_state = bool(self.data_design_state.isChecked())
        self.ch_card.sex = self.ch_card.number_to(self.data_sex.currentIndex(), 'sex')
        self.ch_card.level = self.data_level.value()
        self.ch_card.country = self.ch_card.number_to(self.data_country.currentIndex(), 'country')
        self.ch_card.element = self.ch_card.number_to(self.data_element.currentIndex(), 'element')
        self.ch_card.health_point = self.data_health_def.value()
        self.ch_card.max_health_point = self.data_health_max.value()
        self.ch_card.armor_point = self.data_armor.value()
        self.ch_card.dlc = self.ch_card.number_to(self.data_element.currentIndex(), 'dlc')
        for i in range(1, self.ch_card.skill_num + 1):
            tp_n = getattr(self, f'self.data_skill{i}_name').text()
            tp_d = getattr(self, f'self.data_skill{i}_description').toPlainText()
            tp_v = bool(getattr(self, f'self.data_skill{i}_visible').isChecked())
            setattr(self.ch_card, f'skill{i}', dict(name=tp_n, description=tp_d, visible=tp_v))
        build_data = self.ch_card.pack()
        # noinspection PyBroadException
        try:
            self.cimg = character_card_build(build_data, self.gk_versions['character_data'],
                                             progress_bar=self.pg_bar)
        except Exception:
            self.show_image.mousePressEvent = None
            self.show_image.setText('Error\noutput/error.log')
            import traceback
            with open(os.path.join('output', 'error.log'), 'a', encoding='UTF-8') as log_file:
                log_file.write(traceback.format_exc())
        else:
            image = ImageQt(self.cimg)
            image_scaled = image.scaled(QSize(200, 320), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap = QPixmap.fromImage(image_scaled)
            self.show_image.setPixmap(pixmap)
            self.show_image.mousePressEvent = self.on_label_image_clicked
            self.show_image.setText('')

    def on_label_image_clicked(self, _ev):
        self.pg_bar.setValue(100)
        self.cimg.show()
        self.pg_bar.setValue(0)

    def pack_data(self):
        self.ch_card.id = self.data_id.text()
        self.ch_card.name = self.data_name.text()
        self.ch_card.title = self.data_title.text()
        self.ch_card.designer = self.data_designer.text()
        self.ch_card.design_state = bool(self.data_design_state.isChecked())
        self.ch_card.sex = self.ch_card.number_to(self.data_sex.currentIndex(), 'sex')
        self.ch_card.level = self.data_level.value()
        self.ch_card.country = self.ch_card.number_to(self.data_country.currentIndex(), 'country')
        self.ch_card.element = self.ch_card.number_to(self.data_element.currentIndex(), 'element')
        self.ch_card.health_point = self.data_health_def.value()
        self.ch_card.max_health_point = self.data_health_max.value()
        self.ch_card.armor_point = self.data_armor.value()
        self.ch_card.dlc = self.ch_card.number_to(self.data_dlc.currentIndex(), 'dlc')
        self.ch_card.tip = self.data_tip.toPlainText()
        for i in range(1, self.ch_card.skill_num + 1):
            tp_n = getattr(self, f'self.data_skill{i}_name').text()
            tp_d = getattr(self, f'self.data_skill{i}_description').toPlainText()
            tp_v = bool(getattr(self, f'self.data_skill{i}_visible').isChecked())
            setattr(self.ch_card, f'skill{i}', dict(name=tp_n, description=tp_d, visible=tp_v))
        saved_data = self.ch_card.pack()
        return saved_data

    def save_data(self, refresh):
        saved_data = self.pack_data()
        if saved_data != self.sdata:
            # 保存准备
            save_info = list()
            if saved_data['id'] != self.sdata['id']:
                save_info.append(
                    [get_time(), 'CI', self.sdata['id'], 'id', saved_data['id']]
                )
            for key in saved_data:
                if key != 'id':
                    try:
                        if saved_data[key] != self.sdata[key]:
                            save_info.append(
                                [get_time(), 'C', saved_data['id'], key, self.sdata[key], saved_data[key]]
                            )
                    except KeyError:
                        if key == 'tip' and saved_data[key] == '':
                            save_info.append(
                                [get_time(), 'D-AT', saved_data['id'], key, '']
                            )
                        else:
                            raise
            # 保存内容
            with open(os.path.join('assets', 'card_data.json'), 'w', encoding='UTF-8') as jsonfile:
                for i, char_dict in enumerate(self.gk_data['character_data']):
                    if char_dict['name'] == saved_data['name']:
                        self.gk_data['character_data'][i] = saved_data
                json.dump(self.gk_data, jsonfile, ensure_ascii=False, indent=2)
            with open(os.path.join('assets', 'change_log.gkch'), 'a', encoding='UTF-8') as gkch:
                for log in save_info:
                    gkch.write(str(log) + '\n')
        self.sdata = deepcopy(saved_data)
        if refresh:
            self.ch_card = GKCharacterCard('')
            self.ch_card.unpack(saved_data)
            self.refresh_data()

    def edit_id(self, origin_id):
        """修改角色id"""
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

    def on_id_edit_accepted(self, new_id, window_):
        window_.accept()
        with open(os.path.join('assets', 'card_data.json'), encoding='UTF-8') as data_file:
            gk_character_data = json.load(data_file).get('character_data')
            cids = {i.get('id', None) for i in gk_character_data}
        if new_id in cids:
            error_tip = QMessageBox()
            error_tip.setWindowTitle('错误')
            error_tip.setFont(self.font)
            error_tip.setText('id修改失败：角色id重复。')
            # noinspection PyUnresolvedReferences
            error_tip.setStandardButtons(QMessageBox.Cancel)
            # noinspection PyUnresolvedReferences
            error_tip.setDefaultButton(QMessageBox.Cancel)
            error_tip.exec()
        else:
            self.data_id.setText(new_id)

    def skill_change_add(self):
        self.ch_card.add_skill('技能')
        self.refresh_skill()

    def skill_change_del(self):
        cidx = self.data_skill.currentIndex()
        if cidx >= 0:
            self.ch_card.del_skill(cidx + 1)
            self.refresh_skill()

    def show_or_hide_tip(self):
        if self.show_tip_now:
            self.setFixedSize(650, 420)
            self.show_tip_now = False
        else:
            self.setFixedSize(650 + 224, 420)
            self.show_tip_now = True

    def closeEvent(self, event):
        saved_data = self.pack_data()
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


if __name__ == "__main__":
    app = QApplication([])
    window = EditWindow(0)
    window.show()
    app.exec()
