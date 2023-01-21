from tkinter import *
import json
import time
import random
import os
import pathlib
def to_bin(value, length):
    bits = []
    for i in range (0, length):
        x = length-i-1
        if value >= 2**x:
            value -= 2**x
            bits.append(1)
        else:
            bits.append(0)
    return bits
def to_dez(value):
    length = len(value)
    dez = 0
    for i in range (0, length):
        x = length-1-i
        if value[i] == 1:
            dez += 2**x
    return dez
long_fuse = False
short_fuse = False
short_exp = False
sonic_speed = False
snail_speed = False
poop_mode = False
dynamite_used = False
timebomb_used = False
smoke_used = False
curse_life = 0
exp_range = 2
file = "test.json"
data = json.loads(open(file, "r").read())["world"]
path = str(pathlib.Path(__file__).parent.absolute()) + "/textures/"
files = os.listdir(path)
addpath = "textures/"
print(files)
enemy = []
entity = []
tile = []
master = Tk()
master.title("Plant_The_Bomb")
width = len(data)*20
height = len(data)*20
master.geometry((str(width) + 'x' + str(height + 80)) + '+10+10')
class Enemy():
    def __init__(self, pos, type, health, extra1, extra2, w):
        global enemy
        enemy.append(True)
        self.x, self.y = pos
        #Multiple Texures for multiple Types
        self.obj = w.create_image(self.x*20+10, self.y*20+10, image=textures[20])
        self.hitbox = [(0,0)] #Multiple for Multiple Types
        self.health = health
        self.reg = len(enemy)-1
    def damage(self):
        self.health -= 1
        global w, enemy
        if (self.health <= 0):
            w.delete(self.obj)
            enemy[self.reg] = False
            data[self.x][self.y] = -1

w = Canvas(master, width=width, height = height)
w.pack(expand=YES, fill= BOTH)
w.place(x = 0, y = 80)

inv = Canvas(master,width=width, height =80)
inv.pack(expand=YES, fill= BOTH)
inv.place(x = 0, y = 0)

textures = []
for i in range(0, len(files)):
    textures.append(PhotoImage(file=addpath + files[i]))

files[0]
                    
colit = [textures[8], textures[4], textures[13],textures[6], textures[14], textures[18]]
colita = []
text = []
print(textures)
for j in range(1, len(colit) + 1):
    a = (width -(len(colit)*20))/(len(colit)+1)
    if j == 1:
        colita.append(0)
        inv.create_image(j*a,15, image = textures[3])
        inv.create_image(j*a,15, image = colit[j-1])
        text.append(inv.create_text(j*a,40, text= colita[j-1],fill="black",font=('Calibri 15')))
    else:
        colita.append(0)
        inv.create_image((j*a)+20*(j-1),15, image = textures[3])
        inv.create_image((j*a)+20*(j-1),15, image = colit[j-1])
        text.append(inv.create_text((j*a)+20*(j-1),40, text = colita[j-1],fill="black",font=('Calibri 15')))
        
message = inv.create_text(len(data)*20/2, 60, state = "hidden", text="Default", fill="red", font=('Calibri 15'))
def change_message(text, mode):
    if mode == 0:
        inv.itemconfigure(message, state = "hidden")
    elif mode == 1:
        inv.itemconfigure(message, text = text, state = "normal")
        
        
def update_item(pos, mode, val):
    if mode == 0:
        colita[pos] += val
    elif mode == 1:
        colita[pos] -= val
    elif mode == 2:
        colita[pos] = val
    for l in range(0, len(colit)):
        inv.itemconfigure(text[l], text=colita[l])

for i in range(0, len(data)):
    for j in range(0, len(data)):
        if j % 2 ==0 or i % 2 == 0:
            w.create_image(i*20+10, j*20 +10,  image=textures[9])
        else:
            w.create_image(i*20+10, j*20 +10,  image=textures[10])
            
print (data)
for i in range (0, len(data)):
    apd = []
    for j in range (0, len(data[i])):
        if (data[i][j]["id"] == 0):
            apd.append(w.create_image(i*20+10, j*20 +10,  image=textures[7]))
        elif (data[i][j]["id"] == 2):
            start = (i,j)
            apd.append(w.create_image(i*20+10, j*20 +10,  image=textures[10]))
        elif (data[i][j]["id"] == 3):
            apd.append(w.create_image(i*20+10, j*20 +10,  image=textures[15]))
        elif (data[i][j]["id"] == 4):
            apd.append(w.create_image(i*20+10, j*20 +10,  image=textures[10]))
        elif (data[i][j]["id"] == 6):
            apd.append(None)
            ob = data[i][j]["objectData"]
            entity.append(Enemy((i,j), ob["id2"], ob["health"], ob["extra1"], ob["extra2"], w))
    tile.append(apd)
