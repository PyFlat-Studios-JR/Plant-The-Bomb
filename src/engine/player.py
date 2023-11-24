import src.engine.entity as entity
import src.engine.textureLib as textureLib
from src.engine.block import air
class player(entity.entity):
    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.texture = textureLib.textureLib.getTexture(0)
        self.health = 1
        self.item_timebombs = 0
        self.item_maxbombs = 1
        self.item_range = 0
        self.item_damage = 0
        self.stat_bombs = 1
        self.item_nukes = 0
        self.item_dynamite = 0
        self.tick_move_cooldown_max = 5
        self.tick_move_cooldown = 5
    def onTick(self):
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
                self.world.blocks[nx][ny] = self
                self.world.blocks[nx-dx][ny-dy] = air(self.world)