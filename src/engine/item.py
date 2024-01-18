from PySide6.QtGui import QPainter
from PySide6.QtCore import QRect
import src.engine.block as block
import src.engine.textureLib as textureLib
import random
import src.accountManager.statregister as stats

SCTX = stats.getStatContext()
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
        self.player = world.player
        self.x, self.y = pos
        self.is_destructible = True
        self.is_walkable = True
        self.is_enemy_pickable = True
        self.is_collectable = True
        self.itemtype = None
        self.seed = None
        self.start = None
        self.fin = None
        self.generate(start, fin)
    def generate(self, start, fin, generate=True):
        self.start = start
        self.fin = fin
        seed = self.seed
        if generate:
            seed = random.randint(start, fin)
        self.seed = seed
        if (random.randint(0, 1000) == 0 and start != fin) or (start == fin and start == 0) and (generate or self.itemtype==itemtype.NUKE):
            self.itemtype = itemtype.NUKE
            self.init_textureindex(24)
            return
        if (seed < 40):
            self.itemtype = itemtype.DYNAMITE
            self.init_textureindex(18)
        elif (seed >= 40 and seed < 70):
            self.itemtype = itemtype.HEALTH
            self.init_textureindex(14)
        elif (seed >= 70 and seed < 100):
            self.itemtype = itemtype.DAMAGE
            self.init_textureindex(21)
        elif (seed >= 100 and seed  < 220):
            self.itemtype = itemtype.TIMEBOMB
            self.init_textureindex(16)
        elif (seed >= 220 and seed < 350):
            self.itemtype = itemtype.SHIELD	
            self.init_textureindex(19)
        elif (seed >= 350 and seed < 620):
            self.itemtype = itemtype.BOMB
            self.init_textureindex(12)
        elif (seed >= 620 and seed < 890):
            self.itemtype = itemtype.RANGE
            self.init_textureindex(10)
        elif (seed >= 890 and seed < 1001):
            self.itemtype = itemtype.CURSE
            self.init_textureindex(22)
    def reload_texture(self):
        self.generate(self.start,self.fin,False)
        return super().reload_texture()
    def onDestroy(self):
        self.world.blocks[self.x][self.y] = block.air(self.world)
    def drawEvent(self, painter: QPainter):
        if self.player == None:
            self.player = self.world.player
            return
        if self.player.curses["item_curse"] > 0 and self.player.curses["shield"] <= 0:
            painter.drawImage(QRect(self.x*20,self.y*20,20,20), textureLib.textureLib.getTexture(22))
            return
        super().drawEvent(painter)
    def onPickup(self, player=None):
        SCTX.set("items_collected_total", 1)
        if player.curses["item_curse"] > 0 and player.curses["shield"] <= 0:
            player.addCurse()
            SCTX.set("items_collected_curses", 1)
            player.repaint_inventory()
            return
        match (self.itemtype):
            case itemtype.NUKE:
                player.item_nukes += 1
                SCTX.set("items_collected_nukes", 1)
            case itemtype.DYNAMITE:
                player.item_dynamite += 1
                SCTX.set("items_collected_dynamite", 1)
            case itemtype.HEALTH:
                player.health +=1 
                SCTX.set("items_collected_health", 1)
            case itemtype.DAMAGE:
                player.damage += 1
                SCTX.set("items_collected_damage", 1)
            case itemtype.RANGE:
                player.range += 1
                SCTX.set("items_collected_range", 1)
            case itemtype.TIMEBOMB:
                player.item_timebombs += 1
                SCTX.set("items_collected_timebombs", 1)
            case itemtype.BOMB:
                player.item_maxbombs += 1
                player.stat_bombs += 1
                SCTX.set("items_collected_bombs", 1)
            case itemtype.CURSE:
                player.addCurse()
                SCTX.set("items_collected_curses", 1)
            case itemtype.SHIELD:
                player.addShield()
                SCTX.set("items_collected_shields", 1)
        player.repaint_inventory()
