from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from src.engine.gameWindow import gameWindow
from src.gui.LevelSelectContainer import LevelSelectContainer
from src.gui.StatsTableWidget import StatsTableWidget
from src.gui.KeyBindTable import KeyBindTable

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
        self.widget = QWidget(self.level_select)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 0, 15, 0)
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        icon1 = QIcon()
        icon1.addFile(u"src/gui/images/chevron-left.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QSize(40, 40))

        self.verticalLayout.addWidget(self.pushButton)


        self.horizontalLayout_2.addWidget(self.widget, 0, Qt.AlignLeft)

        self.stackedWidget_2 = QStackedWidget(self.level_select)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget_2.sizePolicy().hasHeightForWidth())
        self.stackedWidget_2.setSizePolicy(sizePolicy1)
        self.widget_2 = QWidget()
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 15, 0, 15)
        self.normal_level_select = LevelSelectContainer(self.widget_2)
        if (self.normal_level_select.columnCount() < 3):
            self.normal_level_select.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.normal_level_select.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.normal_level_select.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.normal_level_select.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.normal_level_select.setObjectName(u"normal_level_select")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.normal_level_select.sizePolicy().hasHeightForWidth())
        self.normal_level_select.setSizePolicy(sizePolicy2)
        self.normal_level_select.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.normal_level_select.setSelectionMode(QAbstractItemView.NoSelection)
        self.normal_level_select.setTextElideMode(Qt.ElideLeft)
        self.normal_level_select.setShowGrid(False)
        self.normal_level_select.setCornerButtonEnabled(False)
        self.normal_level_select.horizontalHeader().setVisible(False)
        self.normal_level_select.horizontalHeader().setHighlightSections(False)
        self.normal_level_select.verticalHeader().setVisible(False)
        self.normal_level_select.verticalHeader().setMinimumSectionSize(30)
        self.normal_level_select.verticalHeader().setDefaultSectionSize(50)
        self.normal_level_select.verticalHeader().setHighlightSections(False)

        self.verticalLayout_3.addWidget(self.normal_level_select)

        self.stackedWidget_2.addWidget(self.widget_2)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.verticalLayout_15 = QVBoxLayout(self.page_5)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 15, 0, 15)
        self.normal_level_select_2 = StatsTableWidget(self.page_5)
        self.normal_level_select_2.setObjectName(u"normal_level_select_2")
        sizePolicy2.setHeightForWidth(self.normal_level_select_2.sizePolicy().hasHeightForWidth())
        self.normal_level_select_2.setSizePolicy(sizePolicy2)
        self.normal_level_select_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.normal_level_select_2.setSelectionMode(QAbstractItemView.NoSelection)

        self.verticalLayout_15.addWidget(self.normal_level_select_2)

        self.stackedWidget_2.addWidget(self.page_5)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.horizontalLayout_21 = QHBoxLayout(self.page_4)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.page_4)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_16 = QVBoxLayout(self.tab)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.frame_24 = QFrame(self.tab)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = KeyBindTable(self.frame_24)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.tableWidget.setObjectName(u"tableWidget")

        self.horizontalLayout_23.addWidget(self.tableWidget)


        self.verticalLayout_16.addWidget(self.frame_24)

        self.frame_25 = QFrame(self.tab)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 15, 0, 15)
        self.pushButton_3 = QPushButton(self.frame_25)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_22.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.frame_25)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_22.addWidget(self.pushButton_4)


        self.verticalLayout_16.addWidget(self.frame_25)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_21.addWidget(self.tabWidget)

        self.stackedWidget_2.addWidget(self.page_4)

        self.horizontalLayout_2.addWidget(self.stackedWidget_2)

        self.widget_3 = QWidget(self.level_select)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(15, -1, 15, -1)
        self.pushButton_2 = QPushButton(self.widget_3)
        self.pushButton_2.setObjectName(u"pushButton_2")
        icon2 = QIcon()
        icon2.addFile(u"src/gui/images/chevron-right.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QSize(40, 40))

        self.verticalLayout_2.addWidget(self.pushButton_2)


        self.horizontalLayout_2.addWidget(self.widget_3, 0, Qt.AlignRight)

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
        self.verticalLayout_13 = QVBoxLayout(self.inventory)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(5, 0, 5, 0)
        self.frame_15 = QFrame(self.inventory)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label = QLabel(self.frame_15)
        self.label.setObjectName(u"label")

        self.horizontalLayout_9.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout_13.addWidget(self.frame_15, 0, Qt.AlignTop)

        self.frame_16 = QFrame(self.inventory)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.range_icon_btn = QPushButton(self.frame_16)
        self.range_icon_btn.setObjectName(u"range_icon_btn")
        sizePolicy.setHeightForWidth(self.range_icon_btn.sizePolicy().hasHeightForWidth())
        self.range_icon_btn.setSizePolicy(sizePolicy)
        self.range_icon_btn.setMinimumSize(QSize(25, 25))
        icon3 = QIcon()
        icon3.addFile(u"src/textures/09_fire.png", QSize(), QIcon.Normal, QIcon.Off)
        self.range_icon_btn.setIcon(icon3)
        self.range_icon_btn.setIconSize(QSize(25, 25))

        self.horizontalLayout_10.addWidget(self.range_icon_btn, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.range_inv_label = QLabel(self.frame_16)
        self.range_inv_label.setObjectName(u"range_inv_label")

        self.horizontalLayout_10.addWidget(self.range_inv_label, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_13.addWidget(self.frame_16)

        self.frame_18 = QFrame(self.inventory)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.bomb_icon_btn = QPushButton(self.frame_18)
        self.bomb_icon_btn.setObjectName(u"bomb_icon_btn")
        sizePolicy.setHeightForWidth(self.bomb_icon_btn.sizePolicy().hasHeightForWidth())
        self.bomb_icon_btn.setSizePolicy(sizePolicy)
        self.bomb_icon_btn.setMinimumSize(QSize(25, 25))
        icon4 = QIcon()
        icon4.addFile(u"src/textures/11_bomb.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bomb_icon_btn.setIcon(icon4)
        self.bomb_icon_btn.setIconSize(QSize(25, 25))

        self.horizontalLayout_12.addWidget(self.bomb_icon_btn, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.bomb_inv_label = QLabel(self.frame_18)
        self.bomb_inv_label.setObjectName(u"bomb_inv_label")

        self.horizontalLayout_12.addWidget(self.bomb_inv_label, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_13.addWidget(self.frame_18)

        self.frame_19 = QFrame(self.inventory)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.health_icon_btn = QPushButton(self.frame_19)
        self.health_icon_btn.setObjectName(u"health_icon_btn")
        sizePolicy.setHeightForWidth(self.health_icon_btn.sizePolicy().hasHeightForWidth())
        self.health_icon_btn.setSizePolicy(sizePolicy)
        self.health_icon_btn.setMinimumSize(QSize(25, 25))
        icon5 = QIcon()
        icon5.addFile(u"src/textures/13_heart.png", QSize(), QIcon.Normal, QIcon.Off)
        self.health_icon_btn.setIcon(icon5)
        self.health_icon_btn.setIconSize(QSize(25, 25))

        self.horizontalLayout_13.addWidget(self.health_icon_btn, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.health_inv_label = QLabel(self.frame_19)
        self.health_inv_label.setObjectName(u"health_inv_label")

        self.horizontalLayout_13.addWidget(self.health_inv_label, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_13.addWidget(self.frame_19)

        self.frame_20 = QFrame(self.inventory)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.timebomb_icon_btn = QPushButton(self.frame_20)
        self.timebomb_icon_btn.setObjectName(u"timebomb_icon_btn")
        sizePolicy.setHeightForWidth(self.timebomb_icon_btn.sizePolicy().hasHeightForWidth())
        self.timebomb_icon_btn.setSizePolicy(sizePolicy)
        self.timebomb_icon_btn.setMinimumSize(QSize(25, 25))
        icon6 = QIcon()
        icon6.addFile(u"src/textures/15_time_bomb.png", QSize(), QIcon.Normal, QIcon.Off)
        self.timebomb_icon_btn.setIcon(icon6)
        self.timebomb_icon_btn.setIconSize(QSize(25, 25))

        self.horizontalLayout_14.addWidget(self.timebomb_icon_btn, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.timebomb_inv_label = QLabel(self.frame_20)
        self.timebomb_inv_label.setObjectName(u"timebomb_inv_label")

        self.horizontalLayout_14.addWidget(self.timebomb_inv_label, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_13.addWidget(self.frame_20)

        self.frame_21 = QFrame(self.inventory)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.dynamite_icon_btn = QPushButton(self.frame_21)
        self.dynamite_icon_btn.setObjectName(u"dynamite_icon_btn")
        sizePolicy.setHeightForWidth(self.dynamite_icon_btn.sizePolicy().hasHeightForWidth())
        self.dynamite_icon_btn.setSizePolicy(sizePolicy)
        self.dynamite_icon_btn.setMinimumSize(QSize(25, 25))
        icon7 = QIcon()
        icon7.addFile(u"src/textures/17_dynamit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.dynamite_icon_btn.setIcon(icon7)
        self.dynamite_icon_btn.setIconSize(QSize(25, 25))

        self.horizontalLayout_15.addWidget(self.dynamite_icon_btn, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.dynamite_inv_label = QLabel(self.frame_21)
        self.dynamite_inv_label.setObjectName(u"dynamite_inv_label")

        self.horizontalLayout_15.addWidget(self.dynamite_inv_label, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_13.addWidget(self.frame_21)

        self.frame_22 = QFrame(self.inventory)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.damage_icon_btn = QPushButton(self.frame_22)
        self.damage_icon_btn.setObjectName(u"damage_icon_btn")
        sizePolicy.setHeightForWidth(self.damage_icon_btn.sizePolicy().hasHeightForWidth())
        self.damage_icon_btn.setSizePolicy(sizePolicy)
        self.damage_icon_btn.setMinimumSize(QSize(25, 25))
        icon8 = QIcon()
        icon8.addFile(u"src/textures/20_sword.png", QSize(), QIcon.Normal, QIcon.Off)
        self.damage_icon_btn.setIcon(icon8)
        self.damage_icon_btn.setIconSize(QSize(25, 25))

        self.horizontalLayout_16.addWidget(self.damage_icon_btn, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.damage_inv_label = QLabel(self.frame_22)
        self.damage_inv_label.setObjectName(u"damage_inv_label")

        self.horizontalLayout_16.addWidget(self.damage_inv_label, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_13.addWidget(self.frame_22)

        self.frame_23 = QFrame(self.inventory)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.nuke_icon_btn = QPushButton(self.frame_23)
        self.nuke_icon_btn.setObjectName(u"nuke_icon_btn")
        sizePolicy.setHeightForWidth(self.nuke_icon_btn.sizePolicy().hasHeightForWidth())
        self.nuke_icon_btn.setSizePolicy(sizePolicy)
        self.nuke_icon_btn.setMinimumSize(QSize(25, 25))
        icon9 = QIcon()
        icon9.addFile(u"src/textures/23_atomic_bomb.png", QSize(), QIcon.Normal, QIcon.Off)
        self.nuke_icon_btn.setIcon(icon9)
        self.nuke_icon_btn.setIconSize(QSize(25, 25))

        self.horizontalLayout_17.addWidget(self.nuke_icon_btn, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.nuke_inv_label = QLabel(self.frame_23)
        self.nuke_inv_label.setObjectName(u"nuke_inv_label")

        self.horizontalLayout_17.addWidget(self.nuke_inv_label, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_13.addWidget(self.frame_23)


        self.horizontalLayout_6.addWidget(self.inventory)

        self.game_widget = gameWindow(self.frame_10)
        self.game_widget.setObjectName(u"game_widget")
        self.game_widget.setMinimumSize(QSize(500, 500))

        self.horizontalLayout_6.addWidget(self.game_widget)

        self.inventory_2 = QFrame(self.frame_10)
        self.inventory_2.setObjectName(u"inventory_2")
        self.inventory_2.setFrameShape(QFrame.StyledPanel)
        self.inventory_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.inventory_2)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.frame_17 = QFrame(self.inventory_2)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_3 = QLabel(self.frame_17)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_19.addWidget(self.label_3, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout_14.addWidget(self.frame_17)

        self.frame = QFrame(self.inventory_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.time_label = QLabel(self.frame)
        self.time_label.setObjectName(u"time_label")

        self.horizontalLayout_11.addWidget(self.time_label)


        self.verticalLayout_14.addWidget(self.frame)

        self.label_5 = QLabel(self.inventory_2)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_14.addWidget(self.label_5)

        self.label_6 = QLabel(self.inventory_2)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_14.addWidget(self.label_6)

        self.label_7 = QLabel(self.inventory_2)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_14.addWidget(self.label_7)

        self.label_8 = QLabel(self.inventory_2)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_14.addWidget(self.label_8)

        self.frame_3 = QFrame(self.inventory_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(5, 0, 5, 0)
        self.pause_button = QPushButton(self.frame_3)
        self.pause_button.setObjectName(u"pause_button")

        self.horizontalLayout_20.addWidget(self.pause_button)


        self.verticalLayout_14.addWidget(self.frame_3)

        self.frame_2 = QFrame(self.inventory_2)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(5, 0, 5, 0)
        self.quit_button = QPushButton(self.frame_2)
        self.quit_button.setObjectName(u"quit_button")

        self.horizontalLayout_18.addWidget(self.quit_button)


        self.verticalLayout_14.addWidget(self.frame_2)


        self.horizontalLayout_6.addWidget(self.inventory_2)


        self.horizontalLayout_5.addWidget(self.frame_10)

        self.stackedWidget.addWidget(self.main)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(3)
        self.stackedWidget_2.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(0)


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
        ___qtablewidgetitem = self.normal_level_select.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Level Name", None));
        ___qtablewidgetitem1 = self.normal_level_select.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Completed in Time", None));
        ___qtablewidgetitem2 = self.normal_level_select.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Start Level", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Action", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Primary", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Secondary", None));
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Inventory", None))
        self.range_icon_btn.setText(QCoreApplication.translate("MainWindow", u" Range", None))
        self.range_inv_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.bomb_icon_btn.setText(QCoreApplication.translate("MainWindow", u" Bombs", None))
        self.bomb_inv_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.health_icon_btn.setText(QCoreApplication.translate("MainWindow", u" Health", None))
        self.health_inv_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.timebomb_icon_btn.setText(QCoreApplication.translate("MainWindow", u" T-Bombs", None))
        self.timebomb_inv_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.dynamite_icon_btn.setText(QCoreApplication.translate("MainWindow", u" Dynamite", None))
        self.dynamite_inv_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.damage_icon_btn.setText(QCoreApplication.translate("MainWindow", u" Damage", None))
        self.damage_inv_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.nuke_icon_btn.setText(QCoreApplication.translate("MainWindow", u" Nukes", None))
        self.nuke_inv_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Stats", None))
        self.time_label.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.label_5.setText("")
        self.label_6.setText("")
        self.label_7.setText("")
        self.label_8.setText("")
        self.pause_button.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.quit_button.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
    # retranslateUi

