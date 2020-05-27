"""
Основной файл программы. Здесь происходят:
  - работа со случайными процессами:
    * генерация выборок;
    * расчёт их характеристик;
    * проверка на однородность;
    * проверка на равномерность и случайность;
  - построение графика зависимости между объёмом выборки и скоростью генерации;
  - вывод информации из предыдущего пункта в файл timing.pdf.
"""


from time import time
from random import randint
from termcolor import colored

from generators import linear, tausworth
from util import mean, deviation, cv, pearson, SIZES, timing_plot


# Задаём диапазон и объём каждой выборки и количество выборок
RANGE, SIZE, COUNT = 10000, 100, 10

# Вычисляем теоретические значения характеристик
theoretical_mean = RANGE / 2
theoretical_deviation = (((RANGE+1)**2 - 1) / 12) ** (1/2)
theoretical_cv = theoretical_deviation / theoretical_mean

# Генерируем выборки
linear_samples = [linear(RANGE, SIZE) for _ in range(COUNT)]
tausworth_samples = [tausworth(RANGE, SIZE) for _ in range(COUNT)]

# Вычисляем выборочные средние
linear_means = [mean(sample) for sample in linear_samples]
tausworth_means = [mean(sample) for sample in tausworth_samples]

# Вычисляем выборочные стандартные отклонения
linear_deviations = [deviation(sample) for sample in linear_samples]
tausworth_deviations = [deviation(sample) for sample in tausworth_samples]

# Вычисляем выборочные коэффициенты вариации
linear_cvs = [cv(sample) for sample in linear_samples]
tausworth_cvs = [cv(sample) for sample in tausworth_samples]


print('\nТеоретические значения характеристик:')
print(' Математическое ожидание:', colored('%.2f' % theoretical_mean, 'yellow'))
print(' Стандартное отклонение:', colored('%.2f' % theoretical_deviation, 'yellow'))
print(' Коэффициент вариации:', colored('%.2f' % theoretical_cv, 'yellow'))

print('\nЛинейный конгруэнтный метод:')
print(' Выборочные средние:')
print(('  {:>9.2f}'*COUNT).format(*linear_means))
print(' Выборочные стандартные отклонения:')
print(('  {:>9.2f}'*COUNT).format(*linear_deviations))
print(' Выборочные коэффициенты вариации:')
print(('  {:>9.2f}'*COUNT).format(*linear_cvs))
print(colored(f' {len([cv for cv in linear_cvs if cv < theoretical_cv])} из {COUNT} выборок однородны', 'yellow'))

print('\nМетод Таусворта:')
print(' Выборочные средние:')
print(('  {:>9.2f}'*COUNT).format(*tausworth_means))
print(' Выборочные стандартные отклонения:')
print(('  {:>9.2f}'*COUNT).format(*tausworth_deviations))
print(' Выборочные коэффициенты вариации:')
print(('  {:>9.2f}'*COUNT).format(*tausworth_cvs))
print(colored(f' {len([cv for cv in tausworth_cvs if cv < theoretical_cv])} из {COUNT} выборок однородны', 'yellow'))

print('\n\nЛинейный конгруэнтный метод:')
for i, sample in enumerate(linear_samples):
    print(f' {i}-я ', end='')
    pearson(sample)

print('\nМетод Таусворта:')
for i, sample in enumerate(tausworth_samples):
    print(f' {i}-я ', end='')
    pearson(sample)


# Счётчики времени генерации (в секундах)
timing = {
    'Линейный конгруэнтный метод': [],
    'Метод Таусворта': [],
    'random.randint()': []
}

for size in SIZES:
    check = time()
    linear(size, size)
    timing['Линейный конгруэнтный метод'].append(time() - check)
    check = time()
    tausworth(size, size)
    timing['Метод Таусворта'].append(time() - check)
    check = time()
    [randint(0, size) for _ in range(size)]
    timing['random.randint()'].append(time() - check)

timing_plot(timing)
