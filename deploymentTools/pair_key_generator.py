import os
import rsa
from ecdsa import SigningKey, VerifyingKey, SECP256k1

dirPath = os.path.dirname(os.path.realpath(__file__)) + "/"
f = open(dirPath + 'keys.txt', 'w')

(pubkey, privkey) = rsa.newkeys(2048)
sk = SigningKey.generate(curve=SECP256k1)
vk = sk.verifying_key

f.write("server:")
f.write("\nauthor ecdsa-SECP256K1 private key: " + str(sk.to_string().hex()))
f.write("\nproject rsa-2048b public key: " + str(pubkey._save_pkcs1_der().hex()))

f.write("\n")

f.write("\nedge:")
f.write("\nauthor ecdsa-SECP256K1 public key: " +  "04" + str(vk.to_string().hex())) # 04 - uncompressed format
f.write("\nproject rsa-2048b private key: " + str(privkey._save_pkcs1_der().hex()))

f.close()