from tkinter import *
from tkinter import messagebox
import resources.crypto as crypto
import resources.compressor as comp
import pathlib, os, time, json, random,functools,hashlib
class trigger():
    def __init__(self,s,l,t,x,y):
        self.x = x
        self.y = y
        self.t = t #01 => on_step 02 => on_collect
        self.l = l #location pointer is set to on event
        self.s = s #scriptloader
        self.collection = False
    def check_collection(self):
        if self.t == 1:
            self.run()
            return
        if self.t == 2 and not self.collection:
            self.run()
            self.collection = True
            return
    def run(self):
        self.s.pointer = self.l
        self.s.run_script()
class scriptLoader():
    def __init__(self, script, world):
        #init world for data collection 
        #IMPROTANT: Initialize scripts AFTER player loading
        self.world = world
        #load script source
        self.source = script
        #initialize scripts
        self.ram = [0]*256 #initialze RAM
        self.pointer = 0   #Initialze pointer 
        #Load trigger events
        self.triggers = []
        self.load_triggers()
    def on_init(self):
        #Execute command ONLY ONCE ON WORLD LOAD
        for i in range (0, len(self.triggers)):
            if self.triggers[i].t == 3:
                self.triggers[i].run()
    def load_triggers(self):
        for i in range (0, len(self.source)):
            if self.source[i] == 0:
                #if programm detects a command initiator, proceed
                if self.source[i+1] == 7:
                    #trigger instruction detected
                    self.triggers.append(trigger(self, i+5, self.source[i+2],self.source[i+3],self.source[i+4]))#jump mark is set after script command
        #hopefully this will work?
    def run_script(self):
        #This method is invoked after hitting a trigger
        #print("Invoked script")
        running = True
        while running:
            #print(self.source[self.pointer])
            if self.source[self.pointer] == 0:
                if self.source[self.pointer+1] == 1: #tp command (tp <x> <y>)
                    tx = self.ram[self.source[self.pointer+2]]
                    ty = self.ram[self.source[self.pointer+3]]
                    px = self.world.p.x
                    py = self.world.p.y
                    vx = tx - px
                    vy = ty - py
                    self.world.p.move(vx,vy)
                    self.pointer += 4
                elif self.source[self.pointer+1] == 2: #edit _ inv command (edit_inv <slot> <amount>)
                    if self.source[self.pointer+2] == 1:
                        self.world.p.inventory["total"] = self.ram[self.source[self.pointer+3]]
                    elif self.source[self.pointer+2] == 2:
                        self.world.p.inventory["exp_range"] = self.ram[self.source[self.pointer+3]]
                    elif self.source[self.pointer+2] == 3:
                        self.world.p.inventory["dynamite"] = self.ram[self.source[self.pointer+3]]
                    elif self.source[self.pointer+2] == 4:
                        self.world.p.inventory["timed_bombs"] = self.ram[self.source[self.pointer+3]]
                    self.world.p.paint_inv()
                    self.pointer += 4
                elif self.source[self.pointer+1] == 3: #edit health
                    #print("edit health")
                    self.world.p.health = self.ram[self.source[self.pointer+2]]
                    self.world.p.paint_inv()
                    self.pointer += 3
                elif self.source[self.pointer+1] == 4: #compare
                    #compare <dest> <v1> <m> <v2>
                    if self.source[self.pointer+4] == 1:
                        # >
                        if self.ram[self.source[self.pointer+3]] > self.ram[self.source[self.pointer+5]]:
                            self.ram[self.source[self.pointer+2]] = 1
                        else:
                            self.ram[self.source[self.pointer+2]] = 0
                    elif self.source[self.pointer+4] == 2:
                        # <
                        if self.ram[self.source[self.pointer+3]] < self.ram[self.source[self.pointer+5]]:
                            self.ram[self.source[self.pointer+2]] = 1
                        else:
                            self.ram[self.source[self.pointer+2]] = 0
                    else:
                        if self.ram[self.source[self.pointer+3]] == self.ram[self.source[self.pointer+5]]:
                            self.ram[self.source[self.pointer+2]] = 1
                        else:
                            self.ram[self.source[self.pointer+2]] = 0
                    self.pointer += 6
                elif self.source[self.pointer+1] == 5: #set variable to value command
                    #print("Set")
                    self.ram[self.source[self.pointer+2]] = self.source[self.pointer+3]
                    self.pointer += 4
                elif self.source[self.pointer+1] == 6: #get
                    if self.source[self.pointer+3] == 1:
                        if self.source[self.pointer+4] == 1:
                            self.ram[self.source[self.pointer+2]] = self.world.p.inventory["total"]
                        elif self.source[self.pointer+4] == 2:
                            self.ram[self.source[self.pointer+2]] = self.world.p.inventory["exp_range"]
                        elif self.source[self.pointer+4] == 3:
                            self.ram[self.source[self.pointer+2]] = self.world.p.inventory["dynamite"]
                        elif self.source[self.pointer+4] == 4:
                            self.ram[self.source[self.pointer+2]] = self.world.p.inventory["timed_bombs"]
                        elif self.source[self.pointer+4] == 5:
                            self.ram[self.source[self.pointer+2]] = self.world.p.health
                    self.pointer += 5
                elif self.source[self.pointer+1] == 8: #if <!condition> <jump>
                    if self.ram[self.source[self.pointer+2]]==0:
                        self.pointer += self.source[self.pointer+3]+4 #jump mark is relative to 00-byte after method execution
                    else:
                        self.pointer += 4
                elif self.source[self.pointer+1] == 9: #jump (if without condition)
                    self.pointer += self.source[self.pointer+2]+3
                elif self.source[self.pointer+1] == 10:
                    #print("add")
                    self.ram[self.source[self.pointer+4]] = self.ram[self.source[self.pointer+3]] + self.ram[self.source[self.pointer+2]]
                    self.pointer += 5
                elif self.source[self.pointer+1] == 11:
                    #print("sub")
                    self.ram[self.source[self.pointer+4]] = self.ram[self.source[self.pointer+3]] - self.ram[self.source[self.pointer+2]]
                    self.pointer += 5
                elif self.source[self.pointer+1] == 12:
                    #print("mult")
                    self.ram[self.source[self.pointer+4]] = self.ram[self.source[self.pointer+3]] * self.ram[self.source[self.pointer+2]]
                    self.pointer += 5
                elif self.source[self.pointer+1] == 13:
                    #print("RETURN")
                    running = False
                elif self.source[self.pointer+1] == 14: #show text
                    self.world.display.inventory.showText(self.source[self.pointer+2])
                    self.pointer += 3
                elif self.source[self.pointer+1] == 15: #drawImage RAM
                    self.ram[self.source[self.pointer+2]] = self.world.display.drawImage(self.ram[self.source[self.pointer+4]],self.ram[self.source[self.pointer+5]],self.ram[self.source[self.pointer+3]])
                    self.pointer += 6
                elif self.source[self.pointer+1] == 16: #drawImage RAM
                    self.ram[self.source[self.pointer+2]] = self.world.display.drawImage(self.source[self.pointer+4],self.source[self.pointer+5],self.source[self.pointer+3])
                    self.pointer += 6
                elif self.source[self.pointer+1] == 17:
                    self.world.display.remove(self.ram[self.source[self.pointer+2]])
                    self.pointer += 3
                elif self.source[self.pointer+1] == 18:
                    self.world.win()
                    self.pointer += 2
            else:
                self.pointer += 1
