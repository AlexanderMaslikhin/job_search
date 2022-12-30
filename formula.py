from math import sqrt


def func(x, pool_list, k_num=None, k_den_0=None, k_den_1=None):
    if k_den_0 is None or k_den_1 is None or k_num is None:
        return func(x, pool_list[1:], pool_list[0][1], pool_list[0][0], 1.)
    if len(pool_list) == 0:
        return k_num, k_den_0, k_den_1, k_num*x/(k_den_0 + k_den_1*x)
    pool0, pool1 = pool_list[0]
    return func(x, pool_list[1:], k_num*pool1, k_den_0*pool0, pool0*k_den_1+k_num)


def find_max(pool_list, f):
    a, b, c, _ = f(0, pool_list)
    k2 = c ** 2
    k1 = 2 * b * c
    k0 = b ** 2 - a * b
    D = k1 ** 2 - 4 * k2 * k0
    x1 = (-k1 + sqrt(D)) / (2*k2)
    x2 = (-k2 - sqrt(D)) / (2*k2)
    return max(x1, x2)


pool_lst = [
        (3753139396, 166740188573),
        (724520588560, 766050680304),
        (10457920653, 1051487855),
        (1722571966294, 2846977754550),
        (22496742244741, 4310194783973)
]

print(find_max(pool_lst, func))
