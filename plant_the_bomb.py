from tkinter import *
import json
import time
import random
import os
import pathlib
import functools
import hashlib
from pathlib import *
lvs = None
solved = False
lid = 0
locked_items = [False,False,False,False,False,False,False]
texts = []
scripts = [None]
scriptdata = []
lvcls = ["white","red","red","red","null"]
lvls = ["active","disabled","disabled","disabled","null"]
path = str(pathlib.Path(__file__).parent.absolute()) + "/maps/"
maps = ["maps/tutorial.json","maps/level1.json","maps/level2.json","maps/level3.json"]
levels = [False,False,False,False]
global_bombs= 1
global_exp  = 2
global_health = 1
path = str(pathlib.Path(__file__).parent.absolute()) + "/textures/"
files = os.listdir(path)
addpath = "textures/"
master = 0
w = 0
inv = 0
master = Tk()
master.title("Plant The Bomb")
width = 25*20
height = 25*20
master.geometry((str(width) + 'x' + str(height + 80)) + '+10+10')
master.resizable(0,0)
w = Canvas(master, width=width, height = height)
w.pack(expand=YES, fill= BOTH)
w.place(x = 0, y = 80)
inv = Canvas(master,width=width, height =80)
inv.pack(expand=YES, fill= BOTH)
inv.place(x = 0, y = 0)
    
player_health = 1
textures = []
for i in range(0, len(files)):
    textures.append(PhotoImage(file=addpath + files[i]))  
colit = [textures[8], textures[4], textures[13],textures[6], textures[14], textures[18]]
colita = []
text = []
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
message = inv.create_text(25*20/2, 60, state = "hidden", text="Default", fill="red", font=('Calibri 15'))
#setup Classes and global methods
start = 0
bombs = [None]
exps  = [None]
items = [None]
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
#TODO
file = ""
data =0
#json.loads(open(file, "r").read())["world"]
#//TODO
enemy = []
entity = []
tile = []
#setup Texture System
class script():
    def __init__(self, pos, cmd, args, stable, s):
        global scripts, locked_items
        self.x,self.y = pos
        self.cmd = cmd
        self.args = args
        self.stable = stable
        st = False
        self.s = s
        if self.s:
            for i in range (0, len(scripts)):
                if scripts[i] == None:
                    self.idx = i
                    st = True
            if not st:
                scripts.append(None)
                self.idx = len(scripts)-1
            scripts[self.idx] = self
    def run(self):
        global scripts,p,w
        if self.s:
            if not self.stable:
                scripts[self.idx] = None
        if self.cmd == 1:
            p.tp(self.args[0],self.args[1])
        elif self.cmd == 2:
            update_item(self.args[0],self.args[2],self.args[1])
        elif self.cmd == 3:
            if self.args[1] == 1:
                locked_items[self.args[0]] = True
            else:
                locked_items[self.args[0]] = False
        elif self.cmd == 4:
            change_message(texts[self.args[0]], 1)
def get_vector(root,top):
    rx,ry = root
    tx,ty = top
    vx = tx - rx
    vy = ty - ry
    return (vx,vy)
class Item():
    def __init__(self, pos, sed, bf):
        global items, locked_items
        self.seed = sed
        if (self.seed < 30):
            self.iid = 3 #3 % Dynamite #check
        elif (self.seed >= 30 and self.seed < 60):
            self.iid = 6 #3 % Health+ #check
        elif (self.seed >= 60 and self.seed  < 300):
            self.iid = 4 #24% Timed Bomb
        elif (self.seed >= 300 and self.seed < 550):
            self.iid = 0 #25% bomb+  #check
        elif (self.seed >= 550 and self.seed < 800):
            self.iid = 1 #25% exp + (oder umgekehrt) #check
        elif (self.seed >= 800 and self.seed < 950):
            self.iid = 2 #20%  Curse #check ?????????????????
        elif (self.seed >= 950):
            self.iid = 5 #5% Smoke Bomb cause its useless
        if locked_items[self.iid] == True and not bf:
            self.exists = False
            return
        else:
            self.exists = True
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
    def collect(self):
        global items, data, tile,w, bombs, exps, exp_range
        #Clean up data
        items[self.idx] = None
        w.delete(tile[self.x][self.y])
        data[self.x][self.y] = -1
        #Code that actually does something
        if (self.iid == 2):
            get_Curse()
        elif (self.iid == 0):
            bombs.append(None)
            exps.append(None)
        elif (self.iid == 1):
            exp_range += 1
        elif (self.iid == 3):
            update_item(3,0, 1)
        elif (self.iid == 4):
            update_item(4,0, 1)
        elif self.iid == 5:
            update_item(2,0,1)
        elif self.iid == 6:
            update_item(5,0,1)
