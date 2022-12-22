# Liquidity pool list is list of tuples of volumes (a, b)
def calc_result(value, pool_list, fee=0.3):
    """
    Функция вычисляет количество монет в итоге. то есть зависимость f(x),
    где x = количество проданных монет в начале цепочки, f(x) = количество полученных
    монет в конце цепочки
    :param value: количество продаваемой первой валюты
    :param pool_list: список пулов
    :param fee: общая комиссия для пулов
    :return: возвращает итоговое количество монет
    """
    fee_coeff = 1 - fee / 100
    value = value * fee_coeff
    for a, b in pool_list:
        value = b - (a * b) / (a + value)
    return value


def prime(value, pool_list):
    """
    Вычисляет производную f'(x)
    :param value:
    :param pool_list:
    :return:
    """
    a, b = pool_list[-1]
    if len(pool_list) == 1:
        return (a * b) / (a + value) ** 2
    else:
        f_x = calc_result(value, pool_list[:-1])
        return (a * b) / (a + f_x) ** 2 * prime(value, pool_list[:-1])


def grad_desc(pool_list, start, iter_num=1e6, lr=1., stop_prime=1e-3):
    """
    grad_desc функция градиентного спуска для (f(x) - x) для нахождения максимума разницы
    между количеством проданных монет и полученных в итоге
    :param pool_list: список пулов
    :param start: начальное значение x
    :param iter_num: предельное количество итераций
    :param lr: скорость спуска
    :param stop_prime: предельное значение модуля производной, на котором останавливается спуск
    :return: значение x в точке останова спуска
    """
    iter_count = 0  # iterations counter
    x = start
    while iter_count < iter_num:
        grad = prime(x, pool_list) - 1 # (f(x) - x)' = f'(x) - 1
        x += grad * lr
        if abs(grad) <= stop_prime:
            break
        iter_count += 1
        if iter_count % 100 == 0:
            print(f'iter: {iter_count}, grad: {grad}, x: {x}')
    return x


if __name__ == '__main__':
    # pool_lst = [
    #     (10, 20),
    #     (5, 10),
    #     (7, 21)
    # ]
    pool_lst = [
        (3753139396, 166740188573),
        (724520588560, 766050680304),
        (10457920653, 1051487855),
        (1722571966294, 2846977754550),
        (22496742244741, 4310194783973)
    ]
    first_coin, second_coin = pool_lst[0]
    start_point = (first_coin * second_coin)/(second_coin - 1) - first_coin
    lr = first_coin / 10000
    x = grad_desc(pool_lst, start_point, lr=lr)
    f_x = calc_result(x, pool_lst)
    revenue = f_x - x
    print(f'При продаже {x} монет в начале цепи получим {f_x} монет')
    print(f'Выручка составит {revenue} монет')
