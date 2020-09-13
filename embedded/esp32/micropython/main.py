"""
Usage example of class fotaSuit
"""
import time
import network
import os
import sys
import machine
from suit import FotaSuit

DEBUG = True
ID_WIFI = 'House'
PSWD_WIFI = 'raquel999'
TYPE_DELIVERY = 'Push'
HOST_BROKER = "192.168.0.103"
UUID_PROJECT = "1" # universal unique id from project (only used if not exists an local manifest).
ID_DEVICE = "84" # id from device inside project.
VERSION = 11 # current version of device (only used if not exists an local manifest).

sta_if = network.WLAN(network.STA_IF)

def connect_wifi(_id, _pswd):

    """
        Connect to wifi, only returns when connection is established.

        Args:
            _id (string): id of wifi
            _pswd (string): password of wifi
        Returns:
            void
    """
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(_id, _pswd)
        while not sta_if.isconnected():
            pass
    print('network ip:', sta_if.ifconfig()[0])

def on_receive_update():
    """
        Callback, called when upgrade file received from fotaSuit.

        Args:
            void
        Returns:
            void
    """

    print("update received!")
    print('next version: ' + str(FOTA.manifest.get_next_version()))
    machine.reset()

while True:

    connect_wifi(ID_WIFI, PSWD_WIFI)

    try:
        FOTA = FotaSuit(UUID_PROJECT, ID_DEVICE, VERSION, HOST_BROKER, on_receive_update, TYPE_DELIVERY, DEBUG)
    except Exception as error:
        print(error)
        sys.exit()

    print('current version: ' + str(FOTA.manifest.version))

    while True:
        # do someting ...
        time.sleep(1)
