import src.engine.entity as entity
import src.engine.textureLib as textureLib
import src.engine.block as block

class bomb(entity.entity):
    def __init__(self, world, pos, type, timer, player):
        super().__init__(world, pos)
        self.explosion = type #Explosion enum: 0=basic 1=dynamite_like
        self.timer = timer #explosion timer in ticks
        self.damage = 0 #explosion damage in units
        self.mode = 0 #0: line, 1: square
        self.range = 0 #range (distance for lines, x*x for squares)
        self.exploded = False
        self.allow_explosions = False
        self.is_destructible = True
        self.texture = None
        self.player = player
        self.bomb_type = 0 #0 == basic
        self.initStats(player)
    def timebomb(player):
        b = bomb(player.world, (player.x,player.y), 0, 3153600000, player)
        b.damage = player.damage
        b.range = player.range
        b.init_textureindex(15)
        b.bomb_type = 1
        return b
    def normalbomb(player):
        b = bomb(player.world, (player.x,player.y), 0, 35, player)
        b.damage = player.damage
        b.range = player.range
        b.init_textureindex(11)
        return b
    def nuke(player):
        b = bomb(player.world, (player.x,player.y), 1, 3153600000, player)
        b.damage = player.damage*5
        b.range = 9
        b.init_textureindex(23)
        b.bomb_type = 2
        return b
    def dynamite(player):
        b = bomb(player.world, (player.x,player.y), 1, 35, player)
        b.damage = player.damage*2
        b.range = 2
        b.init_textureindex(17)
        b.bomb_type = 3
        return b
    def initStats(self, player):
        match(self.explosion):
            case 0:
                self.damage = player.damage
                self.range = player.range
                self.mode = 0
            case 1:
                self.range = 5
                self.damage = player.damage * 2
                self.mode = 1
            case 2:
                self.range = 20
                self.damage = player.damage * 5
                self.mode = 1
    def onTick(self):
        self.timer -= 1
        if self.timer <= 0:
            if not self.exploded:
                self.exploded = True
                self.world.bomb_manager.schedule(self)
    def onDestroy(self):
        self.timer = 0
    def explode(self):
        if self.world.blocks[self.x][self.y] == self:
            self.world.blocks[self.x][self.y] = block.air(self.world)
        else:
            self.player.holding = block.air(self.world)
        if self.bomb_type == 0:
            self.player.stat_bombs += 1
        self.player.repaint_inventory()
        self.explosion_effect()
    def explosion_effect(self):
        if self.explosion == 0:
            textureList = []
            mod = [(-1,0),(1,0),(0,1),(0,-1)]
            for beam in mod:
                mx, my = beam
                for d in range (self.range+1):
                    x = self.x + mx*d
                    y = self.y + my*d
                    cnt = self.world.blocks[x][y].allow_explosions
                    plc = False
                    if self.world.blocks[x][y].is_destructible:
                        self.world.blocks[x][y].onDestroy()
                        if self.world.blocks[x][y].is_alive:
                            self.world.blocks[x][y].onDamage(self.damage)
                        textureList.append((x,y))
                        plc = True
                    if not cnt:
                        break
                    if not plc:
                        textureList.append((x,y))
            self.world.bomb_manager.add_explosion(textureList, 10)
        else:
            textureList = []
            for x in range (-1*self.range+self.x,self.range+self.x+1):
                for y in range (-1*self.range+self.y,self.range+self.y+1):
                    if x in range (0, 25) and y in range (0, 25):
                        if self.world.blocks[x][y].is_destructible:
                            self.world.blocks[x][y].onDestroy()
                            if self.world.blocks[x][y].is_alive:
                                self.world.blocks[x][y].onDamage(self.damage)
                        if self.world.blocks[x][y].is_destructible or self.world.blocks[x][y].allow_explosions:
                            textureList.append((x,y))
            self.world.bomb_manager.add_explosion(textureList, 20)
