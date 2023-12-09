import src.gui.inventoryReloader as inventoryReloader
import src.engine.entity as entity
import src.engine.textureLib as textureLib
from src.engine.block import air
import src.engine.bomb as bomb
import src.engine.block as block
class player(entity.entity):
    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.texture = textureLib.textureLib.getTexture(0)
        self.health = 1
        self.item_timebombs = 0
        self.item_maxbombs = 1
        self.range = 1
        self.damage = 0
        self.stat_bombs = 1
        self.item_nukes = 0
        self.item_dynamite = 0
        self.tick_move_cooldown_max = 2
        self.tick_move_cooldown = 5
        self.holding = None
        self.has_moved = False
        self.repaint_inventory()
    def repaint_inventory(self):
        self.world.win.pr.ui.range_inv_label.setText(f"{self.range}")
        self.world.win.pr.ui.bomb_inv_label.setText(f"({self.stat_bombs}/{self.item_maxbombs})")
        self.world.win.pr.ui.health_inv_label.setText(f"{self.health}")
        self.world.win.pr.ui.dynamite_inv_label.setText(f"{self.item_dynamite}")
        self.world.win.pr.ui.nuke_inv_label.setText(f"{self.item_nukes}")
        self.world.win.pr.ui.timebomb_inv_label.setText(f"{self.item_timebombs}")
        self.world.win.pr.ui.damage_inv_label.setText(f"{self.damage}")
    def handle_bomb(self):
        if 75 in self.world.win.keys_held: #K
            if self.holding == None or type(self.holding) == block.air:
                if self.stat_bombs > 0:
                    self.holding = bomb.bomb.normalbomb(self)
                    self.stat_bombs -= 1
                    self.repaint_inventory()
        if 84 in self.world.win.keys_held: #T
            if self.holding == None or type(self.holding) == block.air:
                if self.item_timebombs > 0:
                    self.holding = bomb.bomb.timebomb(self)
                    self.item_timebombs -= 1
                    self.repaint_inventory()
        if 89 in self.world.win.keys_held: #Y
            if self.holding == None or type(self.holding) == block.air:
                if self.item_dynamite > 0:
                    self.holding = bomb.bomb.dynamite(self)
                    self.item_dynamite -= 1
                    self.repaint_inventory()
        if 78 in self.world.win.keys_held: #N
            if self.holding == None or type(self.holding) == block.air:
                if self.item_nukes > 0:
                    self.holding = bomb.bomb.nuke(self)
                    self.item_nukes -= 1
                    self.repaint_inventory()
    def onDestroy(self):
        if self.holding.is_destructible:
            self.holding.onDestroy()
    def onTick(self):
        if 82 in self.world.win.keys_held:
            textureLib.textureLib.hotreload()
            self.world.reload_all()
            inventoryReloader.inventoryReloader.reloadInventoryIcons(self.world.win.pr.ui)
        self.handle_bomb()
        if self.holding:
            if self.holding.is_tickable:
                self.holding.onTick()
        self.handlemovement()
    def afterupdate(self):
        self.has_moved = False
    def handlemovement(self):
        if self.has_moved:
            return
        if not self.world.win.keys_held:
            self.tick_move_cooldown = 0
        self.tick_move_cooldown -= 1
        if self.tick_move_cooldown <= 0:
            if self.world.win.keys_held:
                self.tick_move_cooldown = self.tick_move_cooldown_max
        else:
            return
        dx = 0
        dy = 0
        if 87 in self.world.win.keys_held:
            dx = 0
            dy = -1
        elif 65 in self.world.win.keys_held:
            dx = -1
            dy = 0
        elif 83 in self.world.win.keys_held:
            dx = 0
            dy = 1
        elif 68 in self.world.win.keys_held:
            dx = 1
            dy = 0
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
                    if self.holding.is_collectable:
                        self.holding.onPickup(self)
                        self.holding = air(self.world)
                self.world.blocks[nx][ny] = self
                self.world.blocks[nx-dx][ny-dy] = replacement