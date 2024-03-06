from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QObject

class ResultScreen(QObject):
    def __init__(self, parent=None, loose: bool=True, restart: callable=None, main:callable=None):
        super().__init__(parent)
        self.win = parent
        self.restart = restart
        self.main = main
        self.text = "Game Over!" if loose else "GG, You Win!"
        self.color = "red" if loose else "green"
        self.widget = QWidget(parent)
        self.widget.setObjectName("no_obj")# Create a QWidget to hold the layout
        self.widget.setStyleSheet("QWidget#no_obj{background-color: none;}")
        self.widget.setLayout(self.create_layout())
    def create_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignVCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        time_text = self.win.pr.ui.time_label.text().split()[1]

        label = QLabel(self.text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"font-size: 40px; color: {self.color}; font-weight: bold; padding: 10px 0;")

        time_label = QLabel(f"Time: {time_text}")
        time_label.setAlignment(Qt.AlignCenter)
        time_label.setStyleSheet("font-size: 24px; color: white;")

        main_layout.addWidget(label)
        main_layout.addSpacing(10)
        main_layout.addWidget(time_label)
        main_layout.addSpacing(50)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(24)

        restart_button = QPushButton("Restart")
        restart_button.setStyleSheet("font-size: 30px; padding: 8px 16px; border-radius: 8px; margin-left: 15px;")
        restart_button.clicked.connect(self.on_button_clicked)
        button_layout.addWidget(restart_button)

        main_menu_button = QPushButton("Main Menu")
        main_menu_button.setStyleSheet("font-size: 30px; padding: 8px 16px; border-radius: 8px; margin-right: 15px;")
        main_menu_button.clicked.connect(self.on_button_clicked)
        button_layout.addWidget(main_menu_button)

        main_layout.addLayout(button_layout)
        return main_layout

    def on_button_clicked(self):
        sender_button = self.sender()
        if sender_button.text() == "Restart":
            self.restart()
        elif sender_button.text() == "Main Menu":
            self.main()
            self.win.world = None
        self.win.pr.ui.quit_button.setEnabled(True)
        self.win.pr.ui.pause_button.setEnabled(True)
        self.widget.deleteLater()