class ATTACK():
    def callType(i):
        TYPE_0 = [(0,0)]
        TYPE_1 = [(-1,0),(0,-1),(0,0),(1,0),(0,1)]
        TYPES = [None,TYPE_0,TYPE_1]
        return TYPES[i]
class tagManager():
    binds = []
    def append(i, t):
        obj = {
            "index": i,
            "tags": t
        }
        tagManager.binds.append(obj)
    def get(i):
        for j in range (0, len(tagManager.binds)):
            if tagManager.binds[j]["index"] == i:
                return tagManager.binds[j]["tags"]
        raise IndexError("[unrecoverable] Could not match searched ID for " + str(i))
class textureManager():
    binds = []
    def append(i,t):
        obj = {
            "index": i,
            "texture": t
        }
        textureManager.binds.append(obj)
    def get(i):
        for j in range (0, len(textureManager.binds)):
            if textureManager.binds[j]["index"] == i:
                return textureManager.binds[j]["texture"]
class display():
    def __init__(self, sizeX, sizeY):
        #Init Frame
        self.frame = Tk()
        self.frame.geometry(str(sizeX*20) + "x" + str(sizeY*20 + 80)) #TODO: add Item Interface
        self.frame.resizable(0,0)
        self.frame.title("Plant the Beta")
        self.width = sizeX*20
        self.height = sizeY*20
        self.canvas = Canvas(self.frame, width=self.width, height = self.height, highlightthickness=0)
        self.canvas.pack(expand=YES, fill= BOTH)
        self.canvas.place(x = 0, y = 80)
        self.updateTasks = []
        #Preload Textures
        path = str(pathlib.Path(__file__).parent.absolute()) + "/textures/"
        files = os.listdir(path)
        self.textures = []
        for i in range(0, len(files)):
            self.textures.append(PhotoImage(file="textures/" + files[i])) 
        self.running = False
        self.inventory = Inventory(self, self.frame)
    def getDimensions(self):
        return (self.width,self.height)
    def kill(self):
        self.running = False
    def collectTextures(self):
        return self.textures
    def drawImage(self, x, y,image):
        return self.canvas.create_image(x*20+10, y*20 +10,  image=self.textures[image]) 
    def move(self,obj ,vx,vy):
        self.canvas.move(obj, vx*20,vy*20)
    def remove(self, obj):
        try:
            if not self.canvas.winfo_exists():
                return
            self.canvas.delete(obj)
        except TclError:
            pass
    def bindKey(self,key, e, *args):
        self.frame.bind(key, lambda event: e(*args))
    def update_game(self):
        for func in self.updateTasks:
            func()
    def addTask(self,task):
        self.updateTasks.append(task)
    def boot(self,framerate):
        dly = (1/framerate)
        self.running = True
        while self.running:
            start = time.time()*1000
            self.frame.update_idletasks()
            self.frame.update()
            self.update_game()
            #time.sleep(dly)
            end = time.time()*1000
            #print(end-start)
            while (end-start) < 39.5:
                end = time.time()*1000
            #ext = time.time()*1000
            #print(ext-start)
class block():
    def __init__(self, world,display, x,y,i,texture):
        self.idx = i
        self.display = display
        self.x = x
        self.y = y
        self.tags = tagManager.get(self.idx)
        self.world = world
        if texture != None:
            self.texture = self.display.drawImage(self.x,self.y,texture)
    def remove(self,doVoid=True):
        self.display.remove(self.texture)
        if "drops" in self.tags:
            a = random.randint(0,1)
            if a == 1:
                self.world.replace_block(self.x,self.y,item(self.world,self.display,self.x,self.y,0,1000))
            else:
                if doVoid:
                    self.world.replace_block(self.x,self.y,block(self.world,self.display,self.x,self.y,-1,None))
        else:
            if doVoid:
                self.world.replace_block(self.x,self.y,block(self.world,self.display,self.x,self.y,-1,None))
