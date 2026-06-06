def pkcs7_pad(data: bytes, block_size=16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

# 测试
if __name__ == "__main__":
    print(pkcs7_pad(b"YELLOW SUBMARINE", 20))