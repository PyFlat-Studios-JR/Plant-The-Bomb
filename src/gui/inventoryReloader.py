
from PySide6.QtGui import QPixmap
import src.engine.textureLib as textureLib

class inventoryReloader():
    def reloadInventoryIcons(ui):
        ui.bomb_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(9)))
        ui.bomb_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(11)))
        ui.bomb_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(13)))
        ui.bomb_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(15)))
        ui.bomb_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(17)))
        ui.bomb_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(20)))
        ui.bomb_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(23)))