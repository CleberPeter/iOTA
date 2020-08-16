"""
Usage example of class fotaSuit
"""
import time
import network
from suit import FotaSuit

DEBUG = True
ID_WIFI = 'House'
PSWD_WIFI = 'raquel999'
TYPE_DELIVERY = 'Push'
HOST_BROKER = "192.168.0.103"
UUID = "1"
VERSION = 11 # current version


def connect_wifi(_id, _pswd):

    """
        Connect to wifi, only returns when connection is established.

        Args:
            _id (string): id of wifi
            _pswd (string): password of wifi
        Returns:
            void
    """
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(_id, _pswd)
        while not sta_if.isconnected():
            pass
    print('network ip:', sta_if.ifconfig()[0])

def on_receive_update(_filename):
    """
        Callback, called when upgrade file received from fotaSuit.

        Args:
            _filename (string): filename of file received.
        Returns:
            void
    """

    print("update received: " + _filename)
"""
connect_wifi(ID_WIFI, PSWD_WIFI)
FOTA = FotaSuit(UUID, VERSION, HOST_BROKER, on_receive_update, TYPE_DELIVERY, DEBUG)

while True:
    # do someting ...
    time.sleep(1)
"""
