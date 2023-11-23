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
        self.verticalLayout_4.setContentsMargins(0, 30, 0, 30)
        self.frame_6 = QFrame(self.mainpage_1)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(280, 0))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_6)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.login_welcome_label = QLabel(self.frame_6)
        self.login_welcome_label.setObjectName(u"login_welcome_label")

        self.verticalLayout_6.addWidget(self.login_welcome_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.frame_4 = QFrame(self.frame_6)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.login_username_entry = QLineEdit(self.frame_4)
        self.login_username_entry.setObjectName(u"login_username_entry")
        self.login_username_entry.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_5.addWidget(self.login_username_entry)

        self.frame_14 = QFrame(self.frame_4)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.login_password_entry = QLineEdit(self.frame_14)
        self.login_password_entry.setObjectName(u"login_password_entry")
        self.login_password_entry.setEchoMode(QLineEdit.Password)
        self.login_password_entry.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.login_password_entry, 0, Qt.AlignVCenter)

        self.login_password_toggle = QPushButton(self.frame_14)
        self.login_password_toggle.setObjectName(u"login_password_toggle")
        icon = QIcon()
        icon.addFile(u"src/gui/images/eye-slash.png", QSize(), QIcon.Selected, QIcon.Off)
        icon.addFile(u"src/gui/images/eye.png", QSize(), QIcon.Selected, QIcon.On)
        self.login_password_toggle.setIcon(icon)
        self.login_password_toggle.setIconSize(QSize(25, 25))
        self.login_password_toggle.setCheckable(True)

        self.horizontalLayout_8.addWidget(self.login_password_toggle, 0, Qt.AlignVCenter)


        self.verticalLayout_5.addWidget(self.frame_14)

        self.login_btn = QPushButton(self.frame_4)
        self.login_btn.setObjectName(u"login_btn")

        self.verticalLayout_5.addWidget(self.login_btn)


        self.verticalLayout_6.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_6)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 10, 0, 0)
        self.login_register_btn = QPushButton(self.frame_5)
        self.login_register_btn.setObjectName(u"login_register_btn")

        self.horizontalLayout_3.addWidget(self.login_register_btn)

        self.login_forgot_password_btn = QPushButton(self.frame_5)
        self.login_forgot_password_btn.setObjectName(u"login_forgot_password_btn")

        self.horizontalLayout_3.addWidget(self.login_forgot_password_btn)

        self.login_help_btn = QPushButton(self.frame_5)
        self.login_help_btn.setObjectName(u"login_help_btn")

        self.horizontalLayout_3.addWidget(self.login_help_btn)


        self.verticalLayout_6.addWidget(self.frame_5, 0, Qt.AlignHCenter|Qt.AlignTop)


        self.verticalLayout_4.addWidget(self.frame_6, 0, Qt.AlignHCenter)

        self.stackedWidget.addWidget(self.mainpage_1)
        self.mainpage_2 = QWidget()
        self.mainpage_2.setObjectName(u"mainpage_2")
        self.verticalLayout_9 = QVBoxLayout(self.mainpage_2)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 30, 0, 30)
        self.frame_7 = QFrame(self.mainpage_2)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(280, 0))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_7)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.register_welcome_label = QLabel(self.frame_7)
        self.register_welcome_label.setObjectName(u"register_welcome_label")

        self.verticalLayout_7.addWidget(self.register_welcome_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.frame_8 = QFrame(self.frame_7)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_8)
        self.verticalLayout_8.setSpacing(15)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.register_username_entry = QLineEdit(self.frame_8)
        self.register_username_entry.setObjectName(u"register_username_entry")
        self.register_username_entry.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_8.addWidget(self.register_username_entry)

        self.register_password_entry = QLineEdit(self.frame_8)
        self.register_password_entry.setObjectName(u"register_password_entry")
        self.register_password_entry.setEchoMode(QLineEdit.Password)
        self.register_password_entry.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_8.addWidget(self.register_password_entry)

        self.register_confirm_entry = QLineEdit(self.frame_8)
        self.register_confirm_entry.setObjectName(u"register_confirm_entry")
        self.register_confirm_entry.setEchoMode(QLineEdit.Password)
        self.register_confirm_entry.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_8.addWidget(self.register_confirm_entry)

        self.register_btn = QPushButton(self.frame_8)
        self.register_btn.setObjectName(u"register_btn")

        self.verticalLayout_8.addWidget(self.register_btn)


        self.verticalLayout_7.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.frame_7)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.register_login_btn = QPushButton(self.frame_9)
        self.register_login_btn.setObjectName(u"register_login_btn")

        self.horizontalLayout_4.addWidget(self.register_login_btn)

        self.register_help_btn = QPushButton(self.frame_9)
        self.register_help_btn.setObjectName(u"register_help_btn")

        self.horizontalLayout_4.addWidget(self.register_help_btn)


        self.verticalLayout_7.addWidget(self.frame_9, 0, Qt.AlignHCenter|Qt.AlignTop)


        self.verticalLayout_9.addWidget(self.frame_7, 0, Qt.AlignHCenter)

        self.stackedWidget.addWidget(self.mainpage_2)
        self.mainpage_3 = QWidget()
        self.mainpage_3.setObjectName(u"mainpage_3")
        self.verticalLayout_12 = QVBoxLayout(self.mainpage_3)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 30, 0, 30)
        self.frame_11 = QFrame(self.mainpage_3)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(280, 0))
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_11)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.login_welcome_label_2 = QLabel(self.frame_11)
        self.login_welcome_label_2.setObjectName(u"login_welcome_label_2")
        self.login_welcome_label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.login_welcome_label_2, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.frame_12 = QFrame(self.frame_11)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_12)
        self.verticalLayout_11.setSpacing(15)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.recovery_username_entry = QLineEdit(self.frame_12)
        self.recovery_username_entry.setObjectName(u"recovery_username_entry")
        self.recovery_username_entry.setEchoMode(QLineEdit.Normal)
        self.recovery_username_entry.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_11.addWidget(self.recovery_username_entry)

        self.recovery_code_entry = QLineEdit(self.frame_12)
        self.recovery_code_entry.setObjectName(u"recovery_code_entry")
        self.recovery_code_entry.setEchoMode(QLineEdit.Password)
        self.recovery_code_entry.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_11.addWidget(self.recovery_code_entry)

        self.recovery_submit_btn = QPushButton(self.frame_12)
        self.recovery_submit_btn.setObjectName(u"recovery_submit_btn")

        self.verticalLayout_11.addWidget(self.recovery_submit_btn)


        self.verticalLayout_10.addWidget(self.frame_12)

        self.frame_13 = QFrame(self.frame_11)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_7.setSpacing(20)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 10, 0, 0)
        self.recovery_login_btn = QPushButton(self.frame_13)
        self.recovery_login_btn.setObjectName(u"recovery_login_btn")

        self.horizontalLayout_7.addWidget(self.recovery_login_btn)

        self.recovery_help_btn = QPushButton(self.frame_13)
        self.recovery_help_btn.setObjectName(u"recovery_help_btn")

        self.horizontalLayout_7.addWidget(self.recovery_help_btn)


        self.verticalLayout_10.addWidget(self.frame_13, 0, Qt.AlignHCenter|Qt.AlignTop)


        self.verticalLayout_12.addWidget(self.frame_11, 0, Qt.AlignHCenter)

        self.stackedWidget.addWidget(self.mainpage_3)
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
        self.custom_maps_btn = QPushButton(self.frame)
        self.custom_maps_btn.setObjectName(u"custom_maps_btn")

        self.verticalLayout.addWidget(self.custom_maps_btn)


        self.horizontalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.level_select)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.start_game_btn = QPushButton(self.frame_2)
        self.start_game_btn.setObjectName(u"start_game_btn")

        self.verticalLayout_2.addWidget(self.start_game_btn)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.level_select)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.map_builder_btn = QPushButton(self.frame_3)
        self.map_builder_btn.setObjectName(u"map_builder_btn")

        self.verticalLayout_3.addWidget(self.map_builder_btn)


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
        self.inventory = QFrame(self.frame_10)
        self.inventory.setObjectName(u"inventory")
        self.inventory.setFrameShape(QFrame.StyledPanel)
        self.inventory.setFrameShadow(QFrame.Raised)
        self.inventory.setLineWidth(0)

        self.horizontalLayout_6.addWidget(self.inventory)

        self.game_widget = QWidget(self.frame_10)
        self.game_widget.setObjectName(u"game_widget")
        self.game_widget.setMinimumSize(QSize(500, 500))

        self.horizontalLayout_6.addWidget(self.game_widget)

        self.inventory_2 = QFrame(self.frame_10)
        self.inventory_2.setObjectName(u"inventory_2")
        self.inventory_2.setFrameShape(QFrame.StyledPanel)
        self.inventory_2.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_6.addWidget(self.inventory_2)


        self.horizontalLayout_5.addWidget(self.frame_10)

        self.stackedWidget.addWidget(self.main)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.login_welcome_label.setText(QCoreApplication.translate("MainWindow", u"Plant The Bomb Login", None))
        self.login_username_entry.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.login_password_entry.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.login_password_toggle.setText("")
        self.login_btn.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.login_register_btn.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.login_forgot_password_btn.setText(QCoreApplication.translate("MainWindow", u"Forgot Password", None))
        self.login_help_btn.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.register_welcome_label.setText(QCoreApplication.translate("MainWindow", u"Plant The Bomb Register", None))
        self.register_username_entry.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.register_password_entry.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.register_confirm_entry.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Confirm Password", None))
        self.register_btn.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.register_login_btn.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.register_help_btn.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.login_welcome_label_2.setText(QCoreApplication.translate("MainWindow", u"Plant The Bomb\n"
"Forgot Password", None))
        self.recovery_username_entry.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.recovery_code_entry.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Recovery Code", None))
        self.recovery_submit_btn.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
        self.recovery_login_btn.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.recovery_help_btn.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.custom_maps_btn.setText(QCoreApplication.translate("MainWindow", u"Custom Maps", None))
        self.start_game_btn.setText(QCoreApplication.translate("MainWindow", u"Main Game?", None))
        self.map_builder_btn.setText(QCoreApplication.translate("MainWindow", u"Map Builder", None))
    # retranslateUi

