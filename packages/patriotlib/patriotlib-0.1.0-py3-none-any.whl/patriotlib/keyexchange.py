# patriotlib/keyexchange.py

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def generate_ecdh_keys():
    private = ec.generate_private_key(ec.SECP384R1())
    return private, private.public_key()


def derive_shared_key(private_key, peer_public_key):
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    return HKDF(hashes.SHA256(), 32, None, b'patriot-handshake').derive(shared_secret)