class randomizer():
    def __init__(self,seedA,seedB):
        self.seedA = seedA
        if seedA == seedB:
            self.seedSet = True
        else:
            self.seedSet = False
        self.seed = random.randint(seedA,seedB)
        self.nuke = False
    def getTexture(self):
        if (random.randint(0,1000) == 0 and not self.seedSet) or (self.seedSet and self.seedA == 0):
            self.nuke = True
            return 24
        if (self.seed < 40):
            return  18 #4 % Dynamite 
        elif (self.seed >= 40 and self.seed < 70):
            return 14 #3 % Health+ 
        elif (self.seed >= 70 and self.seed < 100): #change
            return 21 #3 % Sword ++
        elif (self.seed >= 100 and self.seed  < 220):
            return 16 #12% Timed Bomb
        elif (self.seed >= 220 and self.seed < 350):
            return 19
        elif (self.seed >= 350 and self.seed < 620):
            return 12 #27% bomb+ 
        elif (self.seed >= 620 and self.seed < 890):
            return 10 #27% exp + 
        elif (self.seed >= 890 and self.seed < 1001):
            return 22 #11%  Curse
    def bomb(player):
        player.inventory["total"] += 1
    def time(player):
        player.inventory["timed_bombs"] += 1
    def dyn(player):
        player.inventory["dynamite"] += 1
    def sword(player):
        player.inventory["damage"] += 1
    def curse(player):
        c = random.randint(1,4)
        if player.curse == "shield":
            player.curse_cooldown = 0
        if c == 1:
            player.curse = "short"
            player.curse_cooldown += int(player.curse_cooldown/5)
            player.curse_cooldown += 125
        elif c == 2:
            player.curse = "long"
            player.curse_cooldown += int(player.curse_cooldown/5)
            player.curse_cooldown += 125
        elif c == 3: 
            player.curse = "useless"
            player.curse_cooldown += int(player.curse_cooldown/5)
            player.curse_cooldown += 125
        elif c == 4:
            player.curse = "spray"
            player.curse_cooldown += int(player.curse_cooldown/5)
            player.curse_cooldown += 125
            player.inventory["total"] += 2
    def rg(player):
        player.inventory ["exp_range"] += 1
    def health(player):
        player.health += 1
    def nuke(player):
        player.inventory["nukes"] += 1
    def shield(player):
        player.curse = "shield"
        player.curse_cooldown = 125
    def getCollectionFunction(self):
        if self.nuke:
            return randomizer.nuke
        if (self.seed < 40):
            return  randomizer.dyn
        elif (self.seed >= 40 and self.seed < 70):
            return randomizer.health
        elif (self.seed >= 70 and self.seed < 100):
            return randomizer.sword
        elif (self.seed >= 100 and self.seed  < 220):
            return randomizer.time
        elif (self.seed >= 220 and self.seed < 350):
            return randomizer.shield
        elif (self.seed >= 350 and self.seed < 620):
            return randomizer.bomb
        elif (self.seed >= 620 and self.seed < 890):
            return randomizer.rg
        elif (self.seed >= 890 and self.seed < 1001):
            return randomizer.curse
class item(block):
    def __init__(self,world,display,x,y,seedA,seedB):
        self.randomizer = randomizer(seedA,seedB)
        texture = self.randomizer.getTexture()
        super().__init__(world,display,x,y,5,texture)
        self.cf = self.randomizer.getCollectionFunction()
    def collect(self, player):
        self.cf(player)
        self.remove()
#Enemy Class
#WARNING [SECTION UNDER CONSTRUCTION]
class enemy(block):
    amount = 0
    enemy_init = False
    def __init__(self,world,display,x,y,health=1,attackbox=[]):
        super().__init__(world,display,x,y,6,2)
        enemy.enemy_init = True
        self.health = health
        self.mhealth = health
        self.attackbox = attackbox
        self.healthbar = None
        self.healthbar_display_cooldown = 0
        self.ctype = 0
        enemy.amount += 1
        self.i = None
        self.replace = True
        self.movement_countdown = 10
        self.cpx = 0
        self.cpy = 0
        self.path = []
    def damage(self, amount=1,useless="DO_NOT_USE_THIS_PARAMETER"):
        self.health -= amount
        if self.healthbar == None:
            self.healthbar = self.display.canvas.create_rectangle(self.x*20,self.y*20+17,self.x*20+(int(20*(self.health/self.mhealth))),self.y*20+20,fill="black",outline="black",width=0)
        else:
            x1,y1,x2,y2 = self.display.canvas.coords(self.healthbar)
            x2 = self.x*20+(int(20*(self.health/self.mhealth)))
            self.display.canvas.coords(self.healthbar, x1,y1,x2,y2)
        self.healthbar_display_cooldown = 100
        if self.health <= 0:
            enemy.amount -= 1
            #print(enemy.amount)
            self.display.canvas.delete(self.healthbar)
            #print("Enemy, new",enemy.amount)
            if enemy.amount <= 0:
                #print("YOU WIN")
                self.world.win()
                return False
            if self.i != None:
                self.world.blocks[self.x][self.y] = self.i
                self.remove(False)
            else:
                self.remove()
            #return False
    #Movr function
    def another_one(self):
        def delta(a,b):
            x1,y1 = a
            x2,y2 = b
            return abs(x1-x2)+abs(y1-y2)
        if self.cpx != self.world.p.x or self.cpy != self.world.p.y:
            self.cpx = self.world.p.x
            self.cpy = self.world.p.y
        else:
            return False
        goal = (self.cpx,self.cpy)
        path = []
        visited = [(self.x,self.y)] # (x,y)
        costs = [0]
        r = True
        frontiers = [(self.x,self.y,0)]
        while r:
            fts = []
            while len(frontiers) > 0:
                x,y,c = frontiers.pop(0)
                for ox in range (-1,2):
                    for oy in range (-1,2):
                        if (ox==0 or oy == 0) and (ox != 0 or oy != 0):
                            if (x+ox,y+oy) == goal:
                                #print("PLAYER FOUND")
                                cc = c+1
                                path.append((self.cpx,self.cpy))
                                while cc > 0:
                                    for i in range (len(visited)-1,-1,-1):
                                        o = visited[i]
                                        c = costs[i]
                                        if delta(o, path[-1]) == 1 and c == cc-1:
                                            path.append(o)
                                            cc -= 1
                                path.pop()
                                return path
                            if (x+ox,y+oy) not in visited and "solid" not in self.world.blocks[x+ox][y+oy].tags:
                                visited.append((x+ox,y+oy))
                                fts.append((x+ox,y+oy,c+1))
                                costs.append(c+1)
            if len(fts) > 0:
                frontiers = fts[:]
                #print(frontiers)
            else:
                return None
    def try_pathfind(self):
        self.another_one()
        if self.cpx != self.world.p.x or self.cpy != self.world.p.y:
            self.cpx = self.world.p.x
            self.cpy = self.world.p.y
        else:
            return False
        def delta(a,b):
            xa,ya = a
            xb,yb = b
            r = abs(xb-xa) + abs(yb-ya)
            return r
        path = [(self.x,self.y)]
        goal = (self.cpx,self.cpy)
        visited = [(self.x,self.y)]
        cost = 0
        #Deep first search Algorith for pathfinding
        #1. Go the cheapest path until end
        #2. If path succeeds return path
        #3. If path fails (no unvisited n left) -> step 4
        #4. Backtrack unil unvisited n are left
        #5. If stack is empty -> failure
        #6. return to step 1
        while len(path) > 0:
            #pop cell from stack
            x, y = path.pop()
            nb = []
            #Collect all possible neighbours
            for ox in range (-1,2):
                for oy in range (-1,2):
                    if (ox != 0 or oy != 0) and (ox == 0 or oy == 0):
                        #No check for walls, since it is impossible to land on 
                        cx = x + ox
                        cy = y + oy
                        if "solid" not in self.world.blocks[cx][cy].tags and (cx,cy) not in visited or (cx == self.world.p.x and cy == self.world.p.y):
                            #print(self.world.blocks[14][20].tags)
                            nb.append((cx,cy))
            if len(nb) > 0:
                #Push current back to stack
                path.append((x,y))
            if len(nb) < 1:
                a = 0
            else:
                d = []
                for i in range (0, len(nb)):
                    d.append(delta((x,y),nb[i]))
                m = d[0]
                mi = 0
                for i in range (0, len(d)):
                    if d[i] < m:
                        mi = i
                        m = d[i]
                if nb[mi] == goal:
                    path.append(nb[mi])
                    path.pop(0)
                    return path
                else:
                    path.append(nb[mi])
                    visited.append(nb[mi])
        return None
    def automove(self):
        p = self.another_one()
        #print(p)
        if p == False:
            if len(self.path) > 0:
                px, py = self.path.pop()
            else:
                px,py = self.world.p.x,self.world.p.y
        elif p != [] and p != None:
            self.path = p
            if len(self.path) > 0:
                px,py = self.path.pop()
            else:
                px,py = self.world.p.x,self.world.p.y
        else:
            px,py = self.world.p.x,self.world.p.y
        avd = False
        for ox in range (-1,2):
            for oy in range (-1, 2):
                if self.x + ox < 25 and self.x + ox > -1 and self.y + oy < 25 and self.y + oy > -1:
                    if (ox != 0 or oy != 0) and (ox == 0 or oy == 0):
                        if self.world.blocks[self.x+ox][self.y+oy].idx == 8:
                            avd = True
                            break
        if avd:
            if ox != 0 and oy != 0:
                oy = 0
            if self.move(-1*ox,-1*oy):
                return
        #player coords
        
        #Direction vectors
        tx = px - self.x
        ty = py - self.y
        #print(tx,ty)
        if tx != 0:
            x = int(abs(tx)/tx)
        else:
            x = 0
        if ty != 0:
            y = int(abs(ty)/ty)
        else:
            y = 0
        if abs(tx) > abs(ty):
            if not self.move(x,0):
                self.move(0,y)
        else:
            if not self.move(0,y):
                self.move(x,0)
    def move(self,vx,vy):
        buffer_block = None
        if "solid" not in self.world.blocks[self.x+vx][self.y+vy].tags and (self.x+vx != self.world.p.x or self.y+vy != self.world.p.y):
            #store item
            if "item" in self.world.blocks[self.x+vx][self.y+vy].tags:
                buffer_block = self.world.blocks[self.x+vx][self.y+vy] #bufferitem
            #copy self
            self.world.replace_block(self.x+vx,self.y+vy,self) #clearblock with self
            if self.i != None:    #if stored item
                self.world.replace_block(self.x,self.y,self.i) #place item
            else:
                self.world.replace_block(self.x,self.y,block(self.world,self.display,self.x,self.y,-1,None)) #clear previois
            self.display.move(self.texture,vx,vy)
            self.i = buffer_block #store buffer
            self.x += vx
            self.y += vy
            if self.healthbar != None:
                self.display.canvas.move(self.healthbar,vx*20,vy*20)
            return True
        return False
    def update(self):
        if self.healthbar_display_cooldown > 0:
            self.healthbar_display_cooldown -= 1
        elif self.healthbar != None:
            self.display.canvas.delete(self.healthbar)
            self.healthbar = None
        c = random.randint(0,20)
        if c == 0:
            self.attack()
        if self.movement_countdown <= 0:
            self.automove()
            self.movement_countdown = 10
        else:
            self.movement_countdown -= 1
    def attack(self):
        for obj in self.attackbox:
            nx,ny = obj
            cx = nx + self.x
            cy = ny + self.y
            if "player" in self.world.blocks[cx][cy].tags:
                self.world.blocks[cx][cy].damage()
