#/bin/bash

cd /home/pi/wphone
python3 turn-led-on.py
aplay wphone-ready.wav
python3 wphone.py
