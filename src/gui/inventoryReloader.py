
from PySide6.QtGui import QPixmap
import src.engine.textureLib as textureLib

class inventoryReloader():
    def reloadInventoryIcons(ui):
        ui.range_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(9)))
        ui.bomb_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(11)))
        ui.health_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(13)))
        ui.timebomb_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(15)))
        ui.dynamite_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(17)))
        ui.damage_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(20)))
        ui.nuke_icon_btn.setIcon(QPixmap.fromImage(textureLib.textureLib.getTexture(23)))