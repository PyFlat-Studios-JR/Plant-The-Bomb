from PySide6.QtGui import QKeyEvent
from src.gui.Ui_MainWindow import Ui_MainWindow
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QGraphicsOpacityEffect,
    QLineEdit,
    QWidget,
    QPushButton,
    QMessageBox
)
from PySide6.QtCore import Qt
import sys
from src.accountManager.accounts import getAccountContext
import src.engine.textureLib as textureLib
from src.gui.GlobalEventFilter import GlobalEventFilter
from src.gui.Dialogs import BasicDialog
import src.accountManager.statregister as stats
from src.mapBuilder import main

ACCOUNT = getAccountContext()

def setFocusPolicyRecursive(widget, focusPolicy):
    if isinstance(widget, QPushButton):
        widget.setFocusPolicy(focusPolicy)
    for child in widget.findChildren(QWidget):
        setFocusPolicyRecursive(child, focusPolicy)


class MainWindow(QMainWindow):
    def __init__(self, globalEventFilter:GlobalEventFilter):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.map_builder = main.MainWindow(mw=self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.tabWidget.setCurrentIndex(0)
        self.eventFilter = globalEventFilter
        self.eventFilter.keypress.connect(self.keyPressEvent)
        self.eventFilter.keypress.connect(self.ui.game_widget.keyPressEvent)
        self.eventFilter.keyrelease.connect(self.ui.game_widget.keyReleaseEvent)
        self.bindLevelButtons()
        self.ui.normal_level_select.setUI(self.ui)
        self.ui.normal_level_select_2.setUI(self.ui)
        self.ui.tableWidget.setupKeyBinds(globalEventFilter.eventhappend)
        self.ui.game_widget.parenthook(self)
        self.ui.login_btn.setShortcut("Return")
        self.style_gui()
        self.initKeybinds()
        self.show()
        self.w = None

        setFocusPolicyRecursive(self, Qt.NoFocus)
        self.ui.stackedWidget.setCurrentIndex(5)

    def bindLevelButtons(self):
        self.ui.pushButton.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentIndex(change_page(False))
        )
        self.ui.pushButton_2.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentIndex(change_page(True))
        )
        self.ui.pushButton.setShortcut("Left")
        self.ui.pushButton_2.setShortcut("Right")

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
            BasicDialog(self, "Register Error", "Username must be at least 1 character long!", QMessageBox.Critical)
            return
        if len(pwd) < 1:
            BasicDialog(self, "Register Error", "Password must be at least 1 character long!", QMessageBox.Critical)
            return
        if pwd != cpd:
            BasicDialog(self, "Register Error", "Passwords don't match!", QMessageBox.Critical)
            return
        res = ACCOUNT.createUser(user, pwd)
        match (res):
            case 0:
                BasicDialog(self, "Successfully registered", "Successfully created account", QMessageBox.Information)
                ACCOUNT.loginUser(user, pwd)
                self.ui.normal_level_select.call_page()
            case 1:
                BasicDialog(self, "Register Warning", "Warning: Account already exists", QMessageBox.Warning)

    def action_loginUser(self):
        user = self.ui.login_username_entry.text()
        pwd = self.ui.login_password_entry.text()
        if user == pwd == "":
            self.ui.normal_level_select.call_page()
            return
        res: int = ACCOUNT.loginUser(user, pwd)
        match (res):
            case 0:
                print("Succesfully logged in")
                self.ui.login_username_entry.clear()
                self.ui.login_password_entry.clear()
            case 1:
                BasicDialog(self, "Login Error", "User does not exist!", QMessageBox.Critical)
                return
            case 2:
                BasicDialog(self, "Login Error", "Invalid password", QMessageBox.Critical)
                return
            case other:
                BasicDialog(self, "Login Error", f"Unknown error! Error-Code: {res}", QMessageBox.Critical)
                return

        self.ui.normal_level_select.call_page()

    def action_logoutUser(self):
        ACCOUNT.saveData()
        ACCOUNT.user_content = None
        stats.getStatContext().__init__()
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.stackedWidget.setCurrentIndex(0)


    def initKeybinds(self):
        self.ui.login_register_btn.clicked.connect(self.action_registerPage)
        self.ui.login_btn.clicked.connect(self.action_loginUser)
        self.ui.register_login_btn.clicked.connect(self.action_loginPage)
        self.ui.register_btn.clicked.connect(self.action_registerUser)
        self.ui.login_help_btn.clicked.connect(self.action_generate_recovery)
        self.ui.login_forgot_password_btn.clicked.connect(
            self.temp_action_select_bypass
        )
        self.ui.save_keybinds_btn.clicked.connect(self.ui.tableWidget.saveKeybinds)
        self.ui.reset_keybinds_btn.clicked.connect(self.ui.tableWidget.resetKeybinds)

        self.ui.stackedWidget_2.currentChanged.connect(self.page_changed)
        self.ui.logout_button.clicked.connect(self.action_logoutUser)

    def page_changed(self, index):
        if index == 0:
            self.ui.normal_level_select.call_page()
        elif index == 1:
            self.ui.normal_level_select_2.call_page()
        elif index == 2:
            self.ui.tableWidget.setupKeyBinds(self.eventFilter.eventhappend)

    def keyPressEvent(self, event) -> None:
        self.ui.normal_level_select.keyPressEvent(event)
        self.ui.normal_level_select_2.keyPressEvent(event)



a = QApplication()
a.aboutToQuit.connect(ACCOUNT.saveData)
globalEventFilter = GlobalEventFilter()
a.installEventFilter(globalEventFilter)
textureLib.textureLib.loadFolder("src/textures/", "ERR_IMAGE.png")
b = MainWindow(globalEventFilter)

sys.exit(a.exec())
