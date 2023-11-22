import src.engine.block as block
import src.engine.player as player
import src.engine.bombManager as bombManager
class world():
    def __init__(self):
        self.blocks = [[block.air(self) for x in range (25)] for y in range (25)]
        self.background = None #background drawing
        self.overlay = None #overlay drawing
        self.script_loader = None #scriptLoader
        self.player = None #player
        self.bomb_manager = None #bomb Manager
