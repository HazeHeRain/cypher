from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE=16
key=b"\x00"*16

def pkcs7_pad(d):
    p=16-len(d)%16
    return d+bytes([p])*p

def aes_ecb_enc(d,k):
    return Cipher(algorithms.AES(k),modes.ECB()).encryptor().update(pkcs7_pad(d))

def profile(email):
    email=email.replace("&","").replace("=","")
    return f"email={email}&uid=10&role=user".encode()

def attack():
    blk = aes_ecb_enc(pkcs7_pad(b"admin"),key)
    c1 = aes_ecb_enc(profile("A"*10),key)
    forged = c1[:32] + blk
    return forged

print(attack().hex())