import src.engine.entity as entity

class player(entity.entity):
    def __init__(self, world, pos):
        super().__init__(world, pos)
    def onTick(self):
        pass #override later
