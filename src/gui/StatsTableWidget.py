from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt


class StatsTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def setUI(self, ui):
        self.ui = ui
        self.horizontalHeader().setVisible(True)

    def create_new_stat(self, *args):
        row_count = self.rowCount()
        self.insertRow(row_count)
        for column, data in enumerate(args):
            item = QTableWidgetItem(data)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row_count, column, item)
