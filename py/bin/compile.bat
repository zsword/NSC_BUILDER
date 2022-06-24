@echo off
echo "Compile NSC_Builder ..."

cd %~dp0

cd ..\ztools
pyinstaller -p Drive/ -p Fs/ -p lib/ -p manager/ -p mtp/ -p nutFs/ -p _bottle_websocket_/ -p _EEL_/ --noconfirm squirrel.py
move /Y dist\squirrel\squirrel.exe dist\ztools\
pyinstaller --noconfirm squirrel_lib_call.py
move /Y dist\squirrel_lib_call\squirrel_lib_call.exe dist\ztools\