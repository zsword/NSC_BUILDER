@echo off
echo "Compile NSC_Builder ..."

cd %~dp0

cd ..\ztools
pyinstaller -p Drive/ -p Fs/ -p lib/ -p manager/ -p mtp/ -p nutFs/ -p _bottle_websocket_/ -p _EEL_/ --noconfirm squirrel.py
cd dist
move /S/Q squirrel\squirrel.exe ztools/