from pathlib import Path

def base_dir():
    return Path(__file__).parent.parent.parent

def data_folder():
    root = base_dir()
    rsa_folder = None
    for item in root.iterdir():
        if item.is_dir() and item.name.startswith("RSA"):
            rsa_folder = item
            break
    
    sub_dir = None
    for d in rsa_folder.iterdir():
        if d.is_dir():
            sub_dir = d
            break

    target_dir = None
    for d in sub_dir.iterdir():
        if d.is_dir() and "3-2" in d.name:
            target_dir = d
            break
    return target_dir

def read_rsa_cipher(fid):
    path = data_folder() / f"Frame{fid}"
    content = path.read_text().strip()
    
    modulus = int(content[:256], 16)
    pub_exp = int(content[256:512], 16)
    cipher = int(content[512:], 16)
    return modulus, pub_exp, cipher

def extended_gcd(x, y):
    if y == 0:
        return (x, 1, 0)
    g, a, b = extended_gcd(y, x % y)
    return (g, b, a - (x // y) * b)

def mod_inverse(val, mod):
    g, inv, _ = extended_gcd(val, mod)
    if g != 1:
        raise Exception("不存在逆元")
    return inv % mod

def crt_merge(pairs):
    total = 1
    for _, ni in pairs:
        total *= ni

    res = 0
    for ai, ni in pairs:
        mi = total // ni
        res = (res + ai * mi * mod_inverse(mi, ni)) % total
    return res

def integer_root(num, power):
    l = 0
    r = 1 << ((num.bit_length() + power - 1) // power)
    while l < r:
        mid = (l + r) // 2
        if mid ** power < num:
            l = mid + 1
        else:
            r = mid
    return l, l ** power == num

def parse_result(plain):
    hex_str = f"{plain:0128x}"
    pre = hex_str[:16]
    seq_id = int(hex_str[16:24], 16)
    text = bytes.fromhex(hex_str[-16:]).decode("latin1")
    return pre, seq_id, text

target_list = [3, 8, 12, 16, 20]
cipher_pairs = []

for fid in target_list:
    n, e, c = read_rsa_cipher(fid)
    if e != 5:
        raise Exception(f"Frame{fid} 指数错误")
    cipher_pairs.append((c, n))

merged_val = crt_merge(cipher_pairs)
plaintext, success = integer_root(merged_val, 5)

if not success:
    raise Exception("攻击失败")

pre, seq, chunk = parse_result(plaintext)

print("Hastad 广播攻击 e=5")
print("prefix   =", pre)
print("sequence =", seq)
print("chunk    =", chunk)