from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton

class TextEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Item")
        self.layout = QVBoxLayout()
        
        self.edit_entry = QLineEdit(self)
        self.layout.addWidget(self.edit_entry)
        
        self.save_button = QPushButton("Save", self)
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_clicked)
        
        self.setLayout(self.layout)
        
        self.item_text = ""
        
    def set_item_text(self, text):
        self.item_text = text
        self.edit_entry.setText(text)
        
    def save_clicked(self):
        self.item_text = self.edit_entry.text()
        self.accept()
