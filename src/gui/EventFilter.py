import sys
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QKeyEvent


class EventFilter(QObject):
    def __init__(self, page_index, stackedWidget, function=None):
        super().__init__()
        self.page_index = page_index
        self.stackedWidget = stackedWidget
        self.function = function

    def setUI(self, ui):
        self.ui = ui

    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_F5:
            if self.stackedWidget.currentIndex() == self.page_index:
                if self.function:
                    self.function()
                return True

        return super().eventFilter(obj, event)
