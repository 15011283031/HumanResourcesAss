# 调用加密算法，用于加密数据库链接中的密码
import random  # 加密算法中，用于生成随机加密字符串


def randomstring(n):
    # create random string for prpcrypt,only for 16 numbers
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]),
                        ''.join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", n))
                        .replace(" ", ""))))[0:16]