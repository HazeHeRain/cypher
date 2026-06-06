import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def recover_mrz_character(mrz):
    weights = (7, 3, 1)
    char_map = {str(i): i for i in range(10)}
    char_map["<"] = 0

    def calc_checksum(text):
        total = 0
        for idx, c in enumerate(text):
            total += char_map[c] * weights[idx % 3]
        return total % 10

    for d in "0123456789":
        test_mrz = mrz.replace("?", d)
        if calc_checksum(test_mrz[21:27]) == int(test_mrz[27]):
            return d
    raise ValueError("未找到校验位")

def set_odd_parity(byte):

    parity = bin(byte).count('1') % 2
    return byte if parity == 1 else byte ^ 1

def aes_cbc_decrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()

def strip_bac_padding(data):
    suffix = data.rstrip(b"\x00")
    if suffix.endswith(b"\x01"):
        return suffix[:-1]
    return suffix

if __name__ == "__main__":

    mrz_partial = "12345678<8<<<1110182<111116?<<<<<<<<<<<<<<<4"
    
    recovered_digit = recover_mrz_character(mrz_partial)
    mrz_full = mrz_partial.replace("?", recovered_digit)
    
    mrz_info = mrz_full[:10] + mrz_full[13:20] + mrz_full[21:28]
    
    k_seed = hashlib.sha1(mrz_info.encode()).digest()[:16]
    raw_key = hashlib.sha1(k_seed + b"\x00\x00\x00\x01").digest()[:16]
    
    key_enc = bytes(set_odd_parity(byte) for byte in raw_key)

    cipher_base64 = "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI"
    ciphertext = base64.b64decode(cipher_base64)
    iv = b"\x00" * 16
    
    plain_bytes = aes_cbc_decrypt(ciphertext, key_enc, iv)
    plaintext = strip_bac_padding(plain_bytes).decode("utf-8")

    print("缺失校验位:", recovered_digit)
    print("MRZ 拼接串:", mrz_info)
    print("AES 密钥(含奇校验 hex):", key_enc.hex())
    print("最终答案:", plaintext)