for i in range (0, len(data)):
    for j in range (0, len(data[i])):
        data[i][j] = data[i][j]["id"]
print(data)
class Player():
    def __init__(self, pos, w, m, health):
        self.m = m
        self.x, self.y = pos
        self.obj = w.create_image(self.x*20+10, self.y*20 +10,  image=textures[11])
        self.f = [0,3,6]
        update_item(5, 2, health)
    def move_up(self, w):
        if self.m[self.x][self.y - 1] in self.f :
            return
        else:
            w.move(self.obj, 0, -20)
            self.y = self.y - 1
        self.check_item()
    def move_down(self, w):
        if self.m[self.x][self.y + 1] in self.f: 
            return
        else:
            w.move(self.obj, 0, +20)
            self.y = self.y + 1
        self.check_item()
    def move_left(self, w):
        if self.m[self.x - 1][self.y] in self.f: 
            return
        else:
            w.move(self.obj, -20,0)
            self.x = self.x - 1
        self.check_item()
    def move_right(self, w):
        if self.m[self.x + 1][self.y] in self.f: 
            return
        else:
            w.move(self.obj, +20, 0)
            self.x = self.x + 1
        self.check_item()
    def check_kill(self):
    
        if self.x > 23 or self.x < 0 or self.y > 23 or self.y < 0:
            print("U ded")
            return 1
        elif self.m[self.x][self.y] == 0:
            print("U bad")
            return 1
        elif self.m[self.x][self.y] == 3:
            print("U win")
            return 2
        else:
            return 0
    def check_item(self):
        global items
        for i in range (0, len(items)):
            if items[i] != None:
                if items[i].x == self.x   and  items[i].y == self.y:
                    items[i].collect()
    def damage(self):
        update_item(5, 1, 1)
        if colita[5] <= 0:
            print("U ded")
            quit()
class Bomb():
    def __init__(self,position):
        self.x,self.y = position
        global w, data, short_fuse, long_fuse, timebomb_used, dynamite_used
        data[self.x][self.y] = 0
        if timebomb_used:
            self.c = w.create_image(self.x*20+10, self.y*20 +10,  image=textures[14])
        elif dynamite_used:
            self.c = w.create_image(self.x*20+10, self.y*20 +10,  image=textures[6])
        elif smoke_used:
            self.c = w.create_image(self.x*20+10, self.y*20 +10,  image=textures[13])
        else:
            self.c = w.create_image(self.x*20+10, self.y*20 +10,  image=textures[4])
        if (short_fuse):
            self.life = 10
            self.tb = False
        elif (long_fuse):
            self.life = 100
            self.tb = False
        elif timebomb_used:
            print("Should be TB")
            self.life = 1000000
            self.tb = True
            timebomb_used = False
        else:
            self.life = 35
            self.tb = False
    def explode(self):
        global w, tile, exps
        w.delete(self.c)
        data[self.x][self.y] = -1
        w.delete(tile[self.x][self.y])
        tile[self.x][self.y] = None
        for i in range (0, len(exps)):
            if (exps[i] == None):
                exps[i] = explosion((self.x,self.y))
                return
    def tick_down(self):
        self.life -= 1
