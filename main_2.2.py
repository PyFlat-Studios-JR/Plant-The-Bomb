from src.gui.Ui_MainWindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow , QApplication, QGraphicsOpacityEffect, QLineEdit
from PySide6.QtCore import Signal
from PySide6.QtGui import QPainter
import sys
from src.accountManager.accounts import userManager
from src.engine.textureLib import textureLib
from src.engine.world import world
ACCOUNT = userManager()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow() #<-- das ist die gui datei, muss importiert werden
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.style_gui()
        self.initKeybinds()
        self.show()
        self.w = None
    def style_gui(self):
        self.setStyleSheet(open("src/gui/style.qss").read())

        self.ui.frame_6.setGraphicsEffect(QGraphicsOpacityEffect(self.ui.frame_6))
        self.ui.frame_6.graphicsEffect().setOpacity(0.8)

        self.ui.frame_7.setGraphicsEffect(QGraphicsOpacityEffect(self.ui.frame_7))
        self.ui.frame_7.graphicsEffect().setOpacity(0.8)

        self.ui.frame_11.setGraphicsEffect(QGraphicsOpacityEffect(self.ui.frame_11))
        self.ui.frame_11.graphicsEffect().setOpacity(0.8)

        self.ui.login_password_toggle.clicked.connect(self.toggle_password_visibility)
    def toggle_password_visibility(self, show):
        self.ui.login_password_entry.setEchoMode(QLineEdit.Normal if show else QLineEdit.Password)
    def temp_action_select_bypass(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.ui.game_widget.initworld("src/maps/debug.ptb")
        self.ui.game_widget.update()
        self.ui.game_widget.parenthook(self)
    def action_generate_recovery(self):
        if ACCOUNT.user_content:
            ACCOUNT.user_content.create_recovery_code()
    def action_registerPage(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def action_loginPage(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def action_registerUser(self):
        user = self.ui.register_username_entry.text()
        pwd = self.ui.register_password_entry.text()
        cpd = self.ui.register_confirm_entry.text()
        if (len(user) < 1):
            print("Username must be at least 1 character long!")
            return
        if (len(pwd) < 1):
            print("Password must be at least 1 character long")
            return
        if (pwd != cpd):
            print("Password missmatch!")
            return
        res = ACCOUNT.createUser(user, pwd)
        match(res):
            case 0:
                print("All OKAY")
            case 1:
                print("Cannot create user: user exists!")
    def action_loginUser(self):
        user = self.ui.login_username_entry.text()
        pwd = self.ui.login_password_entry.text()
        res: int = ACCOUNT.loginUser(user, pwd)
        match (res):
            case 0:
                print("All Okay!")
            case 1:
                print("User does not exist!")
            case 2:
                print("Invalid password!")
            case other:
                print(f"Unknown error code: {res}")

    def initKeybinds(self):
        self.ui.login_register_btn.clicked.connect(self.action_registerPage)
        self.ui.login_btn.clicked.connect(self.action_loginUser)
        self.ui.register_login_btn.clicked.connect(self.action_loginPage)
        self.ui.register_btn.clicked.connect(self.action_registerUser)
        self.ui.login_help_btn.clicked.connect(self.action_generate_recovery)
        self.ui.login_forgot_password_btn.clicked.connect(self.temp_action_select_bypass)
    def keyPressEvent(self, event) -> None:
        self.ui.game_widget.keyPressEvent(event)
    def keyReleaseEvent(self, event) -> None:
        self.ui.game_widget.keyReleaseEvent(event)
a = QApplication()
b = MainWindow()
sys.exit(a.exec())