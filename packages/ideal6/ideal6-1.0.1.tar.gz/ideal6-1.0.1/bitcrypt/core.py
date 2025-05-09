from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib

class BitCrypt:
    def __init__(self):
        self.master_key = b"SecretGroub2Key!"
        self.block_size = 16

    def derive_key(self, iv: bytes) -> bytes:
        derived = hashlib.sha256(self.master_key + iv).digest()
        return derived[:16]

    def encrypt(self, plaintext: bytes) -> bytes:
        iv = get_random_bytes(16)
        key = self.derive_key(iv)
        padded = pad(plaintext, self.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        ciphertext = cipher.encrypt(padded)
        return iv + ciphertext

    def decrypt(self, full_ciphertext: bytes) -> bytes:
        if len(full_ciphertext) < 16:
            raise ValueError("Invalid ciphertext: too short to contain IV.")
        iv = full_ciphertext[:16]
        ct = full_ciphertext[16:]
        key = self.derive_key(iv)
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        padded = cipher.decrypt(ct)
        plaintext = unpad(padded, self.block_size)
        return plaintext



