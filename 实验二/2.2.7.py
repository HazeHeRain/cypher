def pkcs7_unpad(data):
    pad = data[-1]
    if pad <1 or pad>16:
        raise ValueError("bad padding")
    if not all(b==pad for b in data[-pad:]):
        raise ValueError("bad padding")
    return data[:-pad]


good = b"ICE ICE BABY\x04\x04\x04\x04"
bad1 = b"ICE ICE BABY\x05\x05\x05\x05"
bad2 = b"ICE ICE BABY\x01\x02\x03\x04"

print(pkcs7_unpad(good))