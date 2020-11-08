from ucryptolib import aes
import uhashlib as hashlib
from uecc import ecdsa
from uecc import pk

def hex_to_bytes(_hex_string):
	"""
		Convert "0A0B10" into 'b\x0A\x0B\x10'.

		Args:
			_hex_string (string): string into hex format.
		Returns:
			byte array.
	"""

	i = 0
	arr = []
	while (i < len(_hex_string)):
		arr.append((int(_hex_string[i],16) << 4) | int(_hex_string[i + 1],16))
		i+=2
	return bytes(arr)

class Security:
	"""
        Security functions for iota framework.

        Args:
            _debug (boolean, optional): enable debug from class. Default is True.
        Returns:
            object from class
    """

	def __init__(self, _debug=True):
		
		self.sha256 = hashlib.sha256()
		
	def aes_256_cbc_init(self, _key):
		"""
            Initialize AES 256.

			Args:
				_key (bytes): key to algorithm

            Returns:
                bytes with plain text.
        """

		_cbc_init_vector = b"OTA_EXEHDA_VRS10"
		self.aes = aes(_key, 2, _cbc_init_vector)

	def aes_256_cbc_decrypt(self, _ciphered):
		"""
            Decryption for AES 256.

			Args:
            	_ciphered (bytes): cipher text.

            Returns:
                bytes with plain text.
        """
		
		_plaintext = self.aes.decrypt(_ciphered)
		return _plaintext

	def sha256_update(self, plaintext):
		self.sha256.update(plaintext)

	def sha256_ret(self):
		_hash = self.sha256.digest()
		self.sha256 = hashlib.sha256() # clean hash buffer
		return _hash
		
	def ecdsa_secp256k1_verifiy_sign(self, _key, _hash, _sign):
		"""
            Verify signature from ecdsa secp256k1.

			Args:
				_key (string): public key to algorithm.
				_hash (bytes): hash of message.
				_sign (string): signature.

            Returns:
                boolean indicating sign verification.
        """
		_key_bytes = hex_to_bytes(_key)
		_ecdsa = ecdsa(_key_bytes)
		_sign_bytes = hex_to_bytes(_sign)

		return _ecdsa.verify(_hash, _sign_bytes)
	
	def rsa_decrypt(self, _key, _ciphered):
		"""
            Decryption for RSA.

			Args:
				_key (string): private key to algorithm.
				_ciphered (string): ciphered text.
				_privatekey (string): private key.

            Returns:
                string with plaintext.
        """

		_key = hex_to_bytes(_key)
		_rsa = pk(_key)
		_ciphered_bytes = hex_to_bytes(_ciphered)

		return _rsa.decrypt(_ciphered_bytes)