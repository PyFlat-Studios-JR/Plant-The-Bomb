import time
import src.engine.block as block
import src.engine.player as player
import src.engine.item as item
import src.engine.bombManager as bombManager
import src.engine.overlayTile as overlayTile
import src.engine.background as background
import src.engine.enemy as enemy
import src.engine.textureLib as textureLib
import src.accountManager.accounts as accounts
from src.gui.ScreenCapture import ScreenRecorder

from src.compressor import compressor
from PySide6.QtGui import QPainter
from PySide6.QtCore import QTimer
import src.accountManager.statregister as stats
import src.engine.scripts as scripts
SCTX = stats.getStatContext()

ACCOUNTS = accounts.getAccountContext()


class world():
    def __init__(self, application, file):
        enemy.enemy._reset_enemies()
        self.blocks = [[block.air(self) for x in range (25)] for y in range (25)] #very good world right now :)
        self.background = background.background(textureLib.textureLib.getTexture(27))
        self.overlay = [[overlayTile.overlayTile(self,(x,y)) for y in range (25)] for x in range (25)] #overlay drawing
        self.script_overlay = [[None for y in range (25)] for x in range (25)] #script-overlay layer
        self.script_overlay_active = False
        self.script_loader = None #scriptLoader
        self.player = None #player
        self.sl = None  #scriptloader
        self.flags = {
            "drop_items":True
                }
        self.bomb_manager = bombManager.bombManager(self) #bomb Manager
        self.win = application
        self.active_level = file
        self.runtime = 0
        self.draw_later = []
        self.load_file(file)
        self.ticker = QTimer()
        self.ticker.timeout.connect(self.tick)
        self.paused = False
        self.win.pr.ui.quit_button.clicked.connect(self.loose)
        #self.win.pr.ui.quit_button.clickable(True)
        self.win.pr.ui.pause_button.clicked.connect(self.pauseunpause)
        if ACCOUNTS.user_content == None:
            print("[WARN] No user is logged in. Your progress will NOT be saved!")
        #self.recorder = ScreenRecorder(self.win.pr)
        #self.recorder.start_recording()
        self.ticker.start(50)
    def pauseunpause(self):
        self.paused = not self.paused
        if self.paused:
            self.ticker.stop()
        else:
            self.ticker.start()
    def reload_all(self):
        for coloumn in self.blocks:
            for cell in coloumn:
                cell.reload_texture()
    def loose(self):
        print("YOU SUCK")
        self.ticker.stop()
        self.recorder.stop_recording()
        #self.win.pr.ui.stackedWidget.setCurrentIndex(0)
        if ACCOUNTS.user_content != None:
            ACCOUNTS.user_content.mark_as_completed(self.active_level, self.win.api_get_runtime(),False)
            ACCOUNTS.saveData()
        self.win.world = None
        self.win.pr.ui.normal_level_select.call_page()
    def setFlag(self, flag, val):
        self.flags[flag] = val
    def winf(self):
        print("GG YOU WON")
        self.ticker.stop()
        #self.recorder.stop_recording()
        #self.win.pr.ui.stackedWidget.setCurrentIndex(0)

        if ACCOUNTS.user_content != None:
            ACCOUNTS.user_content.mark_as_completed(self.active_level, self.win.api_get_runtime())
            print("Completed: " + self.active_level)
            ACCOUNTS.saveData()
        self.win.world = None
        self.win.pr.ui.normal_level_select.call_page()
    def load_file(self, file):
        c = compressor()
        c.load(file)
        c.decompress()
        res, s, _ = c.get_data()
        for x in range (len(res["world"])):
            for y in range (len(res["world"][x])):
                blockdata = res["world"][x][y]
                match (blockdata["id"]):
                    case 0:
                        self.blocks[x][y] = block.bedrock(self, (x,y))
                    case 2:
                        self.blocks[x][y] = player.player(self, (x,y))
                        self.player = self.blocks[x][y]
                    case 3:
                        self.blocks[x][y] = block.brick(self, (x,y))
                    case 4:
                        self.blocks[x][y] = block.water(self, (x,y))
                    case 5:
                        self.blocks[x][y] = item.item(self, (x,y), blockdata["objectData"]["start"], blockdata["objectData"]["fin"])
                    case 6:
                        self.blocks[x][y] = enemy.enemy(self, (x,y),blockdata["objectData"]["health"],blockdata["objectData"]["id2"])
        self.sl = scripts.scriptLoader(self, s)
        self.sl.event(scripts.trevent("on_init",0,0))
    def handle_uiupdate(self):
        self.win.pr.ui.time_label.setText("Time {}:{}:{}:{}.{}".format(*self.win.api_get_runtime()))
    def drawLater(self, e):
        self.draw_later.append(e)
    def tick(self):
        self.runtime += 1
        self.handle_uiupdate()
        start = time.time()
        #try to explode any unexploded explosives
        self.bomb_manager.tick()
        #actually force the player to confine to tickorder
        for coloumn in self.blocks:
            for cell in coloumn:
                if cell.is_tickable:
                    cell.onTick()
        self.win.update()
        if self.player:
            self.player.afterupdate()
        self.sl.event(scripts.trevent("on_tick",0,0))
        #print(time.time()-start)
    def paintEvent(self, painter: QPainter): #do the initialization from elsewhere :)
        self.background.paintEvent(painter) #draw background
        for coloumn in self.blocks:
            for cell in coloumn:
                cell.drawEvent(painter)
        for e in self.draw_later:
            painter.drawImage(*e)
        self.draw_later = []
        #actually have to write this entire code ...
        for coloumn in self.overlay:
            for cell in coloumn:
                if cell.is_occupied:
                    cell.drawEvent(painter)
        if self.script_overlay_active:
            for c in self.script_overlay:
                for i in c:
                    if i:
                        i.drawEvent(painter)