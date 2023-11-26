import src.engine.entity as entity

class bomb(entity.entity):
    def __init__(self, world, pos, type, timer, player):
        super().__init__(world, pos)
        self.explosion = type #Explosion enum: 0=basic 1=dynamite 2=nuke
        self.timer = timer #explosion timer in ticks
        self.damage = 0 #explosion damage in units
        self.mode = 0 #0: line, 1: square
        self.range = 0 #range (distance for lines, x*x for squares)
        self.exploded = False
        self.allow_explosions = False
        self.is_destructible = True
        self.initStats(player)
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
        pass