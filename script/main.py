from sys import exit as sys_exit
from sys import argv as sys_argv
from os import path as os_path
from json import loads as json_loads

from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QApplication, QListWidgetItem, QMainWindow, QButtonGroup)
from CharacterWindow import Ui_MainWindow

import ExtraF as ef
import character_card

with open('data/data.json', encoding='UTF-8') as jsonfile:
    gk_data = json_loads(jsonfile.read())
    character_datas = gk_data['character_data']

# 提前生成完整列表
clist_cid = ef.get_fliter_list(character_datas, None)
cdict_id_to_name = {}
cdict_name_to_id = {}
cdict_id_to_number = {}
i = 0
for c in character_datas:
    cdict_id_to_name[c['id']] = c['name']
    cdict_name_to_id[c['name']] = c['id']
    cdict_id_to_number[c['id']] = i
    i += 1
    

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.label_Text_Verions.setText('Ver.' + gk_data['verions'])
        
        # 左侧筛选
        self.ui.listWidget_List.itemClicked.connect(self.on_listWidget_List_itemClicked)
        # 按钮组fliter_button_group
        self.filter_button_group = QButtonGroup()
        self.filter_button_group.addButton(self.ui.radioButton_FliterID)
        self.filter_button_group.addButton(self.ui.radioButton_FliterName)
       # 连接槽函数
        self.filter_button_group.buttonClicked.connect(self.on_fliter_button_clicked)
        # 初始化
        self.ui.radioButton_FliterName.setChecked(True)
        for character in ef.get_fliter_list(character_datas, None, return_body = 'name'):
            item = QListWidgetItem(character)
            item.setSizeHint(QSize(self.ui.listWidget_List.sizeHintForColumn(0), 16))
            self.ui.listWidget_List.addItem(item)
        
            
        # 连接pushButton和槽函数
        # self.ui.pushButton_Save.clicked.connect(self.on_pushButton_Save_clicked)
        
        # 生成图片
        self.ui.pushButton_ImageBuild.clicked.connect(self.on_pushButton_ImageBuild_clicked)
        
        # [开发] 不可使用
        self.ui.comboBox_Filter.setEnabled(False) #DLC筛选
        self.ui.pushButton_Save.setEnabled(False) #保存
        self.ui.pushButton_Output.setEnabled(False) #导出
        self.ui.pushButton_Input.setEnabled(False) #导入
        self.ui.pushButton_NewCharacter.setEnabled(False) #添加角色
        self.ui.pushButton_ImageBuild.setEnabled(True) #生成图片
        self.ui.pushButton_AllImageBuild.setEnabled(False) #批量生成
    
    
    def on_fliter_button_clicked(self, button):
        """筛选区左下按钮"""
        if button == self.ui.radioButton_FliterID:
            self.return_body = 'id'
        elif button == self.ui.radioButton_FliterName:
            self.return_body = 'name'
        self.ui.listWidget_List.clear()
        for character in ef.get_fliter_list(character_datas, None, return_body = self.return_body):
            item = QListWidgetItem(character)
            item.setSizeHint(QSize(self.ui.listWidget_List.sizeHintForColumn(0), 16))
            self.ui.listWidget_List.addItem(item)
        
    def on_listWidget_List_itemClicked(self, item):
        """角色信息显示"""
        self.id = item.text()
        try:
            self.data = character_datas[cdict_id_to_number[self.id]]
        except KeyError:
            self.data = character_datas[cdict_id_to_number[cdict_name_to_id[self.id]]]
            
        Allname = '「' + self.data['title'] + '·' + self.data['name'] + '」'
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
        
        self.idv  = self.data['id']


        # ... 将其他小部件的内容设置为相应的字典条目
    
    # def on_pushButton_clicked(self):
    #     self.my_dict[self.ui.listWidget_List.currentItem().text()] = {
    #         "field1": self.ui.lineEdit1.text(),
    #         "field2": self.ui.lineEdit2.text(),
    #         "field3": self.ui.spinBox.value(),
    #         "field4": self.ui.comboBox.currentIndex()
    #         # ... 将其他小部件的内容保存到相应的字典条目
    #     }
    
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
            'sex': self.ui.comboBox_Sex.currentIndex(),
            'country': self.ui.comboBox_Country.currentIndex(),
            'element': self.ui.comboBox_Element.currentIndex(),
            'design_info': int(self.ui.checkBox_Finish.isChecked()),
            'level': self.ui.comboBox_StarLevel.currentIndex(),
            'dlc': self.ui.comboBox_DLC.currentIndex(),
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
        
if __name__ == "__main__":
    app = QApplication(sys_argv)

    window = MainWindow()
    window.show()

    sys_exit(app.exec())


#  'skills': [
#      {'name': '狂澜', 'id': 'kuanglan', 'description': '转换技，阳：摸牌阶段，你额外摸三张牌，手牌上限+3，但此出牌阶段你最多使用四张牌；阴：摸牌阶段，你少摸一张牌并可以选择一名攻击范围内的角色视为对其使用一张杀，且本回合你使用牌无次数限制。','origin': True}, 
#      {'name': '断流', 'id': 'dongliu', 'description': '每当你造成伤害时，若此伤害大于一点或者“狂澜”处于阳状态，你可以令受伤角色获得“断流”标记。你使用牌可以额外指定一名带有“断流”标记的角色；当有“断流”标记的角色再次获得此标记时，你摸一张牌。有断流标记的角色，标记会在其结束阶段移除。', 'origin': True}, 
#      {'name': '尽灭', 'id': 'jinmie', 'description': '限定技，出牌阶段结束时，你可以对所有有“断流”标记的角色造成一点伤害，之后移除全部断流标记。', 'origin': True}
#      ]}