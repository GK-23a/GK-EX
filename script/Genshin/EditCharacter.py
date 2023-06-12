import os

from PySide6.QtCore import QRect
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QCheckBox, QComboBox, QWidget, QPushButton, QSpinBox, \
    QProgressBar, QGroupBox, QPlainTextEdit, QTabWidget


class EditWindow(QWidget):
    def __init__(self, character_card):
        super().__init__()
        self.setWindowTitle(f'编辑角色 {character_card.name} - GK-23a/Genshin')
        self.setFixedSize(650, 420)

        font_id = QFontDatabase.addApplicationFont(os.path.join('font', 'MiSans-Demibold.ttf'))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family)
        font.setPointSize(10.5)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font)

        #     id
        show_id = QLabel(self)
        show_id.setText('ID')
        show_id.setGeometry(QRect(25, 30, 38, 16))
        data_id = QLabel(self)
        data_id.setGeometry(QRect(63, 30, 176, 16))
        #    title
        show_title = QLabel(self)
        show_title.setText('称号')
        show_title.setGeometry(QRect(25, 60, 38, 16))
        data_title = QLineEdit(self)
        data_title.setGeometry(QRect(60, 58, 120, 20))
        #    name
        show_name = QLabel(self)
        show_name.setText('名字')
        show_name.setGeometry(QRect(25, 90, 38, 16))
        data_name = QLineEdit(self)
        data_name.setGeometry(QRect(60, 88, 120, 20))
        #    designer
        show_designer = QLabel(self)
        show_designer.setText('设计')
        show_designer.setGeometry(QRect(25, 120, 38, 16))
        data_designer = QLineEdit(self)
        data_designer.setGeometry(QRect(60, 118, 120, 20))
        #    design_state
        show_design_state = QLabel(self)
        show_design_state.setText('状态')
        show_design_state.setGeometry(QRect(25, 150, 38, 16))
        data_design_state = QCheckBox(self)
        data_design_state.setText('设计完成（未勾选状态下，不会生成此角色卡图片）')
        data_design_state.setGeometry(QRect(60, 150, 340, 16))
        #    sex
        show_sex = QLabel(self)
        show_sex.setText('性别')
        show_sex.setGeometry(QRect(190, 60, 35, 16))
        data_sex = QComboBox(self)
        data_sex.addItem('男')
        data_sex.addItem('女')
        data_sex.addItem('其他')
        data_sex.setGeometry(QRect(225, 58, 65, 20))
        #    level
        show_level = QLabel(self)
        show_level.setText('星级')
        show_level.setGeometry(QRect(190, 90, 35, 16))
        data_level = QSpinBox(self)
        data_level.setGeometry(QRect(225, 88, 65, 20))
        #    country
        show_country = QLabel(self)
        show_country.setText('所属')
        show_country.setGeometry(QRect(305, 60, 35, 16))
        data_country = QComboBox(self)
        data_country.addItem('蒙德')
        data_country.addItem('璃月')
        data_country.addItem('稻妻')
        data_country.addItem('须弥')
        data_country.addItem('枫丹')
        data_country.addItem('纳塔')
        data_country.addItem('至冬')
        data_country.addItem('坎瑞亚')
        data_country.addItem('其他')
        data_country.setGeometry(QRect(340, 58, 65, 20))
        #    element
        show_element = QLabel(self)
        show_element.setText('元素')
        show_element.setGeometry(QRect(305, 90, 35, 16))
        data_element = QComboBox(self)
        data_element.addItem('火元素')
        data_element.addItem('水元素')
        data_element.addItem('风元素')
        data_element.addItem('雷元素')
        data_element.addItem('草元素')
        data_element.addItem('冰元素')
        data_element.addItem('岩元素')
        data_element.addItem('其他')
        data_element.setGeometry(QRect(340, 88, 65, 20))
        #    health
        show_health = QLabel(self)
        show_health.setText('体力')
        show_health.setGeometry(QRect(190, 120, 60, 16))
        data_health_def = QSpinBox(self)
        data_health_def.setGeometry(QRect(220, 118, 40, 20))
        data_health_max = QSpinBox(self)
        data_health_max.setGeometry(QRect(270, 118, 40, 20))
        #    armor
        show_armor = QLabel(self)
        show_armor.setText('护甲值')
        show_armor.setGeometry(QRect(320, 120, 60, 16))
        data_armor = QSpinBox(self)
        data_armor.setGeometry(QRect(365, 118, 40, 20))

        # 技能区
        self.data_skill = QTabWidget(self)
        self.data_skill.setGeometry(QRect(25, 200, 380, 210))
        self.data_skill.setStyleSheet('QTabBar::tab{ width:50px; }')
        for i in range(1, character_card.skill_num):
            self.add_skill(getattr(character_card, f'skill{i}'), i)

        # 进度条
        pg_bar = QProgressBar(self)
        pg_bar.setGeometry(QRect(415, 30, 255, 16))
        pg_bar.setFormat('')
        # 图片
        image_box = QGroupBox(self)
        image_box.setGeometry(QRect(415, 60, 214, 350))
        image_box.setTitle('角色立绘/卡面')
        show_image = QLabel(self)
        show_image.setGeometry(QRect(422, 80, 200, 320))

        # 数据显示
        data_id.setText(character_card.id)
        data_name.setText(character_card.name)
        data_title.setText(character_card.title)
        data_designer.setText(character_card.designer)
        data_design_state.setChecked(bool(character_card.design_state))
        data_sex.setCurrentIndex(character_card.to_number('sex'))
        data_level.setValue(character_card.level)
        data_country.setCurrentIndex(character_card.to_number('country'))
        data_element.setCurrentIndex(character_card.to_number('element'))
        data_health_def.setValue(character_card.health_point)
        data_health_max.setValue(character_card.max_health_point)
        data_armor.setValue(character_card.armor_point)

        # 修改id
        edit_id = QPushButton(self)
        edit_id.setGeometry(QRect(253, 28, 40, 22))
        edit_id.setText('修改')
        edit_id.setEnabled(False)
        # 生成角色图片尝试
        edit_id = QPushButton(self)
        edit_id.setGeometry(QRect(305, 28, 100, 22))
        edit_id.setText('生成角色图片')
        edit_id.setEnabled(False)

    def add_skill(self, data, i):
        sw = f"show_skill{i}_Widget"
        sn = f"show_skill{i}_Name"
        dn = f"data_skill{i}_Name"
        sd = f"show_skill{i}_Description"
        dd = f"data_skill{i}_Description"
        dv = f"data_skill{i}_Visible"
        setattr(self, sw, QWidget())
        setattr(self, sn, QLabel(getattr(self, sw)))
        getattr(self, sn).setGeometry(QRect(10, 10, 51, 16))
        getattr(self, sn).setText('技能名字')
        setattr(self, dn, QLineEdit(getattr(self, sw)))
        getattr(self, dn).setGeometry(QRect(70, 8, 113, 20))
        setattr(self, sd, QLabel(getattr(self, sw)))
        getattr(self, sd).setGeometry(QRect(10, 40, 51, 16))
        getattr(self, sd).setText('技能描述')
        setattr(self, dd, QPlainTextEdit(getattr(self, sw)))
        getattr(self, dd).setGeometry(QRect(70, 40, 301, 150))
        setattr(self, dv, QCheckBox(getattr(self, sw)))
        getattr(self, dv).setGeometry(QRect(250, 10, 51, 20))
        getattr(self, dv).setText('可见')
        self.data_skill.addTab(getattr(self, sw), data.get('name'))


class EditIDWindow(QDialog):
    def __init__(self):
        super().__init__()
        pass
