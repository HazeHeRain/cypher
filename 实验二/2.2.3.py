import os, random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16

def pkcs7_pad(data):
    pad = BLOCK_SIZE - len(data)%BLOCK_SIZE
    return data + bytes([pad])*pad

def aes_ecb_enc(d,k): return Cipher(algorithms.AES(k), modes.ECB()).encryptor().update(d)
def aes_cbc_enc(d,k,iv):
    prev = iv
    c = b""
    d = pkcs7_pad(d)
    for i in range(0,len(d),16):
        b = d[i:i+16]
        b = bytes(x^y for x,y in zip(b,prev))
        e = aes_ecb_enc(b,k)
        c += e
        prev = e
    return c

def oracle(data):
    k = os.urandom(16)
    pre = os.urandom(random.randint(5,10))
    suf = os.urandom(random.randint(5,10))
    data = pre+data+suf
    if random.randint(0,1):
        return aes_cbc_enc(data,k,os.urandom(16)), "CBC"
    else:
        return aes_ecb_enc(pkcs7_pad(data),k), "ECB"

def is_ecb(c):
    blks = [c[i:i+16] for i in range(0,len(c),16)]
    return len(blks)!=len(set(blks))

if __name__ == "__main__":
    c,m = oracle(b"A"*64)
    print("real",m,"detect","ECB"if is_ecb(c)else"CBC")