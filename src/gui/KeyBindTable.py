from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeySequence

from src.gui.Dialogs import KeybindDialog
import src.accountManager.keybinds as keys

class KeyBindTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.keys = keys.getKeybindManager()
        self.setFocusPolicy(Qt.NoFocus)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cellDoubleClicked.connect(self.handleCellClicked)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.keybinds = {}
        self.capturing = False

    def setupKeyBinds(self, eventHappened):
        actions = self.keys.get_data()
        self.actions = actions
        self.setRowCount(len(self.actions))
        eventHappened.connect(self.handleEvent)
        for i, action in enumerate(self.actions):
            item1 = QTableWidgetItem(action)
            item1.setTextAlignment(Qt.AlignCenter)
            self.setItem(i, 0, item1)
            keybinds = self.keys.get(action)
            for j in range(1, 3):
                self.keybinds.setdefault(action, {})["primary" if j == 1 else "secondary"] = keybinds[j-1]
                item = QTableWidgetItem(self.getKeyById(keybinds[j-1]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, j, item)

    def saveKeybinds(self, *args):
        for action, keys in self.keybinds.items():
            newBinds = [0]*2
            for key_type, value in keys.items():
                if key_type == "primary":
                    newBinds[0] = value
                else:
                    newBinds[1] = value
            self.keys.set(action, newBinds)

    def handleCellClicked(self, row, column):
        if column == 0: return
        self.capturing = True
        self.row = row
        self.column = column
        self.dialog = KeybindDialog(self.parent())
        self.dialog.rejected.connect(self.stopCapture)
        self.dialog.exec()

    def stopCapture(self):
        self.capturing = False

    def updateKeybind(self, row, column, key, text, operation):
        action = self.item(row, 0).text()
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)

        if operation == "add":
            self.setItem(row, column, item)
            key_type = "primary" if column == 1 else "secondary"
            self.keybinds.setdefault(action, {})[key_type] = key
        elif operation == "delete":
            if action in self.keybinds:
                key_type = "primary" if column == 1 else "secondary"
                self.keybinds[action].pop(key_type, None)
                self.setItem(row, column, QTableWidgetItem(""))

                if not self.keybinds[action]:
                    del self.keybinds[action]

    def checkIfExisting(self, key):
        for action, keys in self.keybinds.items():
            for key_type, value in keys.items():
                if value == key:
                    row = self.actions.index(action)
                    column = 1 if key_type == "primary" else 2
                    return (True, row, column, action)

        return False

    def getKeyById(self, key:int):
        key_text = QKeySequence(key).toString()
        return key_text

    def handleEvent(self, event: QEvent):
        if not self.capturing:
            return False

        new_key_text = ""
        key = None
        event_type = event.type()

        if event_type == QEvent.KeyPress:
            key_event = event
            key = key_event.key()
            if key == Qt.Key_Escape:
                self.capturing = False
                return True
            modifiers = event.modifiers()
            non_modifier_keys = [Qt.Key_Shift, Qt.Key_Control, Qt.Key_Alt, Qt.Key_Meta]
            if modifiers == (Qt.AltModifier | Qt.ControlModifier):
                return True

            if modifiers & ~Qt.NoModifier and key not in non_modifier_keys:
                return True
            new_key_text = QKeySequence(key).toString()

        elif event_type == QEvent.MouseButtonPress:
            button = event.button()
            key = button
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

        alreadyExisting = self.checkIfExisting(key)

        if new_key_text and key and self.column > 0:
            self.capturing = False
            if alreadyExisting:
                self.dialog.accept()
                if self.row == alreadyExisting[1] and self.column == alreadyExisting[2]:
                    return False
                msg = QMessageBox(self.parent())
                msg.setWindowTitle("Overwrite Keybind")
                msg.setText(f"The key '{new_key_text}' is already assigned to '{alreadyExisting[3]}'.")
                msg.setInformativeText("Do you want to overwrite it?")
                msg.addButton(QMessageBox.Yes)
                msg.addButton(QMessageBox.No)
                result = msg.exec()
                if result == QMessageBox.No:
                    return False
                else:
                    self.updateKeybind(alreadyExisting[1], alreadyExisting[2], None, None, "delete")

            self.updateKeybind(self.row, self.column, key, new_key_text, "add")
            self.dialog.accept()

        return False


