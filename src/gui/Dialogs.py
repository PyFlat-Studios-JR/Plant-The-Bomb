from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

class KeybindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel("Please press the new keybind.", self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle("Keybind Instruction")