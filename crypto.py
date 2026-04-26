import hashlib
from cryptography.fernet import Fernet

class Crypt:
    def __init__(self):
        pass

    @classmethod
    def __gen_fernet_obj(cls, key):
        return Fernet(f"{((hashlib.sha256(key.encode())).hexdigest())[:43]}=".encode())

    def encrypt(self, data, key):
        return self.__gen_fernet_obj(key).encrypt(data)

    def decrypt(self, data, key):
        return self.__gen_fernet_obj(key).decrypt(data)