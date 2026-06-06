import os
import random
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16

KEY = b"\x00" * 16

PREFIX = os.urandom(10)

SECRET = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")

def pkcs7_pad(data):
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len]) * pad_len

def aes_ecb_encrypt(data, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    return cipher.encryptor().update(pkcs7_pad(data))

def oracle(user_input):
    return aes_ecb_encrypt(PREFIX + user_input + SECRET, KEY)

def find_prefix_pad():
    for i in range(BLOCK_SIZE):
        d1 = oracle(b"A" * i)
        d2 = oracle(b"A" * (i + 1))
        if d1[:BLOCK_SIZE] == d2[:BLOCK_SIZE]:
            return i
    return 0

def crack_ecb_hard():
    pad = find_prefix_pad()
    result = b""

    while True:
        fill = b"A" * (pad + BLOCK_SIZE - (len(result) % BLOCK_SIZE) - 1)
        target = oracle(fill)[:pad + len(fill) + len(result) + 1]
        found = None

        for b in range(256):
            guess = fill + result + bytes([b])
            current = oracle(guess)[:len(target)]
            if current == target:
                found = bytes([b])
                break

        if not found:
            break
        result += found

    return result

print("开始破解...")
res = crack_ecb_hard()
print("破解结果：")
print(res.decode())