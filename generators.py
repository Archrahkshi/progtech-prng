"""
Файл с генераторами псевдослучайных чисел на основе:
  - линейного конгруэнтного метода;
  - метода Таусворта.
"""


from typing import List
from random import randint


def linear(range_: int, size: int) -> List[int]:
    """
    Генератор псевдослучайных чисел на основе линейного конгруэнтного метода.
    :param range_: Диапазон генерации.
    :param size: Объём генерируемой выборки.
    :return: Сгенерированная выборка из чисел.
    """
    result = []
    m, k, b = 2**31 - 1, 1_220_703_125, 7
    r = randint(1, range_)
    for _ in range(size):
        r = (k * r + b) % m % range_
        result.append(r)
    return result


def tausworth(range_: int, size: int) -> List[int]:
    """
    Генератор псевдослучайных чисел на основе алгоритма Таусворта.
    :param range_: Диапазон генерации.
    :param size: Объём генерируемой выборки.
    :return: Сгенерированная выборка из чисел.
    """
    q = randint(14, 18)
    b0 = '1'
    for i in range(q):
        b0 += str(randint(0, 1))
    r = randint(1, q-1)
    while q % r == 0:
        r += 1
    m = 2**q
    array = []
    for _ in range(size):
        for j in range(q, 2*q):
            b0 += str((int(b0[j-r]) + int(b0[j-q])) % 2)
        b0 = b0[q:]
        array.append(int(b0, 2) % m)
    result = []
    for i in range(len(array)):
        if array[i]//100 != array[i-1]//100:
            result.append(array[i-1] % range_)
        else:
            result.append((array[i]+array[i-1]) % (r*q) % range_)
    return result
