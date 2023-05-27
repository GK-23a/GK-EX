from json import loads as json_loads
from sys import argv as sys_argv
from os import path as os_path

from PIL.ImageQt import ImageQt
from PySide6.QtGui import QColor, QPalette, QPixmap, QImage
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (QApplication, QListWidgetItem, QMainWindow, QButtonGroup)
from CharacterWindow import Ui_MainWindow

import ExtraF
import character_card

with open('data/data.json', encoding='UTF-8') as jsonfile:
    gk_data = json_loads(jsonfile.read())
    gk_character_data = gk_data['character_data']


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 预准备
        self.ui.label_Text_Verions.setText('软件：v1.0   |   牌库：' + gk_data['versions'])
        self.character_data = gk_character_data[:]
        self.cdict_id_to_name = {c['id']: c['name'] for c in gk_character_data}
        self.cdict_id_to_number = {c['id']: i for i, c in enumerate(gk_character_data)}
        
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
        self.save_list = []
        for j in self.filter_list:
            self.save_list.append(j[0])
            
        # [开发] 不可使用
        self.ui.comboBox_Filter.setEnabled(False)#DLC筛选
        
        # 生成图片
        self.ui.pushButton_ImageBuild.clicked.connect(self.on_pushButton_ImageBuild_clicked)
        # 添加角色
        self.ui.pushButton_NewCharacter.clicked.connect(self.on_pushButton_NewCharacter_click)
        
        # 显示第一个
        self.id = self.ui.listWidget_List.item(0).data(Qt.UserRole) #type: ignore
        self.show_data()
        self.ui.listWidget_List.setCurrentRow(0)

    
    def show_data(self):
        """显示数据"""
        self.data = self.character_data[self.cdict_id_to_number[self.id]]
        if self.data['title'] != '':
            Allname = '「' + self.data['title'] + '·' + self.data['name'] + '」'
        else:
            Allname = self.data['name']
        self.ui.label_Text_AllName.setText(Allname)
        color_code = ExtraF.color(self.data['element'])
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
        self.ui.comboBox_Sex.setCurrentIndex(ExtraF.sex(self.data.get('sex', 'male')))
        self.ui.comboBox_Country.setCurrentIndex(ExtraF.country(self.data.get('country', 'others')))
        self.ui.comboBox_Element.setCurrentIndex(ExtraF.element(self.data.get('element', 'others')))
        self.ui.checkBox_Finish.setChecked(bool(self.data.get('design_info', '0')))
        self.ui.comboBox_StarLevel.setCurrentIndex(ExtraF.star(self.data.get('level', 5)))
        self.ui.comboBox_DLC.setCurrentIndex(ExtraF.dlcs(self.data.get('dlc', 'others')))
        
        self.imgpath = os_path.join('data', 'img', 'character', self.data['id'] + '.png')
        if os_path.exists(self.imgpath):
            with open(self.imgpath, 'rb') as f:
                img_data = f.read()
            self.img = QImage.fromData(img_data)
            self.img_scaled = self.img.scaled(QSize(200, 320), Qt.KeepAspectRatio, Qt.SmoothTransformation) #type: ignore
            self.pixmap = QPixmap.fromImage(self.img_scaled)
            self.ui.label_Image.setPixmap(self.pixmap)
            self.ui.label_Image.setText('')
        else:
            self.ui.label_Image.setText('No Image.')
        self.outputimg = None
        
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
        
    def save_data(self, data: dict):
        """保存数据"""
        # 确认是否需要保存
        self.save_tag = False
        if data['id']:
            self.save_info = []
            if data['id'] in self.save_list:
                # 未修改ID
                
                print('未修改ID')
                self.id_num = self.cdict_id_to_number[data['id']]
                for key in self.saved_data:
                    
                    if key == 'skills':
                        
                        self.ss = []
                        # 填充ss列表：曾经的技能名
                        for s in gk_character_data[self.id_num]['skills']:
                            self.ss.append(s['name'])
                        self.ss2 = self.ss[:]
                        
                        self.skill_fix = [[],[],[]]
                        for skill in data['skills']:
                            if skill['enabled']:
                                if skill['name'] in self.ss:
                                    # 检测到
                                    for s in skill:
                                        print(s)
                                        self.skill_fix[2].append(skill['name'])
                                        self.ss.remove(skill['name'])
                                else:
                                    # 未检测到——新增
                                    self.skill_fix[0] = skill['name']
                        for s in self.ss:
                            # 删除的技能
                            self.skill_fix[1] = s
                    
                        
                    else:
                        
                        if key in gk_character_data[self.id_num]:
                            if self.saved_data[key] != gk_character_data[self.id_num][key]:
                                self.save_tag = True
                                self.save_info.append(
                                    [
                                        ExtraF.get_time(),
                                        'M',
                                        data['id'],
                                        key,
                                        gk_character_data[self.id_num][key],
                                        self.saved_data[key]
                                        ]
                                    )
                                print(self.save_info)
                                
            elif self.now_id in self.save_list:
                # 修改了ID
                
                print('修改了ID')
                self.save_tag = True
                pass
            
            else:
                # 新增角色
                
                print('新增角色')
                self.save_tag = True
                self.save_list.append(data['id'])
                
        # 保存操作
        if self.save_tag:
            self.ui.progressBar.setValue(20)
        self.ui.progressBar.setValue(0)

    
    # ID或名字列表点击 - 角色详情显示与保存
    def on_listWidget_List_itemClicked(self, item):
        """保存上一个角色内容，显示新的角色内容"""

        # 保存
        self.saved_data = {
            'id': self.ui.lineEdit_ID.text(),
            'title': self.ui.lineEdit_Title.text(),
            'name': self.ui.lineEdit_Name.text(),
            'designer': self.ui.lineEdit_Designer.text(),
            'health_point': self.ui.spinBox_HP.value(),
            'max_health_point': self.ui.spinBox_HPMax.value(),
            'armor_point': self.ui.spinBox_Armor.value(),
            'sex': ExtraF.sex_back(self.ui.comboBox_Sex.currentIndex()),
            'country': ExtraF.country_back(self.ui.comboBox_Country.currentIndex()),
            'element': ExtraF.element_back(self.ui.comboBox_Element.currentIndex()),
            'design_info': int(self.ui.checkBox_Finish.isChecked()),
            'level': ExtraF.star_back(self.ui.comboBox_StarLevel.currentIndex()),
            'dlc': ExtraF.dlcs_back(self.ui.comboBox_DLC.currentIndex()),
            'skills': []
        }
        for i in range(1, 9):
            self.checkBox_Enabled = f"checkBox_Skill{i}_Enabled"
            if getattr(self.ui, self.checkBox_Enabled).isChecked():
                self.lineEdit_name = f"lineEdit_Skill{i}_Name"
                self.textEdit_Description = f"textEdit_Skill{i}_Description"
                self.checkBox_Visibled = f"checkBox_Skill{i}_Visibled"
                self.saved_data['skills'].append(
                    {
                        'name': getattr(self.ui, self.lineEdit_name).text(),
                        'description': getattr(self.ui, self.textEdit_Description).toPlainText(),
                        'origin': getattr(self.ui, self.checkBox_Visibled).isChecked(),
                        'enabled': getattr(self.ui, self.checkBox_Enabled).isChecked()
                    }
                )
        self.save_data(self.saved_data)
        
        # 显示
        self.id = item.data(Qt.UserRole) #type: ignore
        self.show_data()
        self.now_id = self.data['id']
 
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
        self.newlist = []
        for j in self.filter_list:
            self.newlist.append(j[0])
        while 'new_character_' + str(i) in self.newlist:
            i += 1
        self.new_id = 'new_character_' + str(i)

        self.item = QListWidgetItem(self.new_id)
        self.item.setData(Qt.UserRole, self.new_id) #type: ignore
        self.item.setSizeHint(QSize(self.ui.listWidget_List.sizeHintForColumn(0), 16))
        self.ui.listWidget_List.addItem(self.item)
        self.filter_list.append([self.new_id, self.new_id])
        self.character_data.append(
            {
                'id': self.new_id,
                'title': '',
                'name': self.new_id,
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
        self.cdict_id_to_name[self.new_id] = self.new_id
        self.cdict_id_to_number[self.new_id] = len(self.cdict_id_to_number)
        
        self.ui.listWidget_List.setCurrentRow(len(self.filter_list)-1)
        self.on_listWidget_List_itemClicked(self.item)
        
        
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
            'sex': ExtraF.sex_back(self.ui.comboBox_Sex.currentIndex()),
            'country': ExtraF.country_back(self.ui.comboBox_Country.currentIndex()),
            'element': ExtraF.element_back(self.ui.comboBox_Element.currentIndex()),
            'design_info': int(self.ui.checkBox_Finish.isChecked()),
            'level': ExtraF.star_back(self.ui.comboBox_StarLevel.currentIndex()),
            'dlc': ExtraF.dlcs_back(self.ui.comboBox_DLC.currentIndex()),
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
        
        self.outputimg = character_card.cardbuild(self.cardbuild_data, gk_data['versions'], progress_bar=self.ui.progressBar, ignore_designer=True)
        if self.outputimg:
            self.qimg = ImageQt(self.outputimg)
            self.img_scaled = self.qimg.scaled(QSize(200, 320), Qt.KeepAspectRatio, Qt.SmoothTransformation) #type: ignore
            self.pixmap = QPixmap.fromImage(self.img_scaled)
            self.ui.label_Image.setPixmap(self.pixmap)
            self.ui.label_Image.mousePressEvent = self.on_label_Image_clicked
        self.ui.progressBar.setValue(0)
    
    def on_label_Image_clicked(self, ev):
        if self.outputimg:
            self.ui.progressBar.setValue(100)
            self.outputimg.show()
            self.ui.progressBar.setValue(0)
            
    def closeEvent(self, event):
        
        # 保存
        self.saved_data = {
            'id': self.ui.lineEdit_ID.text(),
            'title': self.ui.lineEdit_Title.text(),
            'name': self.ui.lineEdit_Name.text(),
            'designer': self.ui.lineEdit_Designer.text(),
            'health_point': self.ui.spinBox_HP.value(),
            'max_health_point': self.ui.spinBox_HPMax.value(),
            'armor_point': self.ui.spinBox_Armor.value(),
            'sex': ExtraF.sex_back(self.ui.comboBox_Sex.currentIndex()),
            'country': ExtraF.country_back(self.ui.comboBox_Country.currentIndex()),
            'element': ExtraF.element_back(self.ui.comboBox_Element.currentIndex()),
            'design_info': int(self.ui.checkBox_Finish.isChecked()),
            'level': ExtraF.star_back(self.ui.comboBox_StarLevel.currentIndex()),
            'dlc': ExtraF.dlcs_back(self.ui.comboBox_DLC.currentIndex()),
            'skills': []
        }
        for i in range(1, 9):
            self.checkBox_Enabled = f"checkBox_Skill{i}_Enabled"
            if getattr(self.ui, self.checkBox_Enabled).isChecked():
                self.lineEdit_name = f"lineEdit_Skill{i}_Name"
                self.textEdit_Description = f"textEdit_Skill{i}_Description"
                self.checkBox_Visibled = f"checkBox_Skill{i}_Visibled"
                self.saved_data['skills'].append(
                    {
                        'name': getattr(self.ui, self.lineEdit_name).text(),
                        'description': getattr(self.ui, self.textEdit_Description).toPlainText(),
                        'origin': getattr(self.ui, self.checkBox_Visibled).isChecked()
                    }
                )
        self.save_data(self.saved_data)
        event.accept()
    
if __name__ == "__main__":
    app = QApplication(sys_argv)

    window = MainWindow()
    window.show()
    
    app.exec()
