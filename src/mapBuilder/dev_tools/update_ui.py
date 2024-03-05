import os
main_win  = open("mainwindow_ui.py", "r").read()
new = main_win[main_win.find("self.actionSave ="):]


main_win_new = open("../src/MainWindow.py", "r+").read()
old = main_win_new[:main_win_new.find("self.actionSave")]
res = old+new
res = res.replace("textures/","src/mapBuilder/textures/")
res = res.replace("icons/", "src/mapBuilder/icons/")
open("../src/MainWindow.py", "w").write(res)

os.remove("mainwindow_ui.py")
