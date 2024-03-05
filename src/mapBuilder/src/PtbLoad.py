import json
from src.mapBuilder.src.compressor import *
class PtbLoader():
    def __init__(self):
        self.blocks = [[None for i in range(25)] for j in range(25)]
        self.scripts = None
        self.texts = None
    def load_file(self, filepath:str):
        comp = compressor()
        comp.load(filepath)
        comp.decompress()
        return self.convert_data(comp.get_data())
    def convert_data(self, data:tuple):
        data0 = json.loads(json.dumps(data[0]))
        world = data0["world"]
        self.texts = data0["texts"]
        self.scripts = data[1]
        id_mapping = {
            0: 1, -1: None, 2: 0, 3: 3, 4: 2, 5: {450: 4,700: 5,900: 6,20: 7,150: 8,55: 9,80: 11,0: 12,260: 13},
            6: lambda temp: [10, temp["objectData"]["health"], temp["objectData"]["id2"], temp["objectData"]["id1"]]
        }
        for x in range(25):
            for y in range(25):
                temp = world[x][y]
                id_map = id_mapping.get(temp["id"])
                if id_map is not None:
                    if isinstance(id_map, int):
                        self.blocks[x][y] = id_map
                    elif isinstance(id_map, dict):
                        self.blocks[x][y] = id_map.get(temp["objectData"]["start"])
                    else:
                        self.blocks[x][y] = id_map(temp)
        return self.blocks, self.scripts, self.texts
