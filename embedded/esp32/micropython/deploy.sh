#!/bin/bash
# script to deploy esp32

BASEDIR=$(dirname "$0")

ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/main.py
ampy --port /dev/ttyUSB0 --baud 115200 put "$BASEDIR"/suit.py
picocom /dev/ttyUSB0 -b115200
