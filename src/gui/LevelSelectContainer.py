from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QTableWidget,
    QPushButton,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt


class LevelSelectContainer(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def setUI(self, ui):
        self.ui = ui
        self.horizontalHeader().setVisible(True)

    def level_start(self, name: str):
        self.ui.game_widget.start_level(name)
        self.ui.stackedWidget.setCurrentIndex(4)
        self.ui.game_widget.update()

    def call_page(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.levels = self.ui.game_widget.get_all_levels()
        self.create_all_levels()

    def create_all_levels(self):
        row_count = self.rowCount()
        for row in range(row_count - 1, -1, -1):
            self.removeRow(row)

        for level in self.levels:
            completed = self.ui.game_widget.api_get_time(f"src/maps/{level}")
            self.create_new_level(level, str(completed))

    def create_new_level(self, *args):
        row_count = self.rowCount()
        column_count = self.columnCount()
        self.insertRow(row_count)
        for column, data in enumerate(args):
            item = QTableWidgetItem(data)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row_count, column, item)

        play_button = QPushButton("Play Level")
        play_button.setFocusPolicy(Qt.NoFocus)
        play_button.setObjectName("play")
        play_button.clicked.connect(lambda: self.level_start(f"src/maps/{args[0]}"))
        self.setCellWidget(row_count, column_count - 1, play_button)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_F5:
            if self.ui.stackedWidget_2.currentIndex() == 1:
                self.call_page()

        return super().keyPressEvent(event)