from PySide6.QtGui import QKeyEvent, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QTreeView,
    QHeaderView,
    QItemDelegate
)
from PySide6.QtCore import Qt, QSize

import src.accountManager.statregister as stats

trivial_names = {
    "bombs_placed": "Bombs Placed",
    "dynamite_placed": "Dynamite Placed",
    "nukes_placed": "Nukes Placed",
    "timebombs_placed": "Timebombs Placed",
    "bombs_placed_total": "Total Bombs Placed",
    "damage_dealt": "Damage Dealt",
    "damage_received": "Damage Received",
    "enemies_killed": "Enemies Killed",
    "blocks_exploded": "Blocks Exploded",
    "blocks_walked": "Blocks Walked",
    "items_collected_total": "Total Items Collected",
    "items_collected_damage": "Items Collected - Damage",
    "items_collected_health": "Items Collected - Health",
    "items_collected_bombs": "Items Collected - Bombs",
    "items_collected_dynamite": "Items Collected - Dynamite",
    "items_collected_timebombs": "Items Collected - Timebombs",
    "items_collected_nukes": "Items Collected - Nukes",
    "items_collected_shields": "Items Collected - Shields",
    "items_collected_curses": "Items Collected - Curses",
    "items_collected_range": "Items Collected - Range",
    "times_spent_total": "Total Time Spent",
    "levels_completed_total": "Total Levels Completed",
    "levels_played_total": "Total Levels Played",
    "time_spent_levels_total": "Total Time Spent on Levels",
    "levels_completed": "Levels Completed:",
    "levels_played": "Levels Played:",
    "time_spent_levels": "Time Spent on Levels:",
}


class StatsTableWidget(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Stat", "Value"])
        self.header().setDefaultAlignment(Qt.AlignCenter)
        self.header().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalScrollBar().setVisible(False)

    def setUI(self, ui):
        self.ui = ui

    def call_page(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Stat", "Value"])

        self.stats = stats.getStatContext()

        for stat, data in self.stats.data.items():
            if stat in trivial_names:
                if trivial_names[stat][-1] != ":":
                    self.add_item(None, trivial_names[stat], str(data))
                else:
                    parent_item = self.add_item(None, trivial_names[stat], "")
                    for level_data in data.values():
                        name = level_data["name"].split("/")[-1]
                        self.add_item(parent_item, name, str(level_data["amount"]))

    def add_item(self, parent, name, value):
        if parent is None:
            parent = self.model.invisibleRootItem()
        item = QStandardItem(name)
        value_item = QStandardItem(value)
        value_item.setTextAlignment(Qt.AlignCenter)
        parent.appendRow([item, value_item])
        return item

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_F5:
            if self.ui.stackedWidget_2.currentIndex() == 0:
                self.call_page()

        return super().keyPressEvent(event)
