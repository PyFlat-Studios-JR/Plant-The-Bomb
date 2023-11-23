import src.engine.entity as entity
import src.engine.textureLib as textureLib
class enemy (entity.entity):
    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.is_destructible = True
        self.allow_explosions = True
        self.texture = textureLib.textureLib.getTexture(2)
    def onTick(self):
        return super().onTick() #override later
    def onDestroy(self):
        pass