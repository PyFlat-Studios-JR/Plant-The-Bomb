from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt

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
    "levels_completed": "Level Completed: ",
    "levels_played": "Level Played: ",
    "time_spent_levels": "Time Spent on Level: ",
}


class StatsTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def setUI(self, ui):
        self.ui = ui
        self.horizontalHeader().setVisible(True)

    def call_page(self):
        for row in range(self.rowCount() - 1, -1, -1):
            self.removeRow(row)

        self.stats = stats.getStatContext()
        for stat, data in self.stats.data.items():
            if stat in trivial_names and trivial_names[stat][-1] != " ":
                self.create_new_stat(trivial_names[stat], str(data))
            else:
                for level_data in data.values():
                    name = trivial_names[stat] + level_data["name"].split("/")[-1]
                    self.create_new_stat(name, str(level_data["amount"]))

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
