"""
Usage example of class fotaSuit
"""
import time
import network
import os
import sys
import machine
from suit import FotaSuit

_companytec = False

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

# ECDSA-SECP256K1 public key from AUTHOR to verify signatures.
PUBLIC_KEY_AUTHOR = "04f6d7c46506ec87455d42f66d29adc8d5a2a35787e7b5bf3902a08786e57a4943dc70c95012ae9fffc351f721fc314530b8390e5bfd805e56e6460225d6fbd605" 

# RSA-2048b private key from PROJECT to decrypt AES256 random key.
PRIVATE_KEY_PROJECT = "308204a9020100028201010093878519dd89da824a7c6e475f3b280fcb3c80515b38f088259536f6d6bc0de878d63f956041cad4fbfcda3e53f7b40ac2d454b9944ed02a212d33ed816331981892eacca49a22d03dd6a7a071d71f46cb99aff62941dee4a49943222bcd9ff365dc6012884d85203173153e0b178c87ee56e8d108c7aa4306ef4a360cf2609f2e9fa57dd6aaf5a1b2ccf1d15a1862d7e8164a8690e79990a8057cab2c694a2b22a7d6bd1d4bfd56dc28fdf3e1b277397988b4fcb37978ec04fa50d4d9af2989c3669c54b2e46e2c5a4116c48ee7c987d1ceeac5e56b76152d9b607bc7b1c357264882a1cc66a764c5aae728c125b008bd359609a11c39cdccbfd1d51a0a909b02030100010282010031907c353e6acc10adf9b40b22817b6a22fbc6988eaf489055201681438f96949dd44d34604c7a5aa7f64154635d7b0d8a7b4fa3b1a1f0e9d68f9b3c9615bf59bc17cfeec4f64befee76a9868bf89c376abbcd9444342f305de467db991fd23731e7a21757d7c37c1760f4a80d8df1d6d14a3d99ccfb57c63b3156e154642d224f212b5185ac5a9bb03f5ea1b262482e4354674d62136c731a158fb3cd562e9761a95d8d7c9476badb6a3233088907d142e64168ec85a00c8e124306a70effc48a61fad8a9d2bfec119bd9ed462e2bd113e61f8f525ce26703f9f913dc040c8e4eddd485eb46d6b8512cc9c0e28f86b14a1e720e52147d605cc70d472d279aa102818900d003b4ae9b3207408f4b9a3499e252c26b07bf387bc468df7bcbb246f9bb4af355a630aa39d7f947b5f7e4fdd886a7b354f0dd6766356d5f0a46081ea923e08efe851e14479646be94f689ca030fa2ba13e724d0800d63ad5b7d862f49784f3a1ce3a4d66c7e12dd510c13e68feb492bffcb87bd1b4889e428debd9509b3e8052041f5910b720323027900b58fdddf1b28f35635fc7a6a98062a3765039636b2b09dc52b265096ce3f4ee731ddacbb24de1e5c10cf3d83d119c1bac8625999397549590cec536f72efc59f9a0ad76865217c05db5d540fb72188b55ddcabbe09fa50da3fe03d1c647e22a1e182234a4c66ef94895dd7c5acee563d1a7123d68ce0b02902818900c2aaf52882aceb048c15e096617ce09e79b3a24ca5e7458e0038bcfa9733a40cdd96cdec407dd2183e3f63d9fc0ce85c779d825605dcf22203674eaa02f8446b0dde5e2bf462ba8a18b6307511304cc57f62cd9d2279655313500187b766141efa72400d3b33314c5550cc3ef568e7ed79516c1299b9e4f1d51dbea5ff92920c5a07e05c812d8da902784ce9f450d65da3b00ad0b93f3cc5a7ceadb1364a57aa703b9d8aeeaae41677a383416832236d21295949a1c29cab2fa1a3cfde2b05e744ba3fba41a23deb8b29908535399955f5073a25b03db413b5a937690b2c4767ce2696d6b4acb979a1cc380efc4a365188fec0ae8b80c740743210688b89114701f9028188268899b50ab53c5bc10615ddd801a9376eacb40eda7610f4c9f3a5d2139cf91adb343165da5cf72251282db93c0bc15afa00807bc5296a8fefcfdf9db731e7bcf8c9bde0d2126a7a3f91c443314624295c6f3e6a92345de8de63892373d3e0c0d47b2c3e3decc6425c32da0b94421d8fa446af3ffaff8614660f36088fd254d60d886147a8b23053"

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
        FOTA = FotaSuit(UUID_PROJECT, ID_DEVICE, VERSION, HOST_BROKER, on_receive_update, PRIVATE_KEY_PROJECT, PUBLIC_KEY_AUTHOR, TYPE_DELIVERY, DEBUG)
    except Exception as error:
        print(error)
        sys.exit()

    print('waiting for version: ' + str(FOTA.manifest.get_next_version()))

    while True:
        FOTA.loop()