class Enemy():
    def __init__(self, pos, tpe, health, extra1, extra2, w):
        global enemy
        self.f = [0,3,6, 4]
        enemy.append(True)
        self.x, self.y = pos
        #Multiple Texures for multiple Types
        if tpe == 2:
            self.obj = w.create_image(self.x*20+10, self.y*20+10, image=textures[20])
            self.hitbox = [(0,0),(1,0),(-1,0),(0,1),(0,-1)] #Multiple for Multiple Types
        else:
            self.obj = w.create_image(self.x*20+10, self.y*20+10, image=textures[20])
            self.hitbox = [(0,0)] #Multiple for Multiple Types
        self.health = health
        self.reg = len(enemy)-1 
        self.healthbar = w.create_rectangle(self.x*20,self.y*20+18,self.x*20+20,self.y*20+20, fill="black", outline=None)
        self.maxhealth = health
        self.life = 0
        self.movement_countdown_max = 10
        self.attack_countdown_max = 25
        self.movement_countdown = self.movement_countdown_max
        self.attack_countdown = self.attack_countdown_max
        self.panic = 0
    def damage(self):
        self.health -= 1
        self.update_health()
        global w, enemy
        if (self.health <= 0):
            w.delete(self.obj)
            enemy[self.reg] = False
            entity[self.reg] = None
            data[self.x][self.y] = -1
            w.delete(self.healthbar)
    def move(self):
        global w, data, p
        px = p.x
        py = p.y
        target_vec = (px-self.x,py-self.y)
        vx, vy = target_vec
        if vx != 0:
            if vx >0:
                x = 1
            else:
                x = -1
        else:
            x = 0
        if vy != 0:
            if vy >0:
                y = 1
            else:
                y = -1
        else:
            y = 0
        if data[self.x+x][self.y] not in self.f and  not (self.x+x == p.x and self.y == p.y):
            y = 0
        elif data[self.x][self.y+y] not in self.f and  not (self.x == p.x and self.y+y == p.y):
            x = 0
        if data[self.x+x][self.y +y] in self.f and not (self.x+x == p.x and self.y+y == p.y) and not data[self.x+x][self.y+y] == 6:
            self.panic = 3
        if self.x+x == p.x and self.y + y == p.y:
            panic = 0
        if self.panic > 0:
            di = [(0,1),(0,-1),(1,0),(-1,0)]
            random.shuffle(di)
            if len(di) > 0:
                x,y = di[len(di)-1]
                di.pop()
            if data[self.x+x][self.y +y] in self.f or (self.x+x == p.x and self.y+y == p.y):
                random.shuffle(di)
                if len(di) > 0:
                    x,y = di[len(di)-1]
                    di.pop()
            if data[self.x+x][self.y +y] in self.f or (self.x+x == p.x and self.y+y == p.y):
                random.shuffle(di)
                if len(di) > 0:
                    x,y = di[len(di)-1]
                    di.pop()
            if data[self.x+x][self.y +y] in self.f or (self.x+x == p.x and self.y+y == p.y):
                random.shuffle(di)
                if len(di) > 0:
                    x,y = di[len(di)-1]
                    di.pop()
            self.panic -= 1
        if data[self.x+x][self.y +y] in self.f or (self.x+x == p.x and self.y+y == p.y):
            return
        else:
            w.move(self.obj, x*20, y*20)
            data[self.x][self.y] = -1
            data[self.x+x][self.y +y] = 6
            self.y += y
            self.x += x
    def update(self):
        if (self.movement_countdown > 0):
            self.movement_countdown -= 1
        if self.movement_countdown <= 0:
            self.movement_countdown = self.movement_countdown_max
            self.move()
        if (self.attack_countdown >0):
            self.attack_countdown -= 1
        if (self.attack_countdown <=0):
            self.attack_countdown = self.attack_countdown_max
            self.attack()
    def attack(self):
        global p
        for i in range (0, len(self.hitbox)):
            x,y = self.hitbox[i]
            if p.x == self.x + x and p.y == self.y + y:
                p.damage()
    def update_health(self):
        perc = self.health / self.maxhealth
        pix = perc * 20
        pix = round(pix)
        if self.healthbar != None:
            w.delete(self.healthbar)
            self.healthbar = None
        self.healthbar = w.create_rectangle(self.x*20,self.y*20+18,self.x*20+pix,self.y*20+20, fill="black", outline="black")
        self.life = 50
    def tick_down(self):
        if (self.life > 0):
            self.life -= 1
        if self.life <= 0:
            w.delete(self.healthbar)
            self.healthbar = None
