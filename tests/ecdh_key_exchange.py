from ecdsa import SigningKey, VerifyingKey, ECDH, SECP256k1

private_key_author = "3a412d173259377650f6e760441163838cdc1286c93f5080b37add3b653d03a4"
public_key_project = "04bcabfebae83aa1ed933e517d0aa313edbc7ad95c9eef253782070bb4759937bf6b97d0dbf37ff3cbf389db8de0eb41d6346c6ad5afc40c651a1fbf7e62da03f9"

private_key_author_hex = bytes.fromhex(private_key_author)
public_key_project_hex = bytes.fromhex(public_key_project)

private_key = SigningKey.from_string(private_key_author_hex, curve=SECP256k1)
public_key = VerifyingKey.from_string(public_key_project_hex, curve=SECP256k1)

ecdh = ECDH(curve=SECP256k1,  private_key=private_key, public_key=public_key)
secret = ecdh.generate_sharedsecret_bytes().hex()

print(secret)

# cf7c0ddd238f76c9dc3ff97629c8f23852215d18c67eccb0bf2ba40d271df345