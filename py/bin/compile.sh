#!/bin/bash

cd ../ztools
LIB_PATH=/home/jemichow/.local/lib/python3.7/site-packages
pyinstaller -p Drive/ -p Fs/ -p lib/ -p manager/ -p mtp/ -p nutFs/ -p _bottle_websocket_/ -p _EEL_/ -p $LIB_PATH -p $LIB_PATH/deprecated -p $LIB_PATH/googletrans -p $LIB_PATH/zstandard -p $LIB_PATH/gevent --noconfirm squirrel.py
cp dist/ztools/keys.txt dist/squirrel/
#mv -f dist/squirrel/squirrel dist/ztools/
pyinstaller --noconfirm squirrel_lib_call.py
#mv -f dist/squirrel_lib_call/squirrel_lib_call dist/ztools/