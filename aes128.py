# -*- coding: UTF-8 -*-
from Crypto.Cipher import AES
import hashlib


def md5(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


class Aes128:
    iv = b'\0' * 16
    key = None
    
    def __init__(self, key):
        self.key = key

    def decrypt(self, data):
        cryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cryptor.decrypt(data)

    @staticmethod
    def pad(s):
        bs = AES.block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    def encrypt(self, data):
        cryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cryptor.encrypt(self.pad(data))
