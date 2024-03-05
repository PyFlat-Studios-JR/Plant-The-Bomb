class Block():
    def __init__(self, x,y,texture_id, block_id, damage, health):
        self.x = x
        self.y = y
        self.texture = texture_id
        self.id = block_id
        self.health = health if texture_id == 10 else None
        self.damage = damage if texture_id == 10 else None
        self.edit = True if self.texture == 10 else False
    def get_pos(self):
        return self.x, self.y
    def get_block(self):
        return self.texture
    def get_id(self):
        return self.id
    def get_enemy(self):
        if self.texture == 10:
            return (self.health, self.damage)
    def set_enemy(self, health, damage):
        if self.texture == 10:
            self.health = health
            self.damage = damage