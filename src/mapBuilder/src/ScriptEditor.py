import src.mapBuilder.src.KEYWORDS, re

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.mapBuilder.src.CustomSyntaxHighlighter import CustomSyntaxHighlighter
from src.mapBuilder.src.CustomTextEdit import CustomTextEdit

class ScriptEditor(QDialog):
    def __init__(self, parent, scripts):
        super().__init__(parent=parent)
        self.connection = None
        self.parent = parent
        self.start_scripts = "" if scripts is None else scripts
        self.setWindowTitle("Script-Editor")
        self.setFixedSize(500, 575)

        layout = QVBoxLayout()

        layout.setMenuBar(self.create_menu())

        self.text_edit = CustomTextEdit(self.get_keywords())
        CustomSyntaxHighlighter(self.text_edit.document())
        self.text_edit.setPlainText(self.start_scripts)
        layout.addWidget(self.text_edit)

        compile_btn = QPushButton("Save")
        compile_btn.setObjectName("script_compile_dialog_btn")
        compile_btn.clicked.connect(self.try_compile)
        layout.addWidget(compile_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.exec()

    def closeEvent(self, event):
        if self.text_edit.toPlainText() == self.start_scripts:
            self.accept()
            self.text = self.start_scripts
            self.set_text()
            return
        message_box = QMessageBox(self.parent)
        message_box.setWindowTitle("Syntax Error")
        message_box.setText("Do you want to save the change you made?")
        message_box.setIcon(QMessageBox.Warning)
        message_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        result = message_box.exec()
        if result == QMessageBox.Save:
            self.try_compile()
            event.accept()
        elif result == QMessageBox.Discard:
            event.accept()
        elif result == QMessageBox.Cancel:
            event.ignore()

    def get_keywords(self):
        ret = []
        for keywordlist in src.mapBuilder.src.KEYWORDS.keywords:
            for keyword in keywordlist["keywords"]:
                ret.append(keyword)
        return ret

    def create_menu(self):
        menu = QMenuBar(self)

        tool_menu = QMenu(menu)
        tool_menu.setTitle("Tools")
        pick_coords_action = QAction(self)
        pick_coords_action.setText("Pick Coordinates")
        pick_coords_action.setShortcut("Ctrl+Shift+C")
        pick_coords_action.triggered.connect(lambda: self.pick_coordinates())
        add_teleporter = QAction(self)
        add_teleporter.setText("Add Teleporter")
        add_teleporter.triggered.connect(lambda: self.start_teleporter_adding())
        tool_menu.addAction(pick_coords_action)
        tool_menu.addAction(add_teleporter)
        menu.addMenu(tool_menu)
        return menu

    def pick_coordinates(self):
        self.setVisible(False)
        self.parent.pick_coords()
        self.parent.coord_signal.connect(self.insert_coords)

    def start_teleporter_adding(self):
        self.setVisible(False)

        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Dropdown Dialog")

        layout = QVBoxLayout(dialog)

        dropdown = QComboBox()
        delegate = AlignDelegate(dropdown)
        dropdown.setItemDelegate(delegate)

        lineedit = QComboBoxButton(dropdown)
        lineedit.setReadOnly(True)
        lineedit.setAlignment(Qt.AlignCenter)
        dropdown.setLineEdit(lineedit)
        dropdown.addItems(["on_step", "on_collect", "on_destroy", "on_explode"])
        layout.addWidget(dropdown)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        res = dialog.exec()
        if res:
            msg_box = QMessageBox(self.parent)
            msg_box.setText("Pick the start coordinate for your teleporter")
            msg_box.addButton(QMessageBox.Ok)
            msg_box.setWindowTitle("")
            msg_box.exec()
            self.trigger_text = dropdown.currentText()
            self.parent.pick_coords()
            self.connection = self.parent.coord_signal.connect(self.save_cor)
        else:
            self.setVisible(True)

    def save_cor(self, x, y):
        self.start = x, y
        msg_box = QMessageBox(self.parent)
        msg_box.setText("Pick the target coordinate for your teleporter")
        msg_box.addButton(QMessageBox.Ok)
        msg_box.setWindowTitle("")
        msg_box.exec()
        self.parent.pick_coords()
        self.parent.coord_signal.disconnect(self.connection)
        self.connection = self.parent.coord_signal.connect(self.finish)

    def finish(self, x, y):
        start_x = self.start[0]
        start_y = self.start[1]
        end_x = x
        end_y = y
        command = f"@ {self.trigger_text} on {start_x} {start_y}\nset 0 = {end_x}\nset 1 = {end_y}\ntp to 0 1\nend"
        complete_text = self.text_edit.toPlainText()
        complete_text += "" if complete_text.endswith("\n") or complete_text == "" else "\n"
        self.text_edit.setPlainText(complete_text+command)
        self.setVisible(True)
        self.parent.coord_signal.disconnect(self.connection)


    def insert_coords(self, x, y):
        self.show()
        cursor = self.text_edit.textCursor()
        cursor.insertText(f"{x} {y}")
        self.parent.coord_signal.disconnect()

    def check_for_syntax_errors(self, script):
        lines = script.split("\n")
        errors = []
        for i, line in enumerate(lines):
            ok = False
            for rule in src.mapBuilder.src.RULES.COMMANDS:
                if re.match(rule, line):
                    ok = True
                    break
            if not ok:
                errors.append(i)
        return errors

    def try_compile(self):
        complete_text = self.text_edit.toPlainText()
        errors = self.check_for_syntax_errors(complete_text)
        if errors != [] and complete_text != "":
            message_box = QMessageBox(self.parent)
            message_box.setWindowTitle("Syntax Error")
            error_lines = '\n'.join([f"Line: {error+1}" for error in errors])
            error_message = f"Syntax Error:\n{error_lines}"
            message_box.setText(error_message)
            message_box.setIcon(QMessageBox.Information)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
            return
        self.text = complete_text
        self.set_text()
        self.accept()

    def set_text(self):
        self.parent.set_script_text(self.text)

class QComboBoxButton(QLineEdit):
    def mousePressEvent(self, e):
        combo = self.parent()
        if isinstance(combo, QComboBox):
            combo.showPopup()

class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter