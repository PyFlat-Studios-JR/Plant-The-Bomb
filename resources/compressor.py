import json
class compressor():
    def __init__(self, key = None):
        self.data = None
        self.scripts = b"\x00\x0d"
        self.texts = "::"
        self.mode = 0 #0: compress, 1: decompress
        self.key = key
        self.result = None
        self.name = ""
    def load(self, file):
        f = file.split(".")
        end = f[len(f)-1]
        rest = ""
        for i in range(0, len(f)-1):
            rest += f[i]
            rest += "."
        self.name = rest
        if end == "ptb":
            self.mode = 1
            self.data = open(file, "rb").read()
        elif end == "json":
            self.mode = 0
            self.data = json.loads(open(file, "r").read())
            for i in range (0, len(self.data["world"])):
                for j in range (0, len(self.data["world"][i])):
                    self.data["world"][i][j]["id"] += 1
            try:
                ss = rest + "sbin"
                self.scripts = open(ss,"rb").read()
            except:
                print("[WARNING] Could not retrieve script source")
            try:
                ss = rest + "txt"
                self.texts = open(ss,"r").read()
                self.texts = self.texts.split("\n")
                t = ""
                for i in range (0, len(self.texts)):
                    t += self.texts[i]
                    t += "::"
                self.texts = t
            except:
                if self.data["texts"] != []:
                    self.texts = self.data["texts"]
                    t = "::"
                    for x in self.texts:
                        t += x
                        t += "::"
                    self.texts = t
                else:
                    print("[WARNING] Could not find or load texts")
        else:
            print("[ERROR] Unrecognizable File Format")
        print("Loaded File: " + file)
    def insert_normal(self, world, scripts=None,texts=None):
        if scripts == None:
            scripts = b"\x00\x0d"
        if texts == None:
            try:
                texts = world["texts"]
            except KeyError:
                texts = "::"
        self.scripts = scripts
        self.data = world
        for i in range (0, len(self.data["world"])):
            for j in range (0, len(self.data["world"][i])):
                self.data["world"][i][j]["id"] += 1
        if type(texts) == type(""):
            texts = texts.split("\n")
            ntxt = ""
            for t in texts:
                ntxt += t + "::"
            self.texts = ntxt
        elif type(texts) == type([]):
            ntxt = ""
            for t in texts:
                ntxt += t + "::"
            self.texts = ntxt
        else:
            self.texts = "::"
        #self.texts = texts
        self.mode = 0
    def insert_comp(self, comp):
        self.data = comp
        self.mode = 1
    def get_key(self):
        #Manage Block Ids (Key Byte 1 und 2)
        ids = []
        for i in range (0, len(self.data["world"])):
            for j in range (0, len(self.data["world"][i])):
                ids.append(self.data["world"][i][j]["id"])
        i = max(ids)
        i = util.get_bin_length(i)
        if i > (1 << 16)-1:
            raise ValueError("Required minimum Bitlength for Block Ids exceeds maximum of "+str((1<<16)-1)+ " Bits")
        key_part_1 = (i).to_bytes(2, "big")
        #Now Do the exact same thing for enemy types, and attacks as well as health:
        e_t = [1]
        e_a = [1]
        e_h = [1]
        show_error = False
        for i in range (0, len(self.data["world"])):
            for j in range (0, len(self.data["world"][i])):
                if self.data["world"][i][j]["id"] == 7:
                    try:
                        e_t.append(self.data["world"][i][j]["objectData"]["id1"])
                    except KeyError:
                        show_error = True
                    e_a.append(self.data["world"][i][j]["objectData"]["id2"])
                    e_h.append(self.data["world"][i][j]["objectData"]["health"])
        if show_error:
            print("[WARNING] Using outdated Save format. Could not set enemy type data")
        t = max(e_t)
        a = max(e_a)
        h = max(e_h)
        t = util.get_bin_length(t)
        a = util.get_bin_length(a)
        h = util.get_bin_length(h)
        if t > (1 << 8)-1:
            raise ValueError("Required minimum Bitlength for enemy types exceeds maximum of "+str((1<<8)-1)+ " Bits")
        if a > (1 << 8)-1:
            raise ValueError("Required minimum Bitlength for enemy attacks exceeds maximum of "+str((1<<8)-1)+ " Bits")
        if h > (1 << 32)-1:
            raise ValueError("Required minimum Bitlength for enemy Health exceeds maximum of "+str((1<<32)-1)+ " Bits")
        key_part_2 = (t).to_bytes(1, "big")
        key_part_3 = (a).to_bytes(1, "big")
        key_part_4 = (h).to_bytes(4, "big")
        self.key = key_part_1 + key_part_2 + key_part_3 + key_part_4
        print("Generated Key : " + str(self.key))
    def compress(self):
        if self.mode != 0:
            print("[ERROR] System set to decompression mode: Invalid data")
            return
        if self.data == None:
            print("[ERROR] No data found to compress")
            return
        if self.key == None:
            print("[INFO] No key found. Generating key to match data")
            self.get_key()
        result = b""
        bin_result = ""
        byte_texts = self.texts.encode("ascii")
        bin_enemy = ""
        bin_items = ""
        bin_world = ""
        debug_c_enemy = 0
        debug_c_item = 0
        for i in range (0, len(self.data["world"])):
            for j in range (0, len(self.data["world"][i])):
                bin_world += util.transform_to_bin(self.data["world"][i][j]["id"], int.from_bytes(self.key[0:2],"big"))
                if self.data["world"][i][j]["id"] == 7:
                    debug_c_enemy += 1
                    try:
                        bin_enemy += util.transform_to_bin(self.data["world"][i][j]["objectData"]["id1"], self.key[2])
                    except KeyError:
                        bin_enemy += util.transform_to_bin(1, self.key[2])
                    bin_enemy += util.transform_to_bin(self.data["world"][i][j]["objectData"]["id2"],self.key[3])
                    bin_enemy += util.transform_to_bin(self.data["world"][i][j]["objectData"]["health"],int.from_bytes(self.key[5:],"big"))
                if self.data["world"][i][j]["id"] == 6:
                    debug_c_item += 1
                    v = ""
                    v += util.transform_to_bin(self.data["world"][i][j]["objectData"]["start"],10)
                    v += util.transform_to_bin(self.data["world"][i][j]["objectData"]["fin"],10)
                    #print(v)
                    bin_items += v
        bin_result = bin_world + bin_items + bin_enemy
        #print(bin_result)
        while len(bin_result) % 8 != 0:
            bin_result = bin_result + "0"
        result += self.key
        for b in range (0, int(len(bin_result)/8)):
            result += (util.transform_to_int(bin_result[b*8:b*8+8])).to_bytes(1,"big")
        result += byte_texts
        result += self.scripts
        self.result = result
    def decompress(self):
        if self.mode != 1:
            print("[ERROR] System set to decompression mode: Invalid data")
        if self.data == None:
            print("[ERROR] No data found to compress")
            return
        #Read key
        self.key = self.data[0:8]
        #remove key from data
        self.data = self.data[8:]
        #Fragment key and turn to int
        key_world = int.from_bytes(self.key[0:2], "big")
        key_enemy_t = self.key[2]
        key_enemy_a = self.key[3]
        key_enemy_h = int.from_bytes(self.key[4:], "big")
        #Get exspected World Size
        ex_size_world = 625*key_world
        #turn world binary
        bin_everything = ""
        for i in range (0,len(self.data)):
            bin_everything += util.transform_to_bin(self.data[i],8)
        #print(bin_everything)
        bin_world = bin_everything[0:ex_size_world]
        count_item = 0
        count_enemy = 0
        #Generate enemy and item count
        for i in range (0, int(len(bin_world)/key_world)):
            bid = util.transform_to_int(bin_world[i*key_world:(i+1)*key_world])
            bid -= 1
            if bid == 6:
                count_enemy += 1
            if bid == 5:
                count_item += 1
       # print(count_enemy, count_item)
        ex_size_enemy = count_enemy * (key_enemy_t+key_enemy_h+key_enemy_a)
        ex_size_item = count_item * 20
        ex_size_total = ex_size_enemy + ex_size_item + ex_size_world
        #now that weve go the relevant stuff, we can extend towards bytes
        ex_size_total_pad = ex_size_total
        pad = 0
        while ex_size_total_pad % 8 != 0:
            ex_size_total_pad += 1
            pad += 1
        bin_all = bin_everything[0:ex_size_total]
        byte_size_block_1 = int(ex_size_total_pad/8)
        byte_block_text_and_script = self.data[byte_size_block_1:]
        #Bin world already here
        bin_item = bin_all[ex_size_world:ex_size_world+ex_size_item]
        bin_enemy = bin_all[ex_size_world+ex_size_item:ex_size_world+ex_size_item+ex_size_enemy]
        #Prep done
        #Now start parser
        a_world = []
        idx_item_parse = 0
        idx_enemy_parse = 0
        for i in range (0, int(len(bin_world)/key_world)):
            bin_block = bin_world[i*key_world:(i+1)*key_world]
            int_block = util.transform_to_int(bin_block) - 1
            #bid being block-id
            if int_block == 6:
                bin_enemy_part = bin_enemy[idx_enemy_parse*(key_enemy_t+key_enemy_h+key_enemy_a):(idx_enemy_parse+1)*(key_enemy_t+key_enemy_h+key_enemy_a)]
                bin_enemy_part_etype = bin_enemy_part[0:key_enemy_t]
                bin_enemy_part_ktype = bin_enemy_part[key_enemy_t:key_enemy_t+key_enemy_a]
                bin_enemy_part_health = bin_enemy_part[key_enemy_t+key_enemy_a:]
                int_enemy_part_etype = util.transform_to_int(bin_enemy_part_etype)
                int_enemy_part_ktype = util.transform_to_int(bin_enemy_part_ktype)
                int_enemy_part_health = util.transform_to_int(bin_enemy_part_health)
                o = {
                    "id": int_block,
                    "objectData":
                        {
                        "id1":int_enemy_part_etype,
                        "id2":int_enemy_part_ktype,
                        "health":int_enemy_part_health
                        }
                    }
                idx_enemy_parse += 1
            elif int_block == 5:
                bin_item_part = bin_item[idx_item_parse*20:(idx_item_parse+1)*20]
                bin_item_part_start = bin_item_part[0:10]
                bin_item_part_fin = bin_item_part[10:]
                int_item_part_start = util.transform_to_int(bin_item_part_start)
                int_item_part_fin = util.transform_to_int(bin_item_part_fin)
                o = {
                    "id": int_block,
                    "objectData":
                        {
                        "start":int_item_part_start,
                        "fin":int_item_part_fin
                        }
                    }
                idx_item_parse += 1
            else:
                o = {"id": int_block, "objectData":{}}
            a_world.append(o)
        total_world = []
        for x in range (0, 25):
            total_world_part = a_world[x*25:(x+1)*25]
            total_world.append(total_world_part)
        # byte_block_text_and_script ybtes of text
        texts = []
        ctext = ""
        script_first = 0
        for i in range (0, len(byte_block_text_and_script)):
            #print(ctext)
            if chr(byte_block_text_and_script[i]) == ":" and chr(byte_block_text_and_script[i+1]) == ":":
                if byte_block_text_and_script[i+2] == 0:
                    texts.append(ctext)
                    ctext = ""
                    print("LOL",texts)
                    script_first = i+2
                    break
                texts.append(ctext)
                ctext = ""
            elif chr(byte_block_text_and_script[i]) != ":":
                ctext += chr(byte_block_text_and_script[i])
        if texts == [""]:
            texts = []
        self.texts = texts
        #print(script_first)
        self.scripts = byte_block_text_and_script[script_first:]
        self.result = {
            "world": total_world,
            "texts": texts
            }
        #World done
    def get_data(self):
        return (self.result, self.scripts, self.texts)
    def set_key(self, key):
        self.key = key
    def save(self, path = None):
        if path != None:
            n = ""
            pp = path.split(".")
            for i in range (0, len(pp)-1):
                n += pp[i] + "."
            self.name = n
        if self.result == None:
            print("[ERROR] No data found to save")
            return False
        if self.mode == 0:
            file = open(self.name+"ptb","wb")
            file.write(self.result)
            file.close()
            return True
        elif self.mode == 1:
            pass
            #not yet in here
        else:
            print("[ERROR] No valid Operation")
            return False
class util():
    def get_bin_length(data):
        i = 0
        while True:
            bl = (1 << i)-1
            if bl >= data:
                return i
            i += 1
    def transform_to_bin(data, length=-1):
        t = bin(data).split("b")[1]
        if length > -1:
            while len(t) < length:
                t = "0" + t
        return t
    def transform_to_int(data):
        t = "0b" + data
        return int(t, 2)

"""
cmp = compressor()
cmp.insert_normal(json.loads(open("test.json").read()),b"\x00\x05\x01\x01\x00\x0d","test\ntest\ntest")
cmp.compress()
dc = compressor()
dc.insert_comp(cmp.result)
dc.decompress()
print(dc.get_data()[2])
"""
