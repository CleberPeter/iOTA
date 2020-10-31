from ucryptolib import aes
import uhashlib as hashlib
from uecc import ecdsa

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
            _key (string): key to cryptographic functions.
            _debug (boolean, optional): enable debug from class. Default is True.
        Returns:
            object from class
    """

	def __init__(self, _key, _debug=True):
		
		self.key = hex_to_bytes(_key)
		self.sha256 = hashlib.sha256()
		self.cbc_init_vector = b"OTA_EXEHDA_VRS10"

	def aes_256_cbc_decrypt(self, _ciphered):
		"""
            Decryption for AES 256.

			Args:
            	_ciphered (bytes): cipher text.

            Returns:
                bytes with plain text.
        """

		_aes = aes(self.key, 2, self.cbc_init_vector)
		_plaintext = _aes.decrypt(_ciphered)
		return _plaintext

	def sha256_update(self, plaintext):
		self.sha256.update(plaintext)

	def sha256_ret(self):
		_hash = self.sha256.digest()
		self.sha256 = hashlib.sha256() # clean hash buffer
		return _hash

	def ecdsa_secp256k1_verifiy_sign(self, _plain_text, _sign):
		"""
            Verify signature from ecdsa secp256k1.

			Args:
				_plain_text (string): message.
				_sign (string): signature.

            Returns:
                boolean indicating sign verification.
        """

		_ecdsa = ecdsa(self.key)
		_sign_bytes = hex_to_bytes(_sign)

		return _ecdsa.verify(_plain_text, _sign_bytes)

	