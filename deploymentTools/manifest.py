import hashlib
import math
import rsa
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_der
from Crypto.Cipher import AES

def pad(s):
    """ 
      Simple padding, since the block cipher expects clear text to be multiples of the blocksize.
    """
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

class _manifest:
    def __init__(self, _uuidProject, _version, _type, _dateExpiration, _filesNames, _filesSizes, _filesData, _authorPrivateKey, _projectPublicKey, _aes256_secret_random_key):
        self.uuidProject = _uuidProject
        self.version = _version
        self.type = _type
        self.dateExpiration = _dateExpiration

        self.files = []

        _aes256_init_vector = b"OTA_EXEHDA_VRS10"
        

        for index in range(0, len(_filesNames)):
            
            if _authorPrivateKey:
                # _prk = bytes.fromhex("8964370f8571a7a63b519b4067e3e364100804a0f0b285e1292bf6d8636b168a") 
                _prk = _authorPrivateKey 
                _sign = self.sign_ecdsa(_filesData[index], _prk)

                _aes256_secret_random_key_bytes = bytes.fromhex(_aes256_secret_random_key.hex())
                _aes256 = AES.new(_aes256_secret_random_key_bytes, AES.MODE_CBC, _aes256_init_vector)
                
                _filesData[index] = _aes256.encrypt(pad(_filesData[index]))
                _filesSizes[index] = len(_filesData[index])

                self.files.append({'name': _filesNames[index], 'size': _filesSizes[index], 'sign': _sign})
                self.key = self.get_aes256_random_key_ciphered(_aes256_secret_random_key, _projectPublicKey)

            else:
                self.files.append({'name': _filesNames[index], 'size': _filesSizes[index]})
            
    def get_aes256_random_key_ciphered(self, _aes256_secret_random_key, _projectPublicKey):
        _rsa_public_key = rsa.PublicKey._load_pkcs1_der(_projectPublicKey)

        _aes256_secret_random_key_ciphered = rsa.encrypt(_aes256_secret_random_key, _rsa_public_key)
        return _aes256_secret_random_key_ciphered.hex()

    def sign_ecdsa(self, _msg_bytes, _authorPrivateKey):
                
        sk = SigningKey.from_string(_authorPrivateKey, curve=SECP256k1, hashfunc=hashlib.sha256)

        signature = sk.sign(_msg_bytes,sigencode=sigencode_der)
        return signature.hex()
        