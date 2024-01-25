from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeySequence
from src.gui.GlobalEventFilter import GlobalEventFilter


class KeyBindTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cellClicked.connect(self.handleCellClicked)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.keybinds = {}
        self.capturing = False

    def setupKeyBinds(self, actions, eventHappend):
        self.actions = actions
        self.setRowCount(len(self.actions))
        eventHappend.connect(self.handleEvent)
        for i, action in enumerate(self.actions):
            item1 = QTableWidgetItem(action)
            item1.setTextAlignment(Qt.AlignCenter)
            item2 = QTableWidgetItem("")
            item2.setTextAlignment(Qt.AlignCenter)
            item3 = QTableWidgetItem("")
            item3.setTextAlignment(Qt.AlignCenter)
            self.setItem(i, 0, item1)
            self.setItem(i, 1, item2)
            self.setItem(i, 2, item3)

    def handleCellClicked(self, row, column):
        self.capturing = True
        self.row = row
        self.column = column

    def updateKeybind(self, row, column, key):
        action = self.item(row, 0).text()
        if column == 1:
            self.keybinds[action] = {"primary": key}
        elif column == 2:
            if action not in self.keybinds:
                self.keybinds[action] = {}
            self.keybinds[action]["secondary"] = key

        print(self.keybinds)

    def handleEvent(self, event: QEvent):
        if not self.capturing:
            return False

        new_key_text = ""
        key = None
        event_type = event.type()

        if event_type == QEvent.KeyPress:
            key_event = event
            key = key_event.key()
            modifiers = event.modifiers()
            non_modifier_keys = [Qt.Key_Shift, Qt.Key_Control, Qt.Key_Alt, Qt.Key_Meta]

            if modifiers & ~Qt.NoModifier and key not in non_modifier_keys:
                return True
            new_key_text = QKeySequence(key).toString()

        elif event_type == QEvent.MouseButtonPress:
            button = event.button()
            key = button.value
            buttonText = {
                Qt.LeftButton: "Left Click",
                Qt.RightButton: "Right Click",
                Qt.MiddleButton: "Middle Click",
                Qt.XButton1: "Mouse Button 1",
                Qt.XButton2: "Mouse Button 2",
            }
            new_key_text = buttonText.get(button, f"Button {button}")

        elif event_type == QEvent.Wheel:
            new_key_text = "Mouse Wheel"
            key = 31

        if new_key_text and key and self.column > 0:
            item = QTableWidgetItem(new_key_text)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(self.row, self.column, item)
            self.updateKeybind(self.row, self.column, key)
            self.capturing = False

        return False
