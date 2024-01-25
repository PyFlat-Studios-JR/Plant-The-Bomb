import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt, QEvent, QObject, Signal
from PySide6.QtGui import QKeySequence


class GlobalEventFilter(QObject):
    eventhappend = Signal(QObject)

    def eventFilter(self, obj, event):
        self.eventhappend.emit(event)
        return super(GlobalEventFilter, self).eventFilter(obj, event)


class KeybindsWidget(QMainWindow):
    def __init__(self, eventhappend: Signal):
        super().__init__()
        self.initUI()
        self.keybinds = {}
        self.setFocusPolicy(Qt.NoFocus)
        eventhappend.connect(self.handleEvent)
        self.capturing = False

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

        if new_key_text and key:
            self.table.setItem(self.row, self.column, QTableWidgetItem(new_key_text))
            self.updateKeybind(self.row, self.column, key)
            self.capturing = False

        return False

    def handleCellClicked(self, row, column):
        self.capturing = True
        self.row = row
        self.column = column

    def initUI(self):
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.handleCellClicked)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["Action", "Primary Keybind", "Secondary Keybind"]
        )
        actions = ["Move Forward", "Move Backward", "Jump", "Crouch"]
        self.table.setRowCount(len(actions))

        for i, action in enumerate(actions):
            self.table.setItem(i, 0, QTableWidgetItem(action))
            self.table.setItem(i, 1, QTableWidgetItem("test"))
            self.table.setItem(i, 2, QTableWidgetItem("testi"))

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def updateKeybind(self, row, column, key):
        action = self.table.item(row, 0).text()
        if column == 1:
            self.keybinds[action] = {"primary": key}
        elif column == 2:
            if action not in self.keybinds:
                self.keybinds[action] = {}
            self.keybinds[action]["secondary"] = key

        print(self.keybinds)


def main():
    app = QApplication(sys.argv)
    eventfilter = GlobalEventFilter()
    app.installEventFilter(eventfilter)
    ex = KeybindsWidget(eventfilter.eventhappend)
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
