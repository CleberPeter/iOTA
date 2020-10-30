import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.util import sigencode_der, sigdecode_der

sk = SigningKey.generate(curve=SECP256k1)
vk = sk.verifying_key

print("private key: ", sk.to_string().hex())
print("public key: ",  "04" + vk.to_string().hex()) # uncompressed format