class player(block):
    def __init__(self,world,display,x,y,health=1):
        super().__init__(world,display,x,y,2,0)
        self.health = health
        self.ctype = -1
        self.replace = True
        self.bombconfig = "basic"
        self.timebombs = []
        self.selectable = ["basic","tnt","time","nuke"]
        self.selector = 0
        self.curse = ""
        self.nuke_overlay = None
        self.curse_overlay = None
        self.overlay_type = ""
        self.curse_cooldown = 0 #125
        self.inventory = {
            "total": 1,
            "exp_range": 2,
            "dynamite": 0,
            "timed_bombs": 0,
            "damage": 1,
            "nukes": 0
        }
        self.paint_inv()
    def damage(self, amount=1, t = "NORMAL"):
        if self.curse == "shield":
            if t == "NORMAL":
                return
            elif t == "NUKE":
                self.health -= int(amount/50)
                self.curse = ""
                self.curse_cooldown = 0
            elif t == "ANTIMATTER":
                self.health -= amount
                self.curse = ""
                self.curse_cooldown = 0
                if self.health > 0:
                    print("You know, shield is useless on this?")
                    print("But OK, you just survived an antimatter explosion")
                    print("so i guess, you got that at least.")
        else:
            self.health -= amount
        if self.health <= 0:
            self.world.loose()
            return False
            #self.remove()
    def edit_inv(self, obj, new):
        self.inventory[obj] = new
    def paint_inv(self):
        try:
            self.display.inventory.setValue(0,self.inventory["total"])
            self.display.inventory.setValue(1,self.inventory["exp_range"]-1)
            self.display.inventory.setValue(2,self.inventory["dynamite"])
            self.display.inventory.setValue(3,self.inventory["timed_bombs"])
            self.display.inventory.setValue(4,self.inventory["nukes"])
            self.display.inventory.setValue(5,self.health)
            self.display.inventory.setValue(6,self.inventory["damage"])
        except TclError:
            return
    def edit_bc(self, new):
        self.bombconfig = new
        if self.bombconfig == "basic":
            self.display.inventory.drawImage(11)
            self.selector = 0
        elif self.bombconfig == "tnt":
            self.display.inventory.drawImage(17)
            self.selector = 1
        elif self.bombconfig == "time":
            self.display.inventory.drawImage(15)
            self.selector = 2
        elif self.bombconfig == "nuke":
            self.display.inventory.drawImage(23)
            self.selector = 3
    def detonate_tb(self):
        for i in range (0, len(self.timebombs)):
            self.timebombs[i].explode()
        self.timebombs = []
    def shift(self, d):
        self.selector += d
        if self.selector < 0:
            self.selector = len(self.selectable)-1
        if self.selector == len(self.selectable):
            self.selector = 0
        self.edit_bc(self.selectable[self.selector])
    def move(self, vx,vy):
        if self.curse_overlay != None:
            self.display.canvas.move(self.curse_overlay,vx*20,vy*20)
        if "solid" not in self.world.blocks[self.x+vx][self.y+vy].tags:
            if "item" in self.world.blocks[self.x+vx][self.y+vy].tags:
                self.world.blocks[self.x+vx][self.y+vy].collect(self)
                self.paint_inv()
            self.world.replace_block(self.x+vx,self.y+vy,self)
            if self.replace:
                self.world.replace_block(self.x,self.y,block(self.world,self.display,self.x,self.y,self.ctype,textureManager.get(self.ctype)))
            if self.nuke_overlay != None:
                self.display.canvas.move(self.nuke_overlay, vx*20,vy*20)
            self.display.move(self.texture,vx,vy)
            self.x += vx
            self.y += vy
            self.replace = True
            if self.world.sl != None:
                for i in range (0, len(self.world.sl.triggers)):
                    if self.world.sl.triggers[i].x == self.x and self.world.sl.triggers[i].y == self.y:
                        self.world.sl.triggers[i].check_collection()
    def update(self):
        if self.curse_cooldown > 0 and self.curse_overlay == None:
            if self.curse == "shield":
                self.curse_overlay = self.display.canvas.create_image(self.x*20+10,self.y*20+10,image=self.display.textures[26])
                self.overlay_type = "c_shield"
            else:
                self.curse_overlay = self.display.canvas.create_image(self.x*20+10,self.y*20+10,image=self.display.textures[1])
                self.overlay_type = "c_normal"
        elif self.curse_cooldown > 0 and self.curse_overlay != None:
            if self.curse == "shield" and self.overlay_type == "c_normal":
                self.display.canvas.delete(self.curse_overlay)
                self.curse_overlay = self.display.canvas.create_image(self.x*20+10,self.y*20+10,image=self.display.textures[26])
                self.overlay_type = "c_shield"
            elif self.curse != "shield" and self.overlay_type == "c_shield":
                self.display.canvas.delete(self.curse_overlay)
                self.curse_overlay = self.display.canvas.create_image(self.x*20+10,self.y*20+10,image=self.display.textures[1])
                self.overlay_type = "c_normal"
        elif self.curse_cooldown <= 0 and self.curse_overlay != None:
            self.display.canvas.delete(self.curse_overlay)
            self.overlay_type = ""
            self.curse_overlay = None
        if self.bombconfig == "nuke" and self.nuke_overlay == None:
            self.nuke_overlay = self.display.canvas.create_image(self.x*20+10,self.y*20+10,image=self.display.textures[25])
        elif self.bombconfig != "nuke" and self.nuke_overlay != None:
            self.display.canvas.delete(self.nuke_overlay)
            self.nuke_overlay = None
        if self.curse_cooldown <= 0:
            if self.curse == "spray":
                self.inventory["total"] -= 2
            self.curse = ""
        else:
            self.curse_cooldown -= 1
            #print(self.curse_cooldown)
        if self.curse == "spray" and self.curse_cooldown % 3 == 0:
            self.place_bomb()
    def place_bomb(self):
        if self.world.blocks[self.x][self.y].idx != 8:
            if self.bombconfig == "basic":
                if self.inventory["total"] > 0:
                    self.replace = False
                    if self.curse == "short":
                        self.world.replace_block(self.x,self.y,bomb(self,self.world,self.display,self.x,self.y,dmg=self.inventory["damage"],length=self.inventory["exp_range"],fuse=10))
                    elif self.curse == "long":
                        self.world.replace_block(self.x,self.y,bomb(self,self.world,self.display,self.x,self.y,dmg=self.inventory["damage"],length=self.inventory["exp_range"],fuse=70))
                    elif self.curse == "useless":
                        self.world.replace_block(self.x,self.y,bomb(self,self.world,self.display,self.x,self.y,dmg=self.inventory["damage"],length=2))
                    else:
                        self.world.replace_block(self.x,self.y,bomb(self,self.world,self.display,self.x,self.y,dmg=self.inventory["damage"],length=self.inventory["exp_range"]))
                    self.inventory["total"] -= 1
            elif self.bombconfig == "tnt":
                if self.inventory["dynamite"] > 0:
                    self.replace = False
                    if self.curse == "short":
                        self.world.replace_block(self.x,self.y,bomb(self,self.world,self.display,self.x,self.y,dmg=self.inventory["damage"],explosion=EXPLOSION.SQUARE,texture=17,fuse=10))
                    elif self.curse == "long":
                        self.world.replace_block(self.x,self.y,bomb(self,self.world,self.display,self.x,self.y,dmg=self.inventory["damage"],explosion=EXPLOSION.SQUARE,texture=17,fuse=70))
                    else:
                        self.world.replace_block(self.x,self.y,bomb(self,self.world,self.display,self.x,self.y,dmg=self.inventory["damage"],explosion=EXPLOSION.SQUARE,texture=17))
                    self.inventory["dynamite"] -= 1
            elif self.bombconfig == "time":
                if self.inventory["timed_bombs"] > 0:
                    self.replace = False
                    b = bomb(self,self.world,self.display,self.x,self.y,fuse=1000000,dmg=self.inventory["damage"],length=self.inventory["exp_range"],texture=15)
                    self.timebombs.append(b)
                    self.world.replace_block(self.x,self.y,b)
                    self.inventory["timed_bombs"] -= 1
            elif self.bombconfig == "nuke":
                if self.inventory["nukes"] > 0:
                    self.replace = False
                    b = bomb(self,self.world,self.display,self.x,self.y,fuse=78840000000,dmg=self.inventory["damage"],explosion=EXPLOSION.NUKE,texture = 23)
                    self.world.replace_block(self.x,self.y,b)
                    self.inventory["nukes"] -= 1
            self.paint_inv()
        else:
            return
