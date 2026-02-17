import os, base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

UPLOAD_FOLDER = "uploads"
DECRYPTED_FOLDER = "decrypted"
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)


def encrypt_file(filepath, public_key_str):
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC)

    with open(filepath, "rb") as f:
        plaintext = f.read()

    ciphertext = cipher_aes.encrypt(pad(plaintext, AES.block_size))

    encrypted_filename = os.path.basename(filepath) + ".enc"
    encrypted_path = os.path.join(UPLOAD_FOLDER, encrypted_filename)

    with open(encrypted_path, "wb") as f:
        f.write(cipher_aes.iv)
        f.write(ciphertext)

    public_key = RSA.import_key(public_key_str.encode())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = base64.b64encode(cipher_rsa.encrypt(aes_key)).decode()

    return encrypted_filename, encrypted_key


def decrypt_file(file_record, user):
    encrypted_path = os.path.join(UPLOAD_FOLDER, file_record.stored_filename)

    private_key = RSA.import_key(user.private_key.encode())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(base64.b64decode(file_record.encrypted_key))

    with open(encrypted_path, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    output_path = os.path.join(DECRYPTED_FOLDER, file_record.filename)
    with open(output_path, "wb") as f:
        f.write(plaintext)

    return output_path
