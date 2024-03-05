import random, copy
import src.engine.scriptGraphic as sc
import src.engine.block as block
import src.engine.item as item
import src.engine.enemy as enemy
import src.gui.Dialogs as Dialogs

class trevent():
    def __init__(self, code, x, y):
        self.x = x
        self.y = y
        self.code = code
class trigger():
    def __init__(self, sl, line, event, posx, posy, stable, igpos):
        self.sl  = sl
        self.event = event
        self.posx = posx
        self.posy = posy
        self.stable = stable
        self.used = False
        self.igpos = igpos
        self.line = line
        if self.posx == self.posy == 0 and not self.igpos:
            self.igpos = True
    def _collect(self, event):
        if self.event == event.code:
            if not self.used:
                if self.igpos or (self.posx == event.x and self.posy == event.y):
                    if not self.stable:
                        self.used = True
                    print("Triggered" + event.code)
                    return [True, self.line + 1]
        return [False]
class scriptLoader():
    def __init__(self, world, source):
        self.world = world
        self.source = source[1:]
        source = source[1:]
        self.lines = []
        self.commands = []
        self.ram = [0]*65536
        self.parser = {"position": 0, "running":False}
        self.trigger_list = []
        self._postInit()
        i = 0
        ainf = "0"
        while i< len(source):
            cmd = source[i]
            for k in range (len(self.commands)):
                element = self.commands[k]
                if element["byte"] == cmd and type(cmd) == int:
                    ainf = element["arginf"]
            ll = 1
            #print("INF",ainf)
            for j in range (len(ainf)):
                if ainf[j] == "$" or ainf[j] == "§":
                    ll += 1
                elif ainf[j] == "*":
                    ll += 2
            #print("LL", ll)
            self.lines.append(source[i:i+ll])
            i += ll
        #print(self.lines)
        self._find_triggers()
    def _get_trigger(self,trtp, x,y, l):
        #1: on_init
        #2: on_step
        #3: on_collect
        #4: on_destroy
        #5: on_explode
        #6: on_tick (note that trigger executes AFTER the tick)
        trl = [None, (self,l,"on_init",x,y,False,True),(self,l,"on_step",x,y,True,False),(self, l, "on_collect", x, y, False, False),(self,l,"on_explode",x,y,True,False),(self, l, "on_destroy", x,y,False,False),(self, l, "on_tick", x, y, True, True)]
        return trl[trtp]
    def _find_triggers(self):
        for i in range (len(self.lines)):
            if self.lines[i][0] == 1:
                self.trigger_list.append(trigger(*self._get_trigger(self.lines[i][1],self.lines[i][2],self.lines[i][3],i)))
    def event(self, event):
        for tr in self.trigger_list:
            reply = tr._collect(event)
            if True in reply:
                self.parser["position"] = reply[1]
                self._psr_start()
    def _register_command(self, br, method, arginf):
        self.commands.append({"byte":br,"method":method,"arginf":arginf})
    def _postInit(self):
        self._register_command(0, self._waste, "$"*50)
        self._register_command(1, self._waste, "§$$")    #trigger command (waste method)    trg §type $x $y
        self._register_command(2, self.end, "")           #exit command                      ext
        self._register_command(3, self.add, "***")        #addition command                  add *num1 *num2 *result
        self._register_command(4, self.sub, "***")        #subtraction command               sub *num1 *num2 *result
        self._register_command(5, self.mul, "***")        #multiplication commandm           mul *num1 *num2 *result
        self._register_command(6, self.div, "***")        #divide command (result is rounded)div *num1 *num2 *result
        self._register_command(7, self.set, "*$")         #set command                       set *adress $number
        self._register_command(8, self.nul, "*")          #set adress to 0                   nul *adress
        self._register_command(9, self.get, "*§")           #get command                     get *adress $item
        self._register_command(10, self.set_global, "*§")  #set command (world)               set_global *adress $item
        self._register_command(11,self.win,"")            #win
        self._register_command(12,self.loose,"")          #loose
        self._register_command(13,self.draw_image,"***")     #draw image to screen              drI *x *y *image
        self._register_command(14,self.draw_rect,"*****")      #draw rectangle to scrren          drR *x *y *color_R *color_G *color_B
        self._register_command(15,self.draw_clear,"**")    #clear graphics                    clr *x *y
        self._register_command(16,self.compare,"*§**"),     #compare a with op to b and save c comp *a §op *c => *c
        self._register_command(17,self.jmp, "**")           #jump x lines if cond is > 0  using * for jump lines, to allow for 2 byte input but more realistically it is constant
        self._register_command(18,self.set_flag, "§$")        #apply an flag to your very world setFlag §flag $value
        self._register_command(19,self.tp,"**")             #tp *x *y -- teleports the palyer
        self._register_command(20,self.jmpr, "**")
        self._register_command(21,self.download_ram, "*")   #createMemory at * Creates new, nested storage
        self._register_command(22,self.load_to_nest, "***") # loadToMemory at *adress with index *index from *source
        self._register_command(23,self.load_from_nest, "***") # loadFromMemory at *adress with index *index to *source
        self._register_command(24,self.rand, "***") #randomNumber from *min to *max => *storage
        self._register_command(25,self.load_ptr,"**") #loadFromPointer at *from to *to
        self._register_command(26,self.store_ptr,"**") # storeToPointer value *val to *ptr
        self._register_command(27,self.place_block,"*")
        self._register_command(28,self.show_text,"$*") #showtext *text using $mode
    def _waste(self, *args):
        return None
    def _exec(self, line):
        cmd = line[0]
        for c in self.commands:
            if c["byte"] == cmd:
                cmd = c
                break
        if type (cmd) == int:
            raise RuntimeError("Could not find command for byte {}".format(cmd))
        #print(cmd)
        exc_arg_length = 0
        for c in cmd["arginf"]:
            if c == "*":
                exc_arg_length += 2
            else:
                exc_arg_length += 1
        if exc_arg_length > len(line) - 1:
            raise RuntimeError("Exspected {}, got {} args".format(exc_arg_length, len(line)-1))
        args = ()
        b = 1
        for c in cmd["arginf"]:
            if b in range (len(line)):
                if c == "*":
                    args = args + (255*line[b] + line[b+1],)
                    b += 2
                else:
                    args = args + (line[b],)
                    b += 1
        cmd["method"](*args)
    def _psr_start(self):
        self.parser["running"] = True
        while self.parser["running"]:
            try:
                line = self.lines[self.parser["position"]]
                self._exec(line)
                #print(self.parser["position"], line)
                self.parser["position"] += 1
            except IndexError:
                #print("[DEBUG] EoF Error (cancelled execution)")
                self.end()
    def end(self):
        self.parser["running"] = False
    def add(self, a, b, c):
        self.ram[c] = self.ram[a] + self.ram[b]
    def sub(self, a, b, c):
        self.ram[c] = self.ram[a] - self.ram[b]
    def mul(self, a, b, c):
        self.ram[c] = int(self.ram[a] * self.ram[b])
    def div(self, a, b, c):
        self.ram[c] = round(self.ram[a]/self.ram[b])
    def load_ptr(self, f, t):
        self.ram[t] = self.ram[self.ram[f]]
    def store_ptr(self, v, p):
        self.ram[self.ram[p]] = self.ram[v]
    def set(self, adress, value):
        #print(adress,value)
        self.ram[adress] = value
    def nul(self, adress):
        self.ram[adress] = 0
    def get(self, adress, item):
        #itemlist:
        #0: ERRNO (NONE)
        #1: player health
        #2: player (total)
        #3: player(exp_range)
        #4: player (dynamite)
        #5: player (timed_bombs)
        #6: player (damage)
        #7: player (nukes)
        #8: player (x)
        #9: player (y)
        it = [0, self.world.player.health, self.world.player.item_maxbombs, self.world.player.range, self.world.player.item_dynamite, self.world.player.item_timebombs, self.world.player.damage, self.world.player.item_nukes,self.world.player.x,self.world.player.y]
        self.ram[adress] = it[item]
        self.world.player.repaint_inventory()
    def set_global(self,adress,item):
        if item == 1:
            self.world.player.health = self.ram[adress]
        if item == 2:
            self.world.player.stat_bombs = self.ram[adress]
            self.world.player.item_maxbombs = self.ram[adress]
        if item == 3:
            self.world.player.range = self.ram[adress]
        if item == 4:
            self.world.player.item_dynamite = self.ram[adress]
        if item == 5:
            self.world.player.item_timebombs = self.ram[adress]
        if item == 6:
            self.world.player.damage = self.ram[adress]
        if item == 7:
            self.world.player.item_nukes = self.ram[adress]
        if item == 8 or item == 9:
            print("[WARN] Player coordinates are read-only! Use tp instead!!!")
        self.world.player.repaint_inventory()
    def win(self):
        self.world.winf()
    def loose(self):
        self.world.loose()
    def draw_image(self,x, y, i):
        self.world.script_overlay[self.ram[x]][self.ram[y]] = sc.scriptGraphic(self.ram[x],self.ram[y],txtID=self.ram[i])
    def draw_rect(self,x,y,r,g,b):
        r = self.ram[r]
        g = self.ram[g]
        b = self.ram[b]
        x = self.ram[x]
        y = self.ram[y]
        r = hex(r)[2:]
        if len(r) < 2:
            r = "0" + r
        g = hex(g)[2:]
        if len(g) < 2:
            g = "0" + g
        b = hex(b)[2:]
        if len(b ) < 2:
            b = "0" + b
        self.world.script_overlay[x][y] = sc.scriptGraphic(x,y,color="#"+r+g+b)
    def draw_clear(self, x,y):
        self.world.script_overlay[x][y] = None
    def place_block(self, adress):

        ID = self.ram[adress]
        X = self.ram[adress+1]
        Y = self.ram[adress+2]
        blocktypes = [block.air, block.bedrock, block.brick, block.water, item.item, enemy.enemy]
        bt = blocktypes[ID]
        match (bt):
            case item.item:
                self.world.blocks[X][Y] = item.item(self.world,(X,Y),self.ram[adress+3],self.ram[adress+4])
            case enemy.enemy:
                self.world.blocks[X][Y] = enemy.enemy(self.world, (X,Y),self.ram[adress+3],self.ram[adress+4])
            case block.air:
                self.world.blocks[X][Y] = block.air(self.world)
            case other:
                self.world.blocks[X][Y] = bt(self.world, (X,Y))
        return
    def compare(self, a, op, b, c): #Save 0 if false, save 1 if true
        a = self.ram[a]
        b = self.ram[b]
        ops = [None, ">","<","==","<=",">="]
        op = ops[op]
        self.ram[c] = 0
        if op == ">":
            if a > b:
                self.ram[c] = 1
        if op == "<":
            if a < b:
                self.ram[c] = 1
        if op == "==":
            if a == b:
                self.ram[c] = 1
        if op == "<=":
            if a <= b:
                self.ram[c] = 1
        if op == ">=":
            if a >= b:
                self.ram[c] = 1
    def jmp(self, rel_line, cond):
        if self.ram[cond] != 0:
            self.parser["position"] += (rel_line-1)
    def jmpr(self, rel_line, cond):
        self.jmp(self.ram[rel_line], cond)
    def set_flag(self, flag, value):
        val = True if value != 0 else False
        flags = [None,"drop_items","enemy_damage","enemy_ai"]
        flag = flags[flag]
        self.world.setFlag(flag,val)
    def tp(self, x, y):
        x0 = self.world.player.x
        y0 = self.world.player.y
        x = self.ram[x]
        y = self.ram[y]
        vx = x - x0
        vy = y - y0
        self.world.player.move(vx,vy,True)
    def download_ram(self, slot):
        self.ram[slot] = [0]*65536
    def load_to_nest(self, location, index, source):
        self.ram[location][index] = copy.deepcopy(self.ram[source])
    def load_from_nest(self, location, index, destination):
        self.ram[destination] = copy.deepcopy(self.ram[location][index])
    def rand(self, i, a,d):
        self.ram[d] = random.randint(self.ram[i],self.ram[a])
    def show_text(self, mode, textp):
        #print(mode, textp)
        #print("HELLO",self.world.texts)
        #mapping 0: popup; 1: top; ???
        mode -= 1
        try:
            text_to_show = self.world.texts[self.ram[textp]]
        except Exception as e:
            print("EXCEPTION", e)
            raise RuntimeError(e)
        #print("BYE")
        match (mode):
            case 0:
                Dialogs.BasicDialog(self.world.win.pr,"TEXT",text_to_show,fadeout=1000)
                pass
            case 1:
                self.world.win.pr.ui.sidebar_label.setText(text_to_show)
                pass
