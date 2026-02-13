from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

# AES block size
BLOCK_SIZE = 16


def pad(data):
    padding_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding_len] * padding_len)


def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]


def encrypt_file(file_path):
    key = get_random_bytes(32)  # 256-bit AES key
    cipher = AES.new(key, AES.MODE_CBC)

    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext = cipher.encrypt(pad(plaintext))

    iv = cipher.iv
    enc_file_path = file_path + ".enc"

    with open(enc_file_path, 'wb') as f:
        f.write(iv + ciphertext)

    os.remove(file_path)  # delete original plaintext file
    return key, enc_file_path  # return AES key for sharing
