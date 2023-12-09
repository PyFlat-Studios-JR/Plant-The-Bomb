import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea

class LevelSelectContainer(QWidget):
    def __init__(self,parent=None):
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
        self.scroll_area.setWidget(self.scroll_content)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.layout.addWidget(self.scroll_area)

        self.my_widgets = []
        self.create_widgets()

    def create_widgets(self):
        for _ in range(10):
            my_widget = LevelWidget()
            self.my_widgets.append(my_widget)
            self.add_my_widget(my_widget)

    def add_my_widget(self, my_widget):
        if not self.scroll_content.layout():
            self.scroll_content.setLayout(QVBoxLayout())

        layout = self.scroll_content.layout()
        layout.addWidget(my_widget)

class LevelWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.name_label = QLabel("Level name")
        self.button = QPushButton("Play Level")
        self.stars_widget = StarsWidget()

        layout = QHBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.stars_widget)
        layout.addWidget(self.button)


        self.setLayout(layout)

class StarsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.stars_display = QLabel()
        self.stars_display.setStyleSheet("font-size: 20px;color:yellow")

        layout = QVBoxLayout()
        layout.addWidget(self.stars_display)

        self.setLayout(layout)

        self.set_stars(3)

    def set_stars(self, num_stars):
        stars_text = "★" * num_stars + "☆" * (5 - num_stars)
        self.stars_display.setText(stars_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = LevelSelectContainer()
    my_widget.show()
    sys.exit(app.exec())
