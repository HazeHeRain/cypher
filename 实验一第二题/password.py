import hashlib
import itertools
import time
from multiprocessing import Pool

# 目标哈希
target_hash = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"

# 8个按键，每个按键2种字符（小写/数字 vs 大写/符号）
# 注意顺序：根据键盘布局，左手到右手
key_groups = [
    ('q', 'Q'),   # Q键
    ('w', 'W'),   # W键
    ('5', '%'),   # 5/%
    ('8', '('),   # 8/(
    ('0', '='),   # 0/=
    ('i', 'I'),   # I/i
    ('+', '*'),   # +/*
    ('n', 'N')    # n/N
]

def check_combination(combination):
    """
    combination: 8个字符的列表（从每组的选定字符）
    对该组合的所有排列进行哈希校验
    """
    for perm in itertools.permutations(combination):
        plain = ''.join(perm)
        if hashlib.sha1(plain.encode()).hexdigest() == target_hash:
            return plain
    return None

def generate_combinations():
    """生成所有 2^8 种字符选择组合"""
    indices = range(8)
    for mask in range(256):
        # mask 的二进制位表示每组选哪个字符（0表示第一个，1表示第二个）
        combo = [key_groups[i][(mask >> i) & 1] for i in indices]
        yield combo

def main():
    start = time.time()
    
    # 收集所有组合
    combos = list(generate_combinations())
    print(f"总组合数: {len(combos)}")
    
    # 多进程处理
    with Pool() as pool:
        results = pool.map(check_combination, combos)
    
    # 输出结果
    for res in results:
        if res:
            print(f"\n密码是: {res}")
            break
    else:
        print("未找到密码")
    
    elapsed = time.time() - start
    print(f"运行时间: {elapsed:.2f} 秒")

if __name__ == "__main__":
    main()