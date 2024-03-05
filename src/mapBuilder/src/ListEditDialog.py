
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QListWidget, QPushButton
from src.mapBuilder.src.TextEditDialog import TextEditDialog

class ListEditDialog(QDialog):
    def __init__(self, parent, texts):
        super().__init__(parent)
        self.setObjectName("text_edit_dialog")
        self.setWindowTitle("Edit Texts")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("Enter a new text")
        self.layout.addWidget(self.entry)
        self.entry.returnPressed.connect(self.add_item)

        self.listbox = QListWidget(self)
        self.listbox.setObjectName("text_edit")
        self.layout.addWidget(self.listbox)
        self.listbox.itemDoubleClicked.connect(self.edit_item)

        self.move_up_button = QPushButton("Move Up", self)
        self.move_up_button.clicked.connect(self.move_item_up)
        self.layout.addWidget(self.move_up_button)

        self.move_down_button = QPushButton("Move Down", self)
        self.move_down_button.clicked.connect(self.move_item_down)
        self.layout.addWidget(self.move_down_button)

        self.delete_button = QPushButton("Delete Text", self)
        self.delete_button.clicked.connect(self.delete_item)
        self.layout.addWidget(self.delete_button)

        self.items = []

        if texts is not None:
            for text in texts:
                self.add_item(text)

    def add_item(self, text=None):
        text = self.entry.text() if text is None else text
        if text:
            self.listbox.addItem(text)
            self.items.append(text)
            self.entry.clear()

    def edit_item(self, item):
        current_text = item.text()
        index = self.listbox.row(item)

        dialog = TextEditDialog(self)
        dialog.set_item_text(current_text)

        if dialog.exec_() == QDialog.Accepted:
            new_text = dialog.item_text
            self.listbox.takeItem(index)
            self.listbox.insertItem(index, new_text)
            self.items[index] = new_text

    def move_item_up(self):
        selected_item = self.listbox.currentItem()
        if selected_item:
            index = self.listbox.row(selected_item)
            if index > 0:
                self.listbox.takeItem(index)
                self.listbox.insertItem(index - 1, selected_item.text())
                self.items[index], self.items[index - 1] = self.items[index - 1], self.items[index]

    def move_item_down(self):
        selected_item = self.listbox.currentItem()
        if selected_item:
            index = self.listbox.row(selected_item)
            if index < self.listbox.count() - 1:
                self.listbox.takeItem(index)
                self.listbox.insertItem(index + 1, selected_item.text())
                self.items[index], self.items[index + 1] = self.items[index + 1], self.items[index]

    def delete_item(self):
        selected_item = self.listbox.currentItem()
        if selected_item:
            index = self.listbox.row(selected_item)
            self.listbox.takeItem(index)
            del self.items[index]

    def get_texts(self):
        item_texts = []
        for index in range(self.listbox.count()):
            item = self.listbox.item(index)
            item_texts.append(item.text())
        #result = "\n".join(item_texts)
        return item_texts