import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, ec

def make_signing_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)

def make_session_key():
    return ec.generate_private_key(ec.SECP256R1())

def legacy_fingerprint(data):
    return hashlib.md5(data).hexdigest()   # legacy, do not use
