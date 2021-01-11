from scipy.stats import chi2
from terminaltables import AsciiTable
from Queueing.bin.queueing.generator import Generator
from Queueing.bin.queueing.tools import *


def report(g, theor_mx, theor_dx):
    mx = get_mx(g)
    dx = get_dx(g)
    print('Мат. ожидание: {0} ~ {1}, Дисперсия: {2} ~ {3}.'.format(mx, theor_mx, dx, theor_dx))
    correlation_plot(g)
    scatter_plot(g)
    left, right = confidence_interval(g)
    print('Доверительный интервал ({0}, {1})'.format(left, right))
    print('Статистика критерия значимости:', round((len(g) / dx) ** 0.5 * (mx - theor_mx), 3))


generator = Generator()
number = 1000

mu = 1  # любое натуральное число
print('Проверка экспоненциального распределения со средним значением', mu)
x = generator.generate_exp(mu, number)
print(x)
report(x, mu, mu ** 2)
a = min(x)
b = max(x)
k = round(1.72 * number ** (1 / 3))
step = (b - a) / k
x_points = get_histogram_x_points(a, b, step)
n = get_histogram_n(x, x_points)
plot_histogram(x, 1 / mu, step, x_points, n)
p_i = round(1 / len(x_points), 2)
z = [round((n_i - number * p_i) ** 2 / number * p_i, 2) for n_i in n]
tableData = [['№ интервала', 'Границы интервала', 'Ni', 'Pi', '(Ni-N*Pi)^2 / N*Pi']]
for i in range(len(n)):
    tableData.append([i + 1, '({0}, {1})'.format(x_points[i], x_points[i + 1]), n[i], p_i, z[i]])
resultTable = AsciiTable(tableData)
resultTable.inner_heading_row_border = True
resultTable.outer_border = False
resultTable.inner_row_border = False
print(resultTable.table)
print('Выборочное значение статистики критерия χ^2={0}. При k-3={1} и α={2} табличное значение χ^2={3}'.format(
    round(sum(z), 1), k - 3, 0.05, chi2.ppf(0.95, df=k - 3)))


p = [0.2, 0.2, 0.1, 0.2, 0.3]  # вероятности выпадания величин (сумма равна 1)
print('\nПроверка генератора дискретной случайной величины с таблицей распределения', p)
x = generator.generate_discrete(p, number)
report(x, get_p_mx(p), get_p_dx(p))
frequency_plot(x)
