from security import Security

def unpad(s):
    return s.rstrip("\0").lstrip("\0")

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

_aes256_secret_random_key_bytes = 'LLPGZZFJXSXMUASTBIGPCDJELDIFTITF'.encode()

security = Security()

message = hex_to_bytes('9bb0b83d9cbc95245cd24a9b29831560')
print(message)

# 
print(security.aes_256_cbc_decrypt(_aes256_secret_random_key_bytes, message))