class explosion():
    def __init__(self,pos):
        global short_exp, exp_range, dynamite_used, timebomb_used, smoke_used
        self.x,self.y = pos
        if smoke_used:
            self.life = 500
        else:
            self.life = 5
        self.c = []
        if (short_exp): 
            self.r = 2
        else:
            self.r = exp_range
        self.destr = [3,5]
        print(dynamite_used)
        if dynamite_used:
            print("SHOULD BE DYN")
            self.explode_square()
            dynamite_used = False
        elif smoke_used:
            self.generate_smoke()
            smoke_used = False
        else:
            self.explode_right()
            self.explode_down()
            self.explode_up()
            self.explode_left()
    def explode_right(self):
        global data, tile, w, entity
        for i in range (self.x, self.x+self.r):
            if (i == p.x and self.y == p.y):
                p.damage()
            if (data[i][self.y]== 0):
                return
            if (data[i][self.y] in self.destr):
                self.c.append(w.create_image(i*20+10, self.y*20 +10,  image=textures[8]))
                if not self.check_item((i,self.y)):
                    w.delete(tile[i][self.y])
                    g = data[i][self.y] != 5
                    data[i][self.y] = -1
                    f = random.randint(0,1)
                    if (f == 1 and g):
                        data[i][self.y] = 5
                        item = Item((i,self.y))
                        tile[i][self.y] = w.create_image(i*20+10, self.y*20 +10,  image=item.image)
                return
            else:
                self.c.append(w.create_image(i*20+10, self.y*20 +10,  image=textures[8]))
                if data[i][self.y] == 6:
                    for k in range (0, len(entity)):
                        if i == entity[k].x and self.y == entity[k].y:
                            entity[k].damage()
                            return
                data[i][self.y] = -1
    def explode_down(self):
        global data, tile, w, p
        for i in range (self.y, self.y+self.r):
            if (self.x == p.x and i == p.y):
                p.damage()
            if (data[self.x][i] == 0):
                return
            if (data[self.x][i] in self.destr):
                self.c.append(w.create_image(self.x*20+10, i*20 +10,  image=textures[8]))
                if not self.check_item((self.x,i)):
                    w.delete(tile[self.x][i])
                    g = data[self.x][i] != 5
                    data[self.x][i] = -1
                    f = random.randint(0,1)
                    if (f == 1 and g):
                        data[self.x][i] = 5
                        item = Item((self.x,i))
                        tile[self.x][i] = w.create_image(self.x*20+10, i*20 +10,  image=item.image)
                return
            else:
                self.c.append(w.create_image(self.x*20+10, i*20 +10,  image=textures[8]))
                if data[self.x][i] == 6:
                    for k in range (0, len(entity)):
                        if self.x == entity[k].x and i == entity[k].y:
                            entity[k].damage()
                            return
                data[self.x][i] = -1
    def explode_up(self):
        global data, tile, w, p
        for i in range (0, self.r):
            if (self.x == p.x and self.y-i == p.y):
                p.damage()
            if (data[self.x][self.y - i] == 0):
                return
            if (data[self.x][self.y - i] in self.destr):
                self.c.append(w.create_image(self.x*20+10, (self.y-i)*20 +10,  image=textures[8]))
                if not self.check_item((self.x,self.y-i)):
                    w.delete(tile[self.x][self.y - i])
                    g = data[self.x][self.y-i] != 5
                    data[self.x][self.y - i] = -1
                    f = random.randint(0,1)
                    if (f == 1 and g):
                        data[self.x][self.y-i] = 5
                        item = Item((self.x,self.y-i))
                        tile[self.x][self.y-i] = w.create_image(self.x*20+10, (self.y-i)*20 +10,  image=item.image)
                return
            else:
                self.c.append(w.create_image(self.x*20+10, (self.y-i)*20 +10,  image=textures[8]))
                if data[self.x][self.y-i] == 6:
                    for k in range (0, len(entity)):
                        if self.x == entity[k].x and self.y-i == entity[k].y:
                            entity[k].damage()
                            return
                data[self.x][self.y - i] = -1
    def explode_left(self):
        global data, tile, w, p
        for i in range (0, self.r):
            if (self.x-i == p.x and self.y == p.y):
                p.damage()
            if (data[self.x-i][self.y] == 0):
                return
            if (data[self.x-i][self.y] in self.destr):
                self.c.append(w.create_image((self.x-i)*20+10, self.y*20 +10,  image=textures[8]))
                if not self.check_item((self.x-i,self.y)):
                    w.delete(tile[self.x-i][self.y])
                    g = data[self.x-i][self.y] != 5
                    data[self.x-i][self.y] = -1
                    f = random.randint(0,1)
                    if (f == 1 and g):
                        data[self.x-i][self.y] = 5
                        item = Item((self.x-i,self.y))
                        tile[self.x-i][self.y] = w.create_image((self.x-i)*20+10, self.y*20 +10,  image=item.image)
                return
            else:
                self.c.append(w.create_image((self.x-i)*20+10, self.y*20 +10,  image=textures[8]))
                if data[self.x-i][self.y] == 6:
                    for k in range (0, len(entity)):
                        if self.x-i == entity[k].x and self.y == entity[k].y:
                            entity[k].damage()
                            return
                data[self.x-i][self.y] = -1
    def explode_square(self):
        global data,tile,w,p
        for i in range (self.x-3,self.x+3):
            for j in range (self.y-3,self.y+3):
                if i < len(data) and i >= 0 and j < len(data) and j >= 0:
                    self.c.append(w.create_image(i*20+10, j*20 +10,  image=textures[8]))
                    if (i == p.x and j == p.y):
                        p.damage()
                    if data[i][j] != 0 and data[i][j] != 6:
                        if not self.check_item((i,j)):
                            w.delete(tile[i][j])
                            g = data[i][j] != 5 and data[i][j] != -1
                            data[i][j] = -1
                            f = random.randint(0,1)
                            if (f == 1 and g):
                                data[i][j] = 5
                                item = Item((i,j))
                                tile[i][j] = w.create_image(i*20+10, j*20 +10,  image=item.image)
                    elif data[i][j] == 6:
                        for k in range (0, len(entity)):
                            if i == entity[k].x and j == entity[k].y:
                                entity[k].damage()
    def generate_smoke(self):
        global data, tile, w, p
        for i in range (self.x-3,self.x+4):
            for j in range (self.y-3,self.y+4):
                if i < len(data) and i >= 0 and j < len(data) and j >= 0:
                    if i == self.x-3 or i == self.x+3 or j == self.y-3 or j == self.y+3:
                        self.c.append(w.create_image(i*20+10,j*20+10, image = textures[16]))
                        print(str(i) + ":" + str(j))
        for i in range (self.x-2,self.x+3):
            for j in range (self.y-2,self.y+3):
                if i < len(data) and i >= 0 and j < len(data) and j >= 0:
                    if i == self.x-2 or i == self.x+2 or j == self.y-2 or j == self.y+2:
                        self.c.append(w.create_image(i*20+10,j*20+10, image = textures[17]))
        for i in range (self.x-1,self.x+2):
            for j in range (self.y-1,self.y+2):
                if i < len(data) and i >= 0 and j < len(data) and j >= 0:
                    self.c.append(w.create_image(i*20+10,j*20+10, image = textures[12]))
    def tick_down(self, idx):
        global w, exps
        if (self.life > 0):
            self.life -= 1
        else:
            for i in range (0, len(self.c)):
                w.delete(self.c[i])
            exps[idx] = None
    def check_item(self, pos):
        global items,data
        tmp_x,tmp_y = pos
        for i in range (0, len(items)):
            if items[i] != None:
                if items[i].x == tmp_x   and  items[i].y == tmp_y:
                    w.delete(tile[tmp_x][tmp_y])
                    data[tmp_x][tmp_y] = -1
                    items[i] = None
                    print(items)
                    return True
        return False
