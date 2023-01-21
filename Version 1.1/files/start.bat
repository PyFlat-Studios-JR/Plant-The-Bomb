echo off
cls
if EXIST status.txt (
goto start
)
echo **NOTE**
echo On the first launch of the game, all required additional python modules have to be installed
echo Depending on the already installed modules, this could take a while
echo performing check for required modules
for /F "delims=;" %%i in (requirements.txt) do (
python -c "import pkgutil; import os; os.system('echo %%i: OK' if pkgutil.find_loader('%%i') else 'echo %%i: MISSING')"
)
echo installing required modules...
for /F "delims=;" %%i in (requirements.txt) do (
pip -q -q -q install %%i
echo installed %%i
)
echo Installation successfull
echo OK > status.txt
echo proceeding to start game
:start
echo off
title Plan The Bomb Console
cls
echo **INFO**
echo This Screen has no meaning, just minimize it
echo Running Plant The Bomb v.1.1
python plant_the_bomb.py
cls
echo Process terminated
exit