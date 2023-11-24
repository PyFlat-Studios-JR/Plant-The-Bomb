from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget
from src.engine.world import world
from PySide6.QtGui import QKeyEvent
class gameWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.world = None
        self.keys_held = []
    def initworld(self, file):
        self.world = world(self, file)
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