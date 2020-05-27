"""
Файл со вспомогательными функциями. Включает в себя:
  - функции для вычисления выборочных характеристик:
    * среднего;
    * стандартного отклонения;
    * коэффициента вариации;
  - критерий согласия хи-квадрат Пирсона для простой гипотезы;
  - функцию для отрисовки графика зависимости между объёмом выборки и скоростью генерации.
"""


from typing import List, Dict
import numpy as np
from scipy.stats import chi2
from matplotlib import pyplot as plt
from termcolor import colored


SIZES = (1000, 10_000, 100_000, 1_000_000)


def mean(sample: List[int]) -> float:
    """
    Вычисление выборочного среднего.
    :param sample: Выборка из чисел.
    :return: Выборочное среднее.
    """
    return sum(sample) / len(sample)


def deviation(sample: List[int]) -> float:
    """
    Вычисление выборочного стандартного отклонения.
    :param sample: Выборка из чисел.
    :return: Выборочное стандартное отклонение.
    """
    m = mean(sample)
    return (sum((element-m) ** 2 for element in sample) / len(sample)) ** (1/2)


def cv(sample: List[int]) -> float:
    """
    Вычисление выборочного коэффициента вариации.
    :param sample: Выборка из чисел.
    :return: Выборочный коэффициент вариации.
    """
    return deviation(sample) / mean(sample)


def pearson(sample: List[int]) -> None:
    """
    Проверка выборки на равномерность и случайность с помощью критерия хи-квадрат Пирсона.
    :param sample: Выборка из чисел для проверки.
    :return: Индикаторы равномерности и случайности.
    """
    n = len(sample)                             # Объём выборки
    k = 1 + int(np.log2(n))                     # Количество интервалов (по формуле Стёрджеса)
    p = 1 / k                                   # Вероятность попадания элемента в интервал
    borders = np.linspace(0, 10000.01, k+1)     # Границы интервалов

    # Частоты попадания выборочных данных в соответствующие интервалы
    nu = np.zeros(k)
    for element in sample:
        for i in range(k):
            if borders[i] <= element < borders[i+1]:
                nu[i] += 1
                break

    # Статистика, характеризующая отклонение выборочных данных
    # от соответствующих гипотетических значений
    stat = sum(nu[i]**2 / p for i in range(k)) / n - n

    if stat < chi2.ppf(.1, k-1):
        print('выборка недостаточно случайна')
    elif stat > chi2.ppf(.9, k-1):
        print('выборка недостаточно равномерна')
    else:
        for quantile in np.arange(.1, .91, .01):
            if chi2.ppf(quantile, k-1) >= stat:
                break
        # noinspection PyUnboundLocalVariable
        print('выборка равномерна и случайна с вероятностью', colored('%.2f' % quantile, 'yellow'))


def timing_plot(timing: Dict[str, List[float]]) -> None:
    """
    Построение графиков зависимости времени генерации от объёма выборки.
    :param timing: Измерения времени генерации.
    """
    plt.figure(figsize=(16, 9))
    for label, values in timing.items():
        plt.plot(SIZES, values, label=label)
    plt.grid()
    plt.legend(fontsize=16)
    plt.xlabel('Объём выборки')
    plt.ylabel('Время генерации, с')
    plt.savefig('timing.pdf')