class Inventory():
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.canvas = Canvas(self.master, width=self.parent.width,height=80)
        self.canvas.pack(expand=YES, fill= BOTH)
        self.canvas.place(x = 0, y = 0)
        self.whiteSquare = self.canvas.create_rectangle(475,60,495,80,fill="white",outline="red", width="3")
        self.main_text = self.canvas.create_text(250,70,text="", font="Calibri 15", width=500, justify="center")
        self.image = None
        self.normal = 11
        self.tnt = 17
        self.time = 15
        self.items = []
        self.backgrounds = []
        self.images = []
        self.texts = []
        self.textdata = ["Moin", "Servus"]
        self.drawImage(self.normal)
        self.addIcon(self.normal) #0
        self.addIcon(9)
        self.addIcon(self.tnt)
        self.addIcon(self.time)
        self.addIcon(23)
        self.addIcon(13)
        self.addIcon(20)
    def showText(self, index):
        self.canvas.itemconfig(self.main_text, text=self.textdata[index])
    def clear_screen(self):
        for img in self.images:
            for background in self.backgrounds:
                for text in self.texts:
                    self.canvas.delete(img)
                    self.canvas.delete(background)
                    self.canvas.delete(text)
        self.backgrounds = []
        self.images = []
        self.texts = []
    def setValue(self, iconIndex, value):
        self.canvas.itemconfig(self.texts[iconIndex], text=value)
    def addIcon(self, texture):
        self.clear_screen()
        self.items.append(self.parent.textures[texture])
        for i in range(len(self.items)):
            place = 500/(len(self.items)+1)
            self.backgrounds.append(self.canvas.create_rectangle((i+1)*place-10,10,(i+1)*place+10,30,fill="white",outline="black"))
            self.images.append(self.canvas.create_image((i+1)*place, 20, image = self.items[i]))
            self.texts.append(self.canvas.create_text((i+1)*place, 45, text = "0", font="Calibri 15"))
    def drawImage(self, texture):
        if self.image != None:
            self.canvas.delete(self.image)
        self.image = self.canvas.create_image(485,70,image=self.parent.textures[texture])
