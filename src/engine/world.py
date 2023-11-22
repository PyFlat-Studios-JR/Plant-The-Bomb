import src.engine.block as block
import src.engine.player as player
import src.engine.bombManager as bombManager
import src.engine.overlayTile as overlayTile
from PySide6.QtGui import QPainter
class world():
    def __init__(self):
        self.blocks = [[block.air(self) for x in range (25)] for y in range (25)] #very good world right now :)
        self.background = None #background drawing
        self.overlay = [[overlayTile(self,(x,y)) for y in range (25)] for x in range (25)] #overlay drawing
        self.script_loader = None #scriptLoader
        self.player = None #player
        self.bomb_manager = bombManager.bombManager(self) #bomb Manager
    def tick(self):
        #try to explode any unexploded explosives
        self.bomb_manager.tick()
        #actually force the player to confine to tickorder
        for coloumn in self.blocks:
            for cell in coloumn:
                if cell.is_tickable:
                    cell.tickEvent()
        
    def paintEvent(self, painter: QPainter): #do the initialization from elsewhere :)
        self.background.paintEvent(painter) #draw background
        for coloumn in self.blocks:
            for cell in coloumn:
                if cell.is_tickable:
                    cell.drawEvent(painter)
        #actually have to write this entire code ...
        for coloumn in self.overlay:
            for cell in coloumn:
                if cell.is_occupied:
                    cell.drawEvent(painter)