master.bind('w', lambda event: p.move_up(w))
master.bind('s', lambda event: p.move_down(w))
master.bind('a', lambda event: p.move_left(w))
master.bind('d', lambda event: p.move_right(w))
master.bind('<space>', lambda event: plant())
master.bind('y', lambda event: use_dynamite())
master.bind('t', lambda event: use_time())
master.bind('#', lambda event: exp_time())
master.bind('c', lambda event: get_Curse())
master.bind('m', lambda event: use_smoke())
p = Player(start, w, data, 10)
master.resizable(0,0)
bombs = [None]
exps  = [None]
items = [None]
def exp_time():
    global bombs
    for i in range (0, len(bombs)):
        if bombs[i] != None:
            if bombs[i].tb:
                bombs[i].life = 0
def plant():
    global p, bombs,data
    for i in range (0, len(bombs)):
        if (bombs[i] == None):  
            if (data[p.x][p.y] != 0):
                bombs[i] = Bomb((p.x,p.y))
                return
def exp():
    global bombs, exps
    for i in range (0,len(bombs)):
        if (bombs[i] != None):  
            if (bombs[i].life <= 0):
                bombs[i].explode()
                bombs[i] = None
            else:
                bombs[i].tick_down()
    for i in range (0,len(exps)):
        if (exps[i] != None):
            exps[i].tick_down(i)