class Player():
    def __init__(self, pos, w, m, health):
        self.m = m
        self.x, self.y = pos
        self.obj = w.create_image(self.x*20+10, self.y*20 +10,  image=textures[11])
        self.f = [0,3,6, 4]
        update_item(5, 2, health)
    def tp(self, x,y):
        global w
        vx, vy = get_vector((self.x*20+10,self.y*20+10),(x*20+10,y*20+10))
        w.move(self.obj, vx,vy)
        self.x = x
        self.y = y
        self.check_item()
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
        return 0
    def check_item(self):
        global items, scripts
        for i in range (0, len(items)):
            if items[i] != None:
                if items[i].x == self.x   and  items[i].y == self.y:
                    items[i].collect()
        for i in range (0, len(scripts)):
            if scripts[i] != None:
                if scripts[i].x == self.x   and  scripts[i].y == self.y:
                    scripts[i].run()
    def damage(self):
        update_item(5, 1, 1)
        if colita[5] <= 0:
            update_item(5, 1, 2)
            select_level()
            return
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
        if dynamite_used:
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
                        item = Item((i,self.y),random.randint(0,1000),False)
                        if item.exists:
                            tile[i][self.y] = w.create_image(i*20+10, self.y*20 +10,  image=item.image)
                return
            else:
                self.c.append(w.create_image(i*20+10, self.y*20 +10,  image=textures[8]))
                if data[i][self.y] == 6:
                    for k in range (0, len(entity)):
                        if entity[k] != None:
                            if i == entity[k].x and self.y == entity[k].y:
                                entity[k].damage()
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
                        item = Item((self.x,i),random.randint(0,1000),False)
                        if item.exists:
                            tile[self.x][i] = w.create_image(self.x*20+10, i*20 +10,  image=item.image)
                return
            else:
                self.c.append(w.create_image(self.x*20+10, i*20 +10,  image=textures[8]))
                if data[self.x][i] == 6:
                    for k in range (0, len(entity)):
                        if entity[k] != None:
                            if self.x == entity[k].x and i == entity[k].y:
                                entity[k].damage()
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
                        item = Item((self.x,self.y-i),random.randint(0,1000),False)
                        if item.exists:
                            tile[self.x][self.y-i] = w.create_image(self.x*20+10, (self.y-i)*20 +10,  image=item.image)
                return
            else:
                self.c.append(w.create_image(self.x*20+10, (self.y-i)*20 +10,  image=textures[8]))
                if data[self.x][self.y-i] == 6:
                    for k in range (0, len(entity)):
                        if entity[k] != None:
                            if self.x == entity[k].x and self.y-i == entity[k].y:
                                entity[k].damage()
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
                        item = Item((self.x-i,self.y),random.randint(0,1000),False)
                        if item.exists:
                            tile[self.x-i][self.y] = w.create_image((self.x-i)*20+10, self.y*20 +10,  image=item.image)
                return
            else:
                self.c.append(w.create_image((self.x-i)*20+10, self.y*20 +10,  image=textures[8]))
                if data[self.x-i][self.y] == 6:
                    for k in range (0, len(entity)):
                        if entity[k] != None:
                            if self.x-i == entity[k].x and self.y == entity[k].y:
                                entity[k].damage()
    def explode_square(self):
        global data,tile,w,p
        for i in range (self.x-3,self.x+3):
            for j in range (self.y-3,self.y+3):
                if i < len(data) and i >= 0 and j < len(data) and j >= 0:
                    self.c.append(w.create_image(i*20+10, j*20 +10,  image=textures[8]))
                    if (i == p.x and j == p.y):
                        p.damage()
                        p.damage()
                    if data[i][j] != 0 and data[i][j] != 6:
                        if not self.check_item((i,j)):
                            w.delete(tile[i][j])
                            g = data[i][j] != 5 and data[i][j] != -1
                            data[i][j] = -1
                            f = random.randint(0,1)
                            if (f == 1 and g):
                                data[i][j] = 5
                                item = Item((i,j),random.randint(0,1000), False)
                                if item.exists:
                                    tile[i][j] = w.create_image(i*20+10, j*20 +10,  image=item.image)
                    elif data[i][j] == 6:
                        for k in range (0, len(entity)):
                            if entity[k] != None:
                                if i == entity[k].x and j == entity[k].y:
                                    if entity[k] != None:
                                        entity[k].damage()
                                    if entity[k] != None:
                                        entity[k].damage()
    def generate_smoke(self):
        global data, tile, w, p, entity
        for i in range (self.x-3,self.x+4):
            for j in range (self.y-3,self.y+4):
                if i < len(data) and i >= 0 and j < len(data) and j >= 0:
                    if i == self.x-3 or i == self.x+3 or j == self.y-3 or j == self.y+3:
                        self.c.append(w.create_image(i*20+10,j*20+10, image = textures[16]))
                        for k in range (0,len(entity)):
                            if entity[k] != None:
                                if entity[k].x == i and entity[k].y == j:
                                    entity[k].panic = 10
        for i in range (self.x-2,self.x+3):
            for j in range (self.y-2,self.y+3):
                if i < len(data) and i >= 0 and j < len(data) and j >= 0:
                    if i == self.x-2 or i == self.x+2 or j == self.y-2 or j == self.y+2:
                        self.c.append(w.create_image(i*20+10,j*20+10, image = textures[17]))
                        for k in range (0,len(entity)):
                            if entity[k] != None:
                                if entity[k].x == i and entity[k].y == j:
                                    entity[k].panic = 30
        for i in range (self.x-1,self.x+2):
            for j in range (self.y-1,self.y+2):
                if i < len(data) and i >= 0 and j < len(data) and j >= 0:
                    self.c.append(w.create_image(i*20+10,j*20+10, image = textures[12]))
                    for k in range (0,len(entity)):
                            if entity[k] != None:
                                if entity[k].x == i and entity[k].y == j:
                                    entity[k].panic = 50
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
                    return True
        return False
