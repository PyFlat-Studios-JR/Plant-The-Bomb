from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget
from src.engine.world import world
from PySide6.QtGui import QKeyEvent
import os, re
import src.accountManager.accounts as accounts
ACCOUNTS = accounts.getAccountContext()
class gameWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.world = None
        self.keys_held = []
        self.pr = None
    def initworld(self, file):
        self.world = world(self, file)
        self.update()
    def get_all_levels(self, mappack=None) -> list[str]: #mappack is NOT USED!
        files = os.listdir("src/maps/")
        ffiles = []
        for file in files:
            if re.match(r"^[a-zA-Z0-9_-\() ]+.ptb$",file):
                ffiles.append(file)
        return ffiles
    def start_level(self, level: str) -> None:
        self.world = world(self, level)
    def get_completed(self, level: str) -> bool:
        if ACCOUNTS.user_content == None:
            return False
        return ACCOUNTS.user_content.is_level_completed(f"src/maps/{level}")
    def parenthook(self, prnt):
        self.pr = prnt
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.world:
            self.world.paintEvent(painter)
        painter.end()
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() not in self.keys_held:
            self.keys_held.append(event.key())
    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() in self.keys_held:
            self.keys_held.remove(event.key())