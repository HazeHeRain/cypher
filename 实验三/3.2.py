import random
random.seed(20260515)

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - a // b * y1

def invmod(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("无乘法逆元")
    return x % m

def is_prime(n):
    if n < 2:
        return False

    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n % p == 0:
            return n == p
    d, s = n-1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(10):
        a = random.randrange(2, n-2)
        x = pow(a, d, n)
        if x in (1, n-1):
            continue
        flag = False
        for __ in range(s-1):
            x = pow(x,2,n)
            if x == n-1:
                flag = True
                break
        if not flag:
            return False
    return True

def get_prime(bits):
    while True:

        num = random.getrandbits(bits) | 1 | (1 << (bits-1))
        if is_prime(num) and num %3 !=1:
            return num

if __name__ == "__main__":
    p, q, e =17,23,3
    n = p*q
    phi = (p-1)*(q-1)
    d = invmod(e, phi)
    m =42
    c = pow(m,e,n)
    print("【小RSA测试】",p,q,n,phi,d,c,pow(c,d,n))

    p_big = get_prime(256)
    q_big = get_prime(256)
    while p_big == q_big:
        q_big = get_prime(256)
    n_big = p_big * q_big
    phi_big = (p_big-1)*(q_big-1)
    d_big = invmod(3, phi_big)
    msg = b"ModernCryptography"
    m_big = int.from_bytes(msg, "big")
    c_big = pow(m_big,3,n_big)
    dec_m = pow(c_big, d_big, n_big)
    dec_str = dec_m.to_bytes((dec_m.bit_length()+7)//8,"big").decode()
    print("\n【大RSA密文】",c_big)
    print("【解密原文】",dec_str)