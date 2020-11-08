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
PUBLIC_KEY_AUTHOR = "04f46127e41042bb07c353167b1c98c44336376788c2d9f2e080a19e2841ebd25fb4f324bcf0dc5893b9c84f3571d36646b3825cb4c12716cd0c45cec84ceca16f" 

# RSA-2048b private key from PROJECT to decrypt AES256 random key.
PRIVATE_KEY_PROJECT = "308204a80201000282010100ad2b6a5c2af34609096ef38df1162f5515ca799b2f7fcd05aec348f697bf44fe3798df8d1558b0a26ea00c4f0eb52e7137ac5094092852b5a8eb0f5c3f59f5d43bcb591f2a13a0cbc67fd0c48e064a058772f28bf06098040557814d2706c7328f8187cc7fb059d885edf3a684e2ed21f2c1f15e83fff8758ed2881733b8ab09fc60191cc9ec443bfd0cd29ecfdc8c030925029ee55e9b313bcd5688b862a25b9332323bc4ff65ecc1924bc59fd4980e07830572bc8b6e0101c2961b75b0107db80c46dcb8ea53183fd29950555f9064e10e6b186a2beb014fba6a94f8f35fa605abed32ad75ebab46d1fe1883bcfc2ae1e9c909e7dc54e411d2dc76a9ae3a9d02030100010282010058ab1351d03832932bfe60bd3c45e4c4875cde79848fc6d5f30f514bda95786946e4830b05741d357eb97ab3fc4eef51cf74eee96deaf4b6c9a05a841c781eb4a64d4ffbf21a8cc9ea80c5cfeefcef67f75bf72f8a4c9b69eba64bb1ca9ae0e255b2b86b10b2a6be848d3ba5f7030ef2c40f645cc5f00a330f2a8f6343b1d20e29f065da96f2fd2b802e0b9d555ff0b276e90e1233c04746751f80b4e0d74428c019fae7db6c1b65de7684b3fe8c93a7e118d83cfc4ca02c8672b3bea9de1d9d4128b16246dd34148a0fa3262d310826e60d1bc7c37fe6fc18584ce37a07caf913599c8483a9a12e37fa486f0acb25c87fc0477b8d89c9251d5e3cbe8f84bf4102818900db71021f5762a9ae6302557e9d5016aefaa8449b72d30619bb6e14a5426a1efa1863504700ff2436aa58ee67fd25fb92aa138657d2f655034de65ff0daef40ab94d13a98c2d4a9d6355e29449b9075fff5c5aa2b4f41aee6cee4d956dfb26ccb1ae77e8fdbd72b45328596513f792cafc18b7b281f12a782a78f783b1b644b015b0a61f9290b6db1027900ca04f3b9a57495d45f8428f58a8dee505b2c6673fe6199ce5dc90011c51682219037da3e781d8a92e2cd4cee36c40c9cd1a048dce98cb6b937faae8ca973524872e8b9e98631fae9856d100f40e3be4f1ca52b91d5dae2febd1ccdeb6a148a9e97c57f5dc4081b7581ed90af6407246b5b7a946ff78b3aad028188381331b2a696ecbb464bb3632e79e7c201057cbaa865ea5a2afe1f4277ad3c8b362e32b66237d09e337b94387884fb3b6840a304d040e84a76de96c7aa7a96f1018f51c4f58c7875e79f4f365bf65760f801f1d12d68a074148c804965d26760a358628c0a667a852d3adbc5994db2b09ae9b4a7f500c4536bd40aaa37feb1f7ffb6b080860f88910278087c76c488a7c2177ebfad7ccb0a354598dedf9ae5c7b1cf526f3c1a82fdf40f76e071c188082da707f1f9d653e49e67040348ac46ff4b39b2994c35ca7476b36668524ef5fd297e1fc5ba13f9f4d72cb99652a338a98e3987362b8c451381d331aaf133be255d09eda04e20a00210cc95b62b801c94f3ad0281881195d0a7e000cfbd72c603ed1f2f21e912175477a001d164de07d0fafd6acfffc0ccc6e3f4b17028d9accdac6236309d57bddd5f20e56c982ef46820e37b1a6163fdbebf457bc5f8b292574c54aa2d799cdddd03f6d002a0f57ae418631d14e9d255becb19b19e854ae7fd033ada5e343aa6a5b404c7ccf1d06569b63ab7c7513afe3281de5d3ba6"

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
