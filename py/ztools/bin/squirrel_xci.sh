#!/bin/bash

cd ..

python squirrel.py -b 65536 -pv 11 -kp 11 --RSVcap 605028352 -fat exfat -fx files -ND true -t xci -o "../out/NSCB_temp" -tfile "../out/mlist.txt" -roma TRUE -dmul "calculate"