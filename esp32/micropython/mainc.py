import hashlib

sha256 = hashlib.sha256()

m.update(b"Nobody inspects")

"""
import sys
from uecc import ecdsa
from ucryptolib import aes

def hex_to_bytes(hex_string):
    i = 0
    arr = []
    while (i < len(hex_string)):
        arr.append((int(hex_string[i],16) << 4) | int(hex_string[i + 1],16))
        i+=2
    return bytes(arr)

try:
    _pubkey = "04164639549dc15abf38e6bfa2a4b3cab13cf2820bccdb76fe58507c746b48f174bb3e1c1e54a6865c00e8e90e3349549ddeef7139ef134e9fa30c37652e3951c1"
    _signature = "304502200228721506866a46017c29393ae613d5116c0ab9fa0f96880b65ebe159b403f2022100be97326a24907063a4e8b894214d4a270f37d0a1bcf7aedffb4a2b93932a9826"
    _message = "aui_teste_123"

    _pubkey_array = hex_to_bytes(_pubkey)
    _signature_array = hex_to_bytes(_signature)
    
    _ecdsa = ecdsa(_pubkey_array)

    print(_ecdsa.verify(_message, _signature_array))
    
except Exception as error:
    print(error)
    sys.exit()
"""