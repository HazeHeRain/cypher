import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16
secret = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
key = b"\x00"*16

def pkcs7_pad(d):
    p = 16-len(d)%16
    return d+bytes([p])*p

def aes_ecb_enc(d,k):
    return Cipher(algorithms.AES(k), modes.ECB()).encryptor().update(pkcs7_pad(d))

def oracle(inp):
    return aes_ecb_enc(inp+secret, key)

def crack():
    out = b""
    while True:
        pad = b"A"*(15 - len(out)%16)
        target = oracle(pad)[:len(pad)+len(out)+1]
        found = None
        for b in range(256):
            g = pad+out+bytes([b])
            if oracle(g)[:len(target)]==target:
                found=bytes([b])
                break
        if not found: break
        out+=found
    return out

print(crack().decode())