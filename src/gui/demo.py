import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeySequence


class KeyCaptureButton(QPushButton):
    def __init__(self, row, key_type, wid, parent=None):
        super().__init__("Set Key", parent)
        self.row = row
        self.key_type = key_type  # 'primary' or 'secondary'
        self.clicked.connect(self.captureKey)
        self.capturing = False
        self.wid = wid

    def captureKey(self):
        self.setText("Press a key or mouse button...")
        self.capturing = True

    def event(self, event):
        if self.capturing:
            if event.type() == QEvent.KeyPress:
                key_event = event
                key = key_event.key()

                # Prüfen, ob Modifier-Tasten gedrückt sind (außer bei speziellen Tasten wie Shift alleine)
                if (
                    (event.modifiers() & Qt.ShiftModifier and key != Qt.Key_Shift)
                    or (event.modifiers() & Qt.ControlModifier)
                    or (event.modifiers() & Qt.AltModifier)
                    or (event.modifiers() & Qt.MetaModifier)
                ):
                    return True  # Ignoriere Tastenkombinationen mit Modifiern

                self.setText(QKeySequence(key).toString())
                self.wid.updateKeybind(self.row, key, self.key_type)
                self.capturing = False
                return True
            elif event.type() == QEvent.MouseButtonPress:
                mouse_event = event
                button = mouse_event.button()
                buttonText = {
                    Qt.LeftButton: "Left Click",
                    Qt.RightButton: "Right Click",
                    Qt.MiddleButton: "Middle Click",
                }.get(button, f"Button {button}")
                self.setText(buttonText)
                self.wid.updateKeybind(self.row, button, self.key_type)
                self.capturing = False
                return True

        return super().event(event)


class KeybindsWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.keybinds = {}
        self.setFocusPolicy(Qt.NoFocus)

    def initUI(self):
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["Action", "Primary Keybind", "Secondary Keybind"]
        )
        actions = ["Move Forward", "Move Backward", "Jump", "Crouch"]
        self.table.setRowCount(len(actions))

        for i, action in enumerate(actions):
            self.table.setItem(i, 0, QTableWidgetItem(action))

            primary_btn = KeyCaptureButton(i, "primary", self, self.table)
            self.table.setCellWidget(i, 1, primary_btn)

            secondary_btn = KeyCaptureButton(i, "secondary", self, self.table)
            self.table.setCellWidget(i, 2, secondary_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def updateKeybind(self, row, key, key_type):
        action = self.table.item(row, 0).text()
        if key_type == "primary":
            self.keybinds[action] = {"primary": key}
        else:
            if action not in self.keybinds:
                self.keybinds[action] = {}
            self.keybinds[action]["secondary"] = key


def main():
    app = QApplication(sys.argv)
    ex = KeybindsWidget()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
