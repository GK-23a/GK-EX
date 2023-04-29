from sys import exit as sys_exit
from sys import argv as sys_argv

from os import path as os_path
from json import loads as json_loads
from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QApplication, QListWidgetItem, QMainWindow, QButtonGroup)

from CharacterWindow import Ui_MainWindow
import ExtraF as ef

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
            
        # [开发] 不可使用
        self.ui.comboBox_Filter.setEnabled(False) #DLC筛选
        self.ui.pushButton_Save.setEnabled(False) #保存
        self.ui.pushButton_Output.setEnabled(False) #导出
        self.ui.pushButton_Input.setEnabled(False) #导入
        self.ui.pushButton_NewCharacter.setEnabled(False) #添加角色
        self.ui.pushButton_ImageBuild.setEnabled(False) #生成图片
        self.ui.pushButton_AllImageBuild.setEnabled(False) #批量生成
    
    def on_fliter_button_clicked(self, button):
        if button == self.ui.radioButton_FliterID:
            self.return_body = 'id'
        elif button == self.ui.radioButton_FliterName:
            self.return_body = 'name'
        self.ui.listWidget_List.clear()
        for character in ef.get_fliter_list(character_datas, None, return_body = self.return_body):
            item = QListWidgetItem(character)
            item.setSizeHint(QSize(self.ui.listWidget_List.sizeHintForColumn(0), 16))
            self.ui.listWidget_List.addItem(item)
    
        # 连接pushButton和槽函数
        # self.ui.pushButton_Save.clicked.connect(self.on_pushButton_clicked)
        
        self.ui.pushButton_ImageBuild.clicked.connect(self.on_pushButton_ImageBuild_clicked)
        
        
    def on_listWidget_List_itemClicked(self, item):
        id = item.text()
        try:
            data = character_datas[cdict_id_to_number[id]]
        except KeyError:
            data = character_datas[cdict_id_to_number[cdict_name_to_id[id]]]
            
        Allname = '「' + data['title'] + '·' + data['name'] + '」'
        self.ui.label_Text_AllName.setText(Allname)
        color_code = ef.color(data['element'])
        palelle = QPalette()
        palelle.setColor(QPalette.WindowText, QColor(color_code)) #type: ignore
        self.ui.label_Text_AllName.setPalette(palelle)
        
        if data.get('id', False):
            self.ui.lineEdit_ID.setText(data['id'])
        else:
            raise
        
        self.ui.lineEdit_Title.setText(data.get('title', '角色称号'))
        self.ui.lineEdit_Name.setText(data.get('name', '角色名称'))
        self.ui.lineEdit_Designer.setText(data.get('designer', '设计师'))
        self.ui.spinBox_HP.setValue(data.get('health_point', 0))
        self.ui.spinBox_HPMax.setValue(data.get('max_health_point', 0))
        self.ui.spinBox_Armor.setValue(data.get('armor_point', 0))
        self.ui.comboBox_Sex.setCurrentIndex(ef.sex(data.get('sex', 'male')))
        self.ui.comboBox_Country.setCurrentIndex(ef.country(data.get('country', 'others')))
        self.ui.comboBox_Element.setCurrentIndex(ef.element(data.get('element', 'others')))
        self.ui.checkBox_Finish.setChecked(bool(data.get('design_info', '0')))
        self.ui.comboBox_StarLevel.setCurrentIndex(ef.star(data.get('level', 5)))
        self.ui.comboBox_DLC.setCurrentIndex(ef.dlcs(data.get('dlc', 'others')))
        
        imgpath = os_path.join('img', 'character', data['id'] + '.png')
        if os_path.exists(imgpath):
            self.img = QPixmap(imgpath).scaledToWidth(200)
            self.ui.label_Image.setPixmap(self.img)
            self.ui.label_Image.setText('')
        else:
            self.ui.label_Image.setText('No Image.')
        
        for i in range(1, 9):
            lineEdit_name = f"lineEdit_Skill{i}_Name"
            textEdit_Description = f"textEdit_Skill{i}_Description"
            checkBox_Enabled = f"checkBox_Skill{i}_Enabled"
            checkBox_Visibled = f"checkBox_Skill{i}_Visibled"
            if i <= len(data['skills']):
                self.ui.tabWidget_Skill.setTabText(i-1, data['skills'][i-1]['name'])
                getattr(self.ui, lineEdit_name).setText(data['skills'][i-1]['name'])
                getattr(self.ui, textEdit_Description).setText(data['skills'][i-1]['description'])
                getattr(self.ui, checkBox_Visibled).setChecked(data['skills'][i-1]['origin'])
                getattr(self.ui, checkBox_Enabled).setChecked(True)
            else:
                self.ui.tabWidget_Skill.setTabText(i-1, "+")
                getattr(self.ui, lineEdit_name).setText('')
                getattr(self.ui, textEdit_Description).setText('')
                getattr(self.ui, checkBox_Visibled).setChecked(False)
                getattr(self.ui, checkBox_Enabled).setChecked(False)


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
        print(self.ui.lineEdit_ID.text())
        
if __name__ == "__main__":
    app = QApplication(sys_argv)

    window = MainWindow()
    window.show()

    sys_exit(app.exec())
