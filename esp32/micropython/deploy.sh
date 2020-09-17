#!/bin/bash
# script to deploy esp32

BASEDIR=$(dirname "$0")

if [[ $1 == "--erase" ]]
then
    esptool.py erase_flash
elif [[ $1 == "--write" ]]
then
    esptool.py erase_flash
    esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 firmware.bin
elif [[ $1 == "--write_ota" ]]
then
    esptool.py erase_flash
    esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 firmware_ota.bin
elif [[ $1 != "--only_run" ]]
then 
    :
    ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/boot.py
    #ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/main.py
    #ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/tst_class.py
    #ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/suit.py
    #ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/memory_esp32.py
    #ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/manifest.py

    #ampy --port /dev/ttyUSB0 --baud 115200 rmdir /umqttIota
    #ampy --port /dev/ttyUSB0 --baud 115200 mkdir /umqttIota
    #ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/micropython-lib/umqtt.robust/umqtt/robust.py /umqttIota/robust.py
    #ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/micropython-lib/umqtt.simple/umqtt/simple.py /umqttIota/simple.py
fi

picocom /dev/ttyUSB0 -b115200