import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
)


class LevelSelectContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setMinimumWidth(400)
        self.setStyleSheet("border: none")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.hlayout = QHBoxLayout()
        self.widget = QWidget(self)
        self.label1 = QLabel("Levelname", self.widget)
        self.label2 = QLabel("Difficulty", self.widget)
        self.label3 = QLabel("", self.widget)
        self.hlayout.addWidget(self.label1)
        self.hlayout.addWidget(self.label2)
        self.hlayout.addWidget(self.label3)
        self.widget.setLayout(self.hlayout)

        self.scroll_content = QWidget()
        self.scroll_content.setLayout(QVBoxLayout())
        self.scroll_area.setWidget(self.scroll_content)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.layout.addWidget(self.scroll_area)

    def setUI(self, ui):
        self.ui = ui

    def level_start(self, name: str):
        self.ui.game_widget.start_level(name)
        self.ui.stackedWidget.setCurrentIndex(4)
        self.ui.game_widget.update()

    def call_page(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.stackedWidget.update()
        self.levels = self.ui.game_widget.get_all_levels()

        for level in self.levels:
            completed = False
            if self.ui.game_widget.get_completed(level):
                completed = True
            level_start = self.level_start
            self.create_new_level(level, completed, level_start)

    def create_new_level(self, name: str, completed: bool, level_start):
        my_widget = LevelWidget(name, completed, level_start)

        layout = self.scroll_content.layout()
        layout.addWidget(my_widget)


class LevelWidget(QWidget):
    def __init__(self, name: str, completed: bool, level_start):
        super().__init__()

        self.name_label = QLabel(name.split(".ptb")[0])
        self.button = QPushButton("Play")
        self.button.clicked.connect(lambda: level_start(f"src/maps/{name}"))

        layout = QHBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.button)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = LevelSelectContainer()
    my_widget.show()
    sys.exit(app.exec())
