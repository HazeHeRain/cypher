import base64
from itertools import cycle

# ========== 第2题：逐字节 XOR ==========
def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, cycle(b)))

# ========== 第3题：单字节 XOR 破解（返回评分） ==========
def single_byte_xor_score(ciphertext: bytes) -> tuple:
    """返回 (密钥字节, 解密文本, 分数)"""
    best_score = -1
    best_key = 0
    best_plain = b''
    
    for key in range(256):
        plain = bytes(b ^ key for b in ciphertext)
        score = 0
        for byte in plain:
            if 65 <= byte <= 90 or 97 <= byte <= 122:  # 字母
                score += 1
            elif byte == 32:  # 空格
                score += 1
            elif 32 <= byte <= 126:  # 可打印字符
                score += 0.5
        if score > best_score:
            best_score = score
            best_key = key
            best_plain = plain
    
    return best_key, best_plain, best_score

# ========== 汉明距离 ==========
def hamming_distance(a: bytes, b: bytes) -> int:
    """计算两个字节串的汉明距离（不同bit的个数）"""
    distance = 0
    for x, y in zip(a, b):
        # 计算两个字节有多少bit不同
        diff = x ^ y
        distance += bin(diff).count('1')
    return distance

# ========== 猜测密钥长度 ==========
def guess_keysize(ciphertext: bytes, max_keysize: int = 40) -> int:
    best_keysize = 2
    best_distance = float('inf')
    
    for keysize in range(2, max_keysize + 1):
        # 取前4个块
        blocks = []
        for i in range(4):
            start = i * keysize
            end = start + keysize
            if end <= len(ciphertext):
                blocks.append(ciphertext[start:end])
        
        if len(blocks) < 2:
            continue
        
        # 计算所有块两两之间的归一化汉明距离
        total_distance = 0
        pairs = 0
        for i in range(len(blocks)):
            for j in range(i + 1, len(blocks)):
                dist = hamming_distance(blocks[i], blocks[j])
                total_distance += dist / keysize
                pairs += 1
        
        avg_distance = total_distance / pairs
        
        if avg_distance < best_distance:
            best_distance = avg_distance
            best_keysize = keysize
    
    return best_keysize

# ========== 转置分组并破解每一列 ==========
def break_repeating_key_xor(ciphertext: bytes):
    # 1. 猜测密钥长度
    keysize = guess_keysize(ciphertext)
    print(f"推测的密钥长度: {keysize}")
    
    # 2. 转置分组
    blocks = [[] for _ in range(keysize)]
    for i, byte in enumerate(ciphertext):
        blocks[i % keysize].append(byte)
    
    # 3. 破解每一列（单字节XOR）
    key_bytes = []
    for i, block in enumerate(blocks):
        block_bytes = bytes(block)
        key_byte, plain, _ = single_byte_xor_score(block_bytes)
        key_bytes.append(key_byte)
        print(f"第{i+1}列 密钥字节: {key_byte} -> '{chr(key_byte)}'")
    
    key = bytes(key_bytes)
    print(f"\n完整密钥: {key} -> '{key.decode()}'")
    
    # 4. 解密
    plaintext = xor_bytes(ciphertext, key)
    
    return key, plaintext


# ========== 主程序 ==========
if __name__ == "__main__":
    # 读取文件（题目提供的 base64 密文文件）
    with open("6.txt", "r") as f:
        # 合并所有行，去掉空白字符
        b64_data = "".join(line.strip() for line in f)
    
    # Base64 解码
    ciphertext = base64.b64decode(b64_data)
    
    # 破解
    key, plaintext = break_repeating_key_xor(ciphertext)
    
    # 输出结果
    print("\n" + "="*60)
    print("解密结果:")
    print("="*60)
    print(plaintext.decode(errors='replace'))