class EXPLOSION():
    def BASIC(world,display,dmg,x,y,length):
        results = []
        def explode_vec(vx,vy):
            fresults = []
            for m in range (0,length):
                cx = x + vx*m
                cy = y + vy*m
                if "alive" in world.blocks[cx][cy].tags or (world.p.x == cx and world.p.y == cy):
                    if (world.p.x == cx and world.p.y == cy):
                        if world.p.damage(dmg) == False:
                            return ["_E"]
                    else:
                        if "alive" in world.blocks[cx][cy].tags:
                            world.blocks[cx][cy].damage(dmg)
                            if enemy.amount <= 0:
                                return ["_E"]
                        #except AttributeError:
                        #    print("Tried to call damage function of " + str(type(world.blocks[cx][cy]))) 
                if "breakable" in world.blocks[cx][cy].tags:
                    solid = "blocking" in world.blocks[cx][cy].tags
                    world.blocks[cx][cy].remove()
                    if solid and m != 0:
                        fresults.append(display.drawImage(cx,cy,9))
                        return fresults
                if "blocking" in world.blocks[cx][cy].tags and m!=0:
                    return fresults
                if "bomb" in world.blocks[cx][cy].tags:
                    world.blocks[cx][cy].fuse = 1
                try:
                    fresults.append(display.drawImage(cx,cy,9))
                except TclError:
                    #print("ERRO")
                    return []
            return fresults
        results += explode_vec(1,0)
        if "_E" in results:
            return
        results += explode_vec(-1,0)
        if "_E" in results:
            return
        results += explode_vec(0,1)
        if "_E" in results:
            return
        results += explode_vec(0,-1)
        ##print(results)
        if results == ["_E","_E","_E","_E"]:
            return False
        return results
    def SQUARE(world,display,dmg,x,y,null):
        results = []
        for a in range (-2,3):
            for b in range (-2,3):
                cx = x + a
                cy = y + b
                if cx > -1 and cx < 25 and cy > -1 and cy < 25:
                    if "alive" in world.blocks[cx][cy].tags or (world.p.x == cx and world.p.y == cy):
                        if (world.p.x == cx and world.p.y == cy):
                            if world.p.damage(dmg*2) == False:
                                return False
                            world.p.paint_inv()
                        elif "alive" in world.blocks[cx][cy].tags:
                            if world.blocks[cx][cy].damage(dmg*2) == False:
                                return False
                    if "breakable" in world.blocks[cx][cy].tags:
                        world.blocks[cx][cy].remove()
                    if "bomb" in world.blocks[cx][cy].tags:
                        world.blocks[cx][cy].fuse = 1
                    results.append(display.drawImage(cx,cy,9))
        return results
    def NUKE(world, display, dmg, x,y,null):
        results = []
        for a in range (-10,11):
            for b in range (-10,11):
                cx = x + a
                cy = y + b
                if cx > -1 and cx < 25 and cy > -1 and cy < 25:
                    if "alive" in world.blocks[cx][cy].tags or (world.p.x == cx and world.p.y == cy):
                        if (world.p.x == cx and world.p.y == cy):
                            if world.p.damage(dmg*5,"NUKE") == False:
                                return False
                            world.p.paint_inv()
                        elif "alive" in world.blocks[cx][cy].tags:
                            if world.blocks[cx][cy].damage(dmg*5,"NUKE") == False:
                                return False
                    if "breakable" in world.blocks[cx][cy].tags:
                        world.blocks[cx][cy].remove()
                    if "bomb" in world.blocks[cx][cy].tags:
                        world.blocks[cx][cy].fuse = 1
                    results.append(display.drawImage(cx,cy,9))
        return results
    def ANTIMATTER(world, display, dmg, x,y,null):
        results = []
        for a in range (-1,2):
            for b in range (-1,2):
                cx = x + a
                cy = y + b
                if cx > 0 and cx < 24 and cy > 0 and cy < 24:
                    if "alive" in world.blocks[cx][cy].tags or (world.p.x == cx and world.p.y == cy):
                        if (world.p.x == cx and world.p.y == cy):
                            if world.p.damage((dmg**2)*20, "ANTIMATTER") == False:
                                return False
                            world.p.paint_inv()
                        elif "alive" in world.blocks[cx][cy].tags:
                            if world.blocks[cx][cy].damage((dmg**2)*20,"ANTIMATTER") == False:
                                return False
                    if world.blocks[cx][cy].tags != ["air"] and "alive" not in world.blocks[cx][cy].tags and "bomb" not in world.blocks[cx][cy].tags and(a != 0 or b != 0):
                        world.blocks[cx][cy].remove()
                    if "bomb" in world.blocks[cx][cy].tags:
                        world.blocks[cx][cy].fuse = 1
                    results.append(display.drawImage(cx,cy,9))
        return results
