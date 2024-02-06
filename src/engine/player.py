from PySide6.QtGui import QPainter
from PySide6.QtCore import QRect
import src.gui.inventoryReloader as inventoryReloader
import src.engine.entity as entity
import src.engine.textureLib as textureLib
from src.engine.block import air
import src.engine.bomb as bomb
import src.engine.block as block
import src.engine.textureLib as textureLib
import src.accountManager.statregister as stats
import src.accountManager.keybinds as keybinds
import random
import src.engine.scripts as scripts

STATCTX = stats.getStatContext()
KEYS = keybinds.getKeybindManager()
class player(entity.entity):
    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.texture = textureLib.textureLib.getTexture(0)
        self.health = 1
        self.item_timebombs = 0
        self.item_maxbombs = 1
        self.range = 1
        self.damage = 1
        self.stat_bombs = 1
        self.item_nukes = 0
        self.item_dynamite = 0
        self.tick_move_cooldown_max = 2
        self.tick_move_cooldown = 5
        self.holding = None
        self.has_moved = False
        self.is_alive = True
        self.is_destructible = True
        self.curses = {
            "random_fuse": 0,
            "poop": 0,
            "stat_rand": 0,
            "no_pickup": 0,
            "item_curse": 0,
            "exp_range": 0,
            "shield": 0
        }
        self.repaint_inventory()
    def addCurse(self):
        possible_options = ["random_fuse", "poop", "enemy_spawn", "stat_rand","exp_range"]
        if self.curses["item_curse"] <= 0:
            possible_options.append("no_pickup")
        if self.curses["no_pickup"] <= 0:
            possible_options.append("item_curse")
        random.shuffle(possible_options)
        e = possible_options.pop(0)
        match (e):
            case "poop":
                print(f"POOP")
                self.curses["poop"] += 100
            case "enemy_spawn":
                if self.curses["shield"] <= 0:
                    print("Not yet implemented...")
            case "stat_rand":
                print("Not yet implemented...")
            case other:
                print(f"Added 10s to curse {e}")
                self.curses[e] += 200
    def addShield(self):
        self.curses["shield"] = 200
    def drawEvent(self, painter: QPainter):
        super().drawEvent(painter)
        has_curse = False
        for key in ["random_fuse","poop", "stat_rand","no_pickup", "item_curse", "exp_range"]:
            if self.curses[key] > 0:
                has_curse = True
                break
        if has_curse:
            region = QRect(self.x*20,self.y*20,20,20)
            painter.drawImage(region, textureLib.textureLib.getTexture(1))
        if self.curses["shield"] > 0:
            region = QRect(self.x*20,self.y*20,20,20)
            painter.drawImage(region, textureLib.textureLib.getTexture(26))
        if self.holding:
            self.holding.drawEvent(painter)
    def repaint_inventory(self):
        self.world.win.pr.ui.range_inv_label.setText(f"{self.range}")
        self.world.win.pr.ui.bomb_inv_label.setText(f"({self.stat_bombs}/{self.item_maxbombs})")
        self.world.win.pr.ui.health_inv_label.setText(f"{self.health}")
        self.world.win.pr.ui.dynamite_inv_label.setText(f"{self.item_dynamite}")
        self.world.win.pr.ui.nuke_inv_label.setText(f"{self.item_nukes}")
        self.world.win.pr.ui.timebomb_inv_label.setText(f"{self.item_timebombs}")
        self.world.win.pr.ui.damage_inv_label.setText(f"{self.damage}")
    def is_key_enabled(self, key):
        for keyop in KEYS.get(key):
            if keyop in self.world.win.keys_held:
                return True
        return False
    def handle_bomb(self):
        if 35 in self.world.win.keys_held:
            for row in self.world.blocks:
                for blck in row:
                    if type(blck) == bomb.bomb:
                        if blck.is_timed:
                            blck.timer = 0
            if type(self.holding) == bomb.bomb:
                if self.holding.is_timed:
                    self.holding.timer = 0
        if self.is_key_enabled("place_bomb_normal") or (self.curses["poop"] > 0 and self.curses["shield"] <= 0): #K
            print("HI")
            if self.holding == None or type(self.holding) == block.air:
                if self.stat_bombs > 0:
                    self.holding = bomb.bomb.normalbomb(self)
                    STATCTX.set("bombs_placed", 1)
                    STATCTX.set("bombs_placed_total", 1)
                    self.stat_bombs -= 1
                    self.repaint_inventory()
        if self.is_key_enabled("place_bomb_timed"): #T
            if self.holding == None or type(self.holding) == block.air:
                if self.item_timebombs > 0:
                    self.holding = bomb.bomb.timebomb(self)
                    STATCTX.set("timebombs_placed", 1)
                    STATCTX.set("bombs_placed_total", 1)
                    self.item_timebombs -= 1
                    self.repaint_inventory()
        if self.is_key_enabled("place_bomb_dynamite"):
            if self.holding == None or type(self.holding) == block.air:
                if self.item_dynamite > 0:
                    self.holding = bomb.bomb.dynamite(self)
                    STATCTX.set("dynamite_placed", 1)
                    STATCTX.set("bombs_placed_total", 1)
                    self.item_dynamite -= 1
                    self.repaint_inventory()
        if self.is_key_enabled("place_bomb_nuke"): #N
            if self.holding == None or type(self.holding) == block.air:
                if self.item_nukes > 0:
                    self.holding = bomb.bomb.nuke(self)
                    STATCTX.set("nukes_placed", 1)
                    STATCTX.set("bombs_placed_total", 1)
                    self.item_nukes -= 1
                    self.repaint_inventory()
    def onDestroy(self):
        if self.holding.is_destructible:
            self.holding.onDestroy()
    def onDamage(self, amount):
        if self.curses["shield"] > 0:
            return
        self.health -= amount
        STATCTX.set("damage_received", amount)
        if self.health <= 0:
            if self.holding:
                self.world.blocks[self.x][self.y] = self.holding
            self.world.blocks[self.x][self.y] = block.air(self.world)
            #put the whole level codehere!
            self.world.loose()
        self.repaint_inventory()
    def onTick(self):
        if 82 in self.world.win.keys_held and False: #texture hot reload disabled
            textureLib.textureLib.hotreload()
            self.world.reload_all()
            inventoryReloader.inventoryReloader.reloadInventoryIcons(self.world.win.pr.ui)
        dotk = self.handlemovement()
        #if not dotk:
        #    return
        self.handle_bomb()
        if self.holding:
            if self.holding.is_tickable:
                self.holding.onTick()
        for key in self.curses:
            self.curses[key] = max(0, self.curses[key]-1)
    def afterupdate(self):
        self.has_moved = False
    def move(self, dx, dy):
        if (abs(dx)+abs(dy)):
            self.has_moved = True
        nx = self.x+dx
        ny = self.y+dy
        if nx in range (0, 24) and ny in range (0, 24):
            if self.world.blocks[nx][ny].is_walkable:
                self.x = nx
                self.y = ny
                replacement = air(self.world)
                if self.holding:
                    replacement = self.holding
                if self.world.blocks[nx][ny].is_enemy_pickable:
                    self.holding = self.world.blocks[nx][ny]
                    if self.holding.is_collectable and (self.curses["no_pickup"] <= 0 or self.curses["shield"] > 0):
                        self.holding.onPickup(self)
                        self.holding = air(self.world)
                self.world.blocks[nx][ny] = self
                self.world.blocks[nx-dx][ny-dy] = replacement
                STATCTX.set("blocks_walked", 1)
                self.world.sl.event(scripts.trevent("on_step", self.x,self.y))
                self.world.sl.event(scripts.trevent("on_collect", self.x,self.y))
        return True
    def handlemovement(self):
        if self.has_moved:
            return False
        if not self.world.win.keys_held:
            self.tick_move_cooldown = 0
        self.tick_move_cooldown -= 1
        if self.tick_move_cooldown <= 0:
            if self.world.win.keys_held:
                self.tick_move_cooldown = self.tick_move_cooldown_max
        else:
            return True
        dx = 0
        dy = 0
        if self.is_key_enabled("move_up"):
            dx = 0
            dy = -1
        elif self.is_key_enabled("move_left"):
            dx = -1
            dy = 0
        elif self.is_key_enabled("move_down"):
            dx = 0
            dy = 1
        elif self.is_key_enabled("move_right"):
            dx = 1
            dy = 0
        self.move(dx,dy)