def get_Curse():
    global curse_life, long_fuse, short_fuse, short_exp, poop_mode
    csid = random.randint(1,4)
    if csid == 1:
        long_fuse = True
        short_fuse = False
        short_exp = False
        poop_mode = False
    if csid == 2:
        long_fuse = False
        short_fuse = True
        short_exp = False
        poop_mode = False
    if csid == 3:
        long_fuse = False
        short_fuse = False
        short_exp = True
        poop_mode = False
    if csid == 4:
        ong_fuse = False
        short_fuse = False
        short_exp = False
        poop_mode = True
    curse_life = 250
def use_dynamite():
    global colit, colita, dynamite_used
    if (colita[3] > 0 and not dynamite_used):
        update_item(3, 1, 1)
        dynamite_used = True
        plant()
def use_time():
    global colit, colita, timebomb_used
    if (colita[4] > 0 and not timebomb_used and None in bombs):
        update_item(4,1,1)
        timebomb_used = True
        plant()
def use_smoke():
    global colit, colita, smoke_used, exps
    if (colita[2] > 0 and not smoke_used):
        exps.append(None)
        update_item(2,1,1)
        smoke_used = True
        plant()
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
def change_message(text, mode):
    if mode == 0:
        inv.itemconfigure(message, state = "hidden")
    elif mode == 1:
        inv.itemconfigure(message, text = text, state = "normal")
    else:
        print("ERROR Falsche Übergabe-Werte")
def update_item(pos, mode, val):
    if mode == 0:
        colita[pos] += val
    elif mode == 1:
        colita[pos] -= val
    elif mode == 2:
        colita[pos] = val
    for l in range(0, len(colit)):
        inv.itemconfigure(text[l], text=colita[l])
def exp_time():
    global bombs
    for i in range (0, len(bombs)):
        if bombs[i] != None:
            if bombs[i].tb:
                bombs[i].life = 0
