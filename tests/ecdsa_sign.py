import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.util import sigencode_der, sigdecode_der
import base64

message = b"aui_teste_123"

privkey = "a039169eb60af31b3bf291fab39a15a2f1300663370ff8c6dcc5a8e2fe3c3690"
# pubkey = "04164639549dc15abf38e6bfa2a4b3cab13cf2820bccdb76fe58507c746b48f174bb3e1c1e54a6865c00e8e90e3349549ddeef7139ef134e9fa30c37652e3951c1"

privkey_hex = bytes.fromhex(privkey)
# pubkey_hex = bytes.fromhex(pubkey)

sk = SigningKey.from_string(privkey_hex, curve=SECP256k1, hashfunc=hashlib.sha256)
# vk = VerifyingKey.from_string(pubkey_hex, curve=SECP256k1, hashfunc=hashlib.sha256)
signature = sk.sign(message,sigencode=sigencode_der)

# assert vk.verify(signature, message,sigdecode=sigdecode_der)

print("message: ", message)
print("private key: ", sk.to_string().hex())
# print("public key: ", vk.to_string().hex())
print("signature: ", signature.hex())

