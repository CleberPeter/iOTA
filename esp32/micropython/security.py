from ucryptolib import aes
import uhashlib as hashlib


class Security:
	def __init__(self, _key, _debug=True):
		self.key = _key
		self.cbc_init_vector = b"OTA_EXEHDA_VRS10"

	def aes_256_cbc_decrypt(self, _ciphered):
		_aes = aes(self.key, 2, self.cbc_init_vector)
		_plaintext = _aes.decrypt(_ciphered)
		return _plaintext
	
	def sha_256(self, _plaintext):
		_sha_256 = hashlib.sha256(_plaintext)
		_hashed = _sha_256.digest()
		return _hashed