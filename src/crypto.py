from cryptography.fernet import Fernet
import base64
import hashlib
def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()
def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()
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
        return None
    cleartext = cleartext.decode()
    return cleartext
