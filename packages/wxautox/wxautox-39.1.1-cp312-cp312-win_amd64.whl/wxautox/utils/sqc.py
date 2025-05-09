from typing import Tuple, List
import random
import math
import os

def miller_rabin(n, k = 40):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # 将n-1表示为2^r * d的形式
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # 进行k次测试
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        # 确保生成的数是奇数
        n = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if miller_rabin(n):
            return n

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    def extended_gcd(a, b) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("mny")
    return x % phi

def generate_keypair(bits = 1024):
    # 生成两个大质数
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    
    # 确保p和q不相等
    while p == q:
        q = generate_prime(bits // 2)
    
    # 计算n和欧拉函数值
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # 选择公钥指数e
    e = 65537  # 常用的公钥指数
    
    # 计算私钥指数d
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def pp(m, k):
    # 计算最大消息长度
    max_message_length = k - 11  # 11是PKCS#1 v1.5填充的最小开销
    
    if len(m) > max_message_length:
        raise ValueError(f"xxtc,")
    
    # 生成随机填充字节
    padding_length = k - len(m) - 3  # 3是固定开销
    padding = bytearray()
    
    # 第一个字节必须是0x00
    padding.append(0x00)
    # 第二个字节必须是0x02
    padding.append(0x02)
    
    # 添加随机非零字节
    while len(padding) < padding_length + 2:
        random_byte = os.urandom(1)[0]
        if random_byte != 0:
            padding.append(random_byte)
    
    # 添加分隔符0x00
    padding.append(0x00)
    
    # 添加原始消息
    return bytes(padding) + m

def pu(pm):
    # 检查消息格式
    if len(pm) < 11:
        raise ValueError("xxtd")
    
    # 检查前两个字节
    if pm[0] != 0x00 or pm[1] != 0x02:
        raise ValueError("gscw")
    
    # 查找分隔符
    try:
        separator_index = pm.index(0x00, 2)
    except ValueError:
        raise ValueError("zbdfgf")
    
    # 检查填充长度
    if separator_index < 10:  # 至少需要8个随机字节
        raise ValueError("tctd")
    
    # 返回原始消息
    return pm[separator_index + 1:]

def fa(m, k):
    e, n = k
    if m >= n:
        raise ValueError("xxtc")
    return pow(m, e, n)

def fp(c, o):
    d, n = o
    if c >= n:
        raise ValueError("mwtc")
    return pow(c, d, n)

def sti(x):
    return int.from_bytes(x.encode(), 'big')

def its(b) -> str:
    return b.to_bytes((b.bit_length() + 7) // 8, 'big').decode()

def wa(x, q):
    e, n = q
    key_length = (n.bit_length() + 7) // 8
    
    # 将消息转换为字节
    message_bytes = x.encode()
    
    # 添加PKCS#1填充
    padded_message = pp(message_bytes, key_length)
    
    # 转换为整数并加密
    message_int = int.from_bytes(padded_message, 'big')
    hash = fa(message_int, q)
    hexhash = hex(hash)[2:]
    if len(hexhash) % 2 != 0:
        hexhash = '0' + hexhash
    return bytes.fromhex(hexhash)

def wp(s, h) -> str:
    d, n = h
    key_length = (n.bit_length() + 7) // 8

    ciphertext = int(s.hex(), 16)
    
    # 解密
    padded_message_int = fp(ciphertext, h)
    
    # 转换为字节，确保长度正确
    padded_message = padded_message_int.to_bytes(key_length, 'big')
    
    # 移除填充
    message_bytes = pu(padded_message)

    return message_bytes