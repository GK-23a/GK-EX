import sys
import json
from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QApplication, QCheckBox, 
    QLineEdit, QListWidgetItem, QMainWindow, QTextEdit,
    QWidget, QButtonGroup)

from CharacterWindow import Ui_MainWindow
import character_card
import ExtraF as ef

with open('json/data.json', encoding='UTF-8') as jsonfile:
    gk_data = json.loads(jsonfile.read())
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
        
        self.ui.label_Text_VerionsInfo.setText(gk_data['verions'])


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
        
        if data['id']:
            self.ui.lineEdit_ID.setText(data['id'])
        else:
            raise
        if data['title']: self.ui.lineEdit_Title.setText(data['title'])
        if data['name']: self.ui.lineEdit_Name.setText(data['name'])
        if data['designer']: self.ui.lineEdit_Designer.setText(data['designer'])
        if data['health_point']: self.ui.spinBox_HP.setValue(data['health_point'])
        if data['max_health_point']: self.ui.spinBox_HPMax.setValue(data['max_health_point'])
        if data['armor_point']: self.ui.spinBox_Armor.setValue(data['armor_point'])
        if data['sex']: self.ui.comboBox_Sex.setCurrentIndex(ef.sex(data['sex']))
        if data['country']: self.ui.comboBox_Country.setCurrentIndex(ef.country(data['country']))
        if data['element']: self.ui.comboBox_Element.setCurrentIndex(ef.element(data['element']))
        if data['dedign_info']: self.ui.checkBox_Finish.setChecked(bool(data['design_info']))
        if data['level']: self.ui.comboBox_StarLevel.setCurrentIndex(ef.star(data['level']))
        
        img = QPixmap('img/character/' + data['id'] + '.png')
        self.ui.label_Image.setPixmap(img.scaledToWidth(200))
        
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
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
