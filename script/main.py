from json import loads as json_loads
from sys import exit as sys_exit
from sys import argv as sys_argv
from os import path as os_path

from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (QApplication, QListWidgetItem, QMainWindow, QButtonGroup)
from CharacterWindow import Ui_MainWindow

import ExtraF as ef
import character_card

with open('data/data.json', encoding='UTF-8') as jsonfile:
    gk_data = json_loads(jsonfile.read())
    gk_character_data = gk_data['character_data']

# 提前生成完整列表
cdict_id_to_name = {c['id']: c['name'] for c in gk_character_data}
cdict_id_to_number = {c['id']: i for i, c in enumerate(gk_character_data)}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #预准备
        self.ui.label_Text_Verions.setText('软件：v1.0   |   牌库：' + gk_data['verions'])
        self.character_data = gk_character_data[:]
        
        # 左侧筛选
        self.ui.listWidget_List.itemClicked.connect(self.on_listWidget_List_itemClicked)
        # 按钮组filter_button_group
        self.filter_button_group = QButtonGroup()
        self.filter_button_group.addButton(self.ui.radioButton_FilterID)
        self.filter_button_group.addButton(self.ui.radioButton_FilterName)
        # 连接槽函数
        self.filter_button_group.buttonClicked.connect(self.on_filter_button_clicked)
        # 初始化
        self.ui.radioButton_FilterName.setChecked(True)
        self.filter_list = []
        for data in self.character_data:
            character = [data['id'], data['name']]
            item = QListWidgetItem(character[1])
            item.setData(Qt.UserRole, character[0]) #type: ignore
            item.setSizeHint(QSize(self.ui.listWidget_List.sizeHintForColumn(0), 16))
            self.ui.listWidget_List.addItem(item)
            self.filter_list.append(character)

            
        # [开发] 不可使用
        self.ui.comboBox_Filter.setEnabled(False) #DLC筛选
        self.ui.pushButton_Save.setEnabled(False) #保存
        
        # 生成图片
        self.ui.pushButton_ImageBuild.clicked.connect(self.on_pushButton_ImageBuild_clicked)
        
        # 添加角色
        self.ui.pushButton_NewCharacter.clicked.connect(self.on_pushButton_NewCharacter_click)
        
        # 保存
        # self.ui.pushButton_Save.clicked.connect(self.on_pushButton_Save_clicked)
        
        
        

    # ID或名字列表点击 - 角色详情显示
    def on_listWidget_List_itemClicked(self, item):
        """角色信息显示"""
        self.id = item.data(Qt.UserRole) #type: ignore
        self.data = self.character_data[cdict_id_to_number[self.id]]
        if self.data['title'] != '':
            Allname = '「' + self.data['title'] + '·' + self.data['name'] + '」'
        else:
            Allname = self.data['name']
        self.ui.label_Text_AllName.setText(Allname)
        color_code = ef.color(self.data['element'])
        palelle = QPalette()
        palelle.setColor(QPalette.WindowText, QColor(color_code)) #type: ignore
        self.ui.label_Text_AllName.setPalette(palelle)
        
        if self.data.get('id', False):
            self.ui.lineEdit_ID.setText(self.data['id'])
        else:
            raise
        
        self.ui.lineEdit_Title.setText(self.data.get('title', '角色称号'))
        self.ui.lineEdit_Name.setText(self.data.get('name', '角色名称'))
        self.ui.lineEdit_Designer.setText(self.data.get('designer', '设计师'))
        self.ui.spinBox_HP.setValue(self.data.get('health_point', 0))
        self.ui.spinBox_HPMax.setValue(self.data.get('max_health_point', 0))
        self.ui.spinBox_Armor.setValue(self.data.get('armor_point', 0))
        self.ui.comboBox_Sex.setCurrentIndex(ef.sex(self.data.get('sex', 'male')))
        self.ui.comboBox_Country.setCurrentIndex(ef.country(self.data.get('country', 'others')))
        self.ui.comboBox_Element.setCurrentIndex(ef.element(self.data.get('element', 'others')))
        self.ui.checkBox_Finish.setChecked(bool(self.data.get('design_info', '0')))
        self.ui.comboBox_StarLevel.setCurrentIndex(ef.star(self.data.get('level', 5)))
        self.ui.comboBox_DLC.setCurrentIndex(ef.dlcs(self.data.get('dlc', 'others')))
        
        imgpath = os_path.join('data', 'img', 'character', self.data['id'] + '.png')
        if os_path.exists(imgpath):
            self.img = QPixmap(imgpath).scaledToWidth(200)
            self.ui.label_Image.setPixmap(self.img)
            self.ui.label_Image.setText('')
        else:
            self.ui.label_Image.setText('No Image.')
        
        for i in range(1, 9):
            self.lineEdit_name = f"lineEdit_Skill{i}_Name"
            self.textEdit_Description = f"textEdit_Skill{i}_Description"
            self.checkBox_Enabled = f"checkBox_Skill{i}_Enabled"
            self.checkBox_Visibled = f"checkBox_Skill{i}_Visibled"
            if i <= len(self.data['skills']):
                self.ui.tabWidget_Skill.setTabText(i-1, self.data['skills'][i-1]['name'])
                getattr(self.ui, self.lineEdit_name).setText(self.data['skills'][i-1]['name'])
                getattr(self.ui, self.textEdit_Description).setPlainText(self.data['skills'][i-1]['description'])
                getattr(self.ui, self.checkBox_Visibled).setChecked(self.data['skills'][i-1]['origin'])
                getattr(self.ui, self.checkBox_Enabled).setChecked(True)
            else:
                self.ui.tabWidget_Skill.setTabText(i-1, "+")
                getattr(self.ui, self.lineEdit_name).setText('')
                getattr(self.ui, self.textEdit_Description).setPlainText('')
                getattr(self.ui, self.checkBox_Visibled).setChecked(False)
                getattr(self.ui, self.checkBox_Enabled).setChecked(False)
 
    # ID或名字筛选
    def on_filter_button_clicked(self, button):
        """筛选区左下按钮"""
        if button == self.ui.radioButton_FilterID:
            self.return_num = 0
        elif button == self.ui.radioButton_FilterName:
            self.return_num = 1
        self.ui.listWidget_List.clear()
        
        for character in self.filter_list:
            item = QListWidgetItem(character[self.return_num])
            item.setData(Qt.UserRole, character[0]) #type: ignore
            item.setSizeHint(QSize(self.ui.listWidget_List.sizeHintForColumn(0), 16))
            self.ui.listWidget_List.addItem(item)
  
                
    # 添加角色
    def on_pushButton_NewCharacter_click(self):
        i = 1
        while 'new_character_' + str(i) in self.filter_list:
            i += 1
        
        new_id = 'new_character_' + str(i)
        
        item = QListWidgetItem(new_id)
        item.setData(Qt.UserRole, new_id) #type: ignore
        item.setSizeHint(QSize(self.ui.listWidget_List.sizeHintForColumn(0), 16))
        self.ui.listWidget_List.addItem(item)
        self.filter_list.append(new_id)
        self.character_data.append(
            {
                'id': new_id,
                'title': '',
                'name': new_id,
                'sex': 'both',
                'element': 'others',
                'country': 'others',
                'level': 5,
                'design_info': 0,
                'designer': '',
                'health_point': 3,
                'max_health_point': 3,
                'armor_point': 0,
                'dlc': 'genshin-standard',
                'skills': []
                }
            )
        cdict_id_to_name[new_id] = new_id
        cdict_id_to_number[new_id] = len(cdict_id_to_number)
        
        self.ui.listWidget_List.setCurrentRow(len(self.filter_list)-1)
        self.on_listWidget_List_itemClicked(item)
        
        
    # 生成图片
    def on_pushButton_ImageBuild_clicked(self):
        """GK-23a 图片生成显示"""
        
        self.cardbuild_data = {
            'id': self.ui.lineEdit_ID.text(),
            'title': self.ui.lineEdit_Title.text(),
            'name': self.ui.lineEdit_Name.text(),
            'designer': self.ui.lineEdit_Designer.text(),
            'health_point': self.ui.spinBox_HP.value(),
            'max_health_point': self.ui.spinBox_HPMax.value(),
            'armor_point': self.ui.spinBox_Armor.value(),
            'sex': ef.sex_back(self.ui.comboBox_Sex.currentIndex()),
            'country': ef.country_back(self.ui.comboBox_Country.currentIndex()),
            'element': ef.element_back(self.ui.comboBox_Element.currentIndex()),
            'design_info': int(self.ui.checkBox_Finish.isChecked()),
            'level': ef.star_back(self.ui.comboBox_StarLevel.currentIndex()),
            'dlc': ef.dlcs_back(self.ui.comboBox_DLC.currentIndex()),
            'skills': []
        }
        for i in range(1, 9):
            self.checkBox_Enabled = f"checkBox_Skill{i}_Enabled"
            if getattr(self.ui, self.checkBox_Enabled).isChecked():
                self.lineEdit_name = f"lineEdit_Skill{i}_Name"
                self.textEdit_Description = f"textEdit_Skill{i}_Description"
                self.checkBox_Visibled = f"checkBox_Skill{i}_Visibled"
                self.cardbuild_data['skills'].append(
                    {
                        'name': getattr(self.ui, self.lineEdit_name).text(),
                        'description': getattr(self.ui, self.textEdit_Description).toPlainText(),
                        'origin': getattr(self.ui, self.checkBox_Visibled).isChecked()
                    }
                )
        
        outputimg = character_card.cardbuild(self.cardbuild_data, gk_data['verions'])
        if outputimg:
            outputimg.show()
    
    # 保存
    def on_pushButton_clicked(self):
        pass
        # self.my_dict[self.ui.listWidget_List.currentItem().text()] = {
        #     "field1": self.ui.lineEdit1.text(),
        #     "field2": self.ui.lineEdit2.text(),
        #     "field3": self.ui.spinBox.value(),
        #     "field4": self.ui.comboBox.currentIndex()
        #     # ... 将其他小部件的内容保存到相应的字典条目
        # }

    
if __name__ == "__main__":
    app = QApplication(sys_argv)

    window = MainWindow()
    window.show()

    sys_exit(app.exec())
