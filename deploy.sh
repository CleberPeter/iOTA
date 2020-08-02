#!/bin/bash
# script to deploy esp32

ampy --port /dev/ttyUSB0 --baud 115200 put main.py
picocom /dev/ttyUSB0 -b115200
