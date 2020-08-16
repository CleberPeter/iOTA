#!/bin/bash
# script to deploy esp32

BASEDIR=$(dirname "$0")

# esptool.py erase_flash
# esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 firmware.bin

if [[ $1 != "--only_run" ]]
then 
    :
    ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/main.py
    # ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/suit.py

    # ampy --port /dev/ttyUSB0 --baud 115200 rmdir /umqttIota
    # ampy --port /dev/ttyUSB0 --baud 115200 mkdir /umqttIota
    # ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/micropython-lib/umqtt.robust/umqtt/robust.py /umqttIota/robust.py
    # ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/micropython-lib/umqtt.simple/umqtt/simple.py /umqttIota/simple.py
fi

picocom /dev/ttyUSB0 -b115200
