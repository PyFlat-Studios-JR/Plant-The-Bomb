class register():
    def __init__(self):
        self.data = {
            "bombs_placed": 0,          #done
            "dynamite_placed": 0,       #done
            "nukes_placed": 0,          #done
            "timebombs_placed": 0,      #done
            "bombs_placed_total": 0,    #done

            "damage_dealt": 0,          #done
            "damage_recieved": 0,       #done
            
            "enemies_killed": 0,        #done
            "blocks_exploded": 0,       #done
            "blocks_walked": 0,         #done

            "items_collected_total": 0,         #done
            "items_collected_damage": 0,        #done
            "items_collected_health": 0,        #done
            "items_collected_bombs": 0,         #done
            "items_collected_dynamite": 0,      #done
            "items_collected_timebombs": 0,     #done
            "items_collected_nukes": 0,         #done
            "items_collected_shields": 0,       #done
            "items_collected_curses": 0,        #done
            "items_collected_range": 0,         #done

            #All times are in TICKS! (1/20)th of a second!
            "times_spent_total": 0,          
            
            "levels_completed_total": 0,    #done
            "levels_completed": {},         #done
            "levels_played_total": 0,       #done
            "levels_played": {},            #done
            "time_spent_level_total": 0,    #done
            "time_spent_levels": {}         #done
        }
    def load(self, initv={}):
        keys_completed = []
        for key in initv:
            if key in self.data:
                keys_completed.append(key)
                self.data[key] = initv[key]
    def ret(self):
        return self.data
    def set(self, item, value, add=True):
        if item in self.data:
            if add:
                self.data[item] += value
            else:
                self.data[item] = value
    def get(self, item):
        if item in self.data:
            return self.data[item]
__GLOBAL_REG = None

def getStatContext():
    global __GLOBAL_REG
    if __GLOBAL_REG == None:
        __GLOBAL_REG = register()
    return __GLOBAL_REG
