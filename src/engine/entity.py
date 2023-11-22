import src.engine.block as block

class entity(block.block):
    def __init__(self, world, pos):
        super().__init__(world)
        self.x, self.y = pos
        self.is_tickable = True #all entities are tickable by default
        self.allow_explosions = True #all entities should allow explosions by default.
    def onTick(self): #mandatory ontick function => override
        pass

