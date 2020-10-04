from ucryptolib import aes
import uhashlib as hashlib


class Security:
	def __init__(self, _key, _debug=True):
		self.key = _key
		self.cbc_init_vector = b"OTA_EXEHDA_VRS10"
	
	"""def ecdsa_verify_sign(self, _data):
		_ecdsa = ecdsa(self.key)
		print('_ecdsa')
		print(_ecdsa)
		#return _ecdsa.verify(_data)
	"""
	
	def sha_256(self, _plaintext):
		_sha_256 = hashlib.sha256(_plaintext)
		_hashed = _sha_256.digest()
		return _hashed
		
	def aes_256_cbc_encrypt(self, _plain_text):
		_aes = aes(self.key, 2, self.cbc_init_vector)
		_ciphered = _aes.encrypt(_plain_text)
		return _ciphered

	def aes_256_cbc_decrypt(self, _ciphered):
		_aes = aes(self.key, 2, self.cbc_init_vector)
		_plaintext = _aes.decrypt(_ciphered)
		return _plaintext

	