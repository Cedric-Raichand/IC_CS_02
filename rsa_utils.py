from Crypto.PublicKey import RSA

def generate_keys():
    key = RSA.generate(2048)
    return key.publickey().export_key().decode(), key.export_key().decode()
