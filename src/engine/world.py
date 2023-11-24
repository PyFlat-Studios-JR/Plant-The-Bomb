import time
import src.engine.block as block
import src.engine.player as player
import src.engine.item as item
import src.engine.bombManager as bombManager
import src.engine.overlayTile as overlayTile
import src.engine.background as background
import src.engine.enemy as enemy
from src.compressor import compressor
from PySide6.QtGui import QPainter
from PySide6.QtCore import QTimer
class world():
    def __init__(self, application, file):
        self.blocks = [[block.air(self) for x in range (25)] for y in range (25)] #very good world right now :)
        self.background = background.checkerboard #background drawing
        self.overlay = [[overlayTile.overlayTile(self,(x,y)) for y in range (25)] for x in range (25)] #overlay drawing
        self.script_loader = None #scriptLoader
        self.player = None #player
        self.bomb_manager = bombManager.bombManager(self) #bomb Manager
        self.load_file(file)
        self.ticker = QTimer()
        self.ticker.timeout.connect(self.tick)
        self.win = application
        self.ticker.start(50)
    def load_file(self, file):
        c = compressor()
        c.load(file)
        c.decompress()
        res, _, _ = c.get_data()
        for x in range (len(res["world"])):
            for y in range (len(res["world"][x])):
                blockdata = res["world"][x][y]
                match (blockdata["id"]):
                    case 0:
                        self.blocks[x][y] = block.bedrock(self, (x,y))
                    case 2:
                        self.blocks[x][y] = player.player(self, (x,y))
                    case 3:
                        self.blocks[x][y] = block.brick(self, (x,y))
                    case 4:
                        self.blocks[x][y] = block.water(self, (x,y))
                    case 5:
                        self.blocks[x][y] = item.item(self, (x,y), blockdata["objectData"]["start"], blockdata["objectData"]["fin"])
                    case 6:
                        self.blocks[x][y] = enemy.enemy(self, (x,y))
    def tick(self):
        start = time.time()
        #try to explode any unexploded explosives
        self.bomb_manager.tick()
        #actually force the player to confine to tickorder
        for coloumn in self.blocks:
            for cell in coloumn:
                if cell.is_tickable:
                    cell.onTick()
        self.win.update()
        print(f"tick completed in {round((time.time()-start)*1000,2)}ms")
    def paintEvent(self, painter: QPainter): #do the initialization from elsewhere :)
        self.background.paintEvent(painter) #draw background
        for coloumn in self.blocks:
            for cell in coloumn:
                cell.drawEvent(painter)
        #actually have to write this entire code ...
        for coloumn in self.overlay:
            for cell in coloumn:
                if cell.is_occupied:
                    cell.drawEvent(painter)