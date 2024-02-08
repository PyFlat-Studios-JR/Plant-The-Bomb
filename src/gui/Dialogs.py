from PySide6.QtWidgets import QDialog, QLabel, QMessageBox, QVBoxLayout
from PySide6.QtCore import QTimer
class KeybindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel("Please press the new keybind.", self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle("Keybind Instruction")

class BasicDialog(QMessageBox):
    def __init__(self, parent=None, title:str="", message:str="", icon:int=QMessageBox.Information, fadeout:int=None):
        super().__init__(parent=parent)
        if fadeout:
            self.timer = QTimer()
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.close)
            self.timer.start(fadeout)
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(icon)
        self.exec()

