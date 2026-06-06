import math

p = 1009
q = 3643
phi = (p - 1) * (q - 1)

min_unconcealed = None 
total_e = 0   
count_e = 0    

for e in range(2, phi):
    if math.gcd(e, phi) != 1:
        continue
    
    g1 = math.gcd(e - 1, p - 1)
    g2 = math.gcd(e - 1, q - 1)
    current = (g1 + 1) * (g2 + 1)

    if min_unconcealed is None or current < min_unconcealed:
        min_unconcealed = current
        total_e = e
        count_e = 1
    elif current == min_unconcealed:
        total_e += e
        count_e += 1


print("最小未加密消息数量:", min_unconcealed)
print("满足条件的 e 个数:", count_e)
print("所有 e 的总和（答案）:", total_e)