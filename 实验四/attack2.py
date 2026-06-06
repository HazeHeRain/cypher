import math
import os

def get_rsa_file(frame_id):
    current_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_path, f"Frame{frame_id}")

def read_cipher(frame_id):
    file = get_rsa_file(frame_id)
    with open(file, "r", encoding="utf-8") as f:
        data = f.read().strip()
    
    N = int(data[:256], 16)
    e = int(data[256:512], 16)
    c = int(data[512:], 16)
    return N, e, c

def ex_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = ex_gcd(b, a % b)
    return g, y, x - (a // b) * y

def mod_inverse(a, m):
    g, inv, _ = ex_gcd(a, m)
    if g != 1:
        raise Exception("error")
    return inv % m

def parse_message(m_val):
    hex_val = "{0:0128x}".format(m_val)
    seq_num = int(hex_val[16:24], 16)
    msg = bytes.fromhex(hex_val[-16:]).decode("latin-1")
    return seq_num, msg

f1_n, f1_e, f1_c = read_cipher(1)
f18_n, f18_e, f18_c = read_cipher(18)

prime = math.gcd(f1_n, f18_n)

q1 = f1_n // prime
phi1 = (prime - 1) * (q1 - 1)
d1 = mod_inverse(f1_e, phi1)
m1 = pow(f1_c, d1, f1_n)
seq1, ch1 = parse_message(m1)

q18 = f18_n // prime
phi18 = (prime - 1) * (q18 - 1)
d18 = mod_inverse(f18_e, phi18)
m18 = pow(f18_c, d18, f18_n)
seq18, ch18 = parse_message(m18)

print("Frame1")
print("sequence =", seq1)
print("chunk =", ch1)
print("\nFrame18")
print("sequence =", seq18)
print("chunk =", ch18)