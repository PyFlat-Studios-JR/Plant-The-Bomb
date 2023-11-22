from PySide6.QtCore import QRect
class overlayTile():
    def __init__(self, world, pos):
        self.world = world
        self.texture = None
        self.is_occupied = False
        self.owner = None
        self.x, self.y = pos
    def drawEvent(self, painter):
        if self.texture:
            painter.drawImage(QRect(self.x*20,self.y*20,20,20))
    def occupy(self, owner, texture):
        if self.is_occupied:
            self.owner.release_overlay(self)
        self.owner = owner
        self.texture = texture
    def release(self, owner):
        #backup code to not delete stuff, if the owner has changed.
        if self.owner != owner:
            return
        self.is_occupied = False
        self.texture = None
