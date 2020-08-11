import time
import network
from suit import fotaSuit

debug = True
idWifi = 'House'
pswdWifi = 'raquel999'
typeDelivery = 'Push'
hostBroker = "192.168.0.103"
uuid = "1"
version = 11 # current version

def connect_wifi(id, pswd):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(id, pswd)
        while not sta_if.isconnected():
            pass
    print('network ip:', sta_if.ifconfig()[0])

def onReceiveUpdate(filename):
    print("update received: " + filename)

connect_wifi(idWifi, pswdWifi)
_fota = fotaSuit(uuid, version, hostBroker, onReceiveUpdate, typeDelivery, debug)

while True:
    # do someting ...
    time.sleep(1)