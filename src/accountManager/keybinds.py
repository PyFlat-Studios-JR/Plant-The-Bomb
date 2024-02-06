class keybindManager():
    def __init__(self):
        self.data = {
            "move_up": [87,16777235],
            "move_down":[83,16777237],
            "move_right":[68,16777236],
            "move_left":[65,16777234],
            "place_bomb_normal":[32,75],
            "place_bomb_dynamite":[89,0],
            "place_bomb_timed":[84,0],
            "detonate_timed_bomb": [35, 0],
            "place_bomb_nuke":[78,0]
        }
    def load(self, initv={}):
        keys_completed = []
        for key in initv:
            if key in self.data:
                keys_completed.append(key)
                self.data[key] = initv[key]
    def ret(self):
        return self.data
    def set(self, item, value, add=False):
        if item in self.data:
            if add:
                self.data[item] += value
            else:
                self.data[item] = value
    def get(self, item):
        if item in self.data:
            return self.data[item]
    def get_data(self):
        return list(self.data.keys())
__GLOBAL_REG = None

def getKeybindManager():
    global __GLOBAL_REG
    if __GLOBAL_REG == None:
        __GLOBAL_REG = keybindManager()
    return __GLOBAL_REG
