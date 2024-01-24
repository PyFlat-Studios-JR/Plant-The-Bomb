from src.gui.Ui_MainWindow import Ui_MainWindow
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QGraphicsOpacityEffect,
    QLineEdit,
    QWidget,
    QPushButton,
)
from PySide6.QtCore import Qt, QObject, QEvent
import sys
from src.accountManager.accounts import getAccountContext
import src.engine.textureLib as textureLib

ACCOUNT = getAccountContext()


class GlobalEventFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            pass
        return super(GlobalEventFilter, self).eventFilter(obj, event)


def setFocusPolicyRecursive(widget, focusPolicy):
    if isinstance(widget, QPushButton):
        widget.setFocusPolicy(focusPolicy)
    for child in widget.findChildren(QWidget):
        setFocusPolicyRecursive(child, focusPolicy)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget_2.setCurrentIndex(1)
        self.bindLevelButtons()
        self.ui.normal_level_select.setUI(self.ui)
        self.ui.normal_level_select_2.setUI(self.ui)
        self.ui.game_widget.parenthook(self)
        self.style_gui()
        self.initKeybinds()
        self.show()
        self.w = None

        setFocusPolicyRecursive(self, Qt.NoFocus)

    def bindLevelButtons(self):
        self.ui.pushButton.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentIndex(change_page(False))
        )
        self.ui.pushButton_2.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentIndex(change_page(True))
        )

        def change_page(dir: bool):
            cur_page = self.ui.stackedWidget_2.currentIndex()
            if not dir and cur_page == 0:
                result = self.ui.stackedWidget_2.count() - 1
            elif dir and cur_page == self.ui.stackedWidget_2.count() - 1:
                result = 0
            else:
                if dir:
                    result = cur_page + 1
                else:
                    result = cur_page - 1
            return result

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
        self.ui.login_password_entry.setEchoMode(
            QLineEdit.Normal if show else QLineEdit.Password
        )

    def temp_action_select_bypass(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.ui.game_widget.initworld("src/maps/debug.ptb")
        self.ui.game_widget.update()

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
        if len(user) < 1:
            print("Username must be at least 1 character long!")
            return
        if len(pwd) < 1:
            print("Password must be at least 1 character long")
            return
        if pwd != cpd:
            print("Password missmatch!")
            return
        res = ACCOUNT.createUser(user, pwd)
        match (res):
            case 0:
                print("All OKAY")
            case 1:
                print("Cannot create user: user exists!")

    def action_loginUser(self):
        user = self.ui.login_username_entry.text()
        pwd = self.ui.login_password_entry.text()
        if user == pwd == "":
            self.ui.normal_level_select.call_page()
            return
        res: int = ACCOUNT.loginUser(user, pwd)
        match (res):
            case 0:
                print("All Okay!")
            case 1:
                print("User does not exist!")
                return
            case 2:
                print("Invalid password!")
                return
            case other:
                print(f"Unknown error code: {res}")
                return

        self.ui.normal_level_select.call_page()

    def initKeybinds(self):
        self.ui.login_register_btn.clicked.connect(self.action_registerPage)
        self.ui.login_btn.clicked.connect(self.action_loginUser)
        self.ui.register_login_btn.clicked.connect(self.action_loginPage)
        self.ui.register_btn.clicked.connect(self.action_registerUser)
        self.ui.login_help_btn.clicked.connect(self.action_generate_recovery)
        self.ui.login_forgot_password_btn.clicked.connect(
            self.temp_action_select_bypass
        )

        self.ui.stackedWidget_2.currentChanged.connect(self.page_changed)

    def page_changed(self, index):
        if index == 0:
            self.ui.normal_level_select_2.call_page()
        elif index == 1:
            self.ui.normal_level_select.call_page()

    def keyPressEvent(self, event) -> None:
        self.ui.normal_level_select.keyPressEvent(event)
        self.ui.normal_level_select_2.keyPressEvent(event)
        self.ui.game_widget.keyPressEvent(event)

    def keyReleaseEvent(self, event) -> None:
        self.ui.game_widget.keyReleaseEvent(event)


a = QApplication()
globalEventFilter = GlobalEventFilter()
a.installEventFilter(globalEventFilter)
textureLib.textureLib.loadFolder("src/textures/", "ERR_IMAGE.png")
b = MainWindow()
sys.exit(a.exec())
