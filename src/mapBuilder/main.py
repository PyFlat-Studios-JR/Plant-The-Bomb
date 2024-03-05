import sys, pathlib, os
import copy

from PySide6.QtGui import QMouseEvent
sys.dont_write_bytecode = True

from src.mapBuilder.src.MainWindow import Ui_MainWindow

from src.mapBuilder.src.PtbLoad import PtbLoader
from src.mapBuilder.src.compiler import *
from src.mapBuilder.src.compressor import *
from src.mapBuilder.src.ListEditDialog import ListEditDialog
from src.mapBuilder.src.block import Block
from src.mapBuilder.src.ScriptEditor import ScriptEditor
from src.mapBuilder.src.RedoUndoManager import RedoUndoManager

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class Utils():
    def get_abs_path(relative_path):
        base_path = getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_path, relative_path).replace("\\", "/")
        return path
class MainWindow(QWidget):
    coord_signal = Signal(int, int)
    def __init__(self, dirpath=None, mw=None):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(mw, dirpath)

        self.connect_menu()

        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.prev_page_btn.setDisabled(True)

        self.ui.imagePainter.setMouseTracking(True)

        self.setStyleSheet(open(Utils.get_abs_path("style.qss"), "r").read())

        self.textures = self.load_textures() # Load All Textures

        self.blocks = [[None for i in range(25)] for j in range(25)]

        self.texture_left = 0
        self.texture_right = 0

        self.enemy_damage = False
        self.enemy_health = 1

        self.player = None

        self.scripts = None
        self.texts = None

        self.current_project = None

        self.changes_since_save = False

        self.comp = compiler()

        self.RedoUndoManager = RedoUndoManager(self)

        shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        shortcut.activated.connect(self.RedoUndoManager.strg_z)

        shortcut = QShortcut(QKeySequence("Ctrl+Y"), self)
        shortcut.activated.connect(self.RedoUndoManager.strg_y)


        self.build_background() # Create The Grass Background

        self.build_border() # Create the Endstone Border

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_title) # Update the title to the current mouse pos
        self.timer.start(10)
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_current_block)
        self.timer2.start(25)
        self.drawing = False
        self.ui.imagePainter.mousePressEvent = self.mouse_click_event # Bind the Mouse Click
        self.ui.imagePainter.mouseMoveEvent = self.mouseMove # Bind Mouse Move
        self.ui.imagePainter.mouseReleaseEvent = self.mouseRelease # Bind Mouse Release

        for i in range(len(self.textures)-1):
            button = getattr(self.ui, f"block_button_{i}")
            idx = -1 if i == len(self.textures)-2 else i
            button.mousePressEvent = lambda event=False, index=idx: self.set_textures(event=event, idx=index)

        movie = QMovie(self)
        movie.setFileName(self.textures[2])

        def update_icon():
            self.ui.block_button_2.setIcon(movie.currentPixmap())

        movie.frameChanged.connect(update_icon)
        movie.start()

        self.ui.block_button_15.clicked.connect(self.reset_all_button)

        self.ui.prev_page_btn.clicked.connect(lambda: self.previous_page())
        self.ui.next_page_btn.clicked.connect(lambda: self.next_page())
        shortcut = QShortcut(QKeySequence("Ctrl+Shift+E"), self)
        shortcut.activated.connect(lambda: self.set_textures(None, -1, True))

        shortcut = QShortcut(QKeySequence("Ctrl+1"), self)
        shortcut.activated.connect(lambda: self.switch_to_page(0))
        shortcut = QShortcut(QKeySequence("Ctrl+2"), self)
        shortcut.activated.connect(lambda: self.switch_to_page(1))
        shortcut = QShortcut(QKeySequence("Ctrl+3"), self)
        shortcut.activated.connect(lambda: self.switch_to_page(2))

        self.shortcut_edit_enemy = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.shortcut_edit_enemy.activated.connect(self.end_edit_enemy)
        self.shortcut_edit_enemy.setEnabled(False)

        self.shortcut_pick_coords =  QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.shortcut_pick_coords.activated.connect(self.end_coord_pick)
        self.shortcut_pick_coords.setEnabled(False)

        self.switch_prev_page = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.switch_prev_page.activated.connect(lambda: self.previous_page())

        self.switch_next_page = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.switch_next_page.activated.connect(lambda: self.next_page())

        self.set_textures(None, -1, True)
        self.set_textures(None, -1, False)

        #self.show()

    def copy_grid(self, grid):
        return copy.deepcopy(grid)

    def uncheck(self, action:QAction):
        list = [self.ui.actionMove_Block, self.ui.actionDraw_Line, self.ui.actionDraw_Box, self.ui.actionDraw_Rect]
        for act in list:
            if act != action:
                act.setChecked(False)

    def start_drawing_box(self, filled:bool):
        self.box_filled=filled
        self.uncheck(self.ui.actionDraw_Box if filled else self.ui.actionDraw_Rect)
        self.ui.imagePainter.mousePressEvent = self.start_box
        if not self.ui.actionDraw_Rect.isChecked() and not filled: self.rebind_mouse
        if not self.ui.actionDraw_Box.isChecked() and filled: self.rebind_mouse()
        self.box_x = self.box_y = True
        self.box_images = []

    def start_box(self, event:QMouseEvent):
        self.old_grid = self.copy_grid(self.blocks)
        texture = self.texture_left if event.button() == Qt.LeftButton else self.texture_right
        x, y = self.get_pos()
        self.box_update_timer = QTimer()
        self.box_update_timer.timeout.connect(lambda: self.update_box(x,y,texture))
        self.box_update_timer.start(1)
        self.ui.imagePainter.mouseReleaseEvent = lambda ev: self.update_box(x,y,texture, True)

    def update_box(self, startx, starty, texture, finish=False):
        if not self.isActiveWindow():
            while self.box_images:
                self.ui.imagePainter.remove_image(self.box_images.pop(0))
            self.finish_box()
            return

        if texture == 0: return
        curx, cury = self.get_pos()

        difference_x = curx - startx
        difference_y = cury - starty
        difference_x = 1 if difference_x == 0 else difference_x
        difference_y = 1 if difference_y == 0 else difference_y

        stepx = difference_x // abs(difference_x)
        stepy = difference_y // abs(difference_y)

        while self.box_images:
            self.ui.imagePainter.remove_image(self.box_images.pop(0))

        for i in range(startx, curx+stepx, stepx):
            for j in range(starty, cury+stepy, stepy):
                if (not (i == startx or i == curx or j == starty or j == cury)) and not self.box_filled: continue
                if not (0 < i < 24 and 0 < j < 24): break

                if finish:
                    self.place(i, j, texture)
                    continue

                if texture == -1:
                    is_even = (i%2==0 and j%2==0) or (i%2!=0 and j%2!=0)
                    block_texture = 14 if is_even else 15
                else:
                    block_texture = texture
                self.box_images.append(self.ui.imagePainter.add_image(self.textures[block_texture], i * 20, j * 20, 0.5))
        if finish: self.finish_box()

    def finish_box(self):
        self.box_update_timer.stop()
        self.rebind_mouse()
        self.RedoUndoManager.apply_changes(self.old_grid, self.blocks)
        self.start_drawing_box(self.box_filled)

    def start_drawing_line(self):
        self.uncheck(self.ui.actionDraw_Line)
        self.ui.imagePainter.mousePressEvent = self.start_line
        if not self.ui.actionDraw_Line.isChecked(): self.rebind_mouse()
        self.x_stable = None
        self.check_x = self.check_y = True
        self.line_images = []

    def start_line(self, event:QMouseEvent):
        self.old_grid = self.copy_grid(self.blocks)
        texture = self.texture_left if event.button() == Qt.LeftButton else self.texture_right
        x, y = self.get_pos()
        self.line_update_timer = QTimer()
        self.line_update_timer.timeout.connect(lambda: self.update_line(x,y,texture))
        self.line_update_timer.start(10)
        self.ui.imagePainter.mouseReleaseEvent = lambda ev: self.update_line(x,y,texture, True)

    def update_line(self, startx, starty, texture, finish = False):
        if not self.isActiveWindow():
            while self.line_images:
                self.ui.imagePainter.remove_image(self.line_images.pop(0))
            self.finish_line()
            return
        if texture == 0: return
        curx, cury = self.get_pos()

        difference_x = curx - startx
        difference_y = cury - starty

        if (curx, cury) == (startx, starty):
            if finish: self.finish_line()
            return

        if (curx != startx and self.x_stable is None) or (self.check_x and self.x_stable is not None):
            self.check_y = False
            self.x_stable = False
            difference = difference_x
            line = startx
            xy = curx
        elif (cury != starty and self.x_stable is None) or (self.check_y and self.x_stable is not None):
            self.check_x = False
            self.x_stable = True
            difference = difference_y
            line = starty
            xy = cury

        while self.line_images:
            self.ui.imagePainter.remove_image(self.line_images.pop(0))

        difference = difference or 1
        step = difference // abs(difference)

        if xy + step - line == 1:
            self.x_stable, self.check_x, self.check_y = None, True, True
            return

        for i in range(line, xy + step, step):
            x, y = (startx, i) if self.x_stable else (i, starty)

            if not (0 < x < 24 and 0 < y < 24):
                break

            if finish:
                self.place(x,y,texture)
                continue
            if texture == -1:
                is_even = (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 != 0)
                block_texture = 14 if is_even else 15
            else:
                block_texture = texture

            self.line_images.append(self.ui.imagePainter.add_image(self.textures[block_texture], x * 20, y * 20, 0.5))

        if finish: self.finish_line()

    def finish_line(self):
        self.line_update_timer.stop()
        self.rebind_mouse()
        self.RedoUndoManager.apply_changes(self.old_grid, self.blocks)
        self.start_drawing_line()

    def add_new_text(self):
        listbox = ListEditDialog(self, self.texts)
        listbox.exec()
        texts_before = self.texts
        texts = listbox.get_texts()
        self.texts = None if texts == [] else texts
        if texts_before != self.texts:
            self.changes_since_save = True

    def reset_all_button(self):
        qms = QMessageBox(QMessageBox.Warning, "Warning", "Warning, do you really want to reset?", QMessageBox.Yes | QMessageBox.No, self)
        ret = qms.exec()
        if ret == QMessageBox.Yes:
            self.reset_all()

    def switch_to_page(self, page_index):
        if 0 <= page_index < self.ui.stackedWidget_2.count():
            self.ui.stackedWidget_2.setCurrentIndex(page_index)
            self.update_button_states()

    def previous_page(self):
        current_index = self.ui.stackedWidget_2.currentIndex()
        if current_index > 0:
            self.ui.stackedWidget_2.setCurrentIndex(current_index - 1)
        self.update_button_states()

    def next_page(self):
        current_index = self.ui.stackedWidget_2.currentIndex()
        if current_index < self.ui.stackedWidget_2.count() - 1:
            self.ui.stackedWidget_2.setCurrentIndex(current_index + 1)
        self.update_button_states()

    def update_button_states(self):
        current_index = self.ui.stackedWidget_2.currentIndex()
        self.ui.prev_page_btn.setEnabled(current_index > 0)
        self.ui.next_page_btn.setEnabled(current_index < self.ui.stackedWidget_2.count() - 1)


    def update_current_block(self):
        if self.texture_left >= 0: self.ui.current_left_block.setPixmap(QPixmap(self.textures[self.texture_left]))
        else: self.ui.current_left_block.setPixmap(QPixmap("src/mapBuilder/icons//delete.png").scaled(20, 20))
        if self.texture_right >= 0: self.ui.current_right_block.setPixmap(QPixmap(self.textures[self.texture_right]))
        else: self.ui.current_right_block.setPixmap(QPixmap("src/mapBuilder/icons//delete.png").scaled(20, 20))


    def place(self, x, y, texture_idx, god_mode=False, damage=None, health=None):
        if not god_mode:
            if x <= 0 or x >= 24 or y <= 0 or y >= 24:
                return
        if texture_idx == 0: self.check_for_existing_player()
        if self.blocks[x][y]: self.remove(x,y)
        if texture_idx == -1: return
        block_id = self.ui.imagePainter.add_image(self.textures[texture_idx], x*20, y*20)
        damage = damage if damage is not None else self.enemy_damage
        health = health if health is not None else self.enemy_health
        self.blocks[x][y] = Block(x,y,texture_idx, block_id, damage, health) if texture_idx not in (14,15) else None
        if texture_idx == 0: self.player = self.blocks[x][y]
        self.changes_since_save = True

    def place_obj(self, block: Block, x:int, y:int):
        if block is None:
            self.remove(x, y)
        else:
            texture = block.get_block()
            health, damage = block.get_enemy() or (None, None)
            self.place(x, y, texture, damage=damage, health=health)

    def reset_all(self):
        self.current_project = None
        self.scripts = None
        self.texts = None
        self.RedoUndoManager.__init__(self)
        for x in range(1,24):
            for y in range(1,24):
                if self.blocks[x][y]:
                    self.remove(x,y)

    def connect_menu(self):
        self.ui.actionNew.triggered.connect(lambda: self.reset_all())
        self.ui.actionOpen.triggered.connect(lambda: self.load_map_file())
        self.ui.actionSave.triggered.connect(lambda: self.save_map_file())
        self.ui.actionSave_As.triggered.connect(lambda: self.save_map_file(True))
        self.ui.actionEdit_Scripts.triggered.connect(lambda: ScriptEditor(self, self.scripts))
        self.ui.actionEdit_One.triggered.connect(lambda: self.edit_enemy())
        self.ui.actionEdit_All.triggered.connect(lambda: self.edit_enemy_defaults())
        self.ui.actionEdit_Texts.triggered.connect(lambda: self.add_new_text())
        self.ui.actionDraw_Line.triggered.connect(lambda: self.start_drawing_line())
        self.ui.actionDraw_Box.triggered.connect(lambda: self.start_drawing_box(filled=True))
        self.ui.actionDraw_Rect.triggered.connect(lambda: self.start_drawing_box(filled=False))
        self.ui.actionMove_Block.triggered.connect(lambda: self.start_block_move())

    def set_script_text(self, text):
        old_script = self.scripts
        self.scripts = text
        if self.scripts != old_script:
            self.changes_since_save = True

    def edit_enemy_defaults(self):
        self.enemy_health, self.enemy_damage = self.enemy_edit_messagebox(self.enemy_health, self.enemy_damage)

    def edit_enemy(self):
        self.ui.imagePainter.set_highlight_enmemys(True)
        self.set_builder_items_enabled(False)
        self.ui.imagePainter.mousePressEvent = self.edit_enemy_event
        self.shortcut_edit_enemy.setEnabled(True)

    def end_edit_enemy(self):
        self.ui.imagePainter.set_highlight_enmemys(False)
        self.set_builder_items_enabled(True)
        self.ui.imagePainter.mousePressEvent = self.mouse_click_event
        self.shortcut_edit_enemy.setEnabled(False)
        self.RedoUndoManager.apply_changes(self.old_grid, self.blocks)

    def edit_enemy_event(self, event):
        x,y = self.get_pos()
        if self.blocks[x][y] is None: return
        if self.blocks[x][y].get_block() == 10:
            self.old_grid = self.copy_grid(self.blocks)
            health, damage = self.blocks[x][y].get_enemy()
            health, damage = self.enemy_edit_messagebox(health, damage)
            self.blocks[x][y].set_enemy(health, damage)
            self.end_edit_enemy()

    def enemy_edit_messagebox(self, health:int, damage:bool):
        messagebox = QDialog(self)
        messagebox.setObjectName("enemy_edit_msgbox")
        messagebox.setWindowTitle("Enemy editing window")
        layout = QVBoxLayout()

        main_widget = QStackedWidget()

        page1_layout = QVBoxLayout()
        label = QLabel("Set the enemy's health")
        page1_layout.addWidget(label)
        line_edit = QLineEdit()
        line_edit.setText(str(health))
        line_edit.setValidator(QIntValidator())
        page1_layout.addWidget(line_edit)
        next_button = QPushButton("Next")
        next_button.clicked.connect(lambda: main_widget.setCurrentIndex(1))
        page1_layout.addWidget(next_button)

        main_widget.addWidget(QWidget())
        main_widget.addWidget(QWidget())

        main_widget.widget(0).setLayout(page1_layout)

        page2_layout = QVBoxLayout()
        checkbox = QCheckBox("Enemy Damage")
        checkbox.setChecked(damage)
        page2_layout.addWidget(checkbox)
        page2_layout2 = QHBoxLayout()
        last_button = QPushButton("Back")
        last_button.clicked.connect(lambda: main_widget.setCurrentIndex(0))
        page2_layout2.addWidget(last_button)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: messagebox.accept())
        page2_layout2.addWidget(ok_button)
        page2_layout.addLayout(page2_layout2)
        main_widget.widget(1).setLayout(page2_layout)

        layout.addWidget(main_widget)
        messagebox.setLayout(layout)

        main_widget.setCurrentIndex(0)

        messagebox.exec()
        return (int(line_edit.text()), checkbox.isChecked())

    def start_block_move(self):
        self.uncheck(self.ui.actionMove_Block)
        self.old_grid = self.copy_grid(self.blocks)
        self.ui.imagePainter.mousePressEvent = self.start_moving
        if not self.ui.actionMove_Block.isChecked(): self.rebind_mouse()
        self.move_block_id = None

    def update_moving_block(self, x, y):
        if not self.isActiveWindow():
            if self.move_block_id is not None:
                self.ui.imagePainter.remove_image(self.move_block_id)
            self.end_moving(x,y)
            return
        mx, my = self.get_pos()
        if not (0 < mx < 24 and 0 < my < 24): return
        if self.move_block_id is not None:
            self.ui.imagePainter.remove_image(self.move_block_id)
        self.move_block_id = self.ui.imagePainter.add_image(self.textures[self.blocks[x][y].get_block()], mx*20, my*20, 0.5)

    def start_moving(self, event):
        posx, posy = self.get_pos()
        if self.blocks[posx][posy] is not None and (0 < posx < 24 and 0 < posy < 24):
            self.ui.imagePainter.set_image_visibility(self.blocks[posx][posy].id, False)
            self.ui.imagePainter.mouseReleaseEvent = lambda ev: self.end_moving(posx, posy)
            self.timer3 = QTimer()
            self.timer3.timeout.connect(lambda: self.update_moving_block(posx, posy))
            self.timer3.start(10)

    def end_moving(self, x, y):
        nx, ny = self.get_pos()
        block:Block = self.blocks[x][y]
        self.remove(x,y)
        if block.get_block() == 10:
            self.place(nx,ny, block.get_block(), damage=block.get_enemy()[1], health=block.get_enemy()[0])
        else:
            self.place(nx,ny, block.get_block())

        self.ui.imagePainter.remove_image(self.move_block_id)
        self.rebind_mouse()
        self.timer3.stop()
        self.RedoUndoManager.apply_changes(self.old_grid, self.blocks)
        self.start_block_move()

    def rebind_mouse(self):
        self.ui.imagePainter.mousePressEvent = self.mouse_click_event # Bind the Mouse Click
        self.ui.imagePainter.mouseMoveEvent = self.mouseMove # Bind Mouse Move
        self.ui.imagePainter.mouseReleaseEvent = self.mouseRelease # Bind Mouse Release

    def show_only_block(self, type:int):
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                block = self.blocks[i][j]
                if block is not None and block.get_block() != type and i not in (0,24) and j not in (0,24):
                    self.ui.imagePainter.set_image_visibility(block.get_id(), False)

    def show_every_block(self):
        for blocklists in self.blocks:
            for block in blocklists:
                if block is not None:
                    self.ui.imagePainter.set_image_visibility(block.get_id(), True)

    def remove(self, x, y):
        if self.blocks[x][y] is None: return
        id = self.blocks[x][y].id
        if self.blocks[x][y].get_block() == 0: self.player = None
        self.ui.imagePainter.remove_image(id)
        self.blocks[x][y] = None

    def check_for_existing_player(self):
        if not self.player: return
        x,y = self.player.x, self.player.y
        self.remove(x,y)

    def build_border(self):
        for i in range(25):
            self.place(i, 0, 1, True)
            self.place(0, i, 1, True)
            self.place(24, i, 1, True)
            self.place(i, 24, 1, True)

    def build_background(self):
        for x in range(1,24):
            for y in range(1,24):
                if (x%2==0 and y%2==0) or (x%2!=0 and y%2!=0):
                    self.place(x, y, 14, True)
                else:
                    self.place(x, y, 15, True)

    def load_textures(self):
        textures = []
        self.files = os.listdir(str(pathlib.Path(__file__).parent.absolute()) + "/textures/")
        for file in self.files:
            textures.append(Utils.get_abs_path(f"textures/{file}"))
        return textures


    def set_textures(self, event, idx, side=None):
        if event is not None:
            side = True if event.button() == Qt.LeftButton else False
        if side: self.texture_left = idx
        else: self.texture_right = idx

    def update_title(self):
        ## This has nothing to do with the title update but is essentially to fix another bug!!!
        if not self.isActiveWindow():
            self.drawing=False
        ##
        x,y = self.get_pos()
        if self.current_project is None:
            name_text = "*untitled.ptb"
        else:
            base_name = self.current_project.split("/")[-1]
            name_text = f"*{base_name}" if self.changes_since_save else base_name
        self.setWindowTitle(f"PTB-Map-Builder | (x: {x}, y: {y}) | {name_text}")

    def get_pos(self):
        pos = self.get_mouse_position()
        posx = pos.x() // 20
        posy = pos.y() // 20
        return (posx, posy)

    def get_mouse_position(self):
        cursor_pos = QCursor.pos()
        target_pos = self.ui.imagePainter.mapFromGlobal(cursor_pos)
        return target_pos

    def mouse_click_event(self, event):
        self.old_grid = self.copy_grid(self.blocks)
        self.drawing = True
        b, p = event.button(), self.get_pos()
        x,y = p
        self.current_texture = self.texture_left if b == Qt.LeftButton else self.texture_right
        self.place(x, y, self.current_texture)


    def mouseMove(self, event):
        if self.drawing:
            p = self.get_pos()
            self.place(p[0], p[1], self.current_texture)

    def mouseRelease(self, event):
        self.drawing = False
        self.current_texture = None
        self.RedoUndoManager.apply_changes(self.old_grid, self.blocks)


    def load_map_file(self, path=None):
        if path is not None:
            file_name = path
        else:
            file_name, _ = QFileDialog.getOpenFileName(self, "Load a PTB Map", "", "*.ptb")
            if not file_name: return
        self.reset_all()
        self.current_project = file_name
        out = PtbLoader().load_file(file_name)
        self.scripts = self.comp.decompile(out[1])
        loaded_blocks = out[0]
        self.texts = out[2]
        for i, row in enumerate(loaded_blocks):
            for j, block_data in enumerate(row):
                if block_data is None:
                    self.blocks[i][j] = None
                elif isinstance(block_data, list):
                    self.place(i, j, texture_idx=block_data[0], health=block_data[1], damage=block_data[2])
                else: self.place(i, j, block_data)
        self.changes_since_save = False

    def save_map_file(self, saveAs = False):
        if self.player is None:
            QMessageBox(QMessageBox.Warning, "Warning", "Warning: No player set!\nSet a player to save.", QMessageBox.Ok, self).exec()
            return
        if not saveAs and self.current_project is not None:
            file_name=self.current_project
        else:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save a PTB Map", "", "*.ptb")
            if not file_name: return
        self.current_project = file_name
        block_list, info = self.get_combined_info()
        world = {"world":block_list}
        script = self.comp.compile(self.scripts) if not self.scripts is None else None
        texts = "\n".join(self.texts) if self.texts is not None else None
        com = compressor()
        com.insert_normal(world, script, texts)
        com.compress()
        com.save(file_name)
        self.changes_since_save = False

    def get_combined_info(self):
        block_list = []
        ids = {4: 450, 5: 700, 6: 900, 7: 20, 8: 150, 9: 55, 11: 80, 12: 0, 13: 260}
        item_keys= {4: "bombs", 5: "exp", 7: "dynamite", 8: "time_bombs", 9: "health", 11: "damage", 12: "nukes"}
        info = {
            "enemys": {"damage": [], "no-damage": []},
            "items": {"bombs": 0, "exp": 0, "dynamite": 0, "time_bombs": 0, "nukes": 0, "health": 0, "damage": 0},
            "blocks": 0
        }

        for i in range(25):
            temp = []
            for j in range(25):
                block = self.blocks[i][j]
                if not block:
                    temp.append({"id": -1, "objectData": {}})
                    continue
                if block.texture == 10:
                    health, mode = block.get_enemy()
                    mode = 1 if mode == False else 2
                    block_info = {"id": 6, "objectData": {"health": health, "id2": mode, "id1": 1}}
                    info["enemys"]["no-damage" if block.damage == 2 else "damage"].append(health)
                elif block.texture in ids:
                    start = ids[block.texture]
                    block_info = {"id": 5, "objectData": {"start": start, "fin": start}}
                    if block.texture in item_keys:
                        item_key = item_keys[block.texture]
                        info["items"][item_key] += 1
                elif block.texture == 3:
                    block_info = {"id": 3, "objectData": {}}
                    info["blocks"] += 1
                elif block.texture == 2:
                    block_info = {"id": 4, "objectData": {}}
                elif block.texture == 1:
                    block_info = {"id": 0, "objectData": {}}
                elif block.texture == 0:
                    block_info = {"id": 2, "objectData": {}}
                else:
                    print(block.texture)

                temp.append(block_info)
            block_list.append(temp)

        return block_list, info

    def set_builder_items_enabled(self, enabled:bool):
        for i in range(len(self.textures)):
            button = getattr(self.ui, f"block_button_{i}")
            button.setEnabled(enabled)
        self.menuBar().setEnabled(enabled)
        self.ui.next_page_btn.setEnabled(enabled)
        self.ui.prev_page_btn.setEnabled(enabled)

    def pick_coords(self):
        self.set_builder_items_enabled(False)
        self.ui.imagePainter.mousePressEvent = lambda event: self.get_coords_on_mouse_click()
        self.ui.imagePainter.mouseMoveEvent = self.update_coords_highlighting
        self.shortcut_pick_coords.setEnabled(True)

    def update_coords_highlighting(self, event):
        coords = self.get_pos()
        self.ui.imagePainter.set_highlighted_block(coords[0], coords[1], True)

    def get_coords_on_mouse_click(self):
        x,y = self.get_pos()
        self.coord_signal.emit(x,y)
        self.end_coord_pick()

    def end_coord_pick(self):
        self.shortcut_pick_coords.setEnabled(False)
        self.ui.imagePainter.set_highlighted_block()
        self.rebind_mouse()
        self.set_builder_items_enabled(True)

if __name__ == "__main__":
    app = QApplication([])
    md = MainWindow(sys.argv[0])
    if len(sys.argv) > 1:
        path = sys.argv[1]
        md.load_map_file(path)
    sys.exit(app.exec())