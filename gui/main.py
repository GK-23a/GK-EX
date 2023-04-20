import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow
# from PySide6.QtCore import QFile
from CharacterWindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 连接listWidget_List和槽函数
        self.ui.listWidget_List.itemClicked.connect(self.on_listWidget_List_itemClicked)

        # 连接pushButton和槽函数
        self.ui.pushButton_Save.clicked.connect(self.on_pushButton_clicked)

        # 示例字典
        self.my_dict = {
            "Item 1": {"field1": "Value 1", "field2": "Value 2", "field3": 0, "field4": False},
            "Item 2": {"field1": "Value 3", "field2": "Value 4", "field3": 5, "field4": True},
            # ... 添加其他字典条目
        }

    def on_listWidget_List_itemClicked(self, item):
        name = item.text()
        data = self.my_dict[name]
        self.ui.lineEdit_ID.setText(data["field1"])
        self.ui.lineEdit_Title.setText(data["field2"])
        self.ui.lineEdit_Name.setText(data[])
        self.ui.lineEdit_Designer.setText(data[])
        self.ui.spinBox_HP.setValue(data["field3"])
        self.ui.spinBox_HPMax.setValue(data["field3"])
        self.ui.spinBox_Armor.setValue(data["field3"])
        self.ui.comboBox_Sex.setCurrentIndex(data["field4"])
        self.ui.comboBox_Country.setCurrentIndex(data["field4"])
        self.ui.comboBox_Element.setCurrentIndex(data["field4"])
        self.ui.comboBox_Filter.setCurrentIndex(data["field4"])
        self.ui.comboBox_StarLevel.setCurrentIndex(data["field4"])
        # ... 将其他小部件的内容设置为相应的字典条目

    def on_pushButton_clicked(self):
        self.my_dict[self.ui.listWidget_List.currentItem().text()] = {
            "field1": self.ui.lineEdit1.text(),
            "field2": self.ui.lineEdit2.text(),
            "field3": self.ui.spinBox.value(),
            "field4": self.ui.comboBox.currentIndex(),
            # ... 将其他小部件的内容保存到相应的字典条目
        }

        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())