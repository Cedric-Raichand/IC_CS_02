from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key().decode()
    public_key = key.publickey().export_key().decode()
    return public_key, private_key

def encrypt_key(aes_key, public_key_str):
    public_key = RSA.import_key(public_key_str.encode())
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(aes_key)
    return base64.b64encode(encrypted).decode()

def decrypt_key(encrypted_key, private_key_str):
    private_key = RSA.import_key(private_key_str.encode())
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_key))
    return decrypted