def update_frame():
    exp()
    global curse_life, long_fuse, short_fuse, short_exp, poop_mode, data, Enemy
    if curse_life <= 0:
        long_fuse = False
        short_fuse = False
        short_exp = False
        poop_mode = False
        #print("Lost curse")
    else:
        curse_life -= 1
    if (poop_mode):
        plant()
    global bombs, exp_range
    update_item(0, 2, exp_range-1)
    update_item(1,2, len(bombs))
    if not (True in enemy):
        print("Ya Win")
        quit()
def init_frame():
   change_message("Hello World", 1)
init_frame()
def get_Curse():
    global curse_life, long_fuse, short_fuse, short_exp, poop_mode
    csid = random.randint(1,4)
    if csid == 1:
        long_fuse = True
        short_fuse = False
        short_exp = False
        poop_mode = False
        print("Ya got l-fuse")
    if csid == 2:
        long_fuse = False
        short_fuse = True
        short_exp = False
        poop_mode = False
        print("Ya got s-fuse")
    if csid == 3:
        long_fuse = False
        short_fuse = False
        short_exp = True
        poop_mode = False
        print("Ya got s-exp")
    if csid == 4:
        ong_fuse = False
        short_fuse = False
        short_exp = False
        poop_mode = True
        print("Ya Poop")
    curse_life = 250
class Item():
    def __init__(self, pos):
        global items
        self.seed = random.randint(0,1000)
        if (self.seed < 30):
            self.iid = 3 #3 % Dynamite
        elif (self.seed >= 30 and self.seed < 60):
            self.iid = 6 #3 % Health+
        elif (self.seed >= 60 and self.seed  < 300):
            self.iid = 2 #24% Timed Bomb
        elif (self.seed >= 300 and self.seed < 550):
            self.iid = 0 #25% bomb+
        elif (self.seed >= 550 and self.seed < 800):
            self.iid = 1 #25% exp + (oder umgekehrt)
        elif (self.seed >= 800 and self.seed < 950):
            self.iid = 4 #20% VIRUS
        elif (self.seed >= 950):
            self.iid = 5 #5% Smoke Bomb cause its useless
        if (self.iid == 0):
            self.image = textures[0]
        elif (self.iid == 1):
            self.image = textures[1]
        elif (self.iid == 2):
            self.image = textures[2]
        elif (self.iid == 3):
            self.image = textures[6]
        elif (self.iid == 4):
            self.image = textures[14]
        elif (self.iid == 5):
            self.image = textures[13]
        elif (self.iid == 6):
            self.image = textures[19]
        self.x,self.y = pos
        self.reg = True
        if self.iid == 5:
            if len(exps) < len(bombs) + colita[2]:
                exps.append(None)
        for i in range (0, len(items)):
            if (items[i] == None):
                items[i] = self
                self.reg = False
                self.idx = i
                break;
        if (self.reg):
            items.append(self)
            self.idx = len(items)-1
        print(items)
    def collect(self):
        global items, data, tile,w, bombs, exps, exp_range
        #Clean up data
        items[self.idx] = None
        w.delete(tile[self.x][self.y])
        data[self.x][self.y] = -1
        print(items)
        #Code that actually does something
        if (self.iid == 2):
            get_Curse()
        elif (self.iid == 0):
            bombs.append(None)
            exps.append(None)
        elif (self.iid == 1):
            exp_range += 1
            print(exp_range)
        elif (self.iid == 3):
            update_item(3,0, 1)
        elif (self.iid == 4):
            update_item(4,0, 1)
        elif self.iid == 5:
            update_item(2,0,1)
        elif self.iid == 6:
            update_item(5,0,1)
def use_dynamite():
    global colit, colita, dynamite_used
    if (colita[3] > 0 and not dynamite_used):
        update_item(3, 1, 1)
        dynamite_used = True
        plant()
def use_time():
    global colit, colita, timebomb_used
    if (colita[4] > 0 and not timebomb_used):
        update_item(4,1,1)
        timebomb_used = True
        plant()
def use_smoke():
    global colit, colita, smoke_used
    if (colita[2] > 0 and not smoke_used):
        update_item(2,1,1)
        smoke_used = True
        plant()
"""def use_dyn():
    global dynamite_used
    dynamite_used = True
    print("Used DYN")"""
def end_all():
    os._exit(0)
master.protocol("WM_DELETE_WINDOW", end_all)
while True:
    master.update_idletasks()
    master.update()
    update_frame()
    time.sleep(0.04)
