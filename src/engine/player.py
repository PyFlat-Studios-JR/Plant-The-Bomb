import src.engine.entity as entity
import src.engine.textureLib as textureLib
class player(entity.entity):
    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.texture = textureLib.textureLib.getTexture(0)
    def onTick(self):
        pass #override later
