import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeySequence
from GlobalEventFilter import GlobalEventFilter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setFocusPolicy(Qt.NoFocus)

    def initUI(self):
        self.table = KeyBindTable(None, eventfilter.eventhappend)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)


class KeyBindTable(QTableWidget):
    def __init__(self, actions, eventhappend):
        super().__init__()
        eventhappend.connect(self.handleEvent)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cellClicked.connect(self.handleCellClicked)
        self.setColumnCount(3)
        self.verticalHeader().setVisible(True)
        self.keybinds = {}
        self.setHorizontalHeaderLabels(
            ["Action", "Primary Keybind", "Secondary Keybind"]
        )
        self.actions = ["Move Forward", "Move Backward", "Jump", "Crouch"]
        self.setRowCount(len(self.actions))
        self.capturing = False

        for i, action in enumerate(self.actions):
            self.setItem(i, 0, QTableWidgetItem(action))
            self.setItem(i, 1, QTableWidgetItem(""))
            self.setItem(i, 2, QTableWidgetItem(""))

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

        if new_key_text and key:
            self.setItem(self.row, self.column, QTableWidgetItem(new_key_text))
            self.updateKeybind(self.row, self.column, key)
            self.capturing = False

        return False


def main():
    app = QApplication(sys.argv)
    global eventfilter
    eventfilter = GlobalEventFilter()
    app.installEventFilter(eventfilter)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