def update_frame():
    exp()
    global curse_life, long_fuse, short_fuse, short_exp, poop_mode, data, Enemy, entity, solved
    if curse_life <= 0:
        long_fuse = False
        short_fuse = False
        short_exp = False
        poop_mode = False
    else:
        curse_life -= 1
    for i in range (0,len(entity)):
        if entity[i] != None:
            entity[i].tick_down()
            entity[i].update()
    if (poop_mode):
        plant()
    global bombs, exp_range
    update_item(0, 2, exp_range-1)
    update_item(1,2, len(bombs))
    if not (True in enemy) and len(enemy)>0 and not solved:
        solved = True
        unlock_next()
def kill_all():
    ff = Path("dev_tools/token.txt")
    if ff.is_file():
        st = open("dev_tools/token.txt", "r").read()
        g = st.split(":")
        a = hashlib.md5(g[0].encode()).hexdigest()
        b = hashlib.md5(g[1].encode()).hexdigest()
        c = hashlib.md5(st.encode()).hexdigest()
        if b == "32fd40d699533c83a25a49367f09e299" and a == "d42f9269536867e69b0bf0a815a13f37" and c == "04d3326fff2d27ddbca62e70d0ea7352":
            global enemy
            enemy = [False]
        else:
            return
    else:
        print("lol")
        return
def setup_keybind():
    global master
    master.bind('w', lambda event: p.move_up(w))
    master.bind('W', lambda event: p.move_up(w))
    master.bind('<Up>', lambda event: p.move_up(w))
    master.bind('s', lambda event: p.move_down(w))
    master.bind('S', lambda event: p.move_down(w))
    master.bind('<Down>', lambda event: p.move_down(w))
    master.bind('a', lambda event: p.move_left(w))
    master.bind('A', lambda event: p.move_left(w))
    master.bind('<Left>', lambda event: p.move_left(w))
    master.bind('d', lambda event: p.move_right(w))
    master.bind('D', lambda event: p.move_right(w))
    master.bind('<Right>', lambda event: p.move_right(w))
    master.bind('<space>', lambda event: plant())
    master.bind('y', lambda event: use_dynamite())
    master.bind('Y', lambda event: use_dynamite())
    master.bind('t', lambda event: use_time())
    master.bind('T', lambda event: use_time())
    master.bind('#', lambda event: exp_time())
    master.bind('\'', lambda event: exp_time())
    master.bind('m', lambda event: use_smoke())
    master.bind('M', lambda event: use_smoke())
    master.bind("e", lambda event: select_level())
    master.bind("E", lambda event: select_level())
    master.bind("k", lambda event: kill_all())
def generate_game():
    global data, tile, start, lvs, solved, scripts, scriptdata, texts
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            if j % 2 == 0 and i % 2 == 0 or j % 2 != 0 and i % 2 != 0:
                w.create_image(i*20+10, j*20 +10,  image=textures[9])
            else:
                w.create_image(i*20+10, j*20 +10,  image=textures[10])
    for i in range (0, len(scriptdata)):
        g = scriptdata[i]
        if g["tr"] == 0:
            sc = script((0,0),g["cmd"],g["args"],False,False)
            sc.run()
        elif g["tr"] == -1:
            a = script((g["x"],g["y"]),g["cmd"],g["args"],g["stable"],True)
    #Load Map          
    for i in range (0, len(data)):
        apd = []
        for j in range (0, len(data[i])):
            if (data[i][j] == None):
                apd.append(w.create_image(i*20+10, j*20 +10,  image=textures[21]))
                data[i][j] = 0
            elif (data[i][j]["id"] == 0):
                apd.append(w.create_image(i*20+10, j*20 +10,  image=textures[7]))
            elif (data[i][j]["id"] == 2):
                global start
                start = (i,j) 
                apd.append(None)
            elif (data[i][j]["id"] == 3):
                apd.append(w.create_image(i*20+10, j*20 +10,  image=textures[15]))
            elif (data[i][j]["id"] == 4):
                apd.append(w.create_image(i*20+10, j*20 +10,  image=textures[24]))
            elif (data[i][j]["id"] == -1):
                apd.append(None)
            elif (data[i][j]["id"] == 5):
                ob  = data[i][j]["objectData"]
                f = ob["start"]
                t = ob["fin"]
                item = Item((i,j), random.randint(f,t), True)
                apd.append(w.create_image(i*20+10, j*20 +10,  image=item.image))
            elif (data[i][j]["id"] == 6):
                apd.append(None)
                ob = data[i][j]["objectData"]
                entity.append(Enemy((i,j), ob["id2"], ob["health"], ob["extra1"], ob["extra2"], w))
        tile.append(apd)
    #Simplify Ids
    for i in range (0, len(data)):
        for j in range (0, len(data[i])):
            if type(data[i][j]) != type(1):
                data[i][j] = data[i][j]["id"]
    master.deiconify()
    solved = False
    if (lvs != None):
        lvs.destroy()
        lvs = None
