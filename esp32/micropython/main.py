import sys
from uecc import ecdsa
from ucryptolib import aes

_key = b"1234" * 8
_plain_text = bytes(range(32))
_aes = aes(_key, 2, b"OTA_EXEHDA_VRS10")
print(_aes)

try:
    _ecdsa = ecdsa("key")
    print(_ecdsa.verify("signed_text"))
except Exception as error:
    print(error)
    sys.exit()