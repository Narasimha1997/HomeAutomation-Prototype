from cryptography.fernet import Fernet

class Crpyt():

    def __init__(self, text):
        self.text = text
        self.key = key = 'cWT0KdcSnukiK7KZZf2pur_04aEGoDxQQDd0FcTrjmQ='

    def getKey(self):
        
        k_m = Fernet(key = bytes(self.key.encode('utf-8')))
        key = k_m.encrypt(data = bytes(self.text.encode('utf-8')))
        return key

def key_check(key1, key2):
    if key1 == key2:
        return True
    return False

def password_check(password):
    pwd = open('password.txt', 'r').read()
    return True if pwd == password else False