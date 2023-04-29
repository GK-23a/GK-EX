

################################################################################
## Form generated from reading UI file 'CharacterWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QMetaObject, QRect, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFrame,
    QLabel, QLineEdit, QListWidget, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpinBox, QStatusBar, QTabWidget,
    QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName('MainWindow')
        MainWindow.resize(800, 440)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred) #type: ignore
        sizePolicy.setHorizontalStretch(81)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setFixedSize(800, 440)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        
        ## 基本信息
        # ID
        self.label_Text_ID = QLabel(self.centralwidget)
        self.label_Text_ID.setObjectName('label_Text_ID')
        self.label_Text_ID.setGeometry(QRect(190, 53, 31, 16))
        self.label_Text_ID.setText('ID')
        self.lineEdit_ID = QLineEdit(self.centralwidget)
        self.lineEdit_ID.setObjectName('lineEdit_ID')
        self.lineEdit_ID.setGeometry(QRect(220, 50, 101, 20))
        # 称号
        self.label_Text_Title = QLabel(self.centralwidget)
        self.label_Text_Title.setObjectName('label_Text_Title')
        self.label_Text_Title.setGeometry(QRect(190, 83, 31, 16))
        self.label_Text_Title.setText('称号')
        self.lineEdit_Title = QLineEdit(self.centralwidget)
        self.lineEdit_Title.setObjectName('lineEdit_Title')
        self.lineEdit_Title.setGeometry(QRect(220, 80, 131, 20))
        # 名称
        self.label_Text_Name = QLabel(self.centralwidget)
        self.label_Text_Name.setObjectName('label_Text_Name')
        self.label_Text_Name.setGeometry(QRect(190, 113, 31, 16))
        self.label_Text_Name.setText('名称')
        self.lineEdit_Name = QLineEdit(self.centralwidget)
        self.lineEdit_Name.setObjectName('lineEdit_Name')
        self.lineEdit_Name.setGeometry(QRect(220, 110, 131, 20))
        # 设计师      
        self.label_Text_Designer = QLabel(self.centralwidget)
        self.label_Text_Designer.setObjectName('label_Text_Designer')
        self.label_Text_Designer.setGeometry(QRect(190, 143, 31, 16))
        self.label_Text_Designer.setText('设计')
        self.lineEdit_Designer = QLineEdit(self.centralwidget)
        self.lineEdit_Designer.setObjectName('lineEdit_Designer')
        self.lineEdit_Designer.setGeometry(QRect(220, 140, 131, 20))
        # 设计状态
        self.checkBox_Finish = QCheckBox(self.centralwidget)
        self.checkBox_Finish.setObjectName('checkBox_Finish')
        self.checkBox_Finish.setGeometry(QRect(360, 140, 81, 20))
        self.checkBox_Finish.setText('已设计')
        # 性别
        self.label_Text_Sex = QLabel(self.centralwidget)
        self.label_Text_Sex.setObjectName('label_Text_Sex')
        self.label_Text_Sex.setGeometry(QRect(360, 83, 31, 16))
        self.label_Text_Sex.setText('性别')
        self.comboBox_Sex = QComboBox(self.centralwidget)
        self.comboBox_Sex.addItem('男')
        self.comboBox_Sex.addItem('女')
        self.comboBox_Sex.addItem('其他')
        self.comboBox_Sex.setObjectName('comboBox_Sex')
        self.comboBox_Sex.setGeometry(QRect(390, 80, 68, 22))
        # 星级
        self.label_Text_StarLevel = QLabel(self.centralwidget)
        self.label_Text_StarLevel.setObjectName('label_Text_StarLevel')
        self.label_Text_StarLevel.setGeometry(QRect(360, 113, 31, 16))
        self.label_Text_StarLevel.setText('星级')
        self.comboBox_StarLevel = QComboBox(self.centralwidget)
        self.comboBox_StarLevel.addItem('5')
        self.comboBox_StarLevel.addItem('4')
        self.comboBox_StarLevel.setObjectName('comboBox_StarLevel')
        self.comboBox_StarLevel.setGeometry(QRect(390, 110, 68, 22))
        # 所属
        self.label_Text_Country = QLabel(self.centralwidget)
        self.label_Text_Country.setObjectName('label_Text_Country')
        self.label_Text_Country.setGeometry(QRect(470, 83, 31, 16))
        self.label_Text_Country.setText('所属')
        self.comboBox_Country = QComboBox(self.centralwidget)
        self.comboBox_Country.addItem('蒙德')
        self.comboBox_Country.addItem('璃月')
        self.comboBox_Country.addItem('稻妻')
        self.comboBox_Country.addItem('须弥')
        self.comboBox_Country.addItem('枫丹')
        self.comboBox_Country.addItem('纳塔')
        self.comboBox_Country.addItem('至冬')
        self.comboBox_Country.addItem('坎瑞亚')
        self.comboBox_Country.addItem('其他')
        self.comboBox_Country.setObjectName('comboBox_Country')
        self.comboBox_Country.setGeometry(QRect(500, 80, 68, 22))
        # 元素
        self.label_Text_Element = QLabel(self.centralwidget)
        self.label_Text_Element.setObjectName('label_Text_Element')
        self.label_Text_Element.setGeometry(QRect(470, 113, 31, 16))
        self.label_Text_Element.setText('元素')
        self.comboBox_Element = QComboBox(self.centralwidget)
        self.comboBox_Element.addItem('火元素')
        self.comboBox_Element.addItem('水元素')
        self.comboBox_Element.addItem('风元素')
        self.comboBox_Element.addItem('雷元素')
        self.comboBox_Element.addItem('草元素')
        self.comboBox_Element.addItem('冰元素')
        self.comboBox_Element.addItem('岩元素')
        self.comboBox_Element.addItem('其他')
        self.comboBox_Element.setObjectName('comboBox_Element')
        self.comboBox_Element.setGeometry(QRect(500, 110, 68, 22))
        # 体力
        self.label_Text_Health = QLabel(self.centralwidget)
        self.label_Text_Health.setObjectName('label_Text_Health')
        self.label_Text_Health.setGeometry(QRect(330, 53, 31, 16))
        self.label_Text_Health.setText('体力')
        self.spinBox_HP = QSpinBox(self.centralwidget)
        self.spinBox_HP.setObjectName('spinBox_HP')
        self.spinBox_HP.setGeometry(QRect(360, 50, 42, 22))
        self.spinBox_HPMax = QSpinBox(self.centralwidget)
        self.spinBox_HPMax.setObjectName('spinBox_HPMax')
        self.spinBox_HPMax.setGeometry(QRect(420, 50, 42, 22))
        self.label_Text_Health_ = QLabel(self.centralwidget)
        self.label_Text_Health_.setObjectName('label_Text_Health_')
        self.label_Text_Health_.setGeometry(QRect(408, 53, 16, 16))
        self.label_Text_Health_.setText('/')
        # 初始护甲
        self.label_Text_Armor = QLabel(self.centralwidget)
        self.label_Text_Armor.setObjectName('label_Text_Armor')
        self.label_Text_Armor.setGeometry(QRect(470, 53, 51, 16))
        self.label_Text_Armor.setText('初始护甲')
        self.spinBox_Armor = QSpinBox(self.centralwidget)
        self.spinBox_Armor.setObjectName('spinBox_Armor')
        self.spinBox_Armor.setGeometry(QRect(530, 50, 42, 22))
        self.label_Text_AllName = QLabel(self.centralwidget)
        self.label_Text_AllName.setObjectName('label_Text_AllName')
        self.label_Text_AllName.setGeometry(QRect(190, 20, 381, 20))
        self.label_Text_AllName.setTextFormat(Qt.PlainText) #type: ignore
        self.label_Text_AllName.setWordWrap(False)
        self.label_Text_AllName.setOpenExternalLinks(False)
        
        ## 额外内容
        # DLC包
        self.comboBox_DLC = QComboBox(self.centralwidget)
        self.comboBox_DLC.addItem('原神-标准包')
        self.comboBox_DLC.addItem('原神-诸神包')
        self.comboBox_DLC.addItem('原神-创作包')
        self.comboBox_DLC.addItem('其他')
        self.comboBox_DLC.setObjectName('comboBox_DLC')
        self.comboBox_DLC.setGeometry(QRect(477, 140, 91, 24))
        # 版本号
        self.label_Text_Verions = QLabel(self.centralwidget)
        self.label_Text_Verions.setObjectName('label_Text_Verions')
        self.label_Text_Verions.setGeometry(QRect(660, 380, 128, 16))
        # 分割线
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName('line')
        self.line.setGeometry(QRect(170, 20, 20, 371))
        self.line.setFrameShape(QFrame.VLine) #type: ignore
        self.line.setFrameShadow(QFrame.Sunken) #type: ignore
        # 图片框
        self.label_Image = QLabel(self.centralwidget)
        self.label_Image.setObjectName('label_Image')
        self.label_Image.setGeometry(QRect(590, 50, 200, 320))
        self.label_Image.setStyleSheet('border: 1px solid #999999')
        self.label_Image.setFrameShape(QFrame.NoFrame) #type: ignore
        self.label_Image.setFrameShadow(QFrame.Plain) #type: ignore
        self.label_Image.setLineWidth(10)
        self.label_Image.setMidLineWidth(10)
        
        ## 功能区
        # 右上按钮处
        self.pushButton_NewCharacter = QPushButton(self.centralwidget)
        self.pushButton_NewCharacter.setObjectName('pushButton_NewCharacter')
        self.pushButton_NewCharacter.setGeometry(QRect(450, 20, 61, 24))
        self.pushButton_NewCharacter.setText('添加角色')
        self.pushButton_Save = QPushButton(self.centralwidget)
        self.pushButton_Save.setObjectName('pushButton_Save')
        self.pushButton_Save.setGeometry(QRect(520, 20, 61, 24))
        self.pushButton_Save.setText('保存')
        self.pushButton_ImageBuild = QPushButton(self.centralwidget)
        self.pushButton_ImageBuild.setObjectName('pushButton_ImageBuild')
        self.pushButton_ImageBuild.setGeometry(QRect(590, 20, 61, 24))
        self.pushButton_ImageBuild.setText('生成图片')
        self.pushButton_Input = QPushButton(self.centralwidget)
        self.pushButton_Input.setObjectName('pushButton_Input')
        self.pushButton_Input.setGeometry(QRect(660, 20, 61, 24))
        self.pushButton_Input.setText('导入文件')
        self.pushButton_Output = QPushButton(self.centralwidget)
        self.pushButton_Output.setObjectName('pushButton_Output')
        self.pushButton_Output.setGeometry(QRect(730, 20, 61, 24))
        self.pushButton_Output.setText('导出文件')
        self.pushButton_AllImageBuild = QPushButton(self.centralwidget)
        self.pushButton_AllImageBuild.setObjectName('pushButton_ImageBuild')
        self.pushButton_AllImageBuild.setGeometry(QRect(590, 376, 61, 24))
        self.pushButton_AllImageBuild.setText('批量生成')
        
        # 左侧筛选框
        self.label_Text_FliterS = QLabel(self.centralwidget)
        self.label_Text_FliterS.setObjectName('label_Text_FliterS')
        self.label_Text_FliterS.setGeometry(QRect(20, 24, 71, 16))     
        self.label_Text_FliterS.setText('DLC筛选')   
        self.comboBox_Filter = QComboBox(self.centralwidget)
        self.comboBox_Filter.addItem('全部')
        self.comboBox_Filter.addItem('原神-标准包')
        self.comboBox_Filter.addItem('原神-诸神包')
        self.comboBox_Filter.addItem('原神-创作包')
        self.comboBox_Filter.addItem('其他')
        self.comboBox_Filter.setObjectName('comboBox_Filter')
        self.comboBox_Filter.setGeometry(QRect(77, 21, 91, 22))
        # 左侧显示处
        self.listWidget_List = QListWidget(self.centralwidget)
        self.listWidget_List.setObjectName('listWidget_List')
        self.listWidget_List.setGeometry(QRect(20, 50, 151, 311))
        
        # 左下查看方式
        self.label_Text_FilterN = QLabel(self.centralwidget)
        self.label_Text_FilterN.setObjectName('label_Text_FilterN')
        self.label_Text_FilterN.setGeometry(QRect(20, 370, 51, 16))
        self.label_Text_FilterN.setText('查看方式')
        self.radioButton_FliterName = QRadioButton(self.centralwidget)
        self.radioButton_FliterName.setObjectName('radioButton_FliterName')
        self.radioButton_FliterName.setGeometry(QRect(120, 368, 51, 20))
        self.radioButton_FliterName.setText('名称')
        self.radioButton_FliterID = QRadioButton(self.centralwidget)
        self.radioButton_FliterID.setObjectName('radioButton_FliterID')
        self.radioButton_FliterID.setGeometry(QRect(80, 368, 41, 20))
        self.radioButton_FliterID.setText('ID')
        
        # 技能区
        self.tabWidget_Skill = QTabWidget(self.centralwidget)
        self.tabWidget_Skill.setObjectName('tabWidget_Skill')
        self.tabWidget_Skill.setGeometry(QRect(190, 170, 391, 231))
        self.tabWidget_Skill.setStyleSheet(' QTabBar::tab{ width:48px; } ')
        
        for i in range(1, 9):
            tab_name = f"tab_Skill{i}"
            lineEdit_name = f"lineEdit_Skill{i}_Name"
            label_Text_Name = f"label_Text_Skill{i}_Name"
            label_Text_Description = f"label_Text_Skill{i}_Description"
            textEdit_Description = f"textEdit_Skill{i}_Description"
            checkBox_Enabled = f"checkBox_Skill{i}_Enabled"
            checkBox_Visibled = f"checkBox_Skill{i}_Visibled"
            
            setattr(self, tab_name, QWidget())
            getattr(self, tab_name).setObjectName(tab_name)

            setattr(self, label_Text_Name, QLabel(getattr(self, tab_name)))
            getattr(self, label_Text_Name).setObjectName(label_Text_Name)
            getattr(self, label_Text_Name).setGeometry(QRect(10, 10, 51, 16))
            getattr(self, label_Text_Name).setText('技能名字')

            setattr(self, lineEdit_name, QLineEdit(getattr(self, tab_name)))
            getattr(self, lineEdit_name).setObjectName(lineEdit_name)
            getattr(self, lineEdit_name).setGeometry(QRect(70, 8, 113, 20))
            
            setattr(self, label_Text_Description, QLabel(getattr(self, tab_name)))
            getattr(self, label_Text_Description).setObjectName(label_Text_Description)
            getattr(self, label_Text_Description).setGeometry(QRect(10, 40, 51, 16))
            getattr(self, label_Text_Description).setText('技能描述')
            
            setattr(self, textEdit_Description, QTextEdit(getattr(self, tab_name)))
            getattr(self, textEdit_Description).setObjectName(textEdit_Description)
            getattr(self, textEdit_Description).setGeometry(QRect(70, 40, 301, 150))
            
            setattr(self, checkBox_Visibled, QCheckBox(getattr(self, tab_name)))
            getattr(self, checkBox_Visibled).setObjectName(checkBox_Visibled)
            getattr(self, checkBox_Visibled).setGeometry(QRect(250, 10, 51, 20))
            getattr(self, checkBox_Visibled).setText('可见')
            
            setattr(self, checkBox_Enabled, QCheckBox(getattr(self, tab_name)))
            getattr(self, checkBox_Enabled).setObjectName(checkBox_Enabled)
            getattr(self, checkBox_Enabled).setGeometry(QRect(300, 10, 80, 20))
            getattr(self, checkBox_Enabled).setText('技能存在')
            
            self.tabWidget_Skill.addTab(getattr(self, tab_name), '+')


        self.tabWidget_Skill.setCurrentIndex(0)

        # 其他内容
        font = QFont()
        font.setBold(True)
        self.label_Text_AllName.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName('menubar')
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)
        QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setWindowTitle('GK-23a 设计师编辑器') #type: ignore

    # retranslateUi

