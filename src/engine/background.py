from PySide6.QtCore import QRect
from src.engine.textureLib import textureLib
class background():
    def __init__(self, bg_image):
        self.bg_image = bg_image
    def paintEvent(self, painter):
        painter.drawImage(QRect(0,0,500,500), self.bg_image)

#initialize different backgrounds here...

checkerboard = background(textureLib.getTexture(27))