import src.engine.entity as entity

class bomb(entity.entity):
    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.explosion = 0 #Explosion enum: 0=basic 1=dynamite 2=nuke
        self.timer = 0
    def onTick(self):
        pass
    def onDestroy(self):
        pass