from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QImage, QMovie, QPixmap, QColor, QBrush

class ImagePainterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_entries = {}  # Dictionary to hold image data by image ID
        self.counter = 0
        self.highlighted_block_coords = None  # Store the coordinates of the highlighted block
        self.highlighted_block_active = False
        self.highlight_enemys = False
        self.enemys = []

    def add_image(self, image_path:str, x:int, y:int, opacity:float=1.0):
        self.counter += 1
        image = QImage(image_path)
        self.image_entries[self.counter] = {'position': (x, y), 'image': image, 'visible': True, 'opacity': opacity}
        if image_path.endswith("10_enemy.png"):
            self.enemys.append((x//20, y//20))

        if image_path.endswith(".gif") and opacity==1.0:
            movie = QMovie(image_path)
            movie.frameChanged.connect(self.update)
            movie.start()
            self.image_entries[self.counter]['movie'] = movie
        else:
            self.image_entries[self.counter]['movie'] = None

        self.update()
        return self.counter

    def remove_image(self, unique_id):
        if unique_id in self.image_entries:
            enemy = tuple(x // 20 for x in self.image_entries[unique_id]["position"])
            if enemy in self.enemys:
                self.enemys.remove(enemy)
            del self.image_entries[unique_id]
            self.update()

    def set_image_visibility(self, unique_id, visible):
        if unique_id in self.image_entries:
            self.image_entries[unique_id]['visible'] = visible
            self.update()

    def set_highlighted_block(self, x=0, y=0, active=False):
        self.highlighted_block_coords = (x, y)
        self.highlighted_block_active = active
        self.update()

    def set_highlight_enmemys(self, active=False):
        self.highlight_enemys = active
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for id, entry in self.image_entries.items():
            if entry['visible']:
                x, y = entry['position']
                pixmap = entry['movie'].currentPixmap() if entry['movie'] else QPixmap.fromImage(entry['image'])

                rx, ry = x // 20, y // 20
                painter.setOpacity(entry['opacity'])
                painter.drawPixmap(x, y, pixmap)

                if self.highlighted_block_active and (rx, ry) != self.highlighted_block_coords:
                    painter.fillRect(x, y, pixmap.width(), pixmap.height(), QColor(128, 128, 128, 180))

                if self.highlight_enemys and (rx, ry) not in self.enemys:
                    painter.fillRect(x, y, pixmap.width(), pixmap.height(), QColor(128, 128, 128, 180))
