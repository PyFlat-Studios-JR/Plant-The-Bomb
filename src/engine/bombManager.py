import src.engine.textureLib as textureLib
class bombManager():
    def __init__(self, world):
        self.explosion_waitlist = []
        self.explosions = []
        self.world = world
    def tick(self):
        if len(self.explosion_waitlist) > 0:
            #acutally perform the "exploding task"
            self.explosion_waitlist.pop(0).explode()
        new_exps = []
        for element in self.explosions:
            element["time"] -= 1
            if element["time"] <= 0:
                for x, y in element["list"]:
                    self.world.overlay[x][y].release(self)
            else:
                new_exps.append(element)
        self.explosions = new_exps[::]
    def schedule(self, bomb):
        self.explosion_waitlist.append(bomb)
    def add_explosion(self, list, duration):
        print(f"Added explosion of {duration} with length: {len(list)}")
        self.explosions.append({"time":duration, "list":list})
        for x, y in list:
            self.world.overlay[x][y].occupy(self, textureLib.textureLib.getTexture(9))
    def release_overlay(self, overlay):
        return