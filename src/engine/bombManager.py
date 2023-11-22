class bombManager():
    def __init__(self, world):
        self.explosion_waitlist = []
        self.world = world
    def tick(self):
        if len(self.explosion_waitlist) > 0:
            #acutally perform the "exploding task"
            self.explosion_waitlist.pop(0)
    def schedule(self, bomb):
        self.explosion_waitlist.append(bomb)