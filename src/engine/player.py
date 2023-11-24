import src.engine.entity as entity
import src.engine.textureLib as textureLib
from src.engine.block import air
class player(entity.entity):
    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.texture = textureLib.textureLib.getTexture(0)
        self.health = 1
        self.item_timebombs = 1
        self.item_maxbombs = 1
        self.range = 1
        self.damage = 0
        self.stat_bombs = 1
        self.item_nukes = 0
        self.item_dynamite = 0
        self.tick_move_cooldown_max = 5
        self.tick_move_cooldown = 5
        self.holding = None
        self.repaint_inventory()
    def repaint_inventory(self):
        self.world.win.pr.ui.range_inv_label.setText(f"{self.range}")
        self.world.win.pr.ui.bomb_inv_label.setText(f"({self.stat_bombs}/{self.item_maxbombs})")
        self.world.win.pr.ui.health_inv_label.setText(f"{self.health}")
        self.world.win.pr.ui.dynamite_inv_label.setText(f"{self.item_dynamite}")
        self.world.win.pr.ui.nuke_inv_label.setText(f"{self.item_nukes}")
        self.world.win.pr.ui.timebomb_inv_label.setText(f"{self.item_timebombs}")
        self.world.win.pr.ui.damage_inv_label.setText(f"{self.damage}")
    def onTick(self):
        if self.holding:
            if self.holding.is_tickable:
                self.holding.onTick()
        self.handlemovement()
    def handlemovement(self):
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