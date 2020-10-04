"""from security import Security

_key = b"1234" * 8
_plain_text = bytes(range(32))

print("plain_text: ", _plain_text)
sec = Security(_key, True)
_ciphered = sec.aes_256_cbc_encrypt(_plain_text)
print("ciphered: ",_ciphered)
"""