#setup Global variables
def load_level(s_bombs, s_exp, s_range,ph, Map, i):
    change_message("",1)
    global long_fuse, short_fuse, short_exp, sonic_speed, snail_speed, poop_mode, dynamite_used, smoke_used, timebomb_used, lid
    long_fuse, short_fuse, short_exp, sonic_speed, snail_speed, poop_mode, dynamite_used, smoke_used, timebomb_used = (False,False,False,False,False,False,False,False,False)
    global bombs,exps,items,curse_life,exp_range, scriptdata, scripts, locked_items, texts
    texts = []
    locked_items = [False,False,False,False,False,False,False]
    lid = i
    items = [None]
    bombs = [None]*s_bombs
    exps = [None]*s_exp
    scripts = [None]
    curse_life = 0
    update_item(2, 2, 0)
    update_item(3, 2, 0)
    update_item(4, 2, 0)
    exp_range = s_range
    global enemy, entity,tile,data,  player_health,w,master,p
    enemy = []
    entity = []
    tile = []
    file = Map
    data = json.loads(open(file, "r").read())["world"]
    scriptdata = json.loads(open(file, "r").read())["scripts"]
    texts = json.loads(open(file, "r").read())["texts"]
    player_health = ph
    w = Canvas(master, width=width, height = height)
    w.pack(expand=YES, fill= BOTH)
    w.place(x = 0, y = 80)
    p=0
    generate_game()
    p = Player(start, w, data, player_health)
def kill_game():
    master.destroy()
    lvs.destroy()
    quit()
class levelbutton(Button):
    def __init__(self,i,x,y):
        global lvs, lvcls, lvls, lid, levels
        super().__init__(lvs,text=str(i+1),activebackground=lvcls[i],bg=lvcls[i],state=lvls[i],command=functools.partial(load_level,global_bombs,global_bombs,global_exp,global_health,maps[i], i))
        self.place(x=x*30+10,y=y*30+10,width=20,height=20)
def select_level():
    master.withdraw()
    global lvls, lvcls, lvs, textures
    if lvs == None:
        lvs = Tk()
        lvs.geometry("160" + 'x' + "160" + '+10+10')
        lvs.resizable(0,0)
        lvs.protocol("WM_DELETE_WINDOW", end_all)
    ex = Button(lvs,activebackground="red",bg="red",text="Q", command=lambda:kill_game())
    ex.place(x=130,y=10,width=20,height=20)
    lvs1 = levelbutton(0,0,0)
    lvs2 = levelbutton(1,1,0)
    lvs3 = levelbutton(2,2,0)
    lvs3 = levelbutton(3,3,0) 
    """lvs5 = Button(lvs,bg="whitee",state="active",command=functools.partial(load_level,1,1,2,3,maps[0]))
    lvs5.place(x=130,y=10,width=20,height=20)"""
def unlock_next():
    global lvls, lvcls,lid, levels
    if not levels[lid]:
        for i in range (0, len(lvls)):
            if lvls[i] != "active":
                lvls[i] = "active"
                lvcls[i] = "white"
                lvcls[i-1] = "green"
                levels[lid] = True
                select_level()
                return
    select_level()
def end_all():
    os._exit(0)
master.protocol("WM_DELETE_WINDOW", end_all)
#Main
p = 0
#load_level(1,1,2,3,"showcase.json")
select_level()
setup_keybind()
#select_level()
#Mainloop
while True:
    master.update_idletasks()
    master.update()
    update_frame()
    time.sleep(0.04)
