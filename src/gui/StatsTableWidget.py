from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt

import src.accountManager.statregister as stats


class StatsTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def setUI(self, ui):
        self.ui = ui
        self.horizontalHeader().setVisible(True)

    def call_page(self):
        row_count = self.rowCount()
        for row in range(row_count - 1, -1, -1):
            self.removeRow(row)

        self.stats = stats.getStatContext()
        for stat in self.stats.data:
            self.create_new_stat(stat, str(self.stats.data[stat]))

    def create_new_stat(self, *args):
        row_count = self.rowCount()
        self.insertRow(row_count)
        for column, data in enumerate(args):
            item = QTableWidgetItem(data)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row_count, column, item)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_F5:
            if self.ui.stackedWidget_2.currentIndex() == 0:
                self.call_page()

        return super().keyPressEvent(event)