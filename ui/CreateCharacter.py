import json
import os
from time import asctime, localtime, time

from PySide6.QtCore import QRect
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import (QLabel, QLineEdit, QComboBox, QDialog, QPushButton, QSpinBox, QMessageBox, QApplication)

from cards.GKCard import GKCharacterCard


def get_time(left=0, right=0):
    return asctime(localtime(time()))[4 + left:19 + right]


class IDRepeatError(Exception):
    def __init__(self):
        pass


class CreateWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.save_flag = False
        self.setFixedSize(440, 200)

        font_id = QFontDatabase.addApplicationFont(os.path.join('assets', 'font', 'SDK_SC_85W.ttf'))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font = QFont(font_family)
        self.font.setPointSize(10.5)
        self.font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(self.font)

        #     id
        show_id = QLabel(self)
        show_id.setText('ID')
        show_id.setGeometry(QRect(25, 30, 38, 16))
        self.data_id = QLineEdit(self)
        self.data_id.setGeometry(QRect(60, 28, 160, 20))
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
        #    dlc
        show_dlc = QLabel(self)
        show_dlc.setText('DLC')
        show_dlc.setGeometry(QRect(305, 150, 35, 16))
        self.data_dlc = QComboBox(self)
        self.data_dlc.addItem('标准包')
        self.data_dlc.addItem('诸神包')
        self.data_dlc.addItem('创者包')
        self.data_dlc.addItem('未分类')
        self.data_dlc.setGeometry(QRect(340, 148, 65, 20))

        # 数据加载与显示
        self.ch_card = GKCharacterCard('new_character')

        self.setWindowTitle(f'新增角色 - GK-23a/Genshin')

        # 保存并退出
        save_and_refresh = QPushButton(self)
        save_and_refresh.setGeometry(QRect(326, 28, 80, 22))
        save_and_refresh.setText('保存并退出')
        save_and_refresh.clicked.connect(lambda: self.save_data())

        self.data_id.setText(self.ch_card.id)
        self.data_name.setText(self.ch_card.name)
        self.data_title.setText(self.ch_card.title)
        self.data_designer.setText(self.ch_card.designer)
        self.data_sex.setCurrentIndex(self.ch_card.to_number('sex'))
        self.data_level.setValue(self.ch_card.level)
        self.data_country.setCurrentIndex(self.ch_card.to_number('country'))
        self.data_element.setCurrentIndex(self.ch_card.to_number('element'))
        self.data_health_def.setValue(self.ch_card.health_point)
        self.data_health_max.setValue(self.ch_card.max_health_point)
        self.data_armor.setValue(self.ch_card.armor_point)
        self.data_dlc.setCurrentIndex(self.ch_card.to_number('dlc'))

    def pack_data(self):
        self.ch_card.id = self.data_id.text()
        self.ch_card.name = self.data_name.text()
        self.ch_card.title = self.data_title.text()
        self.ch_card.designer = self.data_designer.text()
        self.ch_card.design_state = False
        self.ch_card.sex = self.ch_card.number_to(self.data_sex.currentIndex(), 'sex')
        self.ch_card.level = self.data_level.value()
        self.ch_card.country = self.ch_card.number_to(self.data_country.currentIndex(), 'country')
        self.ch_card.element = self.ch_card.number_to(self.data_element.currentIndex(), 'element')
        self.ch_card.health_point = self.data_health_def.value()
        self.ch_card.max_health_point = self.data_health_max.value()
        self.ch_card.armor_point = self.data_armor.value()
        self.ch_card.dlc = self.ch_card.number_to(self.data_dlc.currentIndex(), 'dlc')
        for i in range(1, self.ch_card.skill_num + 1):
            tp_n = getattr(self, f'self.data_skill{i}_name').text()
            tp_d = getattr(self, f'self.data_skill{i}_description').toPlainText()
            tp_v = bool(getattr(self, f'self.data_skill{i}_visible').isChecked())
            setattr(self.ch_card, f'skill{i}', dict(name=tp_n, description=tp_d, visible=tp_v))
        saved_data = self.ch_card.pack()
        return saved_data

    def save_data(self, reason=False):
        with open(os.path.join('assets', 'json', 'card_data.json'), encoding='UTF-8') as data_file:
            gk_character_data = json.load(data_file).get('character_data')
            cids = {i.get('id', None) for i in gk_character_data}
        if self.data_id.text() in cids:
            error_tip = QMessageBox()
            error_tip.setWindowTitle('错误')
            error_tip.setFont(self.font)
            error_tip.setText('角色创建失败：角色id重复。')
            # noinspection PyUnresolvedReferences
            error_tip.setStandardButtons(QMessageBox.Cancel)
            # noinspection PyUnresolvedReferences
            error_tip.setDefaultButton(QMessageBox.Cancel)
            error_tip.exec()
        else:
            restart_tip = QMessageBox()
            restart_tip.setWindowTitle('提示')
            restart_tip.setFont(self.font)
            restart_tip.setText('创建角色后需要重启窗口。')
            restart_tip.setInformativeText('您可使用 编辑-保存并重启 来进行重启。')
            # noinspection PyUnresolvedReferences
            restart_tip.setStandardButtons(QMessageBox.Save)
            # noinspection PyUnresolvedReferences
            restart_tip.setDefaultButton(QMessageBox.Save)
            restart_tip.exec()
            try:
                with open(os.path.join('assets', 'json', 'card_data.json'), 'r', encoding='UTF-8') as jsonfile:
                    gk_data = json.load(jsonfile)

                saved_data = self.pack_data()
                cids = [cdata['id'] for cdata in gk_data['character_data']]
                if self.ch_card.id in cids:
                    raise IDRepeatError
                else:
                    gk_data['character_data'].append(saved_data)
                save_info = list()
                save_info.append([get_time(), 'AC', saved_data['id'], saved_data])

                with open(os.path.join('assets', 'json', 'card_data.json'), 'w', encoding='UTF-8') as jsonfile:
                    json.dump(gk_data, jsonfile, ensure_ascii=False)

                with open('output/change_log.gkcl', 'a', encoding='UTF-8') as gkcl:
                    for log in save_info:
                        gkcl.write(str(log) + '\n')

                self.save_flag = True
                self.close()
            except IDRepeatError:
                repeat_tip = QMessageBox()
                repeat_tip.setWindowTitle('错误')
                repeat_tip.setFont(self.font)
                repeat_tip.setText('角色ID重复了！无法保存！')
                repeat_tip.setInformativeText('IDRepeatError')
                # noinspection PyUnresolvedReferences
                repeat_tip.setStandardButtons(QMessageBox.Cancel)
                # noinspection PyUnresolvedReferences
                repeat_tip.setDefaultButton(QMessageBox.Cancel)
                repeat_tip.exec()
                if reason:
                    raise

    def closeEvent(self, event):
        if not self.save_flag:
            exit_tip = QMessageBox()
            exit_tip.setWindowTitle('提示')
            exit_tip.setFont(self.font)
            exit_tip.setText('角色还没有创建！要取消创建嘛？')
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
                try:
                    self.save_data(True)
                except IDRepeatError:
                    event.ignore()
                else:
                    event.accept()
        else:
            event.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = CreateWindow()
    window.show()
    app.exec()
