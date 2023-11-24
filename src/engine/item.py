import src.engine.block as block
import src.engine.textureLib as textureLib
import random
class itemtype():
    NUKE = 0
    DYNAMITE = 1
    HEALTH = 2
    DAMAGE = 3
    TIMEBOMB = 4
    SHIELD = 5
    BOMB = 6
    RANGE = 7
    CURSE = 8
class item(block.block):
    def __init__(self, world, pos, start, fin):
        super().__init__(world)
        self.x, self.y = pos
        self.is_destructible = True
        self.is_walkable = True
        self.is_enemy_pickable = True
        self.is_collectable = True
        self.itemtype = None
        self.generate(start, fin)
    def generate(self, start, fin):
        seed = random.randint(start, fin)
        if (random.randint(0, 1000) == 0 and start != fin) or (start == fin and start == 0):
            self.itemtype = itemtype.NUKE
            self.texture = textureLib.textureLib.getTexture(24)
            return
        if (seed < 40):
            self.itemtype = itemtype.DYNAMITE
            self.texture = textureLib.textureLib.getTexture(18)
        elif (seed >= 40 and seed < 70):
            self.itemtype = itemtype.HEALTH
            self.texture = textureLib.textureLib.getTexture(14)
        elif (seed >= 70 and seed < 100):
            self.itemtype = itemtype.DAMAGE
            self.texture = textureLib.textureLib.getTexture(21)
        elif (seed >= 100 and seed  < 220):
            self.itemtype = itemtype.TIMEBOMB
            self.texture = textureLib.textureLib.getTexture(16)
        elif (seed >= 220 and seed < 350):
            self.itemtype = itemtype.SHIELD	
            self.texture = textureLib.textureLib.getTexture(19)
        elif (seed >= 350 and seed < 620):
            self.itemtype = itemtype.BOMB
            self.texture = textureLib.textureLib.getTexture(12)
        elif (seed >= 620 and seed < 890):
            self.itemtype = itemtype.RANGE
            self.texture = textureLib.textureLib.getTexture(10)
        elif (seed >= 890 and seed < 1001):
            self.itemtype = itemtype.CURSE
            self.texture = textureLib.textureLib.getTexture(22)
    def onDestroy(self):
        pass
    def onPickup(self, player=None):
        match (self.itemtype):
            case itemtype.NUKE:
                player.item_nukes += 1
            case itemtype.DYNAMITE:
                player.item_dynamite += 1
            case itemtype.HEALTH:
                player.health +=1 
            case itemtype.DAMAGE:
                player.damage += 1
            case itemtype.RANGE:
                player.range += 1
            case itemtype.TIMEBOMB:
                player.item_timebombs += 1
            case itemtype.BOMB:
                player.item_maxbombs += 1
                player.stat_bombs += 1
            case itemtype.CURSE:
                print("Item used curse. It didn't affect player")
            case itemtype.SHIELD:
                print("Player used protect. But it failed.")
        player.repaint_inventory()
