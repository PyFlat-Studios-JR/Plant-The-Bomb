from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(900, 500))
        MainWindow.setMaximumSize(QSize(900, 500))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.mainpage_1 = QWidget()
        self.mainpage_1.setObjectName(u"mainpage_1")
        self.verticalLayout_4 = QVBoxLayout(self.mainpage_1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.mainpage_1)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(280, 0))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_6)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_6)
        self.label.setObjectName(u"label")

        self.verticalLayout_6.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.frame_4 = QFrame(self.frame_6)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self.frame_4)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.lineEdit)

        self.lineEdit_2 = QLineEdit(self.frame_4)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.lineEdit_2)

        self.pushButton_7 = QPushButton(self.frame_4)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.verticalLayout_5.addWidget(self.pushButton_7)


        self.verticalLayout_6.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_6)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_4 = QPushButton(self.frame_5)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_3.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.frame_5)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_3.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.frame_5)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_3.addWidget(self.pushButton_6)


        self.verticalLayout_6.addWidget(self.frame_5, 0, Qt.AlignHCenter|Qt.AlignTop)


        self.verticalLayout_4.addWidget(self.frame_6, 0, Qt.AlignHCenter)

        self.stackedWidget.addWidget(self.mainpage_1)
        self.mainpage_2 = QWidget()
        self.mainpage_2.setObjectName(u"mainpage_2")
        self.verticalLayout_9 = QVBoxLayout(self.mainpage_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_7 = QFrame(self.mainpage_2)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(280, 0))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_7)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_7)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_7.addWidget(self.label_2, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.frame_8 = QFrame(self.frame_7)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_8)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_3 = QLineEdit(self.frame_8)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.lineEdit_3)

        self.lineEdit_4 = QLineEdit(self.frame_8)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.lineEdit_4)

        self.lineEdit_5 = QLineEdit(self.frame_8)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.lineEdit_5)

        self.pushButton_8 = QPushButton(self.frame_8)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.verticalLayout_8.addWidget(self.pushButton_8)


        self.verticalLayout_7.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.frame_7)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_9 = QPushButton(self.frame_9)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_4.addWidget(self.pushButton_9)

        self.pushButton_11 = QPushButton(self.frame_9)
        self.pushButton_11.setObjectName(u"pushButton_11")

        self.horizontalLayout_4.addWidget(self.pushButton_11)


        self.verticalLayout_7.addWidget(self.frame_9, 0, Qt.AlignHCenter|Qt.AlignTop)


        self.verticalLayout_9.addWidget(self.frame_7, 0, Qt.AlignHCenter)

        self.stackedWidget.addWidget(self.mainpage_2)
        self.level_select = QWidget()
        self.level_select.setObjectName(u"level_select")
        self.horizontalLayout_2 = QHBoxLayout(self.level_select)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.level_select)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)


        self.horizontalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.level_select)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton_2 = QPushButton(self.frame_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.level_select)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_3 = QPushButton(self.frame_3)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_3.addWidget(self.pushButton_3)


        self.horizontalLayout_2.addWidget(self.frame_3)

        self.stackedWidget.addWidget(self.level_select)
        self.main = QWidget()
        self.main.setObjectName(u"main")
        self.horizontalLayout_5 = QHBoxLayout(self.main)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.main)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_11 = QFrame(self.frame_10)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.frame_11.setLineWidth(0)

        self.horizontalLayout_6.addWidget(self.frame_11)

        self.widget = QWidget(self.frame_10)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(500, 500))

        self.horizontalLayout_6.addWidget(self.widget)

        self.frame_12 = QFrame(self.frame_10)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_6.addWidget(self.frame_12)


        self.horizontalLayout_5.addWidget(self.frame_10)

        self.stackedWidget.addWidget(self.main)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Plant The Bomb Login", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Forgot Password", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Plant The Bomb Register", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Confirm Password", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Custom Maps", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Main Game?", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Map Builder", None))
    # retranslateUi

