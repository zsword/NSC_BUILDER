#!/bin/bash

cd ztools
pyinstaller -p Drive/ -p Fs/ -p lib/ -p manager/ -p mtp/ -p nutFs/ -p _bottle_websocket_/ -p _EEL_/ --noconfirm squirrel.py
cd dist
mv -f squirrel/squirrel ztools/