from src.gui.Ui_MainWindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow , QApplication
from PySide6.QtCore import SIGNAL
import sys
from src.accountManager.accounts import userManager

ACCOUNT = userManager()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow() #<-- das ist die gui datei, muss importiert werden
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.initKeybinds()
        self.show()
    def action_registerUser(self):
        user = self.ui.login_username_entry.text()
        pwd = self.ui.login_password_entry.text()
        if (len(user) < 1):
            print("Username must be at least 1 character long!")
            return
        if (len(pwd) < 1):
            print("Password must be at least 1 character long")
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
        self.ui.login_register_btn.clicked.connect(self.action_registerUser)
        self.ui.login_btn.clicked.connect(self.action_loginUser)
a = QApplication()
b = MainWindow()
sys.exit(a.exec())