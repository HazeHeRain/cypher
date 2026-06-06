import os

def get_file_path(f_id):
    current_folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_folder, f"Frame{f_id}")

def read_rsa_data(f_id):
    with open(get_file_path(f_id), "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    N = int(content[:256], 16)
    e = int(content[256:512], 16)
    c = int(content[512:], 16)
    return N, e, c

def ext_gcd(x, y):
    if y == 0:
        return (x, 1, 0)
    g, a, b = ext_gcd(y, x % y)
    return (g, b, a - (x // y) * b)

def extract_msg(m_val):
    hex_str = format(m_val, '0128x')
    seq_num = int(hex_str[16:24], 16)
    msg_part = bytes.fromhex(hex_str[-16:]).decode('latin-1')
    return seq_num, msg_part

def mod_pow_safe(base, exp, mod):
    if exp >= 0:
        return pow(base, exp, mod)
    inv_base = pow(base, -exp, mod)
    g, inv, _ = ext_gcd(inv_base, mod)
    return inv % mod

N0, e0, c0 = read_rsa_data(0)
N4, e4, c4 = read_rsa_data(4)

gcd_val, s1, s2 = ext_gcd(e0, e4)
m_result = (mod_pow_safe(c0, s1, N0) * mod_pow_safe(c4, s2, N0)) % N0

seq, chunk = extract_msg(m_result)
print("公共模数攻击完成")
print(f"序号 = {seq}")
print(f"片段 = {chunk}")