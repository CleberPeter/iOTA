"""
Usage example of class fotaSuit
"""
import time
import network
import os
import sys
import machine
from suit import FotaSuit

_companytec = True

if _companytec:
    HOST_BROKER = "192.168.0.139"
    ID_WIFI = 'WIFI_P&D' 
    PSWD_WIFI = 'prjtdsnvmnt,1421'
else:
    HOST_BROKER = "192.168.0.102"
    ID_WIFI = 'HOUSE'
    PSWD_WIFI = 'raquel999'

DEBUG = True
TYPE_DELIVERY = 'Push'
UUID_PROJECT = "1" # universal unique id from project (only used if not exists an local manifest).
ID_DEVICE = "84" # id from device inside project.
VERSION = 11 # current version of device (only used if not exists an local manifest).

# public key from server to verify signatures.
PUB_KEY_SRV = "04a15091093d0b516c88c3d0e46dbc0dc3b551da5ff823682559b27e68542c19e611229a22e549bcf45119985e102c6c0077c9c65b17e54648577de72720aa826b" 

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
        FOTA = FotaSuit(UUID_PROJECT, ID_DEVICE, VERSION, HOST_BROKER, on_receive_update, PUB_KEY_SRV, TYPE_DELIVERY, DEBUG)
    except Exception as error:
        print(error)
        sys.exit()

    print('waiting for version: ' + str(FOTA.manifest.get_next_version()))

    while True:
        # do someting ...
        time.sleep(1)
