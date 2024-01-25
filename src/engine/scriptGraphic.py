from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRect
import src.engine.textureLib as textureLib
class scriptGraphic():
    def __init__(self, x,y,color=None, txtID=None):
        if color != None and txtID != None:
            raise RuntimeError("WARNING! The drawing engine got confused, cause you tried to draw a texture and color all at once!")
        self.color = color
        self.txtID = txtID
        self.x = x
        self.y = y
        self.mode = self.color != None
    def drawEvent(self, painter: QPainter):
        if self.mode:
            painter.fillRect(QRect(self.x*20,self.y*20,20,20),QColor(self.color))
        else:
            painter.drawImage(QRect(self.x*20,self.y*20,20,20),textureLib.textureLib.getTexture(self.txtID))