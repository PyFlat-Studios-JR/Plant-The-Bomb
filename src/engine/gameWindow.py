from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget
from src.engine.world import world
from PySide6.QtGui import QKeyEvent
class gameWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.world = None
    def initworld(self, file):
        self.world = world(file)
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.world:
            self.world.paintEvent(painter)
        painter.end()
    