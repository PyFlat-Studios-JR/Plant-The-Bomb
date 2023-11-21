from cryptography.fernet import Fernet
import base64
import hashlib
def encode(text, key):
    key = hashlib.md5(key.encode()).hexdigest()
    key = key.encode("ascii")
    key = base64.b64encode(key)
    msg = text
    msg = msg.encode()
    f = Fernet(key)
    ciphertext = f.encrypt(msg)
    ciphertext = ciphertext.decode()
    return ciphertext
def decode(text, kkey):
    key = hashlib.md5(kkey.encode()).hexdigest()
    key = key.encode("ascii")
    key = base64.b64encode(key)
    msg = text
    msg = msg.encode()
    f = Fernet(key)
    try:
        cleartext = f.decrypt(msg)
    except Exception as ex:
        print(type(ex))
        print(ex)
        print("An Error has ocurred")
        return None
    cleartext = cleartext.decode()
    return cleartext
