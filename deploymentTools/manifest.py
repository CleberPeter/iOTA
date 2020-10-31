import hashlib
import math
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_der

class _manifest:
    def __init__(self, _uuidProject, _version, _type, _dateExpiration, _filesNames, _filesSizes, _filesData, _privateKey):
        self.uuidProject = _uuidProject
        self.version = _version
        self.type = _type
        self.dateExpiration = _dateExpiration

        self.files = []
        for index in range(0, len(_filesNames)):
            
            if _privateKey:
                # _prk = bytes.fromhex("8964370f8571a7a63b519b4067e3e364100804a0f0b285e1292bf6d8636b168a") 
                _prk = _privateKey 
                _sign = self.sign(_filesData[index], _prk)
                self.files.append({'name': _filesNames[index], 'size': _filesSizes[index], 'sign': _sign})
            else:
                self.files.append({'name': _filesNames[index], 'size': _filesSizes[index]})
    
    def sign(self, _msg_bytes, _privateKey):
                
        sk = SigningKey.from_string(_privateKey, curve=SECP256k1, hashfunc=hashlib.sha256)

        signature = sk.sign(_msg_bytes,sigencode=sigencode_der)
        return signature.hex()
        