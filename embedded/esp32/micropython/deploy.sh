#!/bin/bash
# script to deploy esp32

BASEDIR=$(dirname "$0")

#ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/main.py
ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/suit.py

#ampy --port /dev/ttyUSB0 --baud 115200 rmdir /umqttIota
#ampy --port /dev/ttyUSB0 --baud 115200 mkdir /umqttIota
#ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/micropython-lib/umqtt.robust/umqtt/robust.py /umqttIota/robust.py
#ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/micropython-lib/umqtt.simple/umqtt/simple.py /umqttIota/simple.py

picocom /dev/ttyUSB0 -b115200