class bomb(block):
    def __init__(self,parent,world,display,x,y,fuse=35,explosion=EXPLOSION.BASIC,dmg=1,duration=10,texture=11,length=20):
        super().__init__(world,display,x,y,8,texture)
        self.flames = []
        self.fuse = fuse
        self.explosion = explosion
        self.dmg = dmg
        self.duration = duration
        self.exploded = False
        self.length = length
        self.parent = parent
        self.t  = False
        self.state_forcequit = False
        if self.fuse > 10000:
            self.t = True
    def explode(self):
        self.fuse = 0
    def update(self):
        if not self.exploded:
            self.fuse -= 1
            if self.fuse <= 0:
                self.flames = self.explosion(self.world,self.display,self.dmg,self.x,self.y,self.length)
                if self.flames == False:
                    self.state_forcequit = True
                    return False
                self.remove(doVoid=False)
                self.exploded = True
                if self.explosion == EXPLOSION.BASIC and not self.t:
                    self.parent.inventory["total"]+= 1
                    self.parent.paint_inv()
                ##print("Exploded")
        else:
            if self.state_forcequit:
                return False
            self.duration -= 1
            if self.duration <= 0:
                for i in range (0, len(self.flames)):
                    self.display.remove(self.flames[i])
                self.world.replace_block(self.x,self.y,block(self.world,self.display,self.x,self.y,-1,None))
class world():
    def __init__(self, display, gmm, nw):
        self.display = display
        self.gamemenu = gmm
        self.newWorld = nw
        self.width, self.height = self.display.getDimensions()
        self.blocks = []
        self.p = None
        self.sl = None
        self.name = None
        self.tetxs = None
        self.update_c = True
        for x in range (0, int(self.width/20)):
            buffer = []
            for y in range (0, int(self.height/20)):
                buffer.append(None)
            self.blocks.append(buffer)
        self.display.addTask(self.update)
        self.display.addTask(self.check_enemy_death)
    def check_enemy_death(self):
        if enemy.enemy_init:
            for x in range (0, len(self.blocks)):
                for y in range (0, len(self.blocks[x])):
                    if self.blocks[x][y].idx == 6:
                        return
            self.win()
    def win(self):
        if self.newWorld:
            self.gamemenu.progress += 1
        self.ext()
    def loose(self):
        self.ext()
    def ext(self):
        self.display.frame.destroy()
        self.display.kill()
        self.gamemenu.resume()
        self.display.updateTasks = []
        self.update_c = False
        return
    def genDefault(self):
        for x in range (0, int(self.width/20)):
            for y in range (0, int(self.height/20)):
                if (x%2==0 and y%2==0) or (x%2!=0 and y%2!=0):
                    self.display.drawImage(x,y,6)
                else:
                    self.display.drawImage(x,y,7)
    def create_background(self, gen_f=None):
        if gen_f == None:
            gen_f = self.genDefault
        gen_f()
    def update(self):
        for x in range (0, len(self.blocks)):
            for y in range (0, len(self.blocks[x])):
                if self.update_c:
                    if "update" in self.blocks[x][y].tags:
                        if self.blocks[x][y].update() == False:
                            return
                else:
                    return
        self.p.update()
    def replace_block(self,x,y,new):
        self.blocks[x][y] = new
    def loadFromFile(self,path):
        c = comp.compressor()
        c.load("maps/"+path+".ptb")
        c.decompress()
        content, s, z = c.get_data()
        self.sl = scriptLoader(s,self)
        data = content["world"]
        self.name = path
        self.texts = content["texts"]
        print(self.texts)
        self.display.inventory.textdata = self.texts
        for x in range (0, int(self.width/20)):
            for y in range (0, int(self.height/20)):
                ##print(data[x][y])
                if data[x][y]["id"] == 6:
                    self.blocks[x][y] = enemy(self,self.display,x,y,data[x][y]["objectData"]["health"],ATTACK.callType(data[x][y]["objectData"]["id2"]))
                elif data[x][y]["id"] == 5:
                    self.blocks[x][y] = item(self,self.display,x,y,data[x][y]["objectData"]["start"],data[x][y]["objectData"]["fin"])
                elif data[x][y]["id"] == 2:
                    self.p = player(self,self.display,x,y)
                    self.blocks[x][y] = self.p
                    self.display.bindKey("w", self.p.move, 0,-1)
                    self.display.bindKey("s", self.p.move, 0,1)
                    self.display.bindKey("a", self.p.move, -1,0)
                    self.display.bindKey("d", self.p.move, 1,0)
                    self.display.bindKey("<space>",self.p.place_bomb,)
                    self.display.bindKey("q",self.p.edit_bc, "tnt")
                    self.display.bindKey("e",self.p.edit_bc, "basic")
                    self.display.bindKey("f",self.p.edit_bc, "time")
                    self.display.bindKey("r",self.p.edit_bc, "nuke")
                    self.display.bindKey("#",self.p.detonate_tb,)
                    self.display.bindKey("<Left>",self.p.shift,-1)
                    self.display.bindKey("<Right>",self.p.shift,1)
                    #self.display.bindKey("k",self.win,)
                    self.display.bindKey("<Escape>",self.ext,)
                    self.display.bindKey("c",randomizer.curse,self.p)
                    self.display.frame.protocol("WM_DELETE_WINDOW", self.ext)                        
                else:
                    self.blocks[x][y] = block(self, self.display, x,y,data[x][y]["id"],textureManager.get(data[x][y]["id"])) #0 to be replaced with texturemanager
        if self.sl != None:
            self.sl.on_init()
