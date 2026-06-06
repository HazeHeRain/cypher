import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16

def pkcs7_pad(data):
    pad = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad])*pad

def pkcs7_unpad(data):
    return data[:-data[-1]]

def xor(a,b):
    return bytes(x^y for x,y in zip(a,b))

def aes_ecb_enc(data, key):
    c = Cipher(algorithms.AES(key), modes.ECB())
    return c.encryptor().update(data)

def aes_ecb_dec(data, key):
    c = Cipher(algorithms.AES(key), modes.ECB())
    return c.decryptor().update(data)

def cbc_decrypt(cipher, key, iv):
    prev = iv
    plain = b""
    for i in range(0, len(cipher), BLOCK_SIZE):
        blk = cipher[i:i+BLOCK_SIZE]
        dec = aes_ecb_dec(blk, key)
        plain += xor(dec, prev)
        prev = blk
    return pkcs7_unpad(plain)

# 测试
if __name__ == "__main__":
    key = b"YELLOW SUBMARINE"
    iv  = b"\x00"*16
    with open("10.txt") as f:
        cipher = base64.b64decode(f.read())
    print(cbc_decrypt(cipher, key, iv)[:50])