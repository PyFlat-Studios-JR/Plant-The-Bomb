import os
from PySide6.QtGui import QImage
class textureLib():
    __TEXTURES: list[QImage] = []
    __TEXTURE_MAP: dict[str, int] = {}
    __ERR_IMAGE = None
    def loadFolder(path: str, ERR: str):
        textureLib.__ERR_IMAGE = QImage(ERR)
        for file in os.listdir(path):
            if file.endswith(".png"):
                textureLib.__TEXTURES.append(QImage(file))
                file = file.split("_")
                file.pop(0)
                file = "".join(file)
                file = "".join(file.split(".")[:-1]) 
                textureLib.__TEXTURE_MAP[file] = len(textureLib.__TEXTURES)-1
    def getTexture(texture: int | str):
        if textureLib.__ERR_IMAGE == None:
            raise ValueError(f"Texture loader was called before initialization. Do not do that.")
        if type(texture) == str:
            if not texture in textureLib.__TEXTURE_MAP:
                return textureLib.__ERR_IMAGE
            texture = textureLib.__TEXTURE_MAP[texture]
        if type(texture) == int:
            return textureLib.__TEXTURES[texture]
        print(f"UI Failure: unknown parameter type for {texture}: {type(texture)}")
        return textureLib.__ERR_IMAGE
            