class game():
    def __init__(self,usr,pas,prg,sizeX,sizeY,maps):
        if len(maps) > sizeX*sizeY:
            raise IndexError("Could not load World for " + str(maps) + "; Reason: cannot match all maps to buttons")
        for i in range (0, len(maps)):
            if type(maps[i]) != type(""):
                raise IOError(str(maps[i])+" is not a Valid Path")
            if not os.path.exists("maps/" + maps[i] + ".ptb"):
                raise IOError("Could not verify World " + maps[i])
        if usr == "e22c04ba0ddf6454d4076cbefd287fe1":
            EXPLOSION.SQUARE = EXPLOSION.ANTIMATTER
        self.frameSizeY = 20 + sizeY * 30
        self.frameSizeX = 15 + sizeX*30
        self.sizeX = sizeX 
        self.sizeY = sizeY
        self.progress = prg
        self.maps = maps
        self.usr = usr
        self.pas = pas
        self.continue_state_flag = False
        if self.frameSizeX < 35:
            self.frameSizeX = 35
        self.selection_menu = None
        self.buttons = []
        self.running = False
        self.nextlevel = ""
        self.nw = False
        self.loop()
    def ext(self):
        self.save()
        self.selection_menu.destroy()
        self.running = False
        #raise RuntimeError("Test error")
    def boot(self):
        self.selection_menu = Tk()
        self.selection_menu.geometry(str(self.frameSizeX) + "x" + str(self.frameSizeY))
        self.selection_menu.resizable(0,0)
        self.selection_menu.bind("s",lambda event:[self.save()])
        self.buttons = []
        self.running = True
        self.nextlevel = ""
        self.nw = False
        for i in range (0, len(self.maps)):
            self.buttons.append(levelbutton(self,i,i%self.sizeX,int(i/self.sizeY)))
        self.selection_menu.protocol("WM_DELETE_WINDOW", self.ext)
    def save(self):
        path = "saves/" + self.usr + ".txt"
        file = open(path, "w")
        file.write(crypto.encode(str(self.progress),self.pas))
    def loop(self):
        #Create Window
        while True:
            self.save()
            self.boot()
            ##print("should show loop")
            self.running = True
            self.selection_menu.mainloop()
            #End of Loop: collect Information for level bootup...
            if  not self.running:
                ##print("QUIT")
                return
            d = display(25,25)
            w = world(d,self,self.nw)
            w.create_background()
            w.loadFromFile(self.nextlevel)
            w.display.boot(25)
            #print("Process End")
        ##print(self.nextlevel,self.nw)
    def boot_world(self,i,x):
        self.nextlevel = i
        self.nw = x
        self.selection_menu.destroy()
    def resume(self):
        self.continue_state_flag = True
class levelbutton(Button):
    def __init__(self,parent,i,x,y):
        self.parent = parent
        self.mp = self.parent.maps[i]
        self.b = "red"
        if self.parent.progress == i:
            self.b = "white"
        elif self.parent.progress > i:
            self.b = "green"
        s = "active"
        if self.parent.progress < i:
            s = "disabled"
        nl = False
        if self.parent.progress == i:
            nl = True
        super().__init__(self.parent.selection_menu,activebackground=self.b,bg=self.b,state=s,text=i,command=functools.partial(self.parent.boot_world,self.parent.maps[i],nl))
        self.place(x=x*30+10,y=y*30+25,width=20,height=20)
class login():
    def __init__(self,args):
        self.login = Tk()
        self.login.geometry("250x100")
        self.login.resizable(0,0)
        self.login.title("Login")
        self.welcome = Label(self.login, text = "Enter Username and Password", font="Calibri 11")
        self.welcome.place(x=35, y=0)
        self.login.bind("<Return>",lambda ev: [self.try_login()])
        #Username 
        self.ulabel = Label(self.login, text = "Username:", font="Calibri 9")
        self.ulabel.place(x=0,y=20)
        self.username = Entry(self.login, font="Calibri")
        self.username.place(x=65, y=20, width = 185, height = 20)
        #Password
        self.plabel = Label(self.login, text = "Password:", font="Calibri 9")
        self.plabel.place(x=0,y=40)
        self.password = Entry(self.login,  show="*", font="Calibri")
        self.password.place(x=65, y=40, width = 185, height = 20)
        self.submit = Button(self.login, text="Submit", font="Calibri", command = lambda: [self.try_login()])
        self.submit.place(x=10,y=65, width = 230, height = 30)
        self.g = None
        self.args = args
        self.login.mainloop()
    def try_login(self):
        usr = self.username.get()
        uus = usr
        pas = self.password.get()
        #Verify Data
        if len(pas) < 4:
            messagebox.showwarning("ERROR", "Password has to contain at least 4 Digits")
            return
        if len(usr) < 1:
            messagebox.showwarning("ERROR", "Username has to contain at least 1 Digit")
            return
        usr = hashlib.md5(usr.encode()).hexdigest()
        file = "saves/" + usr + ".txt"
        if not os.path.isdir("saves"):
            os.mkdir("saves")
        if os.path.exists(file):
            pass
        else:
            #print("User not found")
            #print("Attempt Register")
            confirm = messagebox.askquestion("WARNING", "You CANNOT change or recover your USERNAME or PASSWORD after registering!!! \n Continue?")
            if confirm == "yes":
                messagebox.showinfo("REGISTER", "You have been registered") #TODO add registry
                open(file,"w").write(crypto.encode("0", pas))
                self.login.destroy()
                a,b,c = self.args
                g = usr
                h = pas
                self.args = (g,h,0,a,b,c)
                #print(self.args)
                self.g = game(*self.args)
                return
            else:
                return
        try:
            content = int(crypto.decode(open(file).read(),pas))
        except Exception:
            messagebox.showwarning("ERROR", "Invalid password")
            return
        self.login.destroy()
        a,b,c = self.args
        g = usr
        h = pas
        self.args = (g,h,content,a,b,c)
        #print(self.args)sd
        self.g = game(*self.args)
#PreInit, static, just load once at startup
tagManager.append(-1,["air"])#air
tagManager.append(0,["solid","blocking"]) #bedrock
tagManager.append(3,["solid","blocking","breakable","drops"]) #brick ss
tagManager.append(2,["solid","alive","player"]) #player todo
tagManager.append(6,["solid","alive","update"]) #enemy
tagManager.append(5,["blocking","breakable","item"]) #item
tagManager.append(4,["solid"]) #water 
tagManager.append(8,["solid","update","bomb"]) #bombs
tagManager.append(7,[])
textureManager.append(-1,None)
textureManager.append(0,4)
textureManager.append(3,3)
textureManager.append(4,5)

l = login((10,10,["tutorial"]+[f"level{i}" for i in range(1,7)]))
#f = game(0,(10,10,["maps/level1.json","maps/level2.json"]))
#Init, actually create eviroment and world, use for each level
