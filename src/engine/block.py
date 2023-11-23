from PySide6.QtCore import QRect
from PySide6.QtGui import QImage, QPainter
import src.engine.textureLib as textureLib
class block():
    def __init__(self, world, **kwargs):
        self.is_destructible = False        #block should have an onDestroy tick event
        self.is_walkable = False            #block is "not solid"
        self.allow_explosions = False       #block is not rock.
        self.is_tickable = False            #block should have a onTick event however this attribute is strictly reserved for entitys. 
        self.is_enemy_pickable = False      #enemies can pick up the block (specifically for items)
        #actual stuff
        self.x = 0
        self.y = 0
        self.world = world
        self.texture: QImage | None = None #QImage
        #kwarg loader
        for key in kwargs:
            self._prc_farg(key, kwargs[key])
    def _prc_farg(self, arg, val):
        #pls do not use this. nothing is private anyway...
        match (arg):
            case "is_destructible":
                self.is_destructible = val
            case "is_walkable":
                self.is_walkable = val
            case "allow_explosions":
                self.allow_explosions = val
            case "x":
                self.x = val
            case "y":
                self.y = val
            case "texture":
                self.texture = val
    def drawEvent(self, painter: QPainter):
        if self.texture == None:
            return
        region = QRect(self.x*20,self.y*20,20,20)
        painter.drawImage(region, self.texture)
class air(block):
    def __init__(self,world):
        super().__init__(world)
        self.is_walkable = True
        self.allow_explosions = True
        self.is_enemy_pickable = True #yes, enemies can "pick up" air. Otherwise that would complicate the pickup code
class brick(block):
    def __init__(self, world, pos):
        super().__init__(world)
        self.x, self.y = pos
        self.is_destructible = True
        self.texture = textureLib.textureLib.getTexture(3)
    def onDestroy(self):
        pass #put stuff like item drops here!
class bedrock(block): #please don't sue, mojang...
    def __init__(self, world, pos):
        super().__init__(world)
        self.x, self.y = pos
        self.texture = textureLib.textureLib.getTexture(4)
class water(block):
    def __init__(self, world, pos):
        super().__init__(world)
        self.x, self.y = pos
        self.allow_explosions = True
        self.texture = textureLib.textureLib.